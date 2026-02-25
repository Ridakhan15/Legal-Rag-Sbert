import re
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

class TextPreprocessor:
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:()\-\']', '', text)
        return text.strip()
    
    def chunk_document(self, document: Dict) -> List[Dict]:
        cleaned_content = self.clean_text(document['content'])
        chunks = self.splitter.split_text(cleaned_content)
        
        chunk_docs = []
        for idx, chunk_text in enumerate(chunks):
            chunk_docs.append({
                'text': chunk_text,
                'chunk_id': idx,
                'source_file': document['filename'],
                'file_type': document['file_type'],
                'total_chunks': len(chunks)
            })
        
        return chunk_docs
    
    def process_documents(self, documents: List[Dict]) -> List[Dict]:
        all_chunks = []
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        
        logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks