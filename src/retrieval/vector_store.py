import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)

class FAISSVectorStore:
    """FAISS-based vector store for similarity search"""
    
    def __init__(self, embedding_dim: int):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.documents = []
    
    def add_embeddings(self, embeddings: np.ndarray, documents: List[Dict]):
        """Add embeddings and corresponding documents to index"""
        
        # Validate inputs
        if embeddings is None or len(embeddings) == 0:
            logger.error("❌ No embeddings provided")
            return
        
        if documents is None or len(documents) == 0:
            logger.error("❌ No documents provided")
            return
        
        if len(embeddings) != len(documents):
            logger.error(f"❌ Mismatch: {len(embeddings)} embeddings vs {len(documents)} documents")
            return
        
        # Ensure embeddings are 2D
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        
        # Verify shape
        if embeddings.shape[1] != self.embedding_dim:
            logger.error(f"❌ Dimension mismatch. Expected {self.embedding_dim}, got {embeddings.shape[1]}")
            return
        
        # Convert to float32 if needed
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype('float32')
        
        # Verify embeddings are valid (not NaN or Inf)
        if np.isnan(embeddings).any():
            logger.error("❌ Embeddings contain NaN values")
            return
        
        if np.isinf(embeddings).any():
            logger.error("❌ Embeddings contain Inf values")
            return
        
        # Add to FAISS index
        logger.info(f"Adding {len(embeddings)} embeddings to index...")
        try:
            self.index.add(embeddings)
            logger.info(f"✅ Successfully added to index. Total vectors: {self.index.ntotal}")
        except Exception as e:
            logger.error(f"❌ Error adding to FAISS index: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Store documents
        self.documents.extend(documents)
        logger.info(f"✅ Stored {len(documents)} document metadata entries")
        logger.info(f"📊 Index now contains: {self.index.ntotal} vectors, {len(self.documents)} documents")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar documents"""
        
        if self.index.ntotal == 0:
            logger.warning("⚠️  Index is empty, no results to return")
            return []
        
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Ensure float32
        if query_embedding.dtype != np.float32:
            query_embedding = query_embedding.astype('float32')
        
        # Search
        scores, indices = self.index.search(query_embedding, top_k)
        
        # Get documents
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and idx < len(self.documents):
                results.append((self.documents[idx], float(score)))
        
        return results
    
    def save(self, index_path: Path, metadata_path: Path):
        """Save index and metadata"""
        index_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(index_path))
        
        # Save metadata
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.documents, f)
        
        logger.info(f"Saved index to {index_path}")
        logger.info(f"  Vectors in index: {self.index.ntotal}")
        logger.info(f"  Documents saved: {len(self.documents)}")
    
    @classmethod
    def load(cls, index_path: Path, metadata_path: Path):
        """Load index and metadata"""
        
        if not index_path.exists():
            raise FileNotFoundError(f"Index file not found: {index_path}")
        
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        
        # Load FAISS index
        index = faiss.read_index(str(index_path))
        
        # Load metadata
        with open(metadata_path, 'rb') as f:
            documents = pickle.load(f)
        
        # Create instance
        store = cls(embedding_dim=index.d)
        store.index = index
        store.documents = documents
        
        logger.info(f"Loaded index with {index.ntotal} embeddings")
        logger.info(f"Loaded {len(documents)} document metadata entries")
        
        return store