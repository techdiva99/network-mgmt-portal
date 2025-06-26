# ui/layouts.py
"""
Tab layouts and complex UI sections for the Network Optimization Platform
"""

import streamlit as st
import pandas as pd
from ui.visualizations import create_quadrant_visualization
from ui.components import create_quadrant_summary_metrics, create_provider_card
from config.brand_colors import BRAND_COLORS
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

def render_optimization_summary_tab(df, results):
    """Render Network Optimization Summary tab"""
    st.markdown("### Network Optimization Summary")
    st.markdown("**AI-driven clinical and financial analysis for network optimization**")
    
    st.markdown("---")
    
    # Get recommendations from quadrant analysis
    if 'quadrant_analysis' in results and 'removal_candidates' in results['quadrant_analysis']:
        removal_candidates = results['quadrant_analysis']['removal_candidates']
        addition_candidates = results['quadrant_analysis']['addition_candidates']
        
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown("#### Priority Network Removals")
            st.markdown("*Providers recommended for contract termination based on performance and cost analysis:*")
            
            for provider in removal_candidates[:5]:
                provider_card_html = create_provider_card(provider, "removal")
                st.markdown(provider_card_html, unsafe_allow_html=True)
            
            # Summary for removals
            if removal_candidates:
                total_removal_savings = sum(p['termination_value'] for p in removal_candidates)
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("Total Annual Savings", f"${total_removal_savings/1000000:.1f}M", 
                             help="Projected annual financial benefit from contract terminations")
                with col_metric2:
                    avg_quality = sum(p['quality_score'] for p in removal_candidates) / len(removal_candidates)
                    quality_improvement = 4.0 - avg_quality
                    st.metric("Network Quality Impact", f"+{quality_improvement:.2f}", 
                             help="Expected improvement in average network quality score")
        
        with col_right:
            st.markdown("#### Strategic Network Additions")
            st.markdown("*High-performing out-of-network providers recommended for contract negotiation:*")
            
            for provider in addition_candidates[:5]:
                provider_card_html = create_provider_card(provider, "addition")
                st.markdown(provider_card_html, unsafe_allow_html=True)
            
            # Summary for additions
            if addition_candidates:
                current_in_network = df[df['network_status'] == 'In-Network']
                addition_quality = sum(p['quality_score'] for p in addition_candidates) / len(addition_candidates)
                current_quality = current_in_network['quality_score'].mean() if not current_in_network.empty else 0
                network_quality_improvement = addition_quality - current_quality
                potential_volume = sum(p['utilizers'] for p in addition_candidates)
                
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("Quality Enhancement", f"+{network_quality_improvement:.2f}", 
                             help="Expected improvement from adding high-performing providers")
                with col_metric2:
                    st.metric("Additional Capacity", f"{potential_volume:,}", 
                             help="Additional member capacity from new provider partnerships")
    
    st.markdown("---")
    
    # Executive Summary Section
    st.markdown("### Executive Summary")
    
    # Calculate overall impact
    total_current_providers = len(df[df['network_status'] == 'In-Network'])
    total_removal_candidates = len(removal_candidates) if 'removal_candidates' in locals() else 0
    total_addition_candidates = len(addition_candidates) if 'addition_candidates' in locals() else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Network Size", f"{total_current_providers}", 
                 help="Total in-network providers in current analysis")
    
    with col2:
        st.metric("Recommended Removals", f"{total_removal_candidates}", 
                 help="Providers recommended for contract termination")
    
    with col3:
        st.metric("Recommended Additions", f"{total_addition_candidates}", 
                 help="Out-of-network providers recommended for recruitment")
    
    with col4:
        net_change = total_addition_candidates - total_removal_candidates
        st.metric("Net Network Change", f"{net_change:+d}", 
                 help="Overall change in provider count")
    
    # Clinical and Business Impact Summary
    st.markdown("#### Key Performance Indicators")
    
    if 'quadrant_analysis' in results and 'financial_impact' in results['quadrant_analysis']:
        financial_impact = results['quadrant_analysis']['financial_impact']
        
        impact_summary = f"""
        **Financial Impact:**
        - Projected annual cost savings: ${financial_impact['total_removal_savings']/1000000:.1f}M from contract optimizations
        - Network efficiency improvement through strategic provider mix optimization
        
        **Quality Enhancement:**
        - Expected network quality score improvement: +{financial_impact['avg_quality_improvement']:.2f} points
        - Enhanced member access to high-performing providers
        
        **Operational Benefits:**
        - Streamlined provider network reducing administrative complexity
        - Improved contract negotiation leverage with performance-based partnerships
        - Enhanced member satisfaction through quality-focused network composition
        
        **Risk Mitigation:**
        - All removal recommendations maintain adequate network coverage
        - Strategic additions strengthen market position and member choice
        - Balanced approach ensuring regulatory compliance and member access standards
        """
        
        st.markdown(impact_summary)
    else:
        st.info("Detailed financial impact analysis will be available after quadrant analysis completion.")
