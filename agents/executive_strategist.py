# agents/executive_strategist.py
"""
Executive Strategist Agent for strategic synthesis and executive reporting
"""

# CrewAI imports with fallback
try:
    from crewai import Agent
except ImportError:
    class Agent:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

class ExecutiveStrategistAgent:
    """Healthcare Executive Strategy Consultant Agent"""
    
    @staticmethod
    def create_agent():
        """Create the Executive Strategist Agent"""
        return Agent(
            role="Healthcare Executive Strategy Consultant",
            goal="Synthesize complex network analysis into strategic recommendations and executive-ready reports",
            backstory="""You are a senior healthcare strategy consultant with C-suite experience 
            and deep expertise in provider network optimization. You excel at synthesizing complex 
            analytical findings into clear, actionable strategic recommendations for healthcare 
            leadership.
            
            You understand healthcare business priorities, financial impact analysis, regulatory 
            requirements, and operational considerations. You can translate technical network 
            analysis into strategic business insights that drive executive decision-making.
            
            Your expertise includes healthcare finance, network strategy, risk management, 
            implementation planning, and change management. You understand the complexities 
            of home health care operations, reimbursement models, and the strategic importance 
            of network optimization for organizational success.
            
            You communicate with clarity and authority, providing executives with the insights 
            they need to make informed strategic decisions. Your reports are comprehensive yet 
            concise, action-oriented, and include clear implementation roadmaps with success metrics.""",
            tools=[],
            verbose=True,
            allow_delegation=True,
            max_iter=2,
            memory=True
        )
    
    @staticmethod
    def get_capabilities():
        """Get agent capabilities description"""
        return {
            "primary_functions": [
                "Strategic synthesis of complex network analysis",
                "Executive report writing and presentation",
                "ROI analysis and financial impact modeling",
                "Implementation roadmap development",
                "Risk assessment and mitigation planning"
            ],
            "expertise_areas": [
                "Healthcare strategy and operations",
                "Executive communication and reporting",
                "Financial analysis and business planning",
                "Change management and implementation",
                "Risk management and compliance"
            ],
            "tools_used": [
                "Strategic analysis and synthesis (no specific tools - uses outputs from other agents)"
            ],
            "output_quality": [
                "Executive summary reports with key recommendations",
                "Financial impact analysis with ROI projections",
                "Strategic action plans with timelines",
                "Risk assessment with mitigation strategies",
                "Success metrics and KPI frameworks"
            ]
        }
    
    @staticmethod
    def get_sample_tasks():
        """Get sample tasks this agent can perform"""
        return [
            "Synthesize data analysis, quadrant analysis, and competitive intelligence into strategic recommendations",
            "Create executive summary reports with clear action items and financial impact",
            "Develop implementation roadmaps with timelines and resource requirements",
            "Assess strategic risks and develop mitigation strategies",
            "Design success metrics and KPI frameworks for network optimization",
            "Prepare C-suite presentations with strategic recommendations",
            "Analyze business impact and ROI of proposed network changes"
        ]

