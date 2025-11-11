from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import FileResponse
from typing import List
import os

from ..models.schemas import (
    QueryRequest,
    QueryResponse,
    ChatRequest,
    HealthResponse,
    UsageStats
)
from ..core.config import get_settings
from .dependencies import get_master_agent, get_llm_manager

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    master_agent = Depends(get_master_agent)
):
    """Process pharmaceutical research query"""
    try:
        context = {
            "provider": request.provider,
            "model": request.model
        }
        
        result = await master_agent.execute(request.query, context)
        
        return QueryResponse(
            success=True,
            query=result["query"],
            plan=result["plan"],
            agent_results=result["agent_results"],
            synthesis=result["synthesis"],
            report_path=result.get("report_path"),
            timestamp=result["timestamp"],
            usage_stats=master_agent.llm_manager.get_usage_stats()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat(
    request: ChatRequest,
    llm_manager = Depends(get_llm_manager)
):
    """Interactive chat"""
    try:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        
        response = await llm_manager.generate(
            messages=messages,
            provider=request.provider,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return {
            "success": True,
            "response": response["content"],
            "usage": response["usage"],
            "cost": response["cost"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/{filename}")
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

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload internal documents"""
    uploaded_files = []
    
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    for file in files:
        content = await file.read()
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        uploaded_files.append({
            "filename": file.filename,
            "size": len(content),
            "type": file.content_type,
            "path": file_path
        })
    
    return {
        "success": True,
        "uploaded": uploaded_files
    }

@router.get("/usage", response_model=UsageStats)
async def get_usage(llm_manager = Depends(get_llm_manager)):
    """Get API usage statistics"""
    return llm_manager.get_usage_stats()

@router.get("/health", response_model=HealthResponse)
async def health_check(llm_manager = Depends(get_llm_manager)):
    """Health check endpoint"""
    from datetime import datetime
    from .. import __version__
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=__version__,
        usage_stats=llm_manager.get_usage_stats()
    )