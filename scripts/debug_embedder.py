# scripts/debug_embeddings.py
import sys
from pathlib import Path
import logging
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from src.models.embedder import SBERTEmbedder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_embeddings():
    logger.info("🔍 DEBUGGING EMBEDDINGS")
    logger.info("="*60)
    
    try:
        embedder = SBERTEmbedder(model_path="models/fine_tuned/legal-sbert-v1")
        logger.info("✅ Embedder created")
        
        # Test texts
        test_texts = [
            "Payment terms are 30 days net.",
            "This agreement is between Company A and Company B.",
            "The contract may be terminated with 60 days notice.",
            "test query about payment terms"
        ]
        
        logger.info("📋 Testing embedding generation...")
        embeddings = embedder.encode(test_texts)
        logger.info(f"✅ Embeddings generated: {embeddings.shape}")
        
        # Check if embeddings are reasonable
        logger.info("📊 Embedding statistics:")
        logger.info(f"  Mean: {np.mean(embeddings):.6f}")
        logger.info(f"  Std: {np.std(embeddings):.6f}") 
        logger.info(f"  Min: {np.min(embeddings):.6f}")
        logger.info(f"  Max: {np.max(embeddings):.6f}")
        
        # Test similarity between related texts
        logger.info("\n🔍 Testing similarity calculation...")
        
        # Embed two related sentences
        text1 = "Payment terms are 30 days"
        text2 = "invoice due in 30 days"
        text3 = "completely unrelated text"
        
        emb1 = embedder.encode([text1])[0]
        emb2 = embedder.encode([text2])[0] 
        emb3 = embedder.encode([text3])[0]
        
        # Calculate cosine similarity
        def cosine_sim(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        
        sim_related = cosine_sim(emb1, emb2)
        sim_unrelated = cosine_sim(emb1, emb3)
        
        logger.info(f"Similarity between related texts: {sim_related:.3f}")
        logger.info(f"Similarity between unrelated texts: {sim_unrelated:.3f}")
        
        if sim_related > sim_unrelated:
            logger.info("✅ Embeddings working correctly - related texts have higher similarity")
        else:
            logger.warning("⚠️ Embeddings might not be working properly")
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_embeddings()
