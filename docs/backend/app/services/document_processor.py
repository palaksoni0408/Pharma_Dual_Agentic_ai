import PyPDF2
import io
from typing import List, Dict, Any
import logging

logger = logging.getLogger("pharma_ai")

class DocumentProcessor:
    """Process uploaded documents"""
    
    def __init__(self):
        self.supported_types = ['.pdf', '.txt', '.doc', '.docx']
    
    async def process_pdf(self, file_content: bytes) -> Dict[str, Any]:
        """Extract text from PDF"""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return {
                "success": True,
                "text": text,
                "pages": len(pdf_reader.pages),
                "metadata": pdf_reader.metadata
            }
        except Exception as e:
            logger.error(f"PDF processing error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def process_text(self, file_content: bytes) -> Dict[str, Any]:
        """Extract text from plain text file"""
        try:
            text = file_content.decode('utf-8')
            return {
                "success": True,
                "text": text,
                "length": len(text)
            }
        except Exception as e:
            logger.error(f"Text processing error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        
        return chunks