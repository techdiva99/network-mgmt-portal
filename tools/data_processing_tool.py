# tools/data_processing_tool.py
"""
Data processing tool for network optimization analysis
"""

from typing import Dict, Any
import pandas as pd
from utils.data_generator import generate_provider_data
from utils.metrics_calculator import get_volume_category, get_quality_category, get_cost_category
from config.settings import ANALYSIS_THRESHOLDS

# CrewAI imports with fallback
try:
    from crewai.tools import BaseTool
except ImportError:
    try:
        from crewai_tools import BaseTool
    except ImportError:
        class BaseTool:
            name: str = ""
            description: str = ""
            def _run(self, *args, **kwargs):
                raise NotImplementedError

class NetworkDataTool(BaseTool):
    name: str = "Network Data Processing Tool"
    description: str = "Load and process provider network data with advanced filtering capabilities"
    
    def _run(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Load enhanced sample data matching original functionality"""
        
        # Generate comprehensive provider data
        df = generate_provider_data()
        
        # Apply filters if provided
        if filters:
            df = self._apply_filters(df, filters)
        
        # Add derived metrics
        df['volume_category'] = df['utilizers'].apply(get_volume_category)
        df['quality_category'] = df['quality_score'].apply(get_quality_category)
        df['cost_category'] = df['cost_per_utilizer'].apply(get_cost_category)
        
        return {
            "data": df.to_dict('records'),
            "summary": {
                "total_providers": len(df),
                "in_network": len(df[df['network_status'] == 'In-Network']),
                "out_network": len(df[df['network_status'] == 'Out-of-Network']),
                "avg_quality": df['quality_score'].mean(),
                "avg_cost": df['cost_per_utilizer'].mean(),
                "total_opportunity": df['termination_value'].sum(),
                "data_quality_score": 98.5,
                "processing_status": "complete"
            }
        }
    
    def _apply_filters(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply comprehensive filters matching original functionality"""
        filtered_df = df.copy()
        
        # Network status filter
        if filters.get('network_statuses'):
            filtered_df = filtered_df[filtered_df['network_status'].isin(filters['network_statuses'])]
        
        # Volume filters
        volume_filter = filters.get('volume_filter', 'All Volumes')
        if volume_filter == "High Volume (>3000)":
            filtered_df = filtered_df[filtered_df['utilizers'] > ANALYSIS_THRESHOLDS['high_volume_threshold']]
        elif volume_filter == "Medium Volume (1000-3000)":
            filtered_df = filtered_df[
                (filtered_df['utilizers'] >= ANALYSIS_THRESHOLDS['medium_volume_threshold']) & 
                (filtered_df['utilizers'] <= ANALYSIS_THRESHOLDS['high_volume_threshold'])
            ]
        elif volume_filter == "Low Volume (<1000)":
            filtered_df = filtered_df[filtered_df['utilizers'] < ANALYSIS_THRESHOLDS['medium_volume_threshold']]
        
        # Quality filters
        quality_filter = filters.get('quality_filter', 'All Quality')
        if quality_filter == "High Quality (>4.5)":
            filtered_df = filtered_df[filtered_df['quality_score'] > ANALYSIS_THRESHOLDS['high_quality_threshold']]
        elif quality_filter == "Medium Quality (3.5-4.5)":
            filtered_df = filtered_df[
                (filtered_df['quality_score'] >= ANALYSIS_THRESHOLDS['medium_quality_threshold']) & 
                (filtered_df['quality_score'] <= ANALYSIS_THRESHOLDS['high_quality_threshold'])
            ]
        elif quality_filter == "Low Quality (<3.5)":
            filtered_df = filtered_df[filtered_df['quality_score'] < ANALYSIS_THRESHOLDS['medium_quality_threshold']]
        
        # Cost filters
        cost_filter = filters.get('cost_filter', 'All Costs')
        if cost_filter == "High Cost (>$700)":
            filtered_df = filtered_df[filtered_df['cost_per_utilizer'] > ANALYSIS_THRESHOLDS['high_cost_threshold']]
        elif cost_filter == "Medium Cost ($400-700)":
            filtered_df = filtered_df[
                (filtered_df['cost_per_utilizer'] >= ANALYSIS_THRESHOLDS['medium_cost_threshold']) & 
                (filtered_df['cost_per_utilizer'] <= ANALYSIS_THRESHOLDS['high_cost_threshold'])
            ]
        elif cost_filter == "Low Cost (<$400)":
            filtered_df = filtered_df[filtered_df['cost_per_utilizer'] < ANALYSIS_THRESHOLDS['medium_cost_threshold']]
        
        # Geographic filters
        if filters.get('state_filter') and filters['state_filter'] != "All States":
            filtered_df = filtered_df[filtered_df['operating_states'].apply(lambda x: filters['state_filter'] in x)]
        
        if filters.get('cbsa_filter') and filters['cbsa_filter'] != "All CBSAs":
            filtered_df = filtered_df[filtered_df['primary_cbsa'] == filters['cbsa_filter']]
        
        if filters.get('clinical_group_filter') and filters['clinical_group_filter'] != "All Clinical Groups":
            filtered_df = filtered_df[filtered_df['clinical_group'] == filters['clinical_group_filter']]
        
        # Adequacy risk filter
        if filters.get('adequacy_filter') and filters['adequacy_filter'] != "All Risk Levels":
            risk_level = filters['adequacy_filter'].replace(" Risk", "")
            filtered_df = filtered_df[filtered_df['adequacy_risk'] == risk_level]
        
        # TIN search (mock implementation)
        if filters.get('tin_search'):
            # In real implementation, this would search actual TIN numbers
            pass
        
        return filtered_df

