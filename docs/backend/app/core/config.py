from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    GOOGLE_API_KEY: str
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 20
    MAX_TOKENS_PER_REQUEST: int = 6000
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # App Settings
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
    MAX_CONCURRENT_AGENTS: int = 5
    
    # Model Settings
    DEFAULT_OPENAI_MODEL: str = "gpt-4o-mini"
    DEFAULT_GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # External APIs (optional)
    CLINICALTRIALS_API_KEY: str = ""
    USPTO_API_KEY: str = ""
    PUBMED_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()