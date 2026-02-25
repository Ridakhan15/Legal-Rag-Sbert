from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from pathlib import Path
import sys
import time

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from api.schemas import QueryRequest, QueryResponse, HealthResponse, Source
from src.rag.pipeline import RAGPipeline
from src.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Legal RAG API",
    description="Retrieval-Augmented Generation API powered by Sentence-BERT for legal document analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global pipeline instance
pipeline = None

@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup"""
    global pipeline
    try:
        logger.info("="*60)
        logger.info("Starting Legal RAG API Server")
        logger.info("="*60)
        logger.info("Loading RAG pipeline...")
        
        start_time = time.time()
        pipeline = RAGPipeline()
        load_time = time.time() - start_time
        
        logger.info(f"✅ Pipeline loaded successfully in {load_time:.2f}s")
        logger.info(f"✅ Index size: {len(pipeline.retriever.vector_store.documents)} documents")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ Failed to load pipeline: {e}")
        import traceback
        traceback.print_exc()
        raise

@app.get("/", response_model=dict, tags=["General"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Legal RAG API - Sentence-BERT powered document Q&A",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns service status and basic metrics
    """
    is_healthy = pipeline is not None
    index_size = len(pipeline.retriever.vector_store.documents) if pipeline else 0
    
    return HealthResponse(
        status="healthy" if is_healthy else "unhealthy",
        model_loaded=is_healthy,
        index_size=index_size,
        version="1.0.0"
    )

@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def query_endpoint(request: QueryRequest):
    """
    Query the RAG system
    
    - **question**: User question about legal contracts
    - **top_k**: Number of documents to retrieve (1-20)
    - **return_sources**: Whether to include source documents
    
    Returns generated answer with optional source citations
    """
    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Pipeline not initialized. Service unavailable."
        )
    
    try:
        logger.info(f"Received query: '{request.question}'")
        logger.info(f"Parameters: top_k={request.top_k}, return_sources={request.return_sources}")
        
        # Run RAG pipeline
        start_time = time.time()
        result = pipeline.query(
            question=request.question,
            top_k=request.top_k,
            return_sources=request.return_sources,
            return_metadata=True
        )
        query_time = time.time() - start_time
        
        logger.info(f"Query completed in {query_time:.2f}s")
        
        # Convert sources to Pydantic models
        if result.get('sources'):
            result['sources'] = [Source(**src) for src in result['sources']]
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    import traceback
    traceback.print_exc()
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please check server logs."}
    )

@app.get("/stats", tags=["Statistics"])
async def get_stats():
    """Get system statistics"""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    return {
        "total_documents": len(pipeline.retriever.vector_store.documents),
        "embedding_dimension": pipeline.retriever.embedder.get_embedding_dim(),
        "model_device": pipeline.retriever.embedder.device,
        "index_type": "FAISS",
        "top_k_default": config.TOP_K,
        "similarity_threshold": config.SIMILARITY_THRESHOLD
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting server...")
    logger.info(f"Host: {config.API_HOST}")
    logger.info(f"Port: {config.API_PORT}")
    
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
        log_level="info"
    )