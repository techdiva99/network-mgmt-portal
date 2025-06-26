# tasks/analysis_tasks.py
"""
Optimization analysis task definitions for quadrant analysis workflow
"""

# CrewAI imports with fallback
try:
    from crewai import Task
except ImportError:
    class Task:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

class OptimizationAnalysisTasks:
    """Optimization analysis task definitions"""
    
    @staticmethod
    def comprehensive_optimization_analysis_task(agent, data_processing_results):
        """Comprehensive quadrant analysis and optimization task"""
        return Task(
            description=f"""
            Perform comprehensive quadrant analysis on the processed provider data for network optimization.
            
            Data Processing Results: {data_processing_results}
            
            Your sophisticated analysis must include:
            
            1. **Provider Performance Quadrant Analysis**
               - Categorize all providers into performance quadrants using quality-cost framework
               - Apply appropriate thresholds for quality (4.0) and cost ($600) metrics
               - Ensure quadrant assignments are accurate and well-justified
               - Analyze distribution of providers across quadrants
            
            2. **High-Priority Removal Candidate Identification**
               - Identify providers in "Optimization Candidates" quadrant
               - Prioritize by termination value and network adequacy risk
               - Exclude providers with "High" network adequacy risk
               - Provide detailed rationale for each removal recommendation
               - Calculate financial impact of proposed removals
            
            3. **Strategic Addition Opportunity Analysis**
               - Identify high-quality out-of-network providers (quality >= 4.0, cost <= $600)
               - Assess market position and competitive advantages
               - Evaluate geographic coverage and clinical group needs
               - Prioritize by quality score and cost efficiency
               - Assess potential for successful recruitment
            
            4. **Financial Impact and ROI Analysis**
               - Calculate total cost savings from removal candidates
               - Project quality improvement from network optimization
               - Assess impact on network utilizer capacity
               - Develop ROI projections for optimization initiatives
               - Include implementation cost considerations
            
            5. **Network Adequacy Risk Assessment**
               - Evaluate network adequacy impact for all recommendations
               - Identify potential coverage gaps from removals
               - Ensure adequate clinical group coverage is maintained
               - Assess geographic coverage impacts
               - Develop risk mitigation strategies
            
            6. **Implementation Prioritization and Planning**
               - Prioritize recommendations by impact, feasibility, and risk
               - Develop implementation timeline (30-day, 90-day, 6-month phases)
               - Identify resource requirements and dependencies
               - Create monitoring and success measurement framework
            
            Focus on actionable recommendations that balance immediate cost savings with long-term quality improvement while maintaining network adequacy and regulatory compliance.
            """,
            agent=agent,
            expected_output="""
            A comprehensive optimization analysis containing:
            
            **Quadrant Analysis Results:**
            - Complete provider categorization with quadrant placement rationale
            - Distribution analysis across all four quadrants
            - Performance insights for each quadrant category
            - Quadrant-specific strategic recommendations
            
            **Priority Removal Recommendations:**
            - Top 10 removal candidates with detailed justification
            - Financial impact analysis for each candidate
            - Network adequacy risk assessment
            - Expected quality improvement from removals
            - Implementation priority ranking
            
            **Strategic Addition Opportunities:**
            - Top 10 out-of-network recruitment targets
            - Competitive analysis and recruitment feasibility
            - Expected quality and capacity improvements
            - Geographic and clinical group coverage benefits
            - Recruitment strategy recommendations
            
            **Comprehensive Financial Analysis:**
            - Total optimization opportunity quantification
            - Annual cost savings projections
            - Quality improvement impact analysis
            - ROI timeline and break-even analysis
            - Implementation cost estimates
            
            **Implementation Roadmap:**
            - Phased implementation plan (immediate, short-term, medium-term)
            - Resource requirements and timeline estimates
            - Risk mitigation strategies and contingency planning
            - Success metrics and KPI framework
            - Stakeholder engagement recommendations
            
            **Network Adequacy Assessment:**
            - Detailed adequacy impact analysis
            - Geographic coverage gap identification
            - Clinical group coverage validation
            - Alternative provider identification
            - Compliance and regulatory considerations
            """
        )
    
    @staticmethod
    def clinical_group_optimization_task(agent, provider_data):
        """Clinical group specific optimization analysis"""
        return Task(
            description=f"""
            Perform detailed optimization analysis by clinical group.
            
            Provider Data: {provider_data}
            
            Your analysis should include:
            
            1. **Clinical Group Performance Analysis**
               - Analyze performance variations across clinical groups
               - Identify top and bottom performing clinical groups
               - Assess optimization opportunities by clinical group
            
            2. **Clinical Group Network Adequacy**
               - Evaluate network adequacy by clinical group and geography
               - Identify critical gaps in clinical group coverage
               - Assess risk levels for proposed optimizations
            
            3. **Clinical Group Strategic Recommendations**
               - Develop clinical group specific optimization strategies
               - Prioritize clinical groups for optimization focus
               - Recommend clinical group expansion or consolidation
            
            Provide detailed clinical group optimization insights.
            """,
            agent=agent,
            expected_output="""
            Clinical group optimization analysis including:
            - Performance analysis by clinical group
            - Network adequacy assessment by clinical group
            - Strategic recommendations for each clinical group
            - Priority clinical groups for optimization focus
            """
        )
    
    @staticmethod
    def financial_optimization_task(agent, quadrant_results):
        """Detailed financial optimization analysis task"""
        return Task(
            description=f"""
            Perform comprehensive financial optimization analysis.
            
            Quadrant Results: {quadrant_results}
            
            Your analysis should include:
            
            1. **Cost Savings Analysis**
               - Calculate total cost savings from optimization
               - Break down savings by provider and quadrant
               - Project annual and multi-year savings
            
            2. **Investment Requirements**
               - Estimate implementation costs
               - Calculate recruitment and transition costs
               - Assess technology and administrative requirements
            
            3. **ROI Analysis and Projections**
               - Develop comprehensive ROI models
               - Create financial projections and scenarios
               - Assess payback periods and break-even analysis
            
            Provide detailed financial optimization recommendations.
            """,
            agent=agent,
            expected_output="""
            Financial optimization analysis including:
            - Detailed cost savings projections
            - Implementation cost estimates
            - ROI analysis and financial projections
            - Financial risk assessment and scenarios
            """
        )

