# ui/layouts.py
"""
Tab layouts and complex UI sections for the Network Optimization Platform
"""

import streamlit as st
import pandas as pd
from ui.visualizations import create_quadrant_visualization
from ui.components import create_quadrant_summary_metrics
#from config.brand_colors import BRAND_COLORS
# # Import network builder components
# from ui.network_builder_components import (
#     create_provider_selection_interface,
#     create_provider_selection_table,
#     create_network_comparison_metrics,
#     create_adequacy_risk_warning,
#     create_financial_impact_summary,
#     create_scenario_recommendations,
#     create_network_builder_summary,
#     create_scenario_export_options
# )
from tools.network_builder_tool import NetworkBuilderTool

def render_network_intelligence_tab(df, results):
    """Render Network Intelligence Dashboard tab"""
    st.markdown("### Network Intelligence Dashboard")
    
    # Quadrant visualization
    if 'quadrant' in df.columns:
        fig_quadrant = create_quadrant_visualization(df)
        st.plotly_chart(fig_quadrant, use_container_width=True)
        
        # Quadrant summary metrics
        st.markdown("---")
        quadrant_summary = df['quadrant'].value_counts()
        create_quadrant_summary_metrics(quadrant_summary)
    else:
        st.info("Quadrant analysis data not available")
    
    st.markdown("---")
    
    # Strategic Recommendations Section - Above Provider Performance Analysis
    st.markdown("### Strategic Recommendations by Quadrant")
    
    if 'quadrant' in df.columns:
        quadrant_recommendations = {
            "Preferred Partners": [
                "Retain and expand partnerships with these high-performing providers",
                "Negotiate favorable contract renewals and volume bonuses",
                "Use as benchmarks for improving other providers",
                "Consider strategic partnerships for network expansion"
            ],
            "Strategic Opportunities": [
                "Negotiate cost reductions while maintaining quality standards",
                "Explore value-based payment models and shared savings",
                "Consider selective contracting strategies",
                "Monitor for potential quality improvements over time"
            ],
            "Performance Focus": [
                "Implement targeted quality improvement programs",
                "Provide additional training and clinical support",
                "Set quality benchmarks with performance monitoring",
                "Consider performance-based incentives and penalties"
            ],
            "Optimization Candidates": [
                "Initiate immediate performance improvement plans",
                "Consider contract termination if no improvement within 90 days",
                "Identify alternative providers in the same market",
                "Ensure network adequacy before any removals"
            ]
        }
        
        # Display recommendations in 2-column layout
        col1, col2 = st.columns(2)
        
        quadrant_colors = {
            "Preferred Partners": "#4CAF50",  # Green
            "Strategic Opportunities": "#FF9800",  # Orange
            "Performance Focus": "#00B4D8",  # Blue
            "Optimization Candidates": "#F44336"  # Red
        }
        
        quadrant_names = list(quadrant_recommendations.keys())
        
        # First column - first 2 quadrants
        with col1:
            for i in [0, 2]:  # Preferred Partners and Performance Focus
                quadrant = quadrant_names[i]
                color = quadrant_colors[quadrant]
                st.markdown(f"""
                <div style="background: white; border-left: 4px solid {color}; padding: 1rem; margin: 0.5rem 0; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: {color}; margin: 0 0 0.5rem 0;">{quadrant}</h4>
                    <ul style="margin: 0; padding-left: 1rem;">
                """, unsafe_allow_html=True)
                
                for recommendation in quadrant_recommendations[quadrant]:
                    st.markdown(f"<li style='margin: 0.25rem 0;'>{recommendation}</li>", unsafe_allow_html=True)
                
                st.markdown("</ul></div>", unsafe_allow_html=True)
        
        # Second column - last 2 quadrants
        with col2:
            for i in [1, 3]:  # Strategic Opportunities and Optimization Candidates
                quadrant = quadrant_names[i]
                color = quadrant_colors[quadrant]
                st.markdown(f"""
                <div style="background: white; border-left: 4px solid {color}; padding: 1rem; margin: 0.5rem 0; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: {color}; margin: 0 0 0.5rem 0;">{quadrant}</h4>
                    <ul style="margin: 0; padding-left: 1rem;">
                """, unsafe_allow_html=True)
                
                for recommendation in quadrant_recommendations[quadrant]:
                    st.markdown(f"<li style='margin: 0.25rem 0;'>{recommendation}</li>", unsafe_allow_html=True)
                
                st.markdown("</ul></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Provider Performance Analysis - Organized by Quadrants
    st.markdown("### Provider Performance Analysis by Quadrant")
    
    if 'quadrant' in df.columns:
        # Center-aligned quadrant tabs with custom CSS
        st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
        }
        /* Custom styling for data tables */
        .stDataFrame {
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create tabs for each quadrant
        quadrant_tabs = st.tabs([
            "Preferred Partners", 
            "Strategic Opportunities", 
            "Performance Focus", 
            "Optimization Candidates"
        ])
        
        # Provider details by quadrant
        quadrant_names = [
            "Preferred Partners", 
            "Strategic Opportunities", 
            "Performance Focus", 
            "Optimization Candidates"
        ]
        
        for idx, (tab, quadrant_name) in enumerate(zip(quadrant_tabs, quadrant_names)):
            with tab:
                quadrant_providers = df[df['quadrant'] == quadrant_name]
                
                if not quadrant_providers.empty:
                    # Quadrant description
                    quadrant_descriptions = {
                        "Preferred Partners": "High Quality, Low Cost - Retain & Expand these top performers",
                        "Strategic Opportunities": "High Quality, High Cost - Negotiate better terms while maintaining quality",
                        "Performance Focus": "Low Quality, Low Cost - Implement quality improvement programs",
                        "Optimization Candidates": "Low Quality, High Cost - Consider alternatives or comprehensive review"
                    }
                    
                    st.info(f"**{quadrant_name}:** {quadrant_descriptions[quadrant_name]}")
                    
                    # Summary metrics for this quadrant
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Providers", len(quadrant_providers))
                    with col2:
                        st.metric("Avg Quality", f"{quadrant_providers['quality_score'].mean():.1f}")
                    with col3:
                        st.metric("Avg Cost", f"${quadrant_providers['cost_per_utilizer'].mean():.0f}")
                    with col4:
                        st.metric("Total Savings Potential", f"${quadrant_providers['termination_value'].sum()/1000000:.1f}M")
                    
                    st.markdown("---")
                    
                    # Prepare data for table display
                    table_data = []
                    for _, provider in quadrant_providers.iterrows():
                        # Process state performance
                        states_good = ', '.join([k for k, v in provider['state_performance'].items() if v in ['Excellent', 'Good']])
                        states_poor = ', '.join([k for k, v in provider['state_performance'].items() if v == 'Poor'])
                        
                        # Process episode performance
                        episodes_leader = ', '.join([k for k, v in provider['episode_performance'].items() if v == 'Leader'])
                        episodes_needs_improvement = ', '.join([k for k, v in provider['episode_performance'].items() if v == 'Needs Improvement'])
                        
                        table_data.append({
                            'Provider Name': provider['name'],
                            'Quality Score': f"{provider['quality_score']:.1f}",
                            'Cost per Utilizer': f"${provider['cost_per_utilizer']:.0f}",
                            'Savings Potential': f"${provider['termination_value']:,.0f}",
                            'Market Position': f"{provider['market_position_percentile']:.0f}th",
                            'Network Status': provider['network_status'],
                            'Primary CBSA': provider['primary_cbsa'],
                            'Adequacy Risk': provider['adequacy_risk'],
                            'Clinical Group': provider['clinical_group'],
                            'Strong States': states_good if states_good else 'None',
                            'Weak States': states_poor if states_poor else 'None',
                            'Leading Episodes': episodes_leader if episodes_leader else 'None',
                            'Improvement Areas': episodes_needs_improvement if episodes_needs_improvement else 'None'
                        })
                    
                    # Convert to DataFrame for better display
                    display_df = pd.DataFrame(table_data)
                    
                    # Configure column display
                    column_config = {
                        'Provider Name': st.column_config.TextColumn(
                            'Provider Name',
                            width='medium',
                            help='Healthcare provider organization name'
                        ),
                        'Quality Score': st.column_config.NumberColumn(
                            'Quality Score',
                            format='%.1f',
                            width='small',
                            help='Clinical quality rating (1-5 scale)'
                        ),
                        'Cost per Utilizer': st.column_config.TextColumn(
                            'Cost per Utilizer',
                            width='small',
                            help='Average cost per member using this provider'
                        ),
                        'Savings Potential': st.column_config.TextColumn(
                            'Savings Potential',
                            width='medium',
                            help='Projected annual savings from contract termination'
                        ),
                        'Market Position': st.column_config.TextColumn(
                            'Market Position',
                            width='small',
                            help='Percentile ranking in local market'
                        ),
                        'Network Status': st.column_config.TextColumn(
                            'Network Status',
                            width='small'
                        ),
                        'Primary CBSA': st.column_config.TextColumn(
                            'Primary CBSA',
                            width='medium',
                            help='Core Based Statistical Area (primary market)'
                        ),
                        'Adequacy Risk': st.column_config.SelectboxColumn(
                            'Adequacy Risk',
                            width='small',
                            options=['Low', 'Medium', 'High'],
                            help='Risk to network adequacy if removed'
                        ),
                        'Clinical Group': st.column_config.TextColumn(
                            'Clinical Group',
                            width='medium'
                        ),
                        'Strong States': st.column_config.TextColumn(
                            'Strong States',
                            width='medium',
                            help='Geographic areas with excellent/good performance'
                        ),
                        'Weak States': st.column_config.TextColumn(
                            'Weak States',
                            width='medium',
                            help='Geographic areas with poor performance'
                        ),
                        'Leading Episodes': st.column_config.TextColumn(
                            'Leading Episodes',
                            width='medium',
                            help='Service lines where provider excels'
                        ),
                        'Improvement Areas': st.column_config.TextColumn(
                            'Improvement Areas',
                            width='medium',
                            help='Service lines needing performance improvement'
                        )
                    }
                    
                    # Display the data table
                    st.dataframe(
                        display_df,
                        column_config=column_config,
                        use_container_width=True,
                        hide_index=True,
                        height=400  # Set reasonable height for scrolling
                    )
                    
                    # Add download button for the data
                    csv = display_df.to_csv(index=False)
                    st.download_button(
                        label=f"Download {quadrant_name} Data",
                        data=csv,
                        file_name=f"{quadrant_name.lower().replace(' ', '_')}_providers.csv",
                        mime="text/csv",
                        help="Download provider data for further analysis"
                    )
                        
                else:
                    st.info(f"No providers currently in the {quadrant_name} category.")
    else:
        # Fallback to original display if no quadrant data
        st.markdown("### All Providers")
        for _, provider in df.head(10).iterrows():
            with st.expander(f"{provider['name']} - ${provider['termination_value']:,.0f} savings"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    **Basic Info:**
                    - Network Status: {provider['network_status']}
                    - Quality Score: {provider['quality_score']:.1f}/5.0
                    - Cost per Utilizer: ${provider['cost_per_utilizer']:.0f}
                    - Termination Value: ${provider['termination_value']:,.0f}
                    - Market Position: {provider['market_position_percentile']:.0f}th percentile
                    """)
                
                with col2:
                    states_good = ', '.join([k for k, v in provider['state_performance'].items() if v in ['Excellent', 'Good']])
                    states_poor = ', '.join([k for k, v in provider['state_performance'].items() if v == 'Poor'])
                    
                    st.markdown(f"""
                    **Geographic Performance:**
                    - Good States: {states_good if states_good else 'None'}
                    - Poor States: {states_poor if states_poor else 'None'}
                    - Primary CBSA: {provider['primary_cbsa']}
                    - Adequacy Risk: {provider['adequacy_risk']}
                    """)
                
                with col3:
                    episodes_leader = ', '.join([k for k, v in provider['episode_performance'].items() if v == 'Leader'])
                    episodes_needs_improvement = ', '.join([k for k, v in provider['episode_performance'].items() if v == 'Needs Improvement'])
                    
                    st.markdown(f"""
                    **Service Lines:**
                    - Leading Episodes: {episodes_leader if episodes_leader else 'None'}
                    - Needs Improvement: {episodes_needs_improvement if episodes_needs_improvement else 'None'}
                    - Clinical Group: {provider['clinical_group']}
                    """)


