from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class QueryRequest(BaseModel):
    """Request schema for RAG query"""
    question: str = Field(..., min_length=1, max_length=500, description="User question")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Number of documents to retrieve")
    return_sources: Optional[bool] = Field(True, description="Include source documents in response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are the termination clauses in the contract?",
                "top_k": 5,
                "return_sources": True
            }
        }

class Source(BaseModel):
    """Source document metadata"""
    text: str = Field(..., description="Document text excerpt")
    source_file: str = Field(..., description="Source filename")
    chunk_id: int = Field(..., description="Chunk identifier")
    similarity_score: float = Field(..., ge=0, le=1, description="Similarity score")

class QueryResponse(BaseModel):
    """Response schema from RAG system"""
    answer: str = Field(..., description="Generated answer")
    question: str = Field(..., description="Original question")
    sources: Optional[List[Source]] = Field(None, description="Retrieved source documents")
    metadata: Optional[Dict] = Field(None, description="Performance metadata")

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    index_size: int = Field(..., description="Number of indexed documents")
    version: str = Field(default="1.0.0", description="API version")