from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import torch
from pathlib import Path
import logging

from src.config import config

logger = logging.getLogger(__name__)

class SBERTEmbedder:
    """Generate embeddings using Sentence-BERT"""
    
    def __init__(self, model_path: Union[str, Path] = None):
        self.model_path = model_path or config.FINE_TUNED_MODEL_PATH
        
        # Load model
        if Path(self.model_path).exists():
            logger.info(f"Loading fine-tuned model from {self.model_path}")
            self.model = SentenceTransformer(str(self.model_path))
        else:
            logger.warning(f"Fine-tuned model not found. Using base model.")
            self.model = SentenceTransformer(config.BASE_MODEL)
        
        # Set device
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        logger.info(f"Using device: {self.device}")
    
    def encode(
        self,
        texts: Union[str, List[str]],
        batch_size: int = 32,
        show_progress: bool = False
    ) -> np.ndarray:
        """
        Generate embeddings for texts
        Returns:
            numpy array of embeddings (n_texts, embedding_dim)
        """
        if isinstance(texts, str):
            texts = [texts]
    
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
    
    # FIX: Ensure 2D array
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
    
        return embeddings
    
    def get_embedding_dim(self) -> int:
        return self.model.get_sentence_embedding_dimension()