# Add this function to ui/layouts.py

# def render_network_builder_tab(df, results):
#     """Render the Network Builder tab - custom network scenario analysis"""
    
#     st.markdown("### Network Builder - Custom Scenario Analysis")
#     st.markdown("*Build and analyze custom provider network scenarios with real-time feedback*")
    
    
    
#     # Initialize session state for network builder
#     if 'selected_providers' not in st.session_state:
#         st.session_state.selected_providers = []
    
#     # Initialize with current network if no selections
#     if not st.session_state.selected_providers and 'network_status' in df.columns:
#         current_network_ids = df[df['network_status'] == 'In-Network']['provider_id'].tolist()
#         st.session_state.selected_providers = current_network_ids
    
#     # Network builder status summary
#     selected_count = len(st.session_state.selected_providers)
#     total_available = len(df)
#     create_network_builder_summary(selected_count, total_available)
    
#     st.markdown("---")
    
#     # Main network builder interface - 2 column layout
#     left_col, right_col = st.columns([1, 1])
    
#     with left_col:
#         st.markdown("### Provider Selection")
        
#         # Provider selection interface with filters
#         filtered_df = create_provider_selection_interface(df, st.session_state.selected_providers)
        
#         # Provider selection table
#         create_provider_selection_table(filtered_df, st.session_state.selected_providers)
    
#     with right_col:
#         st.markdown("### Network Analysis")
        
#         # Only run analysis if providers are selected
#         if st.session_state.selected_providers:
            
#             # Initialize network builder tool
#             network_tool = NetworkBuilderTool()
            
#             # Run network analysis
#             with st.spinner("Analyzing network scenario..."):
#                 try:
#                     # Convert DataFrame to records for tool
#                     provider_data = df.to_dict('records')
                    
#                     # Run analysis
#                     scenario_results = network_tool._run(
#                         all_providers=provider_data,
#                         selected_provider_ids=st.session_state.selected_providers,
#                         scenario_name="Custom Network Scenario"
#                     )
                    
#                     if scenario_results['success']:
#                         # Network comparison metrics
#                         create_network_comparison_metrics(
#                             scenario_results['current_network_metrics'],
#                             scenario_results['proposed_network_metrics'],
#                             scenario_results['scenario_metrics']
#                         )
                        
#                         st.markdown("---")
                        
#                         # Network adequacy warning
#                         create_adequacy_risk_warning(scenario_results['adequacy_assessment'])
                        
#                         st.markdown("---")
                        
#                         # Financial impact summary
#                         create_financial_impact_summary(scenario_results['financial_impact'])
                        
#                         st.markdown("---")
                        
#                         # Scenario recommendations
#                         create_scenario_recommendations(scenario_results['recommendations'])
                        
#                     else:
#                         st.error("Error analyzing network scenario. Please try again.")
                        
#                 except Exception as e:
#                     st.error(f"Analysis error: {str(e)}")
#                     scenario_results = None
#         else:
#             st.info("Please select providers to analyze your custom network scenario.")
#             scenario_results = None
    
#     st.markdown("---")
    
#     # Bottom section - Detailed analysis and export
#     if scenario_results and scenario_results['success']:
        
