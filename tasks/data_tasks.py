# tasks/data_tasks.py
"""
Data processing task definitions for network optimization workflow
"""

# CrewAI imports with fallback
try:
    from crewai import Task
except ImportError:
    class Task:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

class DataProcessingTasks:
    """Data processing task definitions"""
    
    @staticmethod
    def comprehensive_data_processing_task(agent, user_filters):
        """Comprehensive data processing and validation task"""
        return Task(
            description=f"""
            Process the comprehensive provider network dataset with applied filters and perform thorough data quality assessment.
            
            Applied Filters: {user_filters}
            
            Your comprehensive analysis must include:
            
            1. **Data Loading and Validation**
               - Load the complete provider dataset with all network and performance metrics
               - Validate data completeness across all required fields
               - Check for missing or invalid data points
               - Verify clinical group classifications and geographic coverage
            
            2. **Filter Application and Impact Analysis**
               - Apply all user-specified filters accurately
               - Document the impact of each filter on the dataset
               - Ensure filter logic is correctly implemented
               - Validate filtered results for completeness
            
            3. **Data Quality Assessment**
               - Perform comprehensive data quality validation
               - Identify anomalies, outliers, and inconsistencies
               - Check for duplicate providers or conflicting information
               - Validate performance metric ranges and distributions
            
            4. **Clinical Group Analysis**
               - Verify clinical group classifications are accurate
               - Ensure comprehensive coverage across all clinical groups
               - Validate clinical group performance metrics
               - Check for gaps in clinical group coverage by geography
            
            5. **Geographic Data Validation**
               - Validate state and CBSA geographic assignments
               - Check for complete geographic coverage
               - Ensure operating states data is consistent
               - Validate primary CBSA assignments
            
            6. **Performance Metrics Validation**
               - Validate quality scores, cost metrics, and utilization data
               - Check for reasonable ranges and distributions
               - Identify potential data quality issues
               - Ensure metrics are consistent across providers
            
            Prepare clean, validated data ready for downstream quadrant analysis and competitive intelligence.
            Provide detailed data quality report with any issues identified and recommendations for resolution.
            """,
            agent=agent,
            expected_output="""
            A comprehensive data processing report containing:
            
            **Processed Dataset:**
            - Complete filtered dataset ready for analysis
            - All data quality issues resolved or flagged
            - Validated clinical group and geographic assignments
            - Clean performance metrics ready for analysis
            
            **Data Quality Assessment:**
            - Detailed data quality validation results
            - Identification of any anomalies or issues
            - Data completeness analysis across all dimensions
            - Recommendations for data quality improvements
            
            **Filter Impact Analysis:**
            - Summary of filters applied and their impact
            - Provider count changes by filter type
            - Geographic and clinical group coverage after filtering
            - Validation that filters were applied correctly
            
            **Dataset Summary Statistics:**
            - Total providers in filtered dataset
            - Clinical group distribution
            - Geographic coverage summary
            - Performance metric distributions
            - Network status breakdown
            
            **Processing Metadata:**
            - Data processing performance metrics
            - Processing time and efficiency measures
            - Data validation status and quality score
            - Recommendations for optimization workflow
            """
        )
    
    @staticmethod
    def clinical_group_data_analysis_task(agent, processed_data):
        """Clinical group specific data analysis task"""
        return Task(
            description=f"""
            Perform detailed clinical group analysis on the processed provider data.
            
            Processed Data: {processed_data}
            
            Your analysis should focus on:
            
            1. **Clinical Group Distribution Analysis**
               - Analyze provider distribution across all clinical groups
               - Identify gaps in clinical group coverage
               - Assess network adequacy by clinical group
            
            2. **Performance Analysis by Clinical Group**
               - Compare performance metrics across clinical groups
               - Identify top and bottom performing clinical groups
               - Analyze cost and quality variations by clinical group
            
            3. **Geographic Coverage by Clinical Group**
               - Assess clinical group coverage across states and CBSAs
               - Identify geographic gaps in clinical group services
               - Analyze network adequacy risks by clinical group and geography
            
            Provide detailed clinical group insights ready for optimization analysis.
            """,
            agent=agent,
            expected_output="""
            Detailed clinical group analysis including:
            - Clinical group performance benchmarking
            - Geographic coverage assessment by clinical group
            - Network adequacy analysis
            - Identified gaps and optimization opportunities
            """
        )
    
    @staticmethod
    def geographic_data_preparation_task(agent, processed_data):
        """Geographic data preparation and analysis task"""
        return Task(
            description=f"""
            Prepare geographic data analysis for network optimization.
            
            Processed Data: {processed_data}
            
            Your preparation should include:
            
            1. **State-Level Data Aggregation**
               - Aggregate provider data by state
               - Calculate state-level performance metrics
               - Assess network coverage and adequacy by state
            
            2. **CBSA-Level Analysis Preparation**
               - Prepare CBSA-level provider analysis
               - Assess market competition by CBSA
               - Identify expansion and consolidation opportunities
            
            3. **Geographic Network Adequacy Assessment**
               - Evaluate network adequacy across all geographic regions
               - Identify potential adequacy risks from proposed changes
               - Prepare geographic optimization recommendations
            
            Ensure geographic data is properly structured for optimization analysis.
            """,
            agent=agent,
            expected_output="""
            Geographic analysis preparation including:
            - State and CBSA level data aggregations
            - Geographic network adequacy assessment
            - Market analysis by geographic region
            - Geographic optimization opportunity identification
            """
        )

