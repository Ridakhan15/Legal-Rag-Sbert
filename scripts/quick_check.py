# scripts/check_config.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.config import config
    print("📋 Configuration:")
    print(f"EMBEDDINGS_DIR: {getattr(config, 'EMBEDDINGS_DIR', 'Not set')}")
    print(f"TOP_K: {getattr(config, 'TOP_K', 'Not set')}")
    print(f"SIMILARITY_THRESHOLD: {getattr(config, 'SIMILARITY_THRESHOLD', 'Not set')}")
except Exception as e:
    print(f"❌ Error loading config: {e}")
