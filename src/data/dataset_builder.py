import json
import random
from typing import List, Tuple, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TrainingDataBuilder:
    def __init__(self, chunks: List[Dict]):
        self.chunks = chunks
    
    def create_positive_pairs(self, num_pairs: int = 1000) -> List[Tuple[str, str, int]]:
        pairs = []
        chunks_by_file = {}
        
        for chunk in self.chunks:
            file = chunk['source_file']
            if file not in chunks_by_file:
                chunks_by_file[file] = []
            chunks_by_file[file].append(chunk['text'])
        
        for file, file_chunks in chunks_by_file.items():
            if len(file_chunks) < 2:
                continue
            
            for _ in range(min(10, len(file_chunks) // 2)):
                if len(pairs) >= num_pairs:
                    break
                
                idx1, idx2 = random.sample(range(len(file_chunks)), 2)
                pairs.append((file_chunks[idx1], file_chunks[idx2], 1))
        
        return pairs[:num_pairs]
    
    def create_negative_pairs(self, num_pairs: int = 1000) -> List[Tuple[str, str, int]]:
        pairs = []
        chunks_by_file = {}
        
        for chunk in self.chunks:
            file = chunk['source_file']
            if file not in chunks_by_file:
                chunks_by_file[file] = []
            chunks_by_file[file].append(chunk['text'])
        
        files = list(chunks_by_file.keys())
        
        for _ in range(num_pairs):
            if len(files) < 2:
                break
            
            file1, file2 = random.sample(files, 2)
            chunk1 = random.choice(chunks_by_file[file1])
            chunk2 = random.choice(chunks_by_file[file2])
            pairs.append((chunk1, chunk2, 0))
        
        return pairs
    
    def build_training_dataset(self, output_path: Path, num_positive: int = 1000, num_negative: int = 1000):
        logger.info("Creating positive pairs...")
        positive_pairs = self.create_positive_pairs(num_positive)
        
        logger.info("Creating negative pairs...")
        negative_pairs = self.create_negative_pairs(num_negative)
        
        all_pairs = positive_pairs + negative_pairs
        random.shuffle(all_pairs)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            for sent1, sent2, label in all_pairs:
                f.write(json.dumps({
                    'sentence1': sent1,
                    'sentence2': sent2,
                    'label': label
                }) + '\n')
        
        logger.info(f"Saved {len(all_pairs)} training pairs to {output_path}")