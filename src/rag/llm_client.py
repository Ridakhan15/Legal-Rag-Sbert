import os
import logging
from typing import Optional
from huggingface_hub import InferenceClient
from src.config import config

logger = logging.getLogger(__name__)

class LLMClient:
    """
    LLM client using Hugging Face Inference API (100% FREE)
    
    Supported models:
    - mistralai/Mistral-7B-Instruct-v0.2 (fast, good quality)
    - meta-llama/Meta-Llama-3-8B-Instruct (best quality, slower)
    - google/flan-t5-xxl (fast, lightweight)
    """
    
    def __init__(self, model: str = None):
        self.hf_token = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN")
        
        if not self.hf_token or self.hf_token == "your_hf_token_here":
            logger.warning("⚠️  HF token not set. Using mock mode.")
            self.client = None
            self.model = "mock"
            return
        
        # Best free models on HF Inference API
        self.model = model or "mistralai/Mistral-7B-Instruct-v0.2"
        
        try:
            self.client = InferenceClient(token=self.hf_token)
            logger.info(f"✅ Hugging Face client initialized")
            logger.info(f"   Model: {self.model}")
        except Exception as e:
            logger.error(f"❌ HF client init failed: {e}")
            self.client = None
            self.model = "mock"
    
    def generate_answer(
        self,
        query: str,
        context: str,
        temperature: float = None,
        max_tokens: int = None,
        system_prompt: str = None
    ) -> str:
        """Generate answer using Hugging Face model"""
        
        if self.client is None:
            return self._mock_answer(query, context)
        
        temperature = temperature or 0.3
        max_tokens = max_tokens or 500
        
        if system_prompt is None:
            system_prompt = """You are a legal contract analysis assistant.
Answer questions based ONLY on the provided context from legal contracts.
If the context doesn't contain the answer, say so clearly.
Be concise and cite specific contract clauses."""
        
        # Format prompt for instruction-tuned models
        if "Mistral" in self.model or "Llama" in self.model:
            prompt = f"""<s>[INST] {system_prompt}

Context from contracts:
{context}

Question: {query}

Answer: [/INST]"""
        else:
            prompt = f"""Context: {context}

Question: {query}

Answer based on the context above:"""
        
        try:
            logger.info(f"Calling HF model: {self.model}")
            
            response = self.client.text_generation(
                prompt,
                model=self.model,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                return_full_text=False,
                stream=False
            )
            
            answer = response.strip()
            logger.info(f"✅ Generated answer ({len(answer)} chars)")
            return answer
            
        except Exception as e:
            error_msg = str(e)
            
            # Handle rate limit
            if "rate limit" in error_msg.lower():
                logger.warning("⚠️  Rate limit hit. Using mock answer.")
                return self._mock_answer(query, context, note="(Rate limit reached)")
            
            # Handle model loading
            if "loading" in error_msg.lower():
                logger.warning("⚠️  Model loading. Try again in 20 seconds.")
                return self._mock_answer(query, context, note="(Model loading, retry in 20s)")
            
            logger.error(f"❌ HF error: {e}")
            return self._mock_answer(query, context)
    
    def _mock_answer(self, query: str, context: str, note: str = "") -> str:
        """
        Fallback when no LLM available.
        Extracts relevant sentences from context.
        """
        if not context or len(context.strip()) < 10:
            return f"No relevant information found. {note}"
        
        # Score sentences by relevance
        query_words = set(query.lower().split())
        sentences = [s.strip() for s in context.replace('\n', ' ').split('.') 
                     if len(s.strip()) > 30]
        
        scored = []
        for sent in sentences:
            sent_words = set(sent.lower().split())
            overlap = len(query_words & sent_words)
            if overlap > 0:
                scored.append((overlap, sent))
        
        scored.sort(reverse=True)
        top_sentences = [s for _, s in scored[:3]]
        
        if top_sentences:
            answer = "**Based on the contract documents:**\n\n"
            for i, sent in enumerate(top_sentences, 1):
                answer += f"{i}. {sent}.\n"
            if note:
                answer += f"\n_{note}_"
            return answer
        
        # Last resort
        first_chunk = context[:400]
        return f"**Relevant excerpt:**\n\n{first_chunk}...\n\n_{note}_"