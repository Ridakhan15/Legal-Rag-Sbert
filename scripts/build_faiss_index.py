# scripts/build_faiss_index_final.py
import sys
from pathlib import Path
import logging
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from src.models.embedder import SBERTEmbedder
from src.retrieval.vector_store import FAISSVectorStore
from src.config import config  # Use config for consistent paths

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # 1️⃣ Use paths from config
    docs_path = Path("data/docs")
    save_index_path = config.EMBEDDINGS_DIR / "faiss_index.bin"  # Match retriever expectation
    save_meta_path = config.EMBEDDINGS_DIR / "metadata.pkl"      # Match retriever expectation
    
    # Ensure directories exist
    docs_path.mkdir(parents=True, exist_ok=True)
    save_index_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info("📂 Checking data directory...")
    text_files = list(docs_path.glob("*.txt"))
    logger.info(f"Found {len(text_files)} text files")
    
    if not text_files:
        logger.error("❌ No .txt files found. Please add files to data/docs/")
        return
    
    # 2️⃣ Load documents
    documents = []
    for file in text_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    documents.append({"text": text, "source_file": file.name})
                    logger.info(f"✅ Loaded {file.name}")
        except Exception as e:
            logger.error(f"Error reading {file}: {e}")
            continue
    
    logger.info(f"📊 Loaded {len(documents)} documents")
    
    if len(documents) == 0:
        logger.error("❌ No valid documents found")
        return

    # 3️⃣ Create embedder and generate embeddings
    try:
        embedder = SBERTEmbedder(model_path="models/fine_tuned/legal-sbert-v1")
        
        # Use encode() method (standard for SentenceTransformer)
        texts = [doc["text"] for doc in documents]
        logger.info("Generating embeddings...")
        
        embeddings = embedder.encode(texts)
        embeddings = np.array(embeddings, dtype=np.float32)
        logger.info(f"✅ Embeddings shape: {embeddings.shape}")
        
        # 4️⃣ Create and save FAISS index
        vector_store = FAISSVectorStore(embedding_dim=embeddings.shape[1])
        vector_store.add_embeddings(embeddings, documents)
        vector_store.save(save_index_path, save_meta_path)
        
        logger.info(f"💾 Saved index to: {save_index_path}")
        logger.info(f"💾 Saved metadata to: {save_meta_path}")
        logger.info("🎉 FAISS index built successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
