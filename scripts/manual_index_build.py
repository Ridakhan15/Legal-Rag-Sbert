import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import logging
import numpy as np
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.config import config

print("\n" + "="*60)
print("MANUAL INDEX BUILD - STEP BY STEP")
print("="*60)

# STEP 1: List files
print("\n📂 STEP 1: Finding contract files...")
contracts_dir = config.RAW_DATA_DIR / "contracts"

if not contracts_dir.exists():
    print(f"❌ ERROR: Directory not found: {contracts_dir}")
    print("Please run: python scripts/01_prepare_data.py")
    sys.exit(1)

files = list(contracts_dir.glob("*.txt"))
print(f"✅ Found {len(files)} contract files")

if len(files) == 0:
    print("❌ ERROR: No .txt files found!")
    print("Please run: python scripts/01_prepare_data.py")
    sys.exit(1)

# STEP 2: Load documents
print("\n📄 STEP 2: Loading documents...")
documents = []

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if len(content.strip()) > 100:
            documents.append({
                'content': content,
                'filename': file_path.name,
                'file_type': 'txt',
                'path': str(file_path)
            })
            print(f"  ✅ {file_path.name} ({len(content):,} chars)")
    except Exception as e:
        print(f"  ❌ Error loading {file_path.name}: {e}")

print(f"\n✅ Loaded {len(documents)} documents")

if len(documents) == 0:
    print("❌ ERROR: No valid documents loaded!")
    sys.exit(1)

# Show sample
print(f"\n📋 Sample document:")
print(f"  File: {documents[0]['filename']}")
print(f"  Length: {len(documents[0]['content']):,} chars")
print(f"  Preview: {documents[0]['content'][:150]}...")

# STEP 3: Chunk documents
print("\n✂️  STEP 3: Chunking documents...")
from src.data.preprocessor import TextPreprocessor

preprocessor = TextPreprocessor(chunk_size=512, chunk_overlap=50)
all_chunks = []

for doc in documents:
    try:
        chunks = preprocessor.chunk_document(doc)
        all_chunks.extend(chunks)
        print(f"  ✅ {doc['filename']}: {len(chunks)} chunks")
    except Exception as e:
        print(f"  ❌ Error chunking {doc['filename']}: {e}")

print(f"\n✅ Total chunks: {len(all_chunks)}")

if len(all_chunks) == 0:
    print("❌ ERROR: No chunks created!")
    sys.exit(1)

# Show sample chunk
print(f"\n📋 Sample chunk:")
print(f"  Source: {all_chunks[0]['source_file']}")
print(f"  Chunk ID: {all_chunks[0]['chunk_id']}")
print(f"  Length: {len(all_chunks[0]['text'])} chars")
print(f"  Text: {all_chunks[0]['text'][:150]}...")

# STEP 4: Load embedder
print("\n🤖 STEP 4: Loading embedding model...")
from src.models.embedder import SBERTEmbedder

try:
    embedder = SBERTEmbedder()
    print(f"✅ Loaded embedder")
    print(f"  Embedding dimension: {embedder.get_embedding_dim()}")
    print(f"  Device: {embedder.device}")
except Exception as e:
    print(f"❌ Error loading embedder: {e}")
    sys.exit(1)

# STEP 5: Generate embeddings
print("\n🧮 STEP 5: Generating embeddings...")
texts = [chunk['text'] for chunk in all_chunks]
print(f"  Encoding {len(texts)} texts...")

try:
    embeddings = embedder.encode(texts, batch_size=16, show_progress=True)
    print(f"✅ Generated embeddings")
    print(f"  Shape: {embeddings.shape}")
    print(f"  Data type: {embeddings.dtype}")
    print(f"  Memory: {embeddings.nbytes / 1024 / 1024:.2f} MB")
    
    # Verify shape
    if embeddings.ndim != 2:
        print(f"❌ ERROR: Embeddings should be 2D, got {embeddings.ndim}D")
        print(f"  Reshaping...")
        embeddings = embeddings.reshape(-1, embedder.get_embedding_dim())
        print(f"  New shape: {embeddings.shape}")
    
    if embeddings.shape[0] != len(all_chunks):
        print(f"❌ ERROR: Number of embeddings ({embeddings.shape[0]}) doesn't match chunks ({len(all_chunks)})")
        sys.exit(1)
    
except Exception as e:
    print(f"❌ Error generating embeddings: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# STEP 6: Build FAISS index
print("\n🗂️  STEP 6: Building FAISS index...")
from src.retrieval.vector_store import FAISSVectorStore

try:
    vector_store = FAISSVectorStore(embedding_dim=embedder.get_embedding_dim())
    print(f"✅ Created FAISS index")
    print(f"  Dimension: {vector_store.embedding_dim}")
    
    print(f"\n  Adding {len(embeddings)} embeddings...")
    vector_store.add_embeddings(embeddings, all_chunks)
    print(f"✅ Index built with {vector_store.index.ntotal} vectors")
    
except Exception as e:
    print(f"❌ Error building index: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# STEP 7: Save index
print("\n💾 STEP 7: Saving index...")
index_path = config.EMBEDDINGS_DIR / "faiss_index.bin"
metadata_path = config.EMBEDDINGS_DIR / "metadata.pkl"

try:
    config.EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    vector_store.save(index_path, metadata_path)
    
    print(f"✅ Saved index files:")
    print(f"  Index: {index_path} ({index_path.stat().st_size / 1024:.2f} KB)")
    print(f"  Metadata: {metadata_path} ({metadata_path.stat().st_size / 1024:.2f} KB)")
    
except Exception as e:
    print(f"❌ Error saving index: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# STEP 8: Test loading
print("\n🔄 STEP 8: Testing index loading...")
try:
    test_store = FAISSVectorStore.load(index_path, metadata_path)
    print(f"✅ Successfully loaded index")
    print(f"  Vectors: {test_store.index.ntotal}")
    print(f"  Documents: {len(test_store.documents)}")
    
except Exception as e:
    print(f"❌ Error loading index: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# STEP 9: Test search
print("\n🔍 STEP 9: Testing search...")
test_queries = [
    "payment terms",
    "termination clause",
    "confidentiality"
]

for test_query in test_queries:
    try:
        print(f"\n  Query: '{test_query}'")
        query_emb = embedder.encode(test_query)
        print(f"    Query embedding shape: {query_emb.shape}")
        
        results = test_store.search(query_emb, top_k=3)
        print(f"    Found {len(results)} results:")
        
        for i, (doc, score) in enumerate(results, 1):
            print(f"\n      {i}. Score: {score:.3f}")
            print(f"         Source: {doc['source_file']}")
            print(f"         Text: {doc['text'][:80]}...")
        
    except Exception as e:
        print(f"    ❌ Error searching: {e}")

# FINAL SUMMARY
print("\n" + "="*60)
print("✅ SUCCESS! INDEX BUILDING COMPLETE")
print("="*60)
print(f"Total vectors indexed: {vector_store.index.ntotal}")
print(f"Index location: {index_path}")
print(f"Metadata location: {metadata_path}")
print("\nNext steps:")
print("  1. Test RAG: python scripts/test_rag.py")
print("  2. Start API: python api/main.py")
print("  3. Start UI: streamlit run app/streamlit_app.py")
print("="*60 + "\n")