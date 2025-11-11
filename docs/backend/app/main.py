from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from datetime import datetime

from .core.config import get_settings
from .core.llm_manager import LLMManager
from .services.web_scraper import WebScraper
from .agents.master_agent import MasterAgent

# Initialize
app = FastAPI(title="Pharma Agentic AI", version="1.0.0")
settings = get_settings()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
llm_manager = LLMManager(settings)
web_scraper = WebScraper()
master_agent = MasterAgent(llm_manager, web_scraper)

# Request Models
class QueryRequest(BaseModel):
    query: str
    provider: str = "openai"  # or "gemini"
    model: Optional[str] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    provider: str = "openai"
    model: Optional[str] = None

# Routes
@app.get("/")
async def root():
    return {
        "message": "Pharmaceutical Agentic AI System",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "usage_stats": llm_manager.get_usage_stats()
    }

@app.post("/api/query")
async def process_query(request: QueryRequest):
    """Process a research query through the multi-agent system"""
    try:
        context = {
            "provider": request.provider,
            "model": request.model
        }
        
        result = await master_agent.execute(request.query, context)
        
        return {
            "success": True,
            "data": result,
            "usage_stats": llm_manager.get_usage_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Interactive chat interface"""
    try:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        
        response = await llm_manager.generate(
            messages=messages,
            provider=request.provider,
            model=request.model
        )
        
        return {
            "success": True,
            "response": response["content"],
            "usage": response["usage"],
            "cost": response["cost"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/{filename}")
async def download_report(filename: str):
    """Download generated report"""
    filepath = os.path.join("reports", filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=filename
    )

@app.post("/api/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload internal documents for analysis"""
    uploaded_files = []
    
    for file in files:
        content = await file.read()
        # In production, process and store in vector database
        uploaded_files.append({
            "filename": file.filename,
            "size": len(content),
            "type": file.content_type
        })
    
    return {
        "success": True,
        "uploaded": uploaded_files
    }

@app.get("/api/usage")
async def get_usage():
    """Get API usage statistics"""
    return llm_manager.get_usage_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)