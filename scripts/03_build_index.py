import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import config
from src.data.loader import DocumentLoader
from src.data.preprocessor import TextPreprocessor
from src.models.embedder import SBERTEmbedder
from src.retrieval.vector_store import FAISSVectorStore
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 60)
    logger.info("BUILDING FAISS INDEX (DEBUG MODE)")
    logger.info("=" * 60)

    # --------------------------------------------------
    # Step 1: Check data directory
    # --------------------------------------------------
    contracts_dir = config.RAW_DATA_DIR / "contracts"
    logger.info(f"\nChecking directory: {contracts_dir}")

    if not contracts_dir.exists():
        logger.error(f"❌ Directory not found: {contracts_dir}")
        logger.info("Please run: python scripts/01_prepare_data.py first")
        return

    # Count files
    txt_files = list(contracts_dir.glob("*.txt"))
    logger.info(f"Found {len(txt_files)} .txt files")

    if len(txt_files) == 0:
        logger.error("❌ No .txt files found!")
        logger.info("Please run: python scripts/01_prepare_data.py first")
        return

    # Show sample files
    logger.info("\nSample files:")
    for f in txt_files[:5]:
        logger.info(f"  - {f.name}")

    # --------------------------------------------------
    # Step 2: Load documents
    # --------------------------------------------------
    logger.info("\n" + "-" * 60)
    logger.info("Step 1: Loading documents...")
    logger.info("-" * 60)

    loader = DocumentLoader()
    documents = loader.load_all_documents(contracts_dir)
    logger.info(f"✅ Loaded {len(documents)} documents")

    if len(documents) == 0:
        logger.error("❌ No documents loaded!")
        return

    # ------------------------------------------------------------------
    # After loading, make sure we actually have readable text.
    # ------------------------------------------------------------------
    if not documents:
        logger.error("❌ No documents were loaded – aborting.")
        return

    # Remove any document whose content is an empty string.
    # (The loader now returns "" instead of None, but we guard anyway.)
    valid_documents = [doc for doc in documents if doc.get("content")]
    if len(valid_documents) < len(documents):
        logger.warning(
            f"⚠️ {len(documents) - len(valid_documents)} document(s) had empty content and will be ignored."
        )
    documents = valid_documents

    if not documents:
        logger.error("❌ All loaded documents are empty – nothing to index.")
        return

    # ------------------------------------------------------------------
    # Safe preview of the first (non‑empty) document
    # ------------------------------------------------------------------
    first_doc = documents[0]
    logger.info("\nSample document preview:")
    logger.info(f"  File:   {first_doc['filename']}")
    logger.info(f"  Length: {len(first_doc['content'])} characters")
    logger.info(f"  Preview: {first_doc['content'][:200]}...")
    # -------------------------------------------------

    # --------------------------------------------------
    # Step 3: Chunk documents
    # --------------------------------------------------
    logger.info("\n" + "-" * 60)
    logger.info("Step 2: Chunking documents...")
    logger.info("-" * 60)

    preprocessor = TextPreprocessor(chunk_size=512, chunk_overlap=50)
    chunks = preprocessor.process_documents(documents)
    logger.info(f"✅ Created {len(chunks)} chunks from {len(documents)} documents")

    if len(chunks) == 0:
        logger.error("❌ No chunks created!")
        return

    # Show chunk statistics
    logger.info(f"\nChunk statistics:")
    logger.info(f"  Total chunks: {len(chunks)}")
    logger.info(f"  Avg chunks per doc: {len(chunks) / len(documents):.1f}")
    logger.info(f"\nSample chunk:")
    logger.info(f"  Text: {chunks[0]['text'][:150]}...")
    logger.info(f"  Source: {chunks[0]['source_file']}")
    logger.info(f"  Chunk ID: {chunks[0]['chunk_id']}")

    # --------------------------------------------------
    # Step 4: Generate embeddings
    # --------------------------------------------------
    logger.info("\n" + "-" * 60)
    logger.info("Step 3: Generating embeddings...")
    logger.info("-" * 60)

    embedder = SBERTEmbedder()
    logger.info(f"Embedding dimension: {embedder.get_embedding_dim()}")

    texts = [chunk["text"] for chunk in chunks]
    logger.info(f"Encoding {len(texts)} texts...")

    embeddings = embedder.encode(texts, batch_size=32, show_progress=True)
    logger.info(f"✅ Generated embeddings with shape: {embeddings.shape}")

    # --------------------------------------------------
    # Step 5: Build vector store
    # --------------------------------------------------
    logger.info("\n" + "-" * 60)
    logger.info("Step 4: Building FAISS index...")
    logger.info("-" * 60)

    vector_store = FAISSVectorStore(embedding_dim=embedder.get_embedding_dim())
    logger.info(f"Created FAISS index with dimension: {vector_store.embedding_dim}")

    vector_store.add_embeddings(embeddings, chunks)
    logger.info(f"✅ Added {len(embeddings)} embeddings to index")
    logger.info(f"✅ Index now contains {vector_store.index.ntotal} vectors")

    # --------------------------------------------------
    # Step 6: Save
    # --------------------------------------------------
    logger.info("\n" + "-" * 60)
    logger.info("Step 5: Saving index...")
    logger.info("-" * 60)

    index_path = config.EMBEDDINGS_DIR / "faiss_index.bin"
    metadata_path = config.EMBEDDINGS_DIR / "metadata.pkl"

    vector_store.save(index_path, metadata_path)

    # Verify saved files
    logger.info(f"\nVerifying saved files:")
    logger.info(f"  Index file: {index_path.exists()} - {index_path}")
    logger.info(f"  Metadata file: {metadata_path.exists()} - {metadata_path}")

    # --------------------------------------------------
    # Step 7: Test loading
    # --------------------------------------------------
    logger.info("\n" + "-" * 60)
    logger.info("Step 6: Testing index loading...")
    logger.info("-" * 60)

    test_store = FAISSVectorStore.load(index_path, metadata_path)
    logger.info(f"✅ Successfully loaded index with {test_store.index.ntotal} vectors")
    logger.info(f"✅ Loaded {len(test_store.documents)} document metadata entries")

    # --------------------------------------------------
    # Test search
    # --------------------------------------------------
    logger.info("\n" + "-" * 60)
    logger.info("Step 7: Testing search...")
    logger.info("-" * 60)

    test_query = "termination clause"
    logger.info(f"Test query: '{test_query}'")
    query_emb = embedder.encode(test_query)
    results = test_store.search(query_emb, top_k=3)

    logger.info(f"Found {len(results)} results:")
    for i, (doc, score) in enumerate(results, 1):
        logger.info(f"\n  Result {i}:")
        logger.info(f"    Score: {score:.3f}")
        logger.info(f"    Source: {doc['source_file']}")
        logger.info(f"    Text: {doc['text'][:100]}...")

    logger.info("\n" + "=" * 60)
    logger.info("✅ INDEX BUILDING COMPLETE!")
    logger.info("=" * 60)
    logger.info(f"Total vectors indexed: {vector_store.index.ntotal}")
    logger.info(f"Index saved to: {index_path}")
    logger.info(f"Metadata saved to: {metadata_path}")

if __name__ == "__main__":
    main()
