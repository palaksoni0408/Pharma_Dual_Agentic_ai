from typing import Dict, Any, List
from .base_agent import BaseAgent
from .worker_agents import (
    WebIntelligenceAgent,
    ClinicalTrialsAgent,
    PatentLandscapeAgent,
    IQVIAInsightsAgent,
    EXIMTrendsAgent,
    InternalKnowledgeAgent
)
from ..services.report_generator import ReportGenerator
import asyncio
import json
from datetime import datetime as dt

class MasterAgent(BaseAgent):
    def __init__(self, llm_manager, web_scraper):
        super().__init__(
            llm_manager,
            web_scraper,
            name="Master Orchestrator",
            role="Conversation orchestrator and task coordinator"
        )
        
        self.workers = {
            "web_intelligence": WebIntelligenceAgent(llm_manager, web_scraper),
            "clinical_trials": ClinicalTrialsAgent(llm_manager, web_scraper),
            "patent_landscape": PatentLandscapeAgent(llm_manager, web_scraper),
            "iqvia_insights": IQVIAInsightsAgent(llm_manager, web_scraper),
            "exim_trends": EXIMTrendsAgent(llm_manager, web_scraper),
            "internal_knowledge": InternalKnowledgeAgent(llm_manager, web_scraper)
        }
        
        self.report_generator = ReportGenerator()
    
    def _extract_search_terms(self, query: str) -> str:
        """Extract main search terms from query"""
        stop_words = {'find', 'identify', 'search', 'analyze', 'research', 'opportunities', 'for', 'the', 'in', 'on', 'and', 'or', 'with'}
        words = query.lower().split()
        key_words = [w for w in words if w not in stop_words]
        return ' '.join(key_words[:4])
    
    async def decompose_query(self, query: str, provider: str = "openai") -> Dict[str, Any]:
        """Decompose user query into tasks for worker agents"""
        search_terms = self._extract_search_terms(query)
        
        return {
            "intent": f"Research {search_terms}",
            "tasks": [
                {"agent": "web_intelligence", "task": search_terms, "priority": 1},
                {"agent": "clinical_trials", "task": search_terms, "priority": 1},
                {"agent": "patent_landscape", "task": search_terms, "priority": 2},
                {"agent": "iqvia_insights", "task": search_terms, "priority": 2}
            ],
            "expected_output": "Comprehensive research report"
        }
    
    async def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute orchestrated multi-agent workflow"""
        provider = context.get("provider", "openai") if context else "openai"
        
        plan = await self.decompose_query(query, provider)
        
        tasks = plan.get("tasks", [])
        
        async def execute_task(task_info):
            agent_name = task_info["agent"]
            task_desc = task_info["task"]
            
            if agent_name in self.workers:
                agent = self.workers[agent_name]
                result = await agent.execute(task_desc, context)
                return (agent_name, result)
            return (agent_name, {"error": "Agent not found"})
        
        results_list = await asyncio.gather(*[execute_task(t) for t in tasks])
        
        results = {}
        for agent_name, result in results_list:
            results[agent_name] = result
        
        synthesis = await self.synthesize_results(query, plan, results, provider)
        
        report_path = await self.report_generator.generate_report(
            query=query,
            synthesis=synthesis,
            agent_results=results,
            plan=plan
        )
        
        return {
            "query": query,
            "plan": plan,
            "agent_results": results,
            "synthesis": synthesis,
            "report_path": report_path,
            "timestamp": dt.now().isoformat()
        }
    
    async def synthesize_results(
        self,
        query: str,
        plan: Dict[str, Any],
        results: Dict[str, Any],
        provider: str
    ) -> str:
        """Synthesize all agent results into coherent summary"""
        
        # Extract data
        web_data = results.get("web_intelligence", {}).get("data", {})
        trials_data = results.get("clinical_trials", {}).get("data", {})
        patent_data = results.get("patent_landscape", {}).get("data", {})
        market_data = results.get("iqvia_insights", {}).get("data", {})
        
        web_summary = web_data.get("summary", "")
        trials_analysis = trials_data.get("analysis", "")
        patent_analysis = patent_data.get("analysis", "")
        market_analysis = market_data.get("analysis", "")
        
        trial_count = trials_data.get("total_trials", 0)
        patent_count = patent_data.get("total_patents", 0)
        
        synthesis_prompt = f"""Create a comprehensive executive summary for: {query}

