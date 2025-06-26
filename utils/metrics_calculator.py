# utils/metrics_calculator.py
"""
Network performance metrics calculation utilities
"""

import pandas as pd
from config.brand_colors import QUADRANT_COLORS
from config.settings import ANALYSIS_THRESHOLDS

def calculate_network_metrics(df):
    """Calculate enhanced network performance metrics"""
    in_network = df[df['network_status'] == 'In-Network']
    
    return {
        'total_providers': len(df),
        'in_network_providers': len(in_network),
        'out_network_providers': len(df) - len(in_network),
        'total_utilizers': in_network['utilizers'].sum(),
        'avg_cost_per_utilizer': in_network['cost_per_utilizer'].mean(),
        'avg_quality_score': in_network['quality_score'].mean(),
        'network_savings': in_network['termination_value'].sum(),
        'cost_efficiency_percent': 10,
        'high_risk_removals': len(in_network[in_network['adequacy_risk'] == 'High']),
        'total_opportunity': df['termination_value'].sum()
    }

def get_quadrant_category(quality, cost, quality_threshold=None, cost_threshold=None):
    """Categorize providers into performance quadrants"""
    if quality_threshold is None:
        quality_threshold = ANALYSIS_THRESHOLDS['quality_threshold']
    if cost_threshold is None:
        cost_threshold = ANALYSIS_THRESHOLDS['cost_threshold']
    
    if quality >= quality_threshold and cost <= cost_threshold:
        return "Preferred Partners", QUADRANT_COLORS['Preferred Partners']
    elif quality >= quality_threshold and cost > cost_threshold:
        return "Strategic Opportunities", QUADRANT_COLORS['Strategic Opportunities']
    elif quality < quality_threshold and cost <= cost_threshold:
        return "Performance Focus", QUADRANT_COLORS['Performance Focus']
    else:
        return "Optimization Candidates", QUADRANT_COLORS['Optimization Candidates']

def add_quadrant_analysis(df):
    """Add quadrant categories to dataframe"""
    df = df.copy()
    df['quadrant'], df['quadrant_color'] = zip(*df.apply(
        lambda row: get_quadrant_category(row['quality_score'], row['cost_per_utilizer']), axis=1
    ))
    return df

def identify_removal_candidates(df):
    """Identify high-priority removal candidates"""
    return df[
        (df['quadrant'] == 'Optimization Candidates') & 
        (df['adequacy_risk'] != 'High')
    ].sort_values('termination_value', ascending=False)

def identify_addition_candidates(df):
    """Identify strategic addition opportunities"""
    return df[
        (df['network_status'] == 'Out-of-Network') & 
        (df['quality_score'] >= 4.0) & 
        (df['cost_per_utilizer'] <= 600)
    ].sort_values(['quality_score', 'cost_per_utilizer'], ascending=[False, True])

def calculate_financial_impact(removal_candidates, addition_candidates):
    """Calculate comprehensive financial impact"""
    total_removal_savings = removal_candidates['termination_value'].sum() if not removal_candidates.empty else 0
    avg_quality_improvement = (4.0 - removal_candidates['quality_score'].mean()) if not removal_candidates.empty else 0
    
    potential_volume = addition_candidates['utilizers'].sum() if not addition_candidates.empty else 0
    
    return {
        'total_removal_savings': total_removal_savings,
        'avg_quality_improvement': avg_quality_improvement,
        'potential_additional_volume': potential_volume,
        'net_financial_impact': total_removal_savings  # Simplified calculation
    }

def get_volume_category(utilizers):
    """Categorize provider volume"""
    if utilizers > ANALYSIS_THRESHOLDS['high_volume_threshold']:
        return "High Volume"
    elif utilizers >= ANALYSIS_THRESHOLDS['medium_volume_threshold']:
        return "Medium Volume"
    else:
        return "Low Volume"

def get_quality_category(quality_score):
    """Categorize provider quality"""
    if quality_score > ANALYSIS_THRESHOLDS['high_quality_threshold']:
        return "High Quality"
    elif quality_score >= ANALYSIS_THRESHOLDS['medium_quality_threshold']:
        return "Medium Quality"
    else:
        return "Low Quality"

def get_cost_category(cost_per_utilizer):
    """Categorize provider cost"""
    if cost_per_utilizer > ANALYSIS_THRESHOLDS['high_cost_threshold']:
        return "High Cost"
    elif cost_per_utilizer >= ANALYSIS_THRESHOLDS['medium_cost_threshold']:
        return "Medium Cost"
    else:
        return "Low Cost"

