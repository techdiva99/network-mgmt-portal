# crews/network_optimization_crew.py
"""
Main CrewAI crew orchestrator for network optimization analysis
"""

from datetime import datetime
from typing import Dict, Any

# CrewAI imports with fallback
try:
    from crewai import Crew, Process
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    class Crew:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
        def kickoff(self):
            return {"error": "CrewAI not available"}
    
    class Process:
        sequential = "sequential"

# Agent imports
from agents.data_specialist import DataSpecialistAgent
from agents.quadrant_analyst import QuadrantAnalystAgent
from agents.competitive_intelligence import CompetitiveIntelligenceAgent
from agents.executive_strategist import ExecutiveStrategistAgent

# Task imports
from tasks.data_tasks import DataProcessingTasks
from tasks.analysis_tasks import OptimizationAnalysisTasks
from tasks.intelligence_tasks import CompetitiveIntelligenceTasks
from tasks.reporting_tasks import ExecutiveReportingTasks

# Tool imports for fallback analysis
from tools.data_processing_tool import NetworkDataTool
from tools.quadrant_analysis_tool import QuadrantAnalysisTool
from tools.competitive_analysis_tool import CompetitiveAnalysisTool

class NetworkOptimizationCrew:
    """Main crew orchestrator for network optimization analysis"""
    
    def __init__(self):
        self.crewai_available = CREWAI_AVAILABLE
        self.agents = self._initialize_agents()
        self.tasks = self._initialize_tasks()
        
        # Fallback tools for direct analysis
        self.data_tool = NetworkDataTool()
        self.quadrant_tool = QuadrantAnalysisTool()
        self.competitive_tool = CompetitiveAnalysisTool()
    
    def _initialize_agents(self):
        """Initialize all agents"""
        if not self.crewai_available:
            return None
            
        return {
            "data_specialist": DataSpecialistAgent.create_agent(),
            "quadrant_analyst": QuadrantAnalystAgent.create_agent(),
            "competitive_analyst": CompetitiveIntelligenceAgent.create_agent(),
            "executive_strategist": ExecutiveStrategistAgent.create_agent()
        }
    
    def _initialize_tasks(self):
        """Initialize task classes"""
        return {
            "data_tasks": DataProcessingTasks(),
            "analysis_tasks": OptimizationAnalysisTasks(),
            "intelligence_tasks": CompetitiveIntelligenceTasks(),
            "reporting_tasks": ExecutiveReportingTasks()
        }
    
    def run_analysis(self, user_filters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the full network optimization analysis"""
        
        if not self.crewai_available:
            return self._run_fallback_analysis(user_filters)
        
        try:
            return self._run_crewai_analysis(user_filters)
        except Exception as e:
            # Fallback to direct tool analysis if CrewAI fails
            return self._run_fallback_analysis(user_filters, error=str(e))
    
    def _run_crewai_analysis(self, user_filters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis using full CrewAI framework"""
        
        # Create tasks with agents
        data_task = self.tasks["data_tasks"].comprehensive_data_processing_task(
            self.agents["data_specialist"], user_filters
        )
        
        optimization_task = self.tasks["analysis_tasks"].comprehensive_optimization_analysis_task(
            self.agents["quadrant_analyst"], "data_processing_results"
        )
        
        competitive_task = self.tasks["intelligence_tasks"].comprehensive_competitive_analysis_task(
            self.agents["competitive_analyst"], "provider_data"
        )
        
        strategy_task = self.tasks["reporting_tasks"].executive_strategy_synthesis_task(
            self.agents["executive_strategist"], 
            "optimization_results", 
            "competitive_results"
        )
        
        # Create crew
        crew = Crew(
            agents=[
                self.agents["data_specialist"],
                self.agents["quadrant_analyst"],
                self.agents["competitive_analyst"],
                self.agents["executive_strategist"]
            ],
            tasks=[data_task, optimization_task, competitive_task, strategy_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute analysis
        result = crew.kickoff()
        
        return {
            "crew_output": result,
            "success": True,
            "analysis_type": "full_crewai_analysis",
            "timestamp": datetime.now().isoformat(),
            "filters_applied": user_filters,
            "agents_used": list(self.agents.keys()),
            "framework": "CrewAI"
        }
    
    def _run_fallback_analysis(self, user_filters: Dict[str, Any], error: str = None) -> Dict[str, Any]:
        """Run analysis using direct tool calls when CrewAI is not available"""
        
        try:
            # Step 1: Data processing
            data_result = self.data_tool._run(user_filters)
            
            # Step 2: Quadrant analysis
            quadrant_result = self.quadrant_tool._run(data_result["data"])
            
            # Step 3: Competitive analysis
            competitive_result = self.competitive_tool._run(data_result["data"])
            
            # Step 4: Synthesize results
            analysis_summary = self._synthesize_fallback_results(
                data_result, quadrant_result, competitive_result
            )
            
            return {
                "fallback_analysis": True,
                "data_analysis": data_result,
                "quadrant_analysis": quadrant_result,
                "competitive_analysis": competitive_result,
                "analysis_summary": analysis_summary,
                "success": True,
                "analysis_type": "direct_tool_analysis",
                "timestamp": datetime.now().isoformat(),
                "filters_applied": user_filters,
                "framework": "Direct Tools",
                "note": "CrewAI framework not available - using direct tool analysis",
                "error": error
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis_type": "failed_analysis",
                "timestamp": datetime.now().isoformat(),
                "filters_applied": user_filters
            }
    
    def _synthesize_fallback_results(self, data_result, quadrant_result, competitive_result) -> Dict[str, Any]:
        """Synthesize results from direct tool analysis"""
        
        # Extract key insights
        total_providers = data_result["summary"]["total_providers"]
        total_opportunity = data_result["summary"]["total_opportunity"]
        
        removal_candidates = len(quadrant_result.get("removal_candidates", []))
        addition_candidates = len(quadrant_result.get("addition_candidates", []))
        
        financial_impact = quadrant_result.get("financial_impact", {})
        
        # Generate executive summary
        executive_summary = {
            "key_findings": [
                f"Analyzed {total_providers} providers across network",
                f"Identified {removal_candidates} removal candidates",
                f"Found {addition_candidates} strategic addition opportunities",
                f"Total optimization opportunity: ${total_opportunity/1000000:.1f}M"
            ],
            "strategic_recommendations": [
                "Prioritize removal of underperforming, high-cost providers",
                "Recruit high-quality, cost-efficient out-of-network providers", 
                "Focus on clinical groups with highest optimization potential",
                "Maintain network adequacy throughout optimization process"
            ],
            "financial_impact": {
                "total_savings_potential": financial_impact.get("total_removal_savings", 0),
                "quality_improvement": financial_impact.get("avg_quality_improvement", 0),
                "implementation_timeline": "6-12 months"
            },
            "next_steps": [
                "Review detailed removal and addition recommendations",
                "Assess network adequacy impact for proposed changes",
                "Develop implementation timeline with stakeholder engagement",
                "Establish success metrics and monitoring framework"
            ]
        }
        
        return executive_summary
    
    def get_crew_status(self) -> Dict[str, Any]:
        """Get current crew status and capabilities"""
        return {
            "crewai_available": self.crewai_available,
            "agents_initialized": self.agents is not None,
            "available_agents": list(self.agents.keys()) if self.agents else [],
            "available_tools": [
                "NetworkDataTool",
                "QuadrantAnalysisTool", 
                "CompetitiveAnalysisTool"
            ],
            "analysis_capabilities": [
                "Comprehensive data processing and validation",
                "Provider performance quadrant analysis",
                "Competitive intelligence and market positioning",
                "Strategic synthesis and executive reporting"
            ],
            "framework_mode": "CrewAI" if self.crewai_available else "Direct Tools"
        }
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get detailed agent capabilities"""
        if not self.crewai_available:
            return {"error": "CrewAI not available - agent capabilities not accessible"}
        
        return {
            "data_specialist": DataSpecialistAgent.get_capabilities(),
            "quadrant_analyst": QuadrantAnalystAgent.get_capabilities(),
            "competitive_analyst": CompetitiveIntelligenceAgent.get_capabilities(),
            "executive_strategist": ExecutiveStrategistAgent.get_capabilities()
        }

