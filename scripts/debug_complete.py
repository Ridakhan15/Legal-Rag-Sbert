# scripts/debug_faiss_index.py
import sys
from pathlib import Path
import logging
import faiss
import pickle
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from src.models.embedder import SBERTEmbedder
from src.retrieval.retriever import DocumentRetriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_faiss():
    logger.info("🔍 DEBUGGING FAISS INDEX AND EMBEDDINGS")
    logger.info("="*60)
    
    # 1. Check index files
    logger.info("1️⃣ Checking index files...")
    index_path = Path("data/embeddings/faiss_index.bin")
    meta_path = Path("data/embeddings/metadata.pkl")
    
    logger.info(f"Index path: {index_path}")
    logger.info(f"Metadata path: {meta_path}")
    logger.info(f"Index exists: {index_path.exists()}")
    logger.info(f"Metadata exists: {meta_path.exists()}")
    
    if not index_path.exists() or not meta_path.exists():
        logger.error("❌ Index files missing! Need to rebuild FAISS index.")
        return False
    
    # 2. Load and inspect index
    logger.info("2️⃣ Loading FAISS index...")
    try:
        index = faiss.read_index(str(index_path))
        logger.info(f"✅ Index loaded: {index.ntotal} vectors, {index.d} dimensions")
        
        with open(meta_path, 'rb') as f:
            metadata = pickle.load(f)
        logger.info(f"✅ Metadata loaded: {len(metadata)} documents")
        
        # Show document info
        for i, doc in enumerate(metadata[:3]):
            logger.info(f"  Document {i+1}:")
            logger.info(f"    Source: {doc.get('source_file', 'Unknown')}")
            logger.info(f"    Text length: {len(doc.get('text', ''))} chars")
            logger.info(f"    Text preview: {doc.get('text', '')[:100]}...")
            
    except Exception as e:
        logger.error(f"❌ Error loading index: {e}")
        return False
    
    # 3. Test embeddings with actual queries
    logger.info("3️⃣ Testing embeddings and similarity search...")
    try:
        embedder = SBERTEmbedder(model_path="models/fine_tuned/legal-sbert-v1")
        logger.info("✅ Embedder created")
        
        # Test queries
        test_queries = [
            "payment terms",
            "parties to the contract", 
            "termination clauses",
            "contract agreement"
        ]
        
        for query in test_queries:
            logger.info(f"\n🔍 Testing query: '{query}'")
            
            # Generate query embedding
            query_embedding = embedder.encode([query])[0]
            logger.info(f"Query embedding shape: {query_embedding.shape}")
            
            # Search in index
            distances, indices = index.search(np.array([query_embedding]), k=5)
            
            logger.info(f"Search results - distances: {distances[0]}")
            logger.info(f"Search results - indices: {indices[0]}")
            
            # Show actual documents
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx != -1 and idx < len(metadata):
                    doc = metadata[idx]
                    similarity = 1 - distance  # Convert distance to similarity
                    logger.info(f"  Result {i+1}: Similarity: {similarity:.3f}")
                    logger.info(f"    Source: {doc.get('source_file', 'Unknown')}")
                    logger.info(f"    Text: {doc.get('text', '')[:100]}...")
                else:
                    logger.info(f"  Result {i+1}: No match")
                    
    except Exception as e:
        logger.error(f"❌ Error testing embeddings: {e}")
        return False
    
    return True

if __name__ == "__main__":
    debug_faiss()