#         # Detailed analysis tabs
#         detail_tab1, detail_tab2, detail_tab3 = st.tabs([
#             "Provider Changes",
#             "Detailed Analysis", 
#             "Export & Save"
#         ])
        
#         with detail_tab1:
#             st.markdown("#### Provider Network Changes")
            
#             provider_changes = scenario_results['provider_changes']
            
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 st.markdown("##### Providers Added")
#                 if provider_changes['additions']:
#                     added_providers = df[df['provider_id'].isin(provider_changes['additions'])]
#                     for _, provider in added_providers.iterrows():
#                         st.markdown(f"+ **{provider['name']}** ({provider['clinical_group']})")
#                 else:
#                     st.info("No providers added")
            
#             with col2:
#                 st.markdown("##### Providers Removed")
#                 if provider_changes['removals']:
#                     removed_providers = df[df['provider_id'].isin(provider_changes['removals'])]
#                     for _, provider in removed_providers.iterrows():
#                         st.markdown(f"- **{provider['name']}** ({provider['clinical_group']})")
#                 else:
#                     st.info("No providers removed")
            
#             with col3:
#                 st.markdown("##### Change Summary")
#                 st.metric("Providers Added", provider_changes['additions_count'])
#                 st.metric("Providers Removed", provider_changes['removals_count'])
#                 st.metric("Providers Retained", provider_changes['retained_count'])
                
#                 net_change = provider_changes['additions_count'] - provider_changes['removals_count']
#                 st.metric("Net Change", f"{net_change:+d}")
        
#         with detail_tab2:
#             st.markdown("#### Detailed Scenario Analysis")
            
#             # Performance scores breakdown
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.markdown("##### Performance Scores")
#                 scenario_metrics = scenario_results['scenario_metrics']
                
#                 st.metric("Quality Improvement Score", f"{scenario_metrics['quality_improvement_score']:.0f}/100")
#                 st.metric("Cost Efficiency Score", f"{scenario_metrics['cost_efficiency_score']:.0f}/100")
#                 st.metric("Overall Performance Score", f"{scenario_metrics['network_performance_score']:.0f}/100")
                
#                 st.markdown("##### Network Adequacy Breakdown")
#                 adequacy = scenario_results['adequacy_assessment']
#                 st.metric("Clinical Coverage", f"{adequacy['clinical_coverage']['coverage_score']:.0f}%")
#                 st.metric("Geographic Coverage", f"{adequacy['geographic_coverage']['coverage_score']:.0f}%")
#                 st.metric("Risk Assessment", f"{adequacy['high_risk_assessment']['risk_score']:.0f}/100")
            
#             with col2:
#                 st.markdown("##### Financial Breakdown")
#                 financial = scenario_results['financial_impact']
                
#                 # Create financial summary table
#                 financial_summary = pd.DataFrame([
#                     {"Category": "Removal Savings", "Amount": f"${financial['removal_savings']:,.0f}"},
#                     {"Category": "Addition Costs", "Amount": f"${financial['addition_costs']:,.0f}"},
#                     {"Category": "Net Savings", "Amount": f"${financial['net_savings']:,.0f}"},
#                     {"Category": "Quality Value", "Amount": f"${financial['quality_value']:,.0f}"},
#                     {"Category": "Total Value", "Amount": f"${financial['total_value']:,.0f}"}
#                 ])
                
#                 st.dataframe(financial_summary, use_container_width=True, hide_index=True)
                
#                 # ROI analysis
#                 st.markdown("##### ROI Analysis")
#                 if financial['addition_costs'] > 0:
#                     payback_months = (financial['addition_costs'] / max(financial['net_savings'], 1)) * 12
#                     st.metric("Payback Period", f"{payback_months:.1f} months")
                
#                 st.metric("ROI Percentage", f"{financial['roi_percentage']:.0f}%")
        
#         with detail_tab3:
#             st.markdown("#### Export & Save Options")
            
#             # Export scenario results
#             create_scenario_export_options(scenario_results)
            
#             # Download selected providers as CSV
#             if st.session_state.selected_providers:
#                 selected_provider_data = df[df['provider_id'].isin(st.session_state.selected_providers)]
                
#                 # Prepare download data
#                 download_data = selected_provider_data[[
#                     'name', 'quality_score', 'cost_per_utilizer', 'network_status',
#                     'clinical_group', 'primary_cbsa', 'adequacy_risk', 'termination_value'
#                 ]].copy()
                
#                 download_data.columns = [
#                     'Provider Name', 'Quality Score', 'Cost per Utilizer', 'Network Status',
#                     'Clinical Group', 'Primary CBSA', 'Adequacy Risk', 'Savings Potential'
#                 ]
                
#                 csv_data = download_data.to_csv(index=False)
                
#                 st.download_button(
#                     label="Download Selected Providers (CSV)",
#                     data=csv_data,
#                     file_name=f"custom_network_scenario_{len(st.session_state.selected_providers)}_providers.csv",
#                     mime="text/csv",
#                     help="Download the list of selected providers for your custom network"
#                 )
            
#             # Scenario summary for export
#             if scenario_results:
#                 scenario_summary = f"""
# # Network Builder Scenario Analysis Report

# ## Scenario Overview
# - **Scenario Name**: {scenario_results['scenario_name']}
# - **Total Providers Selected**: {len(st.session_state.selected_providers)}
# - **Analysis Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

# ## Key Metrics
# - **Quality Change**: {scenario_results['scenario_metrics']['quality_change']:+.2f} points
# - **Cost Change**: ${scenario_results['scenario_metrics']['cost_change']:+.0f} per utilizer
# - **Provider Change**: {scenario_results['scenario_metrics']['provider_change']:+d} providers
# - **Net Financial Impact**: ${scenario_results['financial_impact']['total_value']:,.0f}

# ## Network Adequacy
# - **Adequacy Level**: {scenario_results['adequacy_assessment']['adequacy_level']}
# - **Adequacy Score**: {scenario_results['adequacy_assessment']['adequacy_score']}/100
# - **Clinical Coverage**: {scenario_results['adequacy_assessment']['clinical_coverage']['coverage_score']:.0f}%
# - **Geographic Coverage**: {scenario_results['adequacy_assessment']['geographic_coverage']['coverage_score']:.0f}%

# ## Recommendations
# {chr(10).join(f"- {rec}" for rec in scenario_results['recommendations'])}

# ## Provider Changes
# - **Added**: {scenario_results['provider_changes']['additions_count']} providers
# - **Removed**: {scenario_results['provider_changes']['removals_count']} providers
# - **Retained**: {scenario_results['provider_changes']['retained_count']} providers
# """
                
#                 st.download_button(
#                     label="Download Scenario Report (TXT)",
#                     data=scenario_summary,
#                     file_name=f"network_scenario_analysis_report.txt",
#                     mime="text/plain",
#                     help="Download a comprehensive analysis report for this scenario"
#                 )
    
#     # Help section
#     with st.expander("Network Builder Help & Tips"):
#         st.markdown("""
#         ### How to Use the Network Builder
        
#         1. **Select Providers**: Use the left panel to search, filter, and select providers for your custom network
#         2. **Quick Actions**: Use the quick selection buttons to rapidly select groups of providers
#         3. **Real-time Analysis**: The right panel updates automatically as you make selections
#         4. **Network Adequacy**: Pay attention to adequacy warnings to ensure regulatory compliance
#         5. **Financial Impact**: Review the financial analysis to understand the business case
#         6. **Export Results**: Save your scenario and download provider lists for implementation
        
#         ### Selection Tips
#         - Start with current in-network providers and make adjustments
#         - Use quality and cost filters to identify optimal providers
#         - Monitor network adequacy scores to avoid coverage gaps
#         - Consider clinical group coverage across all geographic areas
        
#         ### Adequacy Guidelines
#         - **Safe (80-100)**: Network meets all adequacy requirements
#         - **Warning (60-79)**: Some adequacy concerns, monitor closely
#         - **Critical (<60)**: Significant adequacy issues, address before implementation
#         """)

