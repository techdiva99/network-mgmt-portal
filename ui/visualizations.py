# ui/visualizations.py
"""
Chart and visualization components for the Network Optimization Platform
"""

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from config.brand_colors import BRAND_COLORS, QUADRANT_COLORS
from config.settings import ANALYSIS_THRESHOLDS

def create_quadrant_visualization(df):
    """Create quadrant visualization matching original styling"""
    quality_threshold = ANALYSIS_THRESHOLDS['quality_threshold']
    cost_threshold = ANALYSIS_THRESHOLDS['cost_threshold']
    
    # Create visualization with original colors
    fig_quadrant = px.scatter(
        df,
        x='cost_per_utilizer',
        y='quality_score',
        size='utilizers',
        color='quadrant',
        hover_data=['name', 'network_status', 'termination_value'],
        title="Provider Performance Quadrants - AI Agent Analysis",
        labels={
            'cost_per_utilizer': 'Cost per Utilizer ($)',
            'quality_score': 'Quality Score',
            'utilizers': 'Utilizer Count'
        },
        color_discrete_map=QUADRANT_COLORS
    )
    
    # Add threshold lines
    fig_quadrant.add_hline(y=quality_threshold, line_dash="dash", line_color="gray", 
                          annotation_text="Quality Threshold")
    fig_quadrant.add_vline(x=cost_threshold, line_dash="dash", line_color="gray", 
                          annotation_text="Cost Threshold")
    
    fig_quadrant.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font_color=BRAND_COLORS['dark_blue'],
        height=500
    )
    
    return fig_quadrant

def create_competitive_positioning_chart(df):
    """Create competitive positioning scatter plot"""
    fig_comp = px.scatter(
        df,
        x='cost_per_utilizer',
        y='quality_score',
        size='utilizers',
        color='network_status',
        hover_data=['name', 'market_position_percentile', 'clinical_group'],
        title="Competitive Positioning Analysis",
        labels={
            'cost_per_utilizer': 'Cost per Utilizer ($)',
            'quality_score': 'Quality Score',
            'network_status': 'Network Status'
        },
        color_discrete_map={
            'In-Network': BRAND_COLORS['primary_green'],
            'Out-of-Network': BRAND_COLORS['error']
        }
    )
    
    fig_comp.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font_color=BRAND_COLORS['dark_blue'],
        height=500
    )
    
    return fig_comp

def create_market_position_bell_curve(df):
    """Create bell curve visualization for market position distribution"""
    # Create bell curve data
    x_values = np.linspace(0, 100, 100)
    mean_position = 50
    std_dev = 20
    y_values = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_values - mean_position) / std_dev) ** 2)
    
    fig_bell = go.Figure()
    
    # Add bell curve
    fig_bell.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        fill='tonexty',
        name='Market Distribution',
        line=dict(color=BRAND_COLORS['primary_blue'], width=2),
        fillcolor=f"rgba(0, 180, 216, 0.3)"
    ))
    
    # Add provider positions
    for _, provider in df.iterrows():
        fig_bell.add_trace(go.Scatter(
            x=[provider['market_position_percentile']],
            y=[0.002],  # Base of curve
            mode='markers',
            marker=dict(
                size=8,
                color=BRAND_COLORS['primary_green'] if provider['network_status'] == 'In-Network' else BRAND_COLORS['error'],
                symbol='diamond'
            ),
            name=provider['name'],
            hovertemplate=f"<b>{provider['name']}</b><br>" +
                        f"Position: {provider['market_position_percentile']:.0f}th percentile<br>" +
                        f"Quality: {provider['quality_score']:.1f}<br>" +
                        f"Cost: ${provider['cost_per_utilizer']:.0f}<extra></extra>",
            showlegend=False
        ))
    
    fig_bell.update_layout(
        title="Provider Market Position Distribution",
        xaxis_title="Market Position Percentile",
        yaxis_title="Distribution Density",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font_color=BRAND_COLORS['dark_blue'],
        height=400
    )
    
    return fig_bell

