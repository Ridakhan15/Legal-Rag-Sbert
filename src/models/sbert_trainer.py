import torch
from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from torch.utils.data import DataLoader
from typing import List
import json
from pathlib import Path
import logging

from src.config import config

logger = logging.getLogger(__name__)

class SBERTTrainer:
    """Fine-tune Sentence-BERT on domain-specific data"""
    
    def __init__(self, base_model: str = None, output_path: Path = None):
        self.base_model_name = base_model or config.BASE_MODEL
        self.output_path = output_path or config.FINE_TUNED_MODEL_PATH
        
        logger.info(f"Loading base model: {self.base_model_name}")
        self.model = SentenceTransformer(self.base_model_name)
    
    def load_training_data(self, data_path: Path) -> List[InputExample]:
        examples = []
        with open(data_path, 'r') as f:
            for i, line in enumerate(f):
                data = json.loads(line)
                if 'label' not in data:
                    raise ValueError(f"Missing label in line {i}: {data}")
                examples.append(InputExample(
                    texts=[data['sentence1'], data['sentence2']],
                    label=float(data['label'])
                ))

        logger.info(f"Loaded {len(examples)} training examples")
        return examples

       
    
    def train(
        self,
        train_data_path: Path,
        eval_data_path: Path = None,
        batch_size: int = None,
        epochs: int = None,
        warmup_steps: int = None
    ):
        batch_size = batch_size or config.BATCH_SIZE
        epochs = epochs or config.EPOCHS
        warmup_steps = warmup_steps or config.WARMUP_STEPS
        
        # Load data
        train_examples = self.load_training_data(train_data_path)
        
        # Create DataLoader
        train_dataloader = DataLoader(
            train_examples,
            shuffle=True,
            batch_size=batch_size,
            collate_fn=self.model.smart_batching_collate
            )


        
        # Define loss function
        train_loss = losses.CosineSimilarityLoss(self.model)
        
        # Training
        logger.info("Starting training...")
        logger.info(f"Epochs: {epochs}, Batch size: {batch_size}, Warmup: {warmup_steps}")
        
        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=epochs,
            warmup_steps=warmup_steps,
            output_path=str(self.output_path),
            save_best_model=True,
            show_progress_bar=True
        )
        
        logger.info(f"✅ Training complete. Model saved to {self.output_path}")