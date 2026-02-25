from pathlib import Path
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    MODELS_DIR = PROJECT_ROOT / "models"
    EMBEDDINGS_DIR = DATA_DIR / "embeddings"
    
    # Model Configuration
    BASE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    FINE_TUNED_MODEL_PATH = MODELS_DIR / "fine_tuned" / "legal-sbert-v1"
    
    # Training Hyperparameters
    BATCH_SIZE = 16
    EPOCHS = 3
    LEARNING_RATE = 2e-5
    WARMUP_STEPS = 100
    MAX_SEQ_LENGTH = 384
    
    # Chunking Parameters
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    
    # Retrieval Parameters
    TOP_K = 5
    SIMILARITY_THRESHOLD = 0.0  # Accept all results
    
    # RAG Parameters
    MAX_CONTEXT_LENGTH = 2000
    
    # LLM Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = "gpt-3.5-turbo"
    LLM_TEMPERATURE = 0.3
    MAX_TOKENS = 500
    
    # MLOps
    WANDB_PROJECT = "legal-rag-sbert"
    WANDB_API_KEY = os.getenv("WANDB_API_KEY")
    
    # API
    API_HOST = "0.0.0.0"
    API_PORT = 8000

config = Config()