def create_state_opportunity_bar_chart(state_df):
    """Create state opportunity bar chart"""
    if len(state_df) > 0:
        # Create opportunity tiers based on actual data distribution
        state_df_top15 = state_df.head(15).copy()
        
        # Use quartiles of actual data for tier assignment
        q1 = state_df_top15['Total Opportunity'].quantile(0.25)
        q2 = state_df_top15['Total Opportunity'].quantile(0.50)
        q3 = state_df_top15['Total Opportunity'].quantile(0.75)
        
        def assign_tier(value):
            if value >= q3:
                return 'Very High'
            elif value >= q2:
                return 'High'
            elif value >= q1:
                return 'Medium'
            else:
                return 'Low'
        
        state_df_top15['Opportunity_Tier'] = state_df_top15['Total Opportunity'].apply(assign_tier)
        
        tier_colors = {
            'Low': BRAND_COLORS['light_gray'],
            'Medium': BRAND_COLORS['accent_blue'],
            'High': BRAND_COLORS['primary_blue'],
            'Very High': BRAND_COLORS['dark_blue']
        }
        
        fig_states = px.bar(
            state_df_top15,
            x='State',
            y='Total Opportunity',
            title="Top 15 States by Optimization Opportunity",
            labels={'Total Opportunity': 'Opportunity ($)'},
            color='Opportunity_Tier',
            color_discrete_map=tier_colors,
            category_orders={'Opportunity_Tier': ['Low', 'Medium', 'High', 'Very High']}
        )
        fig_states.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title_font_color=BRAND_COLORS['dark_blue']
        )
        return fig_states
    else:
        return None

def create_episode_performance_chart(provider_data):
    """Create episode performance chart for provider detail"""
    episode_perf_df = pd.DataFrame.from_dict(
        provider_data['episode_performance'], 
        orient='index', 
        columns=['Performance']
    ).reset_index()
    episode_perf_df.columns = ['Episode Type', 'Performance']
    
    fig_episode_perf = px.bar(
        episode_perf_df,
        x='Episode Type',
        y='Performance',
        color='Performance',
        title=f"Episode Performance - {provider_data['name']}",
        color_discrete_map={
            'Leader': BRAND_COLORS['success'],
            'Average': BRAND_COLORS['primary_blue'],
            'Needs Improvement': BRAND_COLORS['warning']
        }
    )
    fig_episode_perf.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font_color=BRAND_COLORS['dark_blue'],
        xaxis_tickangle=-45
    )
    
    return fig_episode_perf

def create_state_performance_chart(provider_data):
    """Create state performance chart for provider detail"""
    state_perf_df = pd.DataFrame.from_dict(
        provider_data['state_performance'], 
        orient='index', 
        columns=['Performance']
    ).reset_index()
    state_perf_df.columns = ['State', 'Performance']
    
    fig_state_perf = px.bar(
        state_perf_df,
        x='State',
        y='Performance',
        color='Performance',
        title=f"State Performance - {provider_data['name']}",
        color_discrete_map={
            'Excellent': BRAND_COLORS['success'],
            'Good': BRAND_COLORS['primary_blue'],
            'Poor': BRAND_COLORS['error']
        }
    )
    fig_state_perf.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font_color=BRAND_COLORS['dark_blue']
    )
    
    return fig_state_perf

def create_us_map_choropleth(state_data):
    """Create US map choropleth for geographic analysis"""
    # State codes mapping
    state_codes = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
        'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
        'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
        'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
        'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
        'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    
    # Prepare data for choropleth
    state_df = pd.DataFrame.from_dict(state_data, orient='index').reset_index()
    state_df.columns = ['State', 'Total_Opportunity', 'Provider_Count', 'Avg_Quality', 'Recommendations']
    
    state_df['State_Full'] = state_df['State'].map(state_codes)
    state_df['Hover_Text'] = state_df.apply(lambda row: 
        f"<b>{row['State']}</b><br>" +
        f"Opportunity: ${row['Total_Opportunity']:,.0f}<br>" +
        f"Providers: {row['Provider_Count']}<br>" +
        f"Avg Quality: {row['Avg_Quality']:.1f}<br>" +
        f"Top Recommendation: {row['Recommendations'][0] if row['Recommendations'] else 'Monitor performance'}",
        axis=1
    )
    
    # Create choropleth map
    fig_map = go.Figure(data=go.Choropleth(
        locations=state_df['State'],
        z=state_df['Total_Opportunity'],
        locationmode='USA-states',
        colorscale=[
            [0, BRAND_COLORS['light_gray']],
            [0.3, BRAND_COLORS['accent_blue']],
            [0.6, BRAND_COLORS['primary_blue']],
            [1.0, BRAND_COLORS['dark_blue']]
        ],
        hovertemplate=state_df['Hover_Text'] + '<extra></extra>',
        colorbar_title="Opportunity ($)",
        showscale=True
    ))
    
    fig_map.update_layout(
        title_text='Network Optimization Opportunities by State',
        title_font_color=BRAND_COLORS['dark_blue'],
        geo=dict(
            scope='usa',
            projection=go.layout.geo.Projection(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        height=500
    )
    
    return fig_map

