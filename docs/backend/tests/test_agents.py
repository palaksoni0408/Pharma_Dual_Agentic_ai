import pytest
from app.core.llm_manager import LLMManager
from app.services.web_scraper import WebScraper
from app.agents.master_agent import MasterAgent
from app.core.config import get_settings

@pytest.fixture
def llm_manager():
    settings = get_settings()
    return LLMManager(settings)

@pytest.fixture
def web_scraper():
    return WebScraper()

@pytest.fixture
def master_agent(llm_manager, web_scraper):
    return MasterAgent(llm_manager, web_scraper)

@pytest.mark.asyncio
async def test_master_agent_decompose(master_agent):
    """Test query decomposition"""
    query = "Find repurposing opportunities for metformin"
    plan = await master_agent.decompose_query(query)
    
    assert "intent" in plan
    assert "tasks" in plan
    assert len(plan["tasks"]) > 0

@pytest.mark.asyncio
async def test_web_intelligence_agent(llm_manager, web_scraper):
    """Test web intelligence agent"""
    from app.agents.worker_agents import WebIntelligenceAgent
    
    agent = WebIntelligenceAgent(llm_manager, web_scraper)
    result = await agent.execute("diabetes treatment")
    
    assert result["agent"] == "Web Intelligence Agent"
    assert "data" in result