from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")
    
    @validator('role')
    def validate_role(cls, v):
        if v not in ['user', 'assistant', 'system']:
            raise ValueError('Role must be user, assistant, or system')
        return v

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=10, max_length=2000, description="Research query")
    provider: str = Field(default="openai", description="LLM provider: openai or gemini")
    model: Optional[str] = Field(None, description="Specific model to use")
    
    @validator('provider')
    def validate_provider(cls, v):
        if v not in ['openai', 'gemini']:
            raise ValueError('Provider must be openai or gemini')
        return v

class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="Conversation messages")
    provider: str = Field(default="openai")
    model: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2000, ge=100, le=4000)

class AgentResult(BaseModel):
    agent: str
    output_type: str
    data: Dict[str, Any]
    timestamp: datetime

class UsageStats(BaseModel):
    tokens_used: Dict[str, int]
    total_cost: Dict[str, float]
    total_cost_usd: float

class QueryResponse(BaseModel):
    success: bool
    query: str
    plan: Dict[str, Any]
    agent_results: Dict[str, AgentResult]
    synthesis: str
    report_path: Optional[str]
    timestamp: datetime
    usage_stats: UsageStats

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    usage_stats: UsageStats

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str]
    timestamp: datetime