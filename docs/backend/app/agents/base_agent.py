from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from ..core.llm_manager import LLMManager
from ..services.web_scraper import WebScraper
import json
from datetime import datetime as dt

class BaseAgent(ABC):
    def __init__(self, llm_manager: LLMManager, web_scraper: WebScraper, name: str, role: str):
        self.llm_manager = llm_manager
        self.web_scraper = web_scraper
        self.name = name
        self.role = role
        self.memory = []
    
    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute agent's task"""
        pass
    
    def add_to_memory(self, task: str, result: Any):
        """Add task and result to memory"""
        self.memory.append({
            "task": task,
            "result": result,
            "timestamp": dt.now().isoformat()
        })
    
    async def generate_response(
        self,
        prompt: str,
        provider: str = "openai",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate LLM response"""
        messages = [
            {"role": "system", "content": f"You are {self.name}, a {self.role}. Provide direct, professional responses without conversational phrases."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_manager.generate(
            messages=messages,
            provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response["content"]
    
    def format_output(self, data: Any, output_type: str = "text") -> Dict[str, Any]:
        """Format agent output"""
        return {
            "agent": self.name,
            "output_type": output_type,
            "data": data,
            "timestamp": dt.now().isoformat()
        }
