from functools import lru_cache
from ..core.config import get_settings
from ..core.llm_manager import LLMManager
from ..services.web_scraper import WebScraper
from ..agents.master_agent import MasterAgent

@lru_cache()
def get_llm_manager():
    """Get LLM Manager singleton"""
    settings = get_settings()
    return LLMManager(settings)

@lru_cache()
def get_web_scraper():
    """Get Web Scraper singleton"""
    return WebScraper()

@lru_cache()
def get_master_agent():
    """Get Master Agent singleton"""
    llm_manager = get_llm_manager()
    web_scraper = get_web_scraper()
    return MasterAgent(llm_manager, web_scraper)