import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.pipeline import RAGPipeline
from src.models.embedder import SBERTEmbedder
from src.retrieval.retriever import DocumentRetriever
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("="*60)
    logger.info("TESTING RAG PIPELINE")
    logger.info("="*60)
    
    # Initialize components properly
    logger.info("\nInitializing RAG pipeline components...")
    
    try:
        # Create embedder with your fine-tuned model
        embedder = SBERTEmbedder(model_path="models/fine_tuned/legal-sbert-v1")
        logger.info("✅ Embedder initialized")
        
        # Create retriever with the embedder
        retriever = DocumentRetriever(embedder=embedder)
        logger.info("✅ Retriever initialized")
        
        # Initialize pipeline - check which parameters it accepts
        # Try different initialization patterns
        try:
            # Try with retriever only
            pipeline = RAGPipeline(retriever=retriever)
            logger.info("✅ RAG pipeline initialized with retriever")
        except TypeError as e:
            logger.warning(f"First attempt failed: {e}")
            try:
                # Try without any parameters (let it create its own components)
                pipeline = RAGPipeline()
                logger.info("✅ RAG pipeline initialized without parameters")
                # If this works, try to inject our components
                if hasattr(pipeline, 'retriever'):
                    pipeline.retriever = retriever
                    logger.info("✅ Injected custom retriever")
                if hasattr(pipeline, 'embedder'):
                    pipeline.embedder = embedder
                    logger.info("✅ Injected custom embedder")
            except Exception as e2:
                logger.error(f"Second attempt failed: {e2}")
                return
                
    except Exception as e:
        logger.error(f"❌ Error initializing pipeline: {e}")
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
            result = pipeline.query(
                question=query,
                top_k=3,
                return_sources=True,
                return_metadata=True
            )
            
            print(f"\n📝 Answer:\n{result['answer']}\n")
            print(f"⏱️  Metrics:")

            # Safely get metadata values
            metadata = result.get('metadata', {})
            retrieval_time = metadata.get('retrieval_time', 0.0)
            generation_time = metadata.get('generation_time', 0.0)
            total_time = metadata.get('total_time', 0.0)
            num_sources = metadata.get('num_sources', 0)
            avg_similarity = metadata.get('avg_similarity', 0.0)

            print(f"  - Retrieval time: {retrieval_time:.2f}s")
            print(f"  - Generation time: {generation_time:.2f}s")
            print(f"  - Total time: {total_time:.2f}s")
            print(f"  - Sources used: {num_sources}")
            print(f"  - Avg similarity: {avg_similarity:.3f}")
            
            if result.get('sources'):
                print(f"\n📚 Sources:")
                for i, src in enumerate(result['sources'], 1):
                    print(f"  {i}. {src.get('source_file', 'Unknown')} (similarity: {src.get('similarity_score', 0):.3f})")
                    print(f"     {src.get('text', '')[:100]}...")
            else:
                print(f"\n❌ No sources found")
                
        except Exception as e:
            logger.error(f"❌ Error processing query: {e}")
            print(f"\n📝 Answer:\nI encountered an error while processing your question.\n")
            continue

if __name__ == "__main__":
    main()
