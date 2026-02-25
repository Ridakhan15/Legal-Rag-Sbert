from typing import Dict, List, Optional
import time
import logging

from src.retrieval.retriever import DocumentRetriever
from src.rag.llm_client import LLMClient
from src.config import config

logger = logging.getLogger(__name__)

class RAGPipeline:
    """End-to-end RAG pipeline"""
    
    def __init__(self, retriever: DocumentRetriever = None, llm_client: LLMClient = None):
        self.retriever = retriever or DocumentRetriever()
        self.llm_client = llm_client or LLMClient()
    
    def query(
        self,
        question: str,
        top_k: int = None,
        return_sources: bool = True,
        return_metadata: bool = False
    ) -> Dict:
        start_time = time.time()
        
        logger.info(f"Query: {question}")
        retrieved_docs = self.retriever.retrieve(question, top_k=top_k)
        
        if not retrieved_docs:
            return {
                'answer': "I couldn't find any relevant information to answer your question.",
                'sources': [],
                'metadata': {'num_sources': 0, 'retrieval_time': time.time() - start_time}
            }
        
        retrieval_time = time.time() - start_time
        
        context = self.retriever.get_context(question, top_k=top_k)
        
        gen_start = time.time()
        answer = self.llm_client.generate_answer(question, context)
        generation_time = time.time() - gen_start
        
        total_time = time.time() - start_time
        
        response = {
            'answer': answer,
            'question': question
        }
        
        if return_sources:
            response['sources'] = [
                {
                    'text': doc['text'][:200] + '...',
                    'source_file': doc['source_file'],
                    'chunk_id': doc['chunk_id'],
                    'similarity_score': float(score)
                }
                for doc, score in retrieved_docs
            ]
        
        if return_metadata:
            response['metadata'] = {
                'num_sources': len(retrieved_docs),
                'retrieval_time': retrieval_time,
                'generation_time': generation_time,
                'total_time': total_time,
                'avg_similarity': sum(s for _, s in retrieved_docs) / len(retrieved_docs)
            }
        
        return response