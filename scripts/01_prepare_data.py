import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
import logging
from datasets import load_dataset
from src.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_and_prepare_cuad():
    logger.info("="*60)
    logger.info("DOWNLOADING CUAD DATASET")
    logger.info("="*60)
    
    # Create directories
    config.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    (config.RAW_DATA_DIR / "contracts").mkdir(exist_ok=True)
    
    logger.info("\nDownloading from Hugging Face...")
    
    try:
        # Download dataset
        dataset = load_dataset("cuad", trust_remote_code=True)
        logger.info(f"✅ Dataset loaded successfully")
        logger.info(f"   Train samples: {len(dataset['train'])}")
        
    except Exception as e:
        logger.error(f"❌ Error downloading dataset: {e}")
        logger.info("\nTrying alternative method...")
        
        # Alternative: Use test dataset if main fails
        try:
            dataset = load_dataset("cuad", split="train[:100]", trust_remote_code=True)
        except:
            logger.error("❌ Could not download dataset")
            return
    
    # Save contracts
    logger.info("\n" + "-"*60)
    logger.info("Saving contract documents...")
    logger.info("-"*60)
    
    saved_count = 0
    skipped_count = 0
    
    for idx, example in enumerate(dataset['train']):
        if idx >= 50:  # Limit to 50 for demo
            break
        
        # Get contract text
        contract_text = example.get('context', '')
        
        # Skip if empty or too short
        if len(contract_text.strip()) < 100:
            logger.warning(f"  ⚠️  Skipping contract {idx} (too short: {len(contract_text)} chars)")
            skipped_count += 1
            continue
        
        # Save to file
        contract_path = config.RAW_DATA_DIR / "contracts" / f"contract_{idx:03d}.txt"
        
        try:
            with open(contract_path, 'w', encoding='utf-8') as f:
                f.write(contract_text)
            
            saved_count += 1
            logger.info(f"  ✅ contract_{idx:03d}.txt ({len(contract_text):,} chars)")
            
        except Exception as e:
            logger.error(f"  ❌ Error saving contract {idx}: {e}")
    
    logger.info(f"\n✅ Saved {saved_count} contracts")
    logger.info(f"⚠️  Skipped {skipped_count} (too short)")
    
    # Verify saved files
    logger.info("\n" + "-"*60)
    logger.info("Verifying saved files...")
    logger.info("-"*60)
    
    saved_files = list((config.RAW_DATA_DIR / "contracts").glob("*.txt"))
    logger.info(f"Total .txt files in directory: {len(saved_files)}")
    
    # Check a few files
    for file_path in saved_files[:3]:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"  📄 {file_path.name}: {len(content):,} chars")
        logger.info(f"     Preview: {content[:100]}...")
    
    # Create QA pairs
    logger.info("\n" + "-"*60)
    logger.info("Creating QA pairs for evaluation...")
    logger.info("-"*60)
    
    qa_pairs = []
    
    for idx, example in enumerate(dataset['train'][:50]):
        context = example.get('context', '')
        questions = example.get('questions', [])
        
        if not context or not questions:
            continue
        
        # Take first 2 questions per contract
        for question in questions[:2]:
            if question and len(question.strip()) > 10:
                qa_pairs.append({
                    'question': question,
                    'context': context[:500],
                    'document_id': f"contract_{idx:03d}.txt"
                })
    
    # Save QA pairs
    eval_path = config.PROCESSED_DATA_DIR / "eval_qa.jsonl"
    with open(eval_path, 'w', encoding='utf-8') as f:
        for qa in qa_pairs[:100]:
            f.write(json.dumps(qa) + '\n')
    
    logger.info(f"✅ Created {len(qa_pairs[:100])} QA pairs")
    logger.info(f"   Saved to: {eval_path}")
    
    # Final summary
    logger.info("\n" + "="*60)
    logger.info("DATA PREPARATION COMPLETE")
    logger.info("="*60)
    logger.info(f"📁 Contracts saved: {saved_count}")
    logger.info(f"📁 Location: {config.RAW_DATA_DIR / 'contracts'}")
    logger.info(f"📝 QA pairs: {len(qa_pairs[:100])}")
    logger.info(f"📝 Location: {eval_path}")
    logger.info("="*60)

if __name__ == "__main__":
    download_and_prepare_cuad()