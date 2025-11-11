import re
from typing import Optional

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))

def validate_api_key(api_key: str, provider: str = "openai") -> bool:
    """Validate API key format"""
    if provider == "openai":
        return api_key.startswith("sk-") and len(api_key) > 20
    elif provider == "gemini":
        return len(api_key) > 20
    return False