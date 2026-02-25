import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import config
from src.data.loader import DocumentLoader
from src.data.preprocessor import TextPreprocessor
from src.data.dataset_builder import TrainingDataBuilder
from src.models.sbert_trainer import SBERTTrainer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("="*60)
    logger.info("SENTENCE-BERT TRAINING PIPELINE")
    logger.info("="*60)
    
    # Step 1: Load documents
    logger.info("\nStep 1: Loading documents...")
    loader = DocumentLoader()
    documents = loader.load_all_documents(config.RAW_DATA_DIR / "contracts")
    logger.info(f"Loaded {len(documents)} documents")
    
    # Step 2: Chunk documents
    logger.info("\nStep 2: Chunking documents...")
    preprocessor = TextPreprocessor()
    chunks = preprocessor.process_documents(documents)
    logger.info(f"Created {len(chunks)} chunks")
    
    # Step 3: Build training dataset
    logger.info("\nStep 3: Building training dataset...")
    builder = TrainingDataBuilder(chunks)
    train_path = config.PROCESSED_DATA_DIR / "train_pairs.jsonl"
    
    if not train_path.exists():
        builder.build_training_dataset(
            output_path=train_path,
            num_positive=1000,
            num_negative=1000
        )
    else:
        logger.info(f"Training data already exists at {train_path}")
    
    # Step 4: Train Sentence-BERT
    logger.info("\nStep 4: Training Sentence-BERT...")
    trainer = SBERTTrainer()
    trainer.train(
        train_data_path=train_path,
        batch_size=16,
        epochs=3,
        warmup_steps=100
    )
    
    logger.info("\n" + "="*60)
    logger.info("✅ TRAINING COMPLETE!")
    logger.info("="*60)

if __name__ == "__main__":
    main()