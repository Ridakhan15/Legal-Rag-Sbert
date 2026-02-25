# scripts/test_direct.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.embedder import SBERTEmbedder
from src.retrieval.retriever import DocumentRetriever
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("="*60)
    logger.info("TESTING RETRIEVAL SYSTEM DIRECTLY")
    logger.info("="*60)
    
    # Initialize components
    logger.info("\nInitializing components...")
    
    try:
        # Create embedder
        embedder = SBERTEmbedder(model_path="models/fine_tuned/legal-sbert-v1")
        logger.info("✅ Embedder initialized")
        
        # Create retriever
        retriever = DocumentRetriever(embedder=embedder)
        logger.info("✅ Retriever initialized")
        
    except Exception as e:
        logger.error(f"❌ Error initializing components: {e}")
        return
    
    # Test queries
    test_queries = [
        "What are the termination clauses?",
        "What are the payment terms?",
        "Who are the parties to the contract?"
    ]
    
    for query in test_queries:
        logger.info("\n" + "-"*60)
        logger.info(f"Query: {query}")
        logger.info("-"*60)
        
        try:
            # Use retriever directly
            results = retriever.retrieve(query, top_k=3)
            logger.info(f"Retrieved {len(results)} documents")
            
            print(f"\n📝 Retrieved Documents for: '{query}'")
            
            if results:
                for i, (doc, similarity) in enumerate(results, 1):
                    print(f"\n  {i}. Similarity: {similarity:.3f}")
                    print(f"     Source: {doc.get('source_file', 'Unknown')}")
                    print(f"     Text: {doc.get('text', '')[:200]}...")
            else:
                print("❌ No documents retrieved")
                
        except Exception as e:
            logger.error(f"❌ Error retrieving documents: {e}")
            continue

if __name__ == "__main__":
    main()
