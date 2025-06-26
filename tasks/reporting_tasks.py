# tasks/reporting_tasks.py
"""
Executive reporting task definitions for strategic synthesis and communication
"""

# CrewAI imports with fallback
try:
    from crewai import Task
except ImportError:
    class Task:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

class ExecutiveReportingTasks:
    """Executive reporting task definitions"""
    
    @staticmethod
    def executive_strategy_synthesis_task(agent, optimization_results, competitive_results):
        """Comprehensive executive strategy synthesis and reporting task"""
        return Task(
            description=f"""
            Synthesize all network optimization analysis into a comprehensive executive strategy report for C-suite decision-making.
            
            Analysis Inputs:
            - Optimization Analysis Results: {optimization_results}
            - Competitive Intelligence Results: {competitive_results}
            
            Your executive-level synthesis must include:
            
            1. **Executive Summary with Strategic Findings**
               - Synthesize key findings from all analyses into clear strategic insights
               - Identify top 3-5 strategic priorities for network optimization
               - Highlight critical decision points requiring executive attention
               - Provide clear bottom-line impact assessment
               - Present findings in executive-appropriate language and format
            
            2. **Strategic Recommendations and Action Plan**
               - Develop prioritized strategic recommendations based on all analyses
               - Create actionable implementation roadmap with clear timelines
               - Identify immediate (30-day), short-term (90-day), and medium-term (6-month) actions
               - Specify resource requirements and organizational dependencies
               - Include stakeholder engagement and change management considerations
            
            3. **Comprehensive Financial Impact Analysis**
               - Synthesize financial impact from optimization and competitive analyses
               - Provide detailed ROI projections with scenario analysis
               - Calculate total cost savings, quality improvements, and competitive benefits
               - Include implementation costs and investment requirements
               - Develop financial justification for recommended strategies
            
            4. **Strategic Risk Assessment and Mitigation**
               - Identify and assess all strategic risks from network optimization
               - Evaluate competitive risks and market response scenarios
               - Assess regulatory, operational, and financial risks
               - Develop comprehensive risk mitigation strategies
               - Create contingency plans for high-impact risks
            
            5. **Competitive Positioning Strategy**
               - Integrate competitive intelligence into strategic recommendations
               - Develop competitive positioning and differentiation strategies
               - Identify opportunities for competitive advantage
               - Assess competitive threats and defensive strategies
               - Recommend competitive intelligence monitoring framework
            
            6. **Implementation Framework and Success Metrics**
               - Develop comprehensive implementation framework
               - Create detailed project management and governance structure
               - Design success metrics and KPI dashboard
               - Establish monitoring and reporting mechanisms
               - Include change management and stakeholder communication plans
            
            7. **Strategic Decision Framework**
               - Present clear decision points for executive approval
               - Provide decision criteria and evaluation frameworks
               - Identify go/no-go decision gates
               - Include investment authorization recommendations
               - Present alternative strategic options with trade-off analysis
            
            Write for C-suite executives who need strategic clarity, financial justification, and actionable implementation guidance for transformative network optimization decisions.
            """,
            agent=agent,
            expected_output="""
            A comprehensive executive strategy report containing:
            
            **Executive Summary:**
            - Key strategic findings and insights from comprehensive analysis
            - Top 3-5 strategic priorities with clear business impact
            - Critical decision points requiring executive attention
            - Bottom-line financial and competitive impact summary
            - Strategic recommendation overview with implementation timeline
            
            **Strategic Action Plan:**
            - Prioritized strategic recommendations with detailed rationale
            - Comprehensive implementation roadmap with phases and timelines
            - Resource requirements and organizational impact assessment
            - Stakeholder engagement and change management strategy
            - Success criteria and milestone definitions
            
            **Financial Business Case:**
            - Comprehensive ROI analysis with multiple scenarios
            - Detailed cost-benefit analysis including implementation costs
            - Financial impact projections (savings, quality improvements, competitive benefits)
            - Investment requirements and funding recommendations
            - Payback period and break-even analysis
            
            **Risk Management Framework:**
            - Comprehensive risk assessment (operational, financial, competitive, regulatory)
            - Risk mitigation strategies and contingency plans
            - Risk monitoring and early warning systems
            - Scenario planning for various risk outcomes
            - Decision frameworks for risk response
            
            **Competitive Strategy:**
            - Competitive positioning strategy based on market intelligence
            - Competitive advantage development and protection strategies
            - Market response scenarios and competitive threat mitigation
            - Strategic differentiation and market positioning recommendations
            - Competitive intelligence monitoring and response framework
            
            **Implementation Excellence Framework:**
            - Detailed project management and governance structure
            - Success metrics, KPIs, and performance monitoring dashboard
            - Change management and organizational readiness assessment
            - Stakeholder communication and engagement strategy
            - Quality assurance and continuous improvement framework
            
            **Executive Decision Package:**
            - Clear go/no-go recommendation with supporting analysis
            - Investment authorization request with detailed justification
            - Alternative strategic options with trade-off analysis
            - Decision criteria and evaluation framework
            - Next steps and immediate action requirements
            """
        )
    
    @staticmethod
    def board_presentation_preparation_task(agent, executive_strategy_results):
        """Board presentation preparation task"""
        return Task(
            description=f"""
            Prepare board-level presentation materials based on executive strategy analysis.
            
            Executive Strategy Results: {executive_strategy_results}
            
            Your preparation should include:
            
            1. **Board-Level Executive Summary**
               - Distill strategy into board-appropriate summary
               - Focus on strategic impact and financial implications
               - Highlight key decisions requiring board oversight
               - Present clear recommendations for board consideration
            
            2. **Financial Investment Proposal**
               - Prepare investment proposal for board approval
               - Include detailed financial justification
               - Present ROI analysis and financial projections
               - Address financial risks and mitigation strategies
            
            3. **Strategic Risk and Governance Considerations**
               - Present strategic risks requiring board attention
               - Address governance and oversight requirements
               - Include regulatory and compliance considerations
               - Present risk management framework for board review
            
            Prepare comprehensive board presentation materials.
            """,
            agent=agent,
            expected_output="""
            Board presentation materials including:
            - Board-level executive summary with strategic recommendations
            - Financial investment proposal with detailed justification
            - Strategic risk assessment and governance framework
            - Key decisions and approvals required from board
            """
        )
    
    @staticmethod
    def stakeholder_communication_strategy_task(agent, strategy_results):
        """Stakeholder communication strategy development task"""
        return Task(
            description=f"""
            Develop comprehensive stakeholder communication strategy for network optimization.
            
            Strategy Results: {strategy_results}
            
            Your strategy should include:
            
            1. **Stakeholder Analysis and Mapping**
               - Identify all key stakeholders affected by network optimization
               - Assess stakeholder influence and impact levels
               - Develop stakeholder engagement priorities
               - Create stakeholder communication matrix
            
            2. **Communication Strategy by Stakeholder Group**
               - Develop tailored communication strategies for each stakeholder group
               - Create key messages and talking points
               - Identify optimal communication channels and timing
               - Address stakeholder concerns and resistance points
            
            3. **Change Management Communication Plan**
               - Develop comprehensive change communication plan
               - Create communication timeline and milestone communications
               - Address change resistance and adoption strategies
               - Include feedback mechanisms and two-way communication
            
            Provide comprehensive stakeholder communication strategy.
            """,
            agent=agent,
            expected_output="""
            Stakeholder communication strategy including:
            - Comprehensive stakeholder analysis and engagement priorities
            - Tailored communication strategies for each stakeholder group
            - Change management communication plan with timelines
            - Key messages, talking points, and communication materials
            """
        )
    
    @staticmethod
    def performance_monitoring_framework_task(agent, implementation_plan):
        """Performance monitoring and success measurement framework task"""
        return Task(
            description=f"""
            Develop comprehensive performance monitoring framework for network optimization.
            
            Implementation Plan: {implementation_plan}
            
            Your framework should include:
            
            1. **Success Metrics and KPI Framework**
               - Define comprehensive success metrics across all optimization dimensions
               - Create KPI dashboard with leading and lagging indicators
               - Establish baseline measurements and target performance levels
               - Include financial, quality, and operational performance metrics
            
            2. **Monitoring and Reporting Structure**
               - Design monitoring processes and reporting cadence
               - Create performance reporting templates and dashboards
               - Establish data collection and validation processes
               - Define escalation procedures for performance issues
            
            3. **Continuous Improvement Framework**
               - Develop continuous improvement processes
               - Create feedback loops and adjustment mechanisms
               - Include lessons learned capture and application
               - Design optimization refinement processes
            
            Provide comprehensive performance monitoring and success measurement framework.
            """,
            agent=agent,
            expected_output="""
            Performance monitoring framework including:
            - Comprehensive KPI framework with success metrics
            - Monitoring processes and reporting structure
            - Performance dashboards and reporting templates
            - Continuous improvement and optimization refinement processes
            """
        )

