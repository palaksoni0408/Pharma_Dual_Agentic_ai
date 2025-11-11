import pytest
from app.services.web_scraper import WebScraper

@pytest.fixture
def web_scraper():
    return WebScraper()

@pytest.mark.asyncio
async def test_pubmed_search(web_scraper):
    """Test PubMed search"""
    results = await web_scraper.search_pubmed("diabetes", max_results=5)
    assert len(results) > 0
    assert "title" in results[0]

@pytest.mark.asyncio
async def test_clinical_trials_search(web_scraper):
    """Test clinical trials search"""
    results = await web_scraper.search_clinical_trials("cancer", max_results=5)
    assert len(results) > 0
    assert "nct_id" in results[0]