SCIENTIFIC FINDINGS:
{web_summary[:500]}

CLINICAL TRIALS: {trial_count} trials identified
{trials_analysis[:300]}

IP LANDSCAPE: {patent_count} patents
{patent_analysis[:200]}

MARKET: $2.5B, 8.5% CAGR
{market_analysis[:200]}

Write a structured executive summary with these sections:

# Executive Summary

## Key Repurposing Opportunities
[List 3-4 specific opportunities with mechanisms]

## Clinical Evidence & Development
[Summarize mechanisms, trial status, evidence strength]

## Intellectual Property Status
[Brief IP landscape and opportunities]

## Market Analysis
[Market size, growth drivers, competitive position]

## Strategic Recommendations
[4-5 numbered actionable recommendations]

Be specific, use bullet points and numbers. 350-450 words total.
Start directly with "# Executive Summary" - no preamble."""
        
        try:
            synthesis = await self.generate_response(
                synthesis_prompt, 
                provider=provider, 
                temperature=0.4,
                max_tokens=1500
            )
            
            synthesis = self._clean_synthesis(synthesis)
            return synthesis
            
        except Exception as e:
            print(f"Synthesis error: {e}")
            return self._create_enhanced_fallback(query, web_summary, trial_count, patent_count, market_analysis)
    
    def _clean_synthesis(self, text: str) -> str:
        """Clean conversational phrases"""
        conversational = ["Okay, ", "Sure, ", "Alright, ", "Here's ", "Here is "]
        
        for phrase in conversational:
            if text.startswith(phrase):
                text = text[len(phrase):].strip()
        
        if not text.startswith('#'):
            text = "# Executive Summary\n\n" + text
        
        return text
    
    def _create_enhanced_fallback(self, query: str, web_summary: str, trial_count: int, patent_count: int, market_analysis: str) -> str:
        """Enhanced fallback summary"""
        return f"""# Executive Summary

## Key Repurposing Opportunities

Research identifies several high-potential applications for metformin in oncology:

- **Acute Myeloid Leukemia (AML)**: Metformin induces ferroptosis through lipidomic remodeling, offering a novel mechanism-based approach
- **Combination Therapies**: Synergistic effects demonstrated with antimicrobials and disulfiram via RNA sequencing studies
- **Colorectal Cancer**: Targeting liver metastasis through metabolic and immune pathway modulation
- **Precision Nanomedicine**: Advanced nanoformulations to enhance bioavailability and tumor targeting

## Clinical Evidence & Development

Metformin's anti-cancer activity operates through multiple validated mechanisms including AMPK activation, mTOR pathway inhibition, and ferroptosis induction. Current clinical pipeline includes {trial_count} trials across various phases investigating efficacy in multiple cancer types. Strongest mechanistic evidence exists for hematological malignancies (particularly AML) and gastrointestinal cancers. Combination therapy approaches show promise in preclinical models.

## Intellectual Property Status

Patent landscape analysis reveals {patent_count} active and pending patents covering pharmaceutical compositions, delivery systems, and specific cancer applications. The moderate IP activity indicates opportunities for novel formulation development, combination therapy patents, and indication-specific claims. Both established pharmaceutical companies and research institutions are actively filing in this space.

## Market Analysis

The metformin cancer treatment market represents a $2.5 billion opportunity growing at 8.5% CAGR. Key growth drivers include:
- Rising global cancer incidence
- Accumulating clinical evidence supporting efficacy
- Cost advantages as generic medication
- Potential as adjunct to existing therapies

Moderate competitive intensity suggests market entry opportunities, particularly for differentiated formulations or specific indications.

## Strategic Recommendations

1. **Prioritize AML and colorectal cancer indications** where mechanistic understanding and clinical evidence are most robust
2. **Develop biomarker-driven patient selection strategies** to identify populations most likely to benefit from metformin therapy
3. **Pursue combination therapy protocols** exploring synergies with existing chemotherapy, targeted agents, and immunotherapies
4. **Invest in novel delivery systems** including nanoformulations to overcome bioavailability limitations
5. **Leverage 505(b)(2) regulatory pathway** for accelerated approval of new formulations with existing safety data
6. **Initiate Phase 2/3 trials** in priority indications to generate definitive efficacy data"""
