import openai  # pyright: ignore[reportMissingImports]
import google.generativeai as genai  # pyright: ignore[reportMissingImports]
from typing import Optional, Dict, Any
import tiktoken
import asyncio
from collections import deque
from datetime import datetime as dt, timedelta

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    async def acquire(self):
        now = dt.now()
        while self.requests and (now - self.requests[0]) > timedelta(seconds=self.time_window):
            self.requests.popleft()
        
        if len(self.requests) >= self.max_requests:
            sleep_time = (self.requests[0] + timedelta(seconds=self.time_window) - now).total_seconds()
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            self.requests.popleft()
        
        self.requests.append(now)

class LLMManager:
    def __init__(self, config):
        self.config = config
        self.openai_client = openai.AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        genai.configure(api_key=config.GOOGLE_API_KEY)
        
        self.openai_limiter = RateLimiter(config.MAX_REQUESTS_PER_MINUTE)
        self.gemini_limiter = RateLimiter(config.MAX_REQUESTS_PER_MINUTE)
        
        self.total_tokens_used = {"openai": 0, "gemini": 0}
        self.total_cost = {"openai": 0.0, "gemini": 0.0}
        
    def count_tokens(self, text: str, model: str = "gpt-4") -> int:
        """Count tokens in text"""
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except:
            return len(text) // 4
    
    def estimate_cost(self, tokens: int, model: str, is_completion: bool = False) -> float:
        """Estimate API call cost"""
        costs = {
            "gpt-4": {"prompt": 0.03/1000, "completion": 0.06/1000},
            "gpt-3.5-turbo": {"prompt": 0.0015/1000, "completion": 0.002/1000},
            "gemini-pro": {"prompt": 0.00025/1000, "completion": 0.0005/1000},
        }
        
        model_key = "gpt-4" if "gpt-4" in model else "gpt-3.5-turbo" if "gpt" in model else "gemini-pro"
        cost_type = "completion" if is_completion else "prompt"
        
        return tokens * costs[model_key][cost_type]
    
    async def call_openai(
        self,
        messages: list,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """Call OpenAI API"""
        await self.openai_limiter.acquire()
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            usage = response.usage
            self.total_tokens_used["openai"] += usage.total_tokens
            self.total_cost["openai"] += self.estimate_cost(usage.prompt_tokens, model, False)
            self.total_cost["openai"] += self.estimate_cost(usage.completion_tokens, model, True)
            
            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens
                },
                "cost": self.estimate_cost(usage.prompt_tokens, model, False) + 
                        self.estimate_cost(usage.completion_tokens, model, True),
                "model": model
            }
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            raise
    
    async def call_gemini(
        self,
        messages: list,
        model: str = "gemini-2.0-flash-exp",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        max_retries: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """Call Gemini API with retry logic for rate limits"""
        await self.gemini_limiter.acquire()
        
        # Shorten prompt for Gemini
        prompt = "\n".join([f"{m['role']}: {m['content'][:500]}" for m in messages])
        
        model_instance = genai.GenerativeModel(model)
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
        
        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(max_retries):
            try:
                response = await asyncio.to_thread(
                    model_instance.generate_content,
                    prompt,
                    generation_config=generation_config
                )
                
                # Extract text from response - handle both simple and complex responses
                text_content = None
                try:
                    # Try simple text access first
                    text_content = response.text
                except Exception:
                    # Fallback to parts extraction
                    if hasattr(response, 'candidates') and response.candidates:
                        candidate = response.candidates[0]
                        if hasattr(candidate, 'content') and candidate.content:
                            if hasattr(candidate.content, 'parts'):
                                parts_text = []
                                for part in candidate.content.parts:
                                    if hasattr(part, 'text') and part.text:
                                        parts_text.append(part.text)
                                if parts_text:
                                    text_content = "".join(parts_text)
                
                if not text_content:
                    raise ValueError("No text content found in Gemini response")
                
                input_tokens = self.count_tokens(prompt)
                output_tokens = self.count_tokens(text_content)
                total_tokens = input_tokens + output_tokens
                
                self.total_tokens_used["gemini"] += total_tokens
                self.total_cost["gemini"] += self.estimate_cost(input_tokens, "gemini-pro", False)
                self.total_cost["gemini"] += self.estimate_cost(output_tokens, "gemini-pro", True)
                
                return {
                    "content": text_content,
                    "usage": {
                        "prompt_tokens": input_tokens,
                        "completion_tokens": output_tokens,
                        "total_tokens": total_tokens
                    },
                    "cost": self.estimate_cost(input_tokens, "gemini-pro", False) + 
                            self.estimate_cost(output_tokens, "gemini-pro", True),
                    "model": model
                }
                
            except Exception as e:
                error_str = str(e)
                last_exception = e
                
                # Check if it's a 429 rate limit error
                if "429" in error_str or "Resource exhausted" in error_str:
                    if attempt < max_retries - 1:
                        # Exponential backoff: 2^attempt seconds
                        wait_time = 2 ** attempt
                        print(f"Gemini API rate limited (429). Retrying in {wait_time} seconds... (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        error_msg = f"Gemini API rate limit exceeded after {max_retries} attempts. Please try again later."
                        print(f"Gemini API Error: {error_msg}")
                        raise Exception(error_msg)
                else:
                    # For other errors, don't retry
                    print(f"Gemini API Error: {error_str}")
                    raise
        
        # If we get here, all retries failed
        raise last_exception
    
    async def generate(
        self,
        messages: list,
        provider: str = "openai",
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Unified generation interface"""
        if provider == "openai":
            model = model or "gpt-4"
            return await self.call_openai(messages, model, **kwargs)
        elif provider == "gemini":
            model = model or "gemini-2.0-flash-exp"
            return await self.call_gemini(messages, model, **kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            "tokens_used": self.total_tokens_used,
            "total_cost": self.total_cost,
            "total_cost_usd": sum(self.total_cost.values())
        }
