"""Application constants"""

# Agent names
AGENT_WEB_INTELLIGENCE = "web_intelligence"
AGENT_CLINICAL_TRIALS = "clinical_trials"
AGENT_PATENT_LANDSCAPE = "patent_landscape"
AGENT_IQVIA_INSIGHTS = "iqvia_insights"
AGENT_EXIM_TRENDS = "exim_trends"
AGENT_INTERNAL_KNOWLEDGE = "internal_knowledge"

# API endpoints
PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
CLINICAL_TRIALS_BASE_URL = "https://clinicaltrials.gov/api/query/"
USPTO_BASE_URL = "https://ppubs.uspto.gov/dirsearch-public/"

# File types
ALLOWED_DOCUMENT_TYPES = ['.pdf', '.txt', '.doc', '.docx']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Cache keys
CACHE_PREFIX_PUBMED = "pubmed"
CACHE_PREFIX_TRIALS = "trials"
CACHE_PREFIX_PATENTS = "patents"

# Rate limiting
DEFAULT_RATE_LIMIT = 20  # requests per minutes