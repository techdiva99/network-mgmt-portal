# agents/data_specialist.py
"""
Data Specialist Agent for comprehensive provider network data processing
"""

from tools.data_processing_tool import NetworkDataTool

# CrewAI imports with fallback
try:
    from crewai import Agent
except ImportError:
    class Agent:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

class DataSpecialistAgent:
    """Senior Healthcare Data Specialist Agent"""
    
    @staticmethod
    def create_agent():
        """Create the Data Specialist Agent"""
        return Agent(
            role="Senior Healthcare Data Specialist",
            goal="Process and analyze comprehensive provider network data with advanced filtering and quality assessment",
            backstory="""You are a seasoned healthcare data specialist with 15+ years of experience 
            in provider network analytics. You excel at data processing, quality assessment, 
            and extracting meaningful insights from complex healthcare datasets. 
            
            You understand the nuances of provider performance metrics, network adequacy requirements, 
            clinical group classifications, and can identify data quality issues that could impact 
            optimization decisions. Your expertise includes PDGM models, MMTA categories, and 
            behavioral health classifications.
            
            You are meticulous about data validation, always check for anomalies, and provide 
            comprehensive data quality reports. You understand the critical importance of accurate 
            data in healthcare network optimization decisions.""",
            tools=[NetworkDataTool()],
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            memory=True
        )
    
    @staticmethod
    def get_capabilities():
        """Get agent capabilities description"""
        return {
            "primary_functions": [
                "Comprehensive provider data loading and validation",
                "Advanced filtering by clinical groups, geography, and performance metrics",
                "Data quality assessment and anomaly detection",
                "Statistical analysis and data profiling",
                "Data preparation for downstream analysis"
            ],
            "expertise_areas": [
                "Healthcare provider data structures",
                "Clinical group classifications (MMTA, Behavioral Health, etc.)",
                "Network adequacy assessment",
                "Geographic coverage analysis",
                "Performance metric validation"
            ],
            "tools_used": [
                "NetworkDataTool for data processing and filtering"
            ],
            "output_quality": [
                "Comprehensive data quality reports",
                "Filtered datasets ready for analysis",
                "Data anomaly identification",
                "Processing performance metrics"
            ]
        }
    
    @staticmethod
    def get_sample_tasks():
        """Get sample tasks this agent can perform"""
        return [
            "Load and validate provider network data with quality assessment",
            "Apply complex filters for clinical groups, states, and performance metrics",
            "Identify data quality issues and recommend corrections",
            "Generate data profiling reports for network composition",
            "Prepare cleaned datasets for quadrant and competitive analysis",
            "Analyze data completeness across geographic regions",
            "Validate clinical group classifications and coverage"
        ]

