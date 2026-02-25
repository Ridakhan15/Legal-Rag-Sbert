from typing import List, Dict, Tuple
import numpy as np
from pathlib import Path
import logging

from src.models.embedder import SBERTEmbedder
from src.retrieval.vector_store import FAISSVectorStore
from src.config import config

logger = logging.getLogger(__name__)

class DocumentRetriever:
    """Retriever for RAG system"""
    
    def __init__(self, embedder: SBERTEmbedder = None, vector_store: FAISSVectorStore = None):
        self.embedder = embedder or SBERTEmbedder()
        
        if vector_store is None:
            index_path = config.EMBEDDINGS_DIR / "faiss_index.bin"
            metadata_path = config.EMBEDDINGS_DIR / "metadata.pkl"
            self.vector_store = FAISSVectorStore.load(index_path, metadata_path)
        else:
            self.vector_store = vector_store
    
    def retrieve(
        self,
        query: str,
        top_k: int = None,
        similarity_threshold: float = None
    ) -> List[Tuple[Dict, float]]:
        top_k = top_k or config.TOP_K
        similarity_threshold = similarity_threshold or config.SIMILARITY_THRESHOLD
        
        query_embedding = self.embedder.encode(query)
        results = self.vector_store.search(query_embedding, top_k=top_k)
        
        filtered_results = [
            (doc, score) for doc, score in results
            if score >= similarity_threshold
        ]
        
        logger.info(f"Retrieved {len(filtered_results)} documents for query")
        return filtered_results
    
    def get_context(self, query: str, top_k: int = None, max_length: int = None) -> str:
        max_length = max_length or config.MAX_CONTEXT_LENGTH
        
        results = self.retrieve(query, top_k=top_k)
        
        context_parts = []
        current_length = 0
        
        for doc, score in results:
            chunk_text = doc['text']
            chunk_length = len(chunk_text)
            
            if current_length + chunk_length > max_length:
                remaining = max_length - current_length
                if remaining > 100:
                    context_parts.append(chunk_text[:remaining])
                break
            
            context_parts.append(chunk_text)
            current_length += chunk_length
        
        context = "\n\n".join(context_parts)
        logger.info(f"Built context with {len(context_parts)} chunks ({current_length} chars)")
        
        return context