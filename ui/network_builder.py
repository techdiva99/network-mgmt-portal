# ui/network_builder.py
"""
Complete Network Builder tab implementation
"""
from ui.network_builder_components import *
from tools.network_builder_tool import NetworkBuilderTool


def render_network_builder_tab(df, results):
    """Render the Network Builder tab - custom network scenario analysis"""
    
    st.markdown("### Network Builder - Custom Scenario Analysis")
    st.markdown("*Build and analyze custom provider network scenarios with real-time feedback*")
    
    # Initialize session state for network builder
    if 'selected_providers' not in st.session_state:
        st.session_state.selected_providers = []
    
    if 'saved_scenarios' not in st.session_state:
        st.session_state.saved_scenarios = []
    
    # Initialize with current network if no selections and provider_id exists
    if not st.session_state.selected_providers and 'network_status' in df.columns:
        if 'provider_id' in df.columns:
            current_network_ids = df[df['network_status'] == 'In-Network']['provider_id'].tolist()
            st.session_state.selected_providers = current_network_ids
        else:
            # Fallback: use index if provider_id doesn't exist
            current_network_indices = df[df['network_status'] == 'In-Network'].index.tolist()
            st.session_state.selected_providers = [f"IDX_{idx}" for idx in current_network_indices]
    
    # Network builder status summary
    selected_count = len(st.session_state.selected_providers)
    total_available = len(df)
    selection_percentage = (selected_count / total_available * 100) if total_available > 0 else 0
    
    st.markdown(f"""
    <div style="background: #E1F5FE; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <h5 style="color: #003F5C; margin: 0 0 0.5rem 0;">Network Builder Status</h5>
        <p style="margin: 0; color: #003F5C;">
            <strong>{selected_count}</strong> providers selected from <strong>{total_available}</strong> available 
            (<strong>{selection_percentage:.1f}%</strong> of total network)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main network builder interface - 2 column layout
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        st.markdown("### Provider Selection")
        
        # Quick selection actions
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Select All In-Network", use_container_width=True):
                if 'provider_id' in df.columns:
                    in_network_ids = df[df['network_status'] == 'In-Network']['provider_id'].tolist()
                else:
                    in_network_ids = [f"IDX_{idx}" for idx in df[df['network_status'] == 'In-Network'].index.tolist()]
                st.session_state.selected_providers = list(set(st.session_state.selected_providers + in_network_ids))
                st.rerun()
        
        with col2:
            if st.button("Select High Quality (≥4.5)", use_container_width=True):
                if 'provider_id' in df.columns:
                    high_quality_ids = df[df['quality_score'] >= 4.5]['provider_id'].tolist()
                else:
                    high_quality_ids = [f"IDX_{idx}" for idx in df[df['quality_score'] >= 4.5].index.tolist()]
                st.session_state.selected_providers = list(set(st.session_state.selected_providers + high_quality_ids))
                st.rerun()
        
        with col3:
            if st.button("Select Preferred Partners", use_container_width=True):
                if 'quadrant' in df.columns:
                    if 'provider_id' in df.columns:
                        preferred_ids = df[df['quadrant'] == 'Preferred Partners']['provider_id'].tolist()
                    else:
                        preferred_ids = [f"IDX_{idx}" for idx in df[df['quadrant'] == 'Preferred Partners'].index.tolist()]
                    st.session_state.selected_providers = list(set(st.session_state.selected_providers + preferred_ids))
                    st.rerun()
        
        with col4:
            if st.button("Clear All Selections", use_container_width=True):
                st.session_state.selected_providers = []
                st.rerun()
        
        st.markdown("---")
        
        # Search and filter section
        st.markdown("##### Search & Filter Providers")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            # Text search
            search_term = st.text_input("Search by provider name", placeholder="Enter provider name...")
            
            # Quality filter
            quality_range = st.slider(
                "Quality Score Range",
                min_value=float(df['quality_score'].min()),
                max_value=float(df['quality_score'].max()),
                value=(float(df['quality_score'].min()), float(df['quality_score'].max())),
                step=0.1
            )
        
        with filter_col2:
            # Clinical group filter
            clinical_groups = df['clinical_group'].unique().tolist()
            selected_clinical_groups = st.multiselect(
                "Clinical Groups",
                options=clinical_groups,
                default=clinical_groups
            )
            
            # Cost filter
            cost_range = st.slider(
                "Cost per Utilizer Range",
                min_value=int(df['cost_per_utilizer'].min()),
                max_value=int(df['cost_per_utilizer'].max()),
                value=(int(df['cost_per_utilizer'].min()), int(df['cost_per_utilizer'].max())),
                step=10
            )
        
        with filter_col3:
            # Network status filter
            network_statuses = df['network_status'].unique().tolist()
            selected_network_statuses = st.multiselect(
                "Network Status",
                options=network_statuses,
                default=network_statuses
            )
            
            # Quadrant filter (if available)
            if 'quadrant' in df.columns:
                quadrants = df['quadrant'].unique().tolist()
                selected_quadrants = st.multiselect(
                    "Performance Quadrants",
                    options=quadrants,
                    default=quadrants
                )
            else:
                selected_quadrants = []
        
        # Apply filters
        filtered_df = df.copy()
        
        # Apply search filter
        if search_term:
            filtered_df = filtered_df[filtered_df['name'].str.contains(search_term, case=False, na=False)]
        
        # Apply other filters
        filtered_df = filtered_df[
            (filtered_df['quality_score'] >= quality_range[0]) &
            (filtered_df['quality_score'] <= quality_range[1]) &
            (filtered_df['cost_per_utilizer'] >= cost_range[0]) &
            (filtered_df['cost_per_utilizer'] <= cost_range[1]) &
            (filtered_df['clinical_group'].isin(selected_clinical_groups)) &
            (filtered_df['network_status'].isin(selected_network_statuses))
        ]
        
        if 'quadrant' in df.columns and selected_quadrants:
            filtered_df = filtered_df[filtered_df['quadrant'].isin(selected_quadrants)]
        
        # Provider selection table
        st.markdown("##### Available Providers")
        st.markdown(f"*Showing {len(filtered_df)} providers (filtered from total)*")
        
        if filtered_df.empty:
            st.warning("No providers match the current filters.")
        else:
            # Prepare table data with selection checkboxes
            table_data = []
            
            for idx, provider in filtered_df.iterrows():
                # Handle both provider_id and index-based identification
                if 'provider_id' in provider:
                    provider_identifier = provider['provider_id']
                else:
                    provider_identifier = f"IDX_{idx}"
                
                is_selected = provider_identifier in st.session_state.selected_providers
                
                table_data.append({
                    'Select': is_selected,
                    'Provider Name': provider['name'],
                    'Quality Score': f"{provider['quality_score']:.1f}",
                    'Cost per Utilizer': f"${provider['cost_per_utilizer']:.0f}",
                    'Network Status': provider['network_status'],
                    'Clinical Group': provider['clinical_group'],
                    'Market Position': f"{provider.get('market_position_percentile', 0):.0f}th" if 'market_position_percentile' in provider else "N/A",
                    'Adequacy Risk': provider.get('adequacy_risk', 'Unknown'),
                    'Savings Potential': f"${provider.get('termination_value', 0):,.0f}",
                    'provider_identifier': provider_identifier  # Hidden column for processing
                })
            
            # Convert to DataFrame
            display_df = pd.DataFrame(table_data)
            
            # Create the editable dataframe
            edited_df = st.data_editor(
                display_df.drop('provider_identifier', axis=1),  # Hide identifier from display
                column_config={
                    "Select": st.column_config.CheckboxColumn(
                        "Select",
                        help="Select providers for your network",
                        default=False,
                        width="small"
                    ),
                    "Provider Name": st.column_config.TextColumn("Provider Name", width="medium"),
                    "Quality Score": st.column_config.TextColumn("Quality Score", width="small"),
                    "Cost per Utilizer": st.column_config.TextColumn("Cost per Utilizer", width="small"),
                    "Network Status": st.column_config.TextColumn("Network Status", width="small"),
                    "Clinical Group": st.column_config.TextColumn("Clinical Group", width="medium"),
                    "Market Position": st.column_config.TextColumn("Market Position", width="small"),
                    "Adequacy Risk": st.column_config.SelectboxColumn("Adequacy Risk", options=["Low", "Medium", "High", "Unknown"], width="small"),
                    "Savings Potential": st.column_config.TextColumn("Savings Potential", width="small")
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )
            
            # Update selected providers based on checkbox changes
            newly_selected = []
            for idx, row in edited_df.iterrows():
                provider_identifier = display_df.iloc[idx]['provider_identifier']
                if row['Select']:
                    newly_selected.append(provider_identifier)
            
            # Update session state
            st.session_state.selected_providers = newly_selected
            
            # Display selection summary
            st.info(f"Selected {len(newly_selected)} providers for your network")
    
    with right_col:
        st.markdown("### Network Analysis")
        
        # Only run analysis if providers are selected
        if st.session_state.selected_providers:
            
            # Simple network analysis without external tools
            with st.spinner("Analyzing network scenario..."):
                try:
                    # Get current and proposed networks
                    current_network = df[df['network_status'] == 'In-Network'] if 'network_status' in df.columns else df.head(0)
                    
                    # Handle both provider_id and index-based selection
                    if 'provider_id' in df.columns:
                        proposed_network = df[df['provider_id'].isin(st.session_state.selected_providers)]
                    else:
                        # Extract indices from identifier strings
                        selected_indices = []
                        for identifier in st.session_state.selected_providers:
                            if identifier.startswith('IDX_'):
                                try:
                                    idx = int(identifier.replace('IDX_', ''))
                                    selected_indices.append(idx)
                                except:
                                    pass
                        proposed_network = df.loc[selected_indices] if selected_indices else df.head(0)
                    
                    # Calculate basic metrics
                    def get_network_metrics(network_df):
                        if network_df.empty:
                            return {
                                "provider_count": 0,
                                "avg_quality": 0,
                                "avg_cost": 0,
                                "total_utilizers": 0,
                                "clinical_groups": 0,
                                "states_covered": 0
                            }
                        
                        return {
                            "provider_count": len(network_df),
                            "avg_quality": network_df['quality_score'].mean(),
                            "avg_cost": network_df['cost_per_utilizer'].mean(),
                            "total_utilizers": network_df['utilizers'].sum() if 'utilizers' in network_df.columns else 0,
                            "clinical_groups": network_df['clinical_group'].nunique(),
                            "states_covered": len(set([state for states in network_df['operating_states'] for state in states])) if 'operating_states' in network_df.columns else 0
                        }
                    
                    current_metrics = get_network_metrics(current_network)
                    proposed_metrics = get_network_metrics(proposed_network)
                    
                    # Network comparison metrics
                    st.markdown("#### Network Comparison")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("##### Current Network")
                        st.metric("Providers", current_metrics['provider_count'])
                        st.metric("Avg Quality", f"{current_metrics['avg_quality']:.1f}")
                        st.metric("Avg Cost", f"${current_metrics['avg_cost']:.0f}")
                        st.metric("Clinical Groups", current_metrics['clinical_groups'])
                    
                    with col2:
                        st.markdown("##### Proposed Network")
                        st.metric("Providers", proposed_metrics['provider_count'])
                        st.metric("Avg Quality", f"{proposed_metrics['avg_quality']:.1f}")
                        st.metric("Avg Cost", f"${proposed_metrics['avg_cost']:.0f}")
                        st.metric("Clinical Groups", proposed_metrics['clinical_groups'])
                    
                    with col3:
                        st.markdown("##### Impact Analysis")
                        
                        # Quality change
                        quality_delta = proposed_metrics['avg_quality'] - current_metrics['avg_quality']
                        st.metric("Quality Change", f"{quality_delta:+.2f}", delta=f"{quality_delta:.2f}")
                        
                        # Cost change
                        cost_delta = proposed_metrics['avg_cost'] - current_metrics['avg_cost']
                        st.metric("Cost Change", f"${cost_delta:+.0f}", delta=f"${cost_delta:.0f}", delta_color="inverse")
                        
                        # Provider change
                        provider_delta = proposed_metrics['provider_count'] - current_metrics['provider_count']
                        st.metric("Provider Change", f"{provider_delta:+d}", delta=f"{provider_delta}")
                    
                    st.markdown("---")
                    
                    # Simple adequacy assessment
                    st.markdown("#### Network Adequacy Assessment")
                    
                    # Calculate adequacy score
                    adequacy_score = 0
                    adequacy_issues = []
                    
                    if proposed_metrics['provider_count'] < 5:
                        adequacy_issues.append("Insufficient providers (minimum: 5)")
                    else:
                        adequacy_score += 30
                    
                    if proposed_metrics['clinical_groups'] < 3:
                        adequacy_issues.append("Limited clinical group coverage")
                    else:
                        adequacy_score += 35
                    
                    if proposed_metrics['avg_quality'] < 3.5:
                        adequacy_issues.append("Below-average network quality")
                    else:
                        adequacy_score += 35
                    
                    # Determine adequacy level
                    if adequacy_score >= 80:
                        adequacy_level = "Safe"
                        adequacy_color = "success"
                    elif adequacy_score >= 60:
                        adequacy_level = "Warning"
                        adequacy_color = "warning"
                    else:
                        adequacy_level = "Critical"
                        adequacy_color = "error"
                    
                    # Display adequacy warning
                    if adequacy_color == "error":
                        st.error(f"🔴 **{adequacy_level}** Network Adequacy Risk (Score: {adequacy_score}/100)")
                    elif adequacy_color == "warning":
                        st.warning(f"🟡 **{adequacy_level}** Network Adequacy Risk (Score: {adequacy_score}/100)")
                    else:
                        st.success(f"🟢 **{adequacy_level}** Network Adequacy (Score: {adequacy_score}/100)")
                    
                    if adequacy_issues:
                        st.markdown("**Issues to Address:**")
                        for issue in adequacy_issues:
                            st.markdown(f"- {issue}")
                    
                    st.markdown("---")
                    
                    # Basic financial impact
                    st.markdown("#### Financial Impact Analysis")
                    
                    if 'termination_value' in df.columns:
                        # Calculate financial impact
                        current_total_value = current_network['termination_value'].sum() if not current_network.empty else 0
                        proposed_total_value = proposed_network['termination_value'].sum() if not proposed_network.empty else 0
                        
                        financial_impact = proposed_total_value - current_total_value
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Current Network Value", f"${current_total_value/1000000:.1f}M")
                        
                        with col2:
                            st.metric("Proposed Network Value", f"${proposed_total_value/1000000:.1f}M")
                        
                        with col3:
                            st.metric("Financial Impact", f"${financial_impact/1000000:.1f}M", 
                                     delta=f"${financial_impact/1000000:.1f}M")
                    
                    st.markdown("---")
                    
                    # Strategic recommendations
                    st.markdown("#### Strategic Recommendations")
                    
                    recommendations = []
                    
                    if quality_delta > 0.2:
                        recommendations.append("✅ Excellent quality improvement")
                    elif quality_delta < -0.2:
                        recommendations.append("⚠️ Quality decrease detected")
                    
                    if cost_delta < -50:
                        recommendations.append("✅ Significant cost savings achieved")
                    elif cost_delta > 50:
                        recommendations.append("⚠️ Cost increase noted")
                    
                    if adequacy_level == 'Critical':
                        recommendations.append("🚨 Critical: Address network adequacy issues before implementation")
                    elif adequacy_level == 'Warning':
                        recommendations.append("⚠️ Warning: Monitor network adequacy during implementation")
                    else:
                        recommendations.append("✅ Network adequacy maintained")
                    
                    if provider_delta < -10:
                        recommendations.append("📋 Significant network reduction - ensure adequate coverage")
                    elif provider_delta > 10:
                        recommendations.append("📋 Network expansion - monitor integration costs")
                    
                    for rec in recommendations:
                        st.markdown(rec)
                        
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")
        else:
            st.info("Please select providers to analyze your custom network scenario.")
    
    st.markdown("---")
    
    # Export functionality
    if st.session_state.selected_providers:
        st.markdown("### Export & Save")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export Provider List", use_container_width=True):
                if 'provider_id' in df.columns:
                    selected_provider_data = df[df['provider_id'].isin(st.session_state.selected_providers)]
                else:
                    # Handle index-based selection
                    selected_indices = []
                    for identifier in st.session_state.selected_providers:
                        if identifier.startswith('IDX_'):
                            try:
                                idx = int(identifier.replace('IDX_', ''))
                                selected_indices.append(idx)
                            except:
                                pass
                    selected_provider_data = df.loc[selected_indices] if selected_indices else df.head(0)
                
                if not selected_provider_data.empty:
                    # Prepare download data
                    download_columns = ['name', 'quality_score', 'cost_per_utilizer', 'network_status', 'clinical_group']
                    available_columns = [col for col in download_columns if col in selected_provider_data.columns]
                    download_data = selected_provider_data[available_columns].copy()
                    
                    csv_data = download_data.to_csv(index=False)
                    
                    st.download_button(
                        label="Download Selected Providers (CSV)",
                        data=csv_data,
                        file_name=f"custom_network_scenario_{len(st.session_state.selected_providers)}_providers.csv",
                        mime="text/csv",
                        help="Download the list of selected providers for your custom network"
                    )
                else:
                    st.warning("No valid providers selected for export.")
        
        with col2:
            if st.button("Save Scenario", use_container_width=True):
                scenario_name = f"Custom Network {len(st.session_state.saved_scenarios) + 1}"
                
                st.session_state.saved_scenarios.append({
                    'name': scenario_name,
                    'selected_providers': st.session_state.selected_providers.copy(),
                    'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
                })
                st.success(f"Scenario saved as '{scenario_name}'!")
        
        with col3:
            if st.session_state.saved_scenarios:
                selected_scenario = st.selectbox(
                    "Load Saved Scenario",
                    options=[scenario['name'] for scenario in st.session_state.saved_scenarios],
                    key="scenario_selector"
                )
                
                if st.button("Load Scenario", use_container_width=True):
                    for scenario in st.session_state.saved_scenarios:
                        if scenario['name'] == selected_scenario:
                            st.session_state.selected_providers = scenario['selected_providers'].copy()
                            st.success(f"Loaded scenario: {selected_scenario}")
                            st.rerun()
    
    # Help section
    with st.expander("Network Builder Help & Tips"):
        st.markdown("""
        ### How to Use the Network Builder
        
        1. **Select Providers**: Use the left panel to search, filter, and select providers for your custom network
        2. **Quick Actions**: Use the quick selection buttons to rapidly select groups of providers
        3. **Real-time Analysis**: The right panel updates automatically as you make selections
        4. **Network Adequacy**: Pay attention to adequacy warnings to ensure regulatory compliance
        5. **Financial Impact**: Review the financial analysis to understand the business case
        6. **Export Results**: Save your scenario and download provider lists for implementation
        
        ### Selection Tips
        - Start with current in-network providers and make adjustments
        - Use quality and cost filters to identify optimal providers
        - Monitor network adequacy scores to avoid coverage gaps
        - Consider clinical group coverage across all geographic areas
        
        ### Adequacy Guidelines
        - **Safe (80-100)**: Network meets all adequacy requirements
        - **Warning (60-79)**: Some adequacy concerns, monitor closely
        - **Critical (<60)**: Significant adequacy issues, address before implementation
        """)

def render_network_builder_tab(df, results):
    """Render the Network Builder tab - custom network scenario analysis"""
    
    st.markdown("### Network Builder - Custom Scenario Analysis")
    st.markdown("*Build and analyze custom provider network scenarios with real-time feedback*")
    
    # Import network builder components
    from ui.network_builder_components import (
        create_provider_selection_interface,
        create_provider_selection_table,
        create_network_comparison_metrics,
        create_adequacy_risk_warning,
        create_financial_impact_summary,
        create_scenario_recommendations,
        create_network_builder_summary,
        create_scenario_export_options
    )
    
    
    # Initialize session state for network builder
    if 'selected_providers' not in st.session_state:
        st.session_state.selected_providers = []
    
    # Initialize with current network if no selections
    if not st.session_state.selected_providers and 'network_status' in df.columns:
        current_network_ids = df[df['network_status'] == 'In-Network']['provider_id'].tolist()
        st.session_state.selected_providers = current_network_ids
    
    # Network builder status summary
    selected_count = len(st.session_state.selected_providers)
    total_available = len(df)
    create_network_builder_summary(selected_count, total_available)
    
    st.markdown("---")
    
    # Main network builder interface - 2 column layout
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        st.markdown("### Provider Selection")
        
        # Provider selection interface with filters
        filtered_df = create_provider_selection_interface(df, st.session_state.selected_providers)
        
        # Provider selection table
        create_provider_selection_table(filtered_df, st.session_state.selected_providers)
    
    with right_col:
        st.markdown("### Network Analysis")
        
        # Only run analysis if providers are selected
        if st.session_state.selected_providers:
            
            # Initialize network builder tool
            network_tool = NetworkBuilderTool()
            
            # Run network analysis
            with st.spinner("Analyzing network scenario..."):
                try:
                    # Convert DataFrame to records for tool
                    provider_data = df.to_dict('records')
                    
                    # Run analysis
                    scenario_results = network_tool._run(
                        all_providers=provider_data,
                        selected_provider_ids=st.session_state.selected_providers,
                        scenario_name="Custom Network Scenario"
                    )
                    
                    if scenario_results['success']:
                        # Network comparison metrics
                        create_network_comparison_metrics(
                            scenario_results['current_network_metrics'],
                            scenario_results['proposed_network_metrics'],
                            scenario_results['scenario_metrics']
                        )
                        
                        st.markdown("---")
                        
                        # Network adequacy warning
                        create_adequacy_risk_warning(scenario_results['adequacy_assessment'])
                        
                        st.markdown("---")
                        
                        # Financial impact summary
                        create_financial_impact_summary(scenario_results['financial_impact'])
                        
                        st.markdown("---")
                        
                        # Scenario recommendations
                        create_scenario_recommendations(scenario_results['recommendations'])
                        
                    else:
                        st.error("Error analyzing network scenario. Please try again.")
                        
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")
                    scenario_results = None
        else:
            st.info("Please select providers to analyze your custom network scenario.")
            scenario_results = None
    
    st.markdown("---")
    
    # Bottom section - Detailed analysis and export
    if scenario_results and scenario_results['success']:
        
        # Detailed analysis tabs
        detail_tab1, detail_tab2, detail_tab3 = st.tabs([
            "Provider Changes",
            "Detailed Analysis", 
            "Export & Save"
        ])
        
        with detail_tab1:
            st.markdown("#### Provider Network Changes")
            
            provider_changes = scenario_results['provider_changes']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("##### Providers Added")
                if provider_changes['additions']:
                    added_providers = df[df['provider_id'].isin(provider_changes['additions'])]
                    for _, provider in added_providers.iterrows():
                        st.markdown(f"+ **{provider['name']}** ({provider['clinical_group']})")
                else:
                    st.info("No providers added")
            
            with col2:
                st.markdown("##### Providers Removed")
                if provider_changes['removals']:
                    removed_providers = df[df['provider_id'].isin(provider_changes['removals'])]
                    for _, provider in removed_providers.iterrows():
                        st.markdown(f"- **{provider['name']}** ({provider['clinical_group']})")
                else:
                    st.info("No providers removed")
            
            with col3:
                st.markdown("##### Change Summary")
                st.metric("Providers Added", provider_changes['additions_count'])
                st.metric("Providers Removed", provider_changes['removals_count'])
                st.metric("Providers Retained", provider_changes['retained_count'])
                
                net_change = provider_changes['additions_count'] - provider_changes['removals_count']
                st.metric("Net Change", f"{net_change:+d}")
        
        with detail_tab2:
            st.markdown("#### Detailed Scenario Analysis")
            
            # Performance scores breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Performance Scores")
                scenario_metrics = scenario_results['scenario_metrics']
                
                st.metric("Quality Improvement Score", f"{scenario_metrics['quality_improvement_score']:.0f}/100")
                st.metric("Cost Efficiency Score", f"{scenario_metrics['cost_efficiency_score']:.0f}/100")
                st.metric("Overall Performance Score", f"{scenario_metrics['network_performance_score']:.0f}/100")
                
                st.markdown("##### Network Adequacy Breakdown")
                adequacy = scenario_results['adequacy_assessment']
                st.metric("Clinical Coverage", f"{adequacy['clinical_coverage']['coverage_score']:.0f}%")
                st.metric("Geographic Coverage", f"{adequacy['geographic_coverage']['coverage_score']:.0f}%")
                st.metric("Risk Assessment", f"{adequacy['high_risk_assessment']['risk_score']:.0f}/100")
            
            with col2:
                st.markdown("##### Financial Breakdown")
                financial = scenario_results['financial_impact']
                
                # Create financial summary table
                financial_summary = pd.DataFrame([
                    {"Category": "Removal Savings", "Amount": f"${financial['removal_savings']:,.0f}"},
                    {"Category": "Addition Costs", "Amount": f"${financial['addition_costs']:,.0f}"},
                    {"Category": "Net Savings", "Amount": f"${financial['net_savings']:,.0f}"},
                    {"Category": "Quality Value", "Amount": f"${financial['quality_value']:,.0f}"},
                    {"Category": "Total Value", "Amount": f"${financial['total_value']:,.0f}"}
                ])
                
                st.dataframe(financial_summary, use_container_width=True, hide_index=True)
                
                # ROI analysis
                st.markdown("##### ROI Analysis")
                if financial['addition_costs'] > 0:
                    payback_months = (financial['addition_costs'] / max(financial['net_savings'], 1)) * 12
                    st.metric("Payback Period", f"{payback_months:.1f} months")
                
                st.metric("ROI Percentage", f"{financial['roi_percentage']:.0f}%")
        
        with detail_tab3:
            st.markdown("#### Export & Save Options")
            
            # Export scenario results
            create_scenario_export_options(scenario_results)
            
            # Download selected providers as CSV
            if st.session_state.selected_providers:
                selected_provider_data = df[df['provider_id'].isin(st.session_state.selected_providers)]
                
                # Prepare download data
                download_data = selected_provider_data[[
                    'name', 'quality_score', 'cost_per_utilizer', 'network_status',
                    'clinical_group', 'primary_cbsa', 'adequacy_risk', 'termination_value'
                ]].copy()
                
                download_data.columns = [
                    'Provider Name', 'Quality Score', 'Cost per Utilizer', 'Network Status',
                    'Clinical Group', 'Primary CBSA', 'Adequacy Risk', 'Savings Potential'
                ]
                
                csv_data = download_data.to_csv(index=False)
                
                st.download_button(
                    label="Download Selected Providers (CSV)",
                    data=csv_data,
                    file_name=f"custom_network_scenario_{len(st.session_state.selected_providers)}_providers.csv",
                    mime="text/csv",
                    help="Download the list of selected providers for your custom network"
                )
            
            # Scenario summary for export
            if scenario_results:
                scenario_summary = f"""
# Network Builder Scenario Analysis Report

## Scenario Overview
- **Scenario Name**: {scenario_results['scenario_name']}
- **Total Providers Selected**: {len(st.session_state.selected_providers)}
- **Analysis Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

## Key Metrics
- **Quality Change**: {scenario_results['scenario_metrics']['quality_change']:+.2f} points
- **Cost Change**: ${scenario_results['scenario_metrics']['cost_change']:+.0f} per utilizer
- **Provider Change**: {scenario_results['scenario_metrics']['provider_change']:+d} providers
- **Net Financial Impact**: ${scenario_results['financial_impact']['total_value']:,.0f}

## Network Adequacy
- **Adequacy Level**: {scenario_results['adequacy_assessment']['adequacy_level']}
- **Adequacy Score**: {scenario_results['adequacy_assessment']['adequacy_score']}/100
- **Clinical Coverage**: {scenario_results['adequacy_assessment']['clinical_coverage']['coverage_score']:.0f}%
- **Geographic Coverage**: {scenario_results['adequacy_assessment']['geographic_coverage']['coverage_score']:.0f}%

## Recommendations
{chr(10).join(f"- {rec}" for rec in scenario_results['recommendations'])}

## Provider Changes
- **Added**: {scenario_results['provider_changes']['additions_count']} providers
- **Removed**: {scenario_results['provider_changes']['removals_count']} providers
- **Retained**: {scenario_results['provider_changes']['retained_count']} providers
"""
                
                st.download_button(
                    label="Download Scenario Report (TXT)",
                    data=scenario_summary,
                    file_name=f"network_scenario_analysis_report.txt",
                    mime="text/plain",
                    help="Download a comprehensive analysis report for this scenario"
                )
    
    # Help section
    with st.expander("Network Builder Help & Tips"):
        st.markdown("""
        ### How to Use the Network Builder
        
        1. **Select Providers**: Use the left panel to search, filter, and select providers for your custom network
        2. **Quick Actions**: Use the quick selection buttons to rapidly select groups of providers
        3. **Real-time Analysis**: The right panel updates automatically as you make selections
        4. **Network Adequacy**: Pay attention to adequacy warnings to ensure regulatory compliance
        5. **Financial Impact**: Review the financial analysis to understand the business case
        6. **Export Results**: Save your scenario and download provider lists for implementation
        
        ### Selection Tips
        - Start with current in-network providers and make adjustments
        - Use quality and cost filters to identify optimal providers
        - Monitor network adequacy scores to avoid coverage gaps
        - Consider clinical group coverage across all geographic areas
        
        ### Adequacy Guidelines
        - **Safe (80-100)**: Network meets all adequacy requirements
        - **Warning (60-79)**: Some adequacy concerns, monitor closely
        - **Critical (<60)**: Significant adequacy issues, address before implementation
        """)

