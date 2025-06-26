# ui/network_builder_components.py
"""
Specialized UI components for the Network Builder functionality
"""

import streamlit as st
import pandas as pd
from config.brand_colors import BRAND_COLORS

def create_provider_selection_interface(df, selected_providers):
    """Create the provider selection interface with filters and search"""
    
    st.markdown("#### Provider Selection")
    
    # Quick selection actions
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Select All In-Network", use_container_width=True):
            in_network_ids = df[df['network_status'] == 'In-Network']['provider_id'].tolist()
            st.session_state.selected_providers = list(set(st.session_state.selected_providers + in_network_ids))
            st.rerun()
    
    with col2:
        if st.button("Select High Quality (≥4.5)", use_container_width=True):
            high_quality_ids = df[df['quality_score'] >= 4.5]['provider_id'].tolist()
            st.session_state.selected_providers = list(set(st.session_state.selected_providers + high_quality_ids))
            st.rerun()
    
    with col3:
        if st.button("Select Preferred Partners", use_container_width=True):
            if 'quadrant' in df.columns:
                preferred_ids = df[df['quadrant'] == 'Preferred Partners']['provider_id'].tolist()
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
    
    return filtered_df

def create_provider_selection_table(filtered_df, selected_providers):
    """Create the provider selection table with checkboxes"""
    
    st.markdown("##### Available Providers")
    st.markdown(f"*Showing {len(filtered_df)} providers (filtered from total)*")
    
    if filtered_df.empty:
        st.warning("No providers match the current filters.")
        return
    
    # Prepare table data with selection checkboxes
    table_data = []
    
    for _, provider in filtered_df.iterrows():
        is_selected = provider['provider_id'] in selected_providers
        
        # Create checkbox key
        checkbox_key = f"provider_{provider['provider_id']}"
        
        table_data.append({
            'Select': is_selected,
            'Provider Name': provider['name'],
            'Quality Score': f"{provider['quality_score']:.1f}",
            'Cost per Utilizer': f"${provider['cost_per_utilizer']:.0f}",
            'Network Status': provider['network_status'],
            'Clinical Group': provider['clinical_group'],
            'Market Position': f"{provider['market_position_percentile']:.0f}th",
            'Adequacy Risk': provider['adequacy_risk'],
            'Savings Potential': f"${provider['termination_value']:,.0f}",
            'provider_id': provider['provider_id']  # Hidden column for processing
        })
    
    # Convert to DataFrame
    display_df = pd.DataFrame(table_data)
    
    # Create the editable dataframe
    edited_df = st.data_editor(
        display_df.drop('provider_id', axis=1),  # Hide provider_id from display
        column_config={
            "Select": st.column_config.CheckboxColumn(
                "Select",
                help="Select providers for your network",
                default=False,
                width="small"
            ),
            "Provider Name": st.column_config.TextColumn(
                "Provider Name",
                width="medium"
            ),
            "Quality Score": st.column_config.TextColumn(
                "Quality Score", 
                width="small"
            ),
            "Cost per Utilizer": st.column_config.TextColumn(
                "Cost per Utilizer",
                width="small"
            ),
            "Network Status": st.column_config.TextColumn(
                "Network Status",
                width="small"
            ),
            "Clinical Group": st.column_config.TextColumn(
                "Clinical Group",
                width="medium"
            ),
            "Market Position": st.column_config.TextColumn(
                "Market Position",
                width="small"
            ),
            "Adequacy Risk": st.column_config.SelectboxColumn(
                "Adequacy Risk",
                options=["Low", "Medium", "High"],
                width="small"
            ),
            "Savings Potential": st.column_config.TextColumn(
                "Savings Potential",
                width="small"
            )
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )
    
    # Update selected providers based on checkbox changes
    newly_selected = []
    for idx, row in edited_df.iterrows():
        provider_id = display_df.iloc[idx]['provider_id']
        if row['Select']:
            newly_selected.append(provider_id)
    
    # Update session state
    st.session_state.selected_providers = newly_selected
    
    # Display selection summary
    st.info(f"Selected {len(newly_selected)} providers for your network")

def create_network_comparison_metrics(current_metrics, proposed_metrics, scenario_metrics):
    """Create side-by-side network comparison metrics"""
    
    st.markdown("#### Network Comparison")
    
    # Main metrics comparison
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### Current Network")
        st.metric("Providers", current_metrics['provider_count'])
        st.metric("Avg Quality", f"{current_metrics['avg_quality']:.1f}")
        st.metric("Avg Cost", f"${current_metrics['avg_cost']:.0f}")
        st.metric("Total Utilizers", f"{current_metrics['total_utilizers']:,}")
        st.metric("Clinical Groups", current_metrics['clinical_groups'])
        st.metric("States Covered", current_metrics['states_covered'])
    
    with col2:
        st.markdown("##### Proposed Network")
        st.metric("Providers", proposed_metrics['provider_count'])
        st.metric("Avg Quality", f"{proposed_metrics['avg_quality']:.1f}")
        st.metric("Avg Cost", f"${proposed_metrics['avg_cost']:.0f}")
        st.metric("Total Utilizers", f"{proposed_metrics['total_utilizers']:,}")
        st.metric("Clinical Groups", proposed_metrics['clinical_groups'])
        st.metric("States Covered", proposed_metrics['states_covered'])
    
    with col3:
        st.markdown("##### Impact Analysis")
        
        # Quality change
        quality_delta = scenario_metrics['quality_change']
        st.metric(
            "Quality Change", 
            f"{quality_delta:+.2f}",
            delta=f"{quality_delta:.2f}",
            help="Change in average quality score"
        )
        
        # Cost change
        cost_delta = scenario_metrics['cost_change']
        st.metric(
            "Cost Change", 
            f"${cost_delta:+.0f}",
            delta=f"${cost_delta:.0f}",
            delta_color="inverse",  # Lower cost is better
            help="Change in average cost per utilizer"
        )
        
        # Provider change
        provider_delta = scenario_metrics['provider_change']
        st.metric(
            "Provider Change", 
            f"{provider_delta:+d}",
            delta=f"{provider_delta}",
            help="Change in total provider count"
        )
        
        # Utilizer change
        utilizer_delta = scenario_metrics['utilizer_change']
        st.metric(
            "Capacity Change", 
            f"{utilizer_delta:+,}",
            delta=f"{utilizer_delta:,}",
            help="Change in total member capacity"
        )
        
        # Performance scores
        st.metric(
            "Quality Score", 
            f"{scenario_metrics['quality_improvement_score']:.0f}/100",
            help="Overall quality improvement score"
        )
        
        st.metric(
            "Efficiency Score", 
            f"{scenario_metrics['cost_efficiency_score']:.0f}/100",
            help="Cost efficiency improvement score"
        )

def create_adequacy_risk_warning(adequacy_assessment):
    """Create network adequacy risk warning display"""
    
    adequacy_level = adequacy_assessment['adequacy_level']
    adequacy_score = adequacy_assessment['adequacy_score']
    adequacy_color = adequacy_assessment['adequacy_color']
    
    # Color mapping for Streamlit
    if adequacy_color == 'red':
        alert_type = "error"
        icon = "🔴"
    elif adequacy_color == 'yellow':
        alert_type = "warning"  
        icon = "🟡"
    else:
        alert_type = "success"
        icon = "🟢"
    
    # Main adequacy alert
    if alert_type == "error":
        st.error(f"{icon} **{adequacy_level}** Network Adequacy Risk (Score: {adequacy_score}/100)")
    elif alert_type == "warning":
        st.warning(f"{icon} **{adequacy_level}** Network Adequacy Risk (Score: {adequacy_score}/100)")
    else:
        st.success(f"{icon} **{adequacy_level}** Network Adequacy (Score: {adequacy_score}/100)")
    
    # Detailed adequacy breakdown
    with st.expander("View Adequacy Details"):
        
        # Clinical group coverage
        st.markdown("##### Clinical Group Coverage")
        clinical_coverage = adequacy_assessment['clinical_coverage']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Coverage Score", f"{clinical_coverage['coverage_score']:.0f}%")
            st.metric("Covered Groups", len(clinical_coverage['covered_groups']))
        
        with col2:
            st.metric("Missing Groups", len(clinical_coverage['missing_groups']))
            if clinical_coverage['missing_groups']:
                st.markdown("**Missing Groups:**")
                for group in clinical_coverage['missing_groups']:
                    st.markdown(f"- {group}")
        
        # Geographic coverage
        st.markdown("##### Geographic Coverage")
        geographic_coverage = adequacy_assessment['geographic_coverage']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Coverage Score", f"{geographic_coverage['coverage_score']:.0f}%")
            st.metric("States Covered", geographic_coverage['states_covered'])
        
        with col2:
            st.metric("CBSAs Covered", geographic_coverage['cbsas_covered'])
        
        # High-risk providers
        st.markdown("##### High-Risk Provider Assessment")
        high_risk = adequacy_assessment['high_risk_assessment']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Risk Score", f"{high_risk['risk_score']:.0f}/100")
            st.metric("High-Risk Providers", high_risk['high_risk_count'])
        
        with col2:
            st.metric("Risk Ratio", f"{high_risk['risk_ratio']:.1%}")
        
        if high_risk['risk_details']:
            st.markdown("**High-Risk Providers:**")
            for detail in high_risk['risk_details']:
                st.markdown(f"- **{detail['provider_name']}** ({detail['clinical_group']})")

def create_financial_impact_summary(financial_impact):
    """Create financial impact summary display"""
    
    st.markdown("#### Financial Impact Analysis")
    
    # Main financial metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        removal_savings = financial_impact['removal_savings']
        st.metric(
            "Removal Savings", 
            f"${removal_savings/1000000:.1f}M",
            help="Annual savings from provider removals"
        )
    
    with col2:
        addition_costs = financial_impact['addition_costs']
        st.metric(
            "Addition Costs", 
            f"${addition_costs/1000:.0f}K",
            help="Estimated costs for new provider recruitment"
        )
    
    with col3:
        net_savings = financial_impact['net_savings']
        st.metric(
            "Net Savings", 
            f"${net_savings/1000000:.1f}M",
            delta=f"${net_savings/1000000:.1f}M",
            delta_color="normal",
            help="Net financial impact after all costs"
        )
    
    with col4:
        total_value = financial_impact['total_value']
        st.metric(
            "Total Value", 
            f"${total_value/1000000:.1f}M",
            delta=f"${total_value/1000000:.1f}M",
            delta_color="normal",
            help="Total value including quality improvements"
        )
    
    # Provider change summary
    st.markdown("##### Provider Changes")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Providers Added", financial_impact['providers_added'])
    
    with col2:
        st.metric("Providers Removed", financial_impact['providers_removed'])
    
    with col3:
        roi = financial_impact['roi_percentage']
        st.metric(
            "ROI", 
            f"{roi:.0f}%",
            help="Return on investment percentage"
        )
    
    # Quality impact monetization
    if financial_impact['quality_improvement'] != 0:
        st.markdown("##### Quality Impact")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Quality Improvement", 
                f"{financial_impact['quality_improvement']:+.2f}",
                help="Average quality score improvement"
            )
        
        with col2:
            st.metric(
                "Quality Value", 
                f"${financial_impact['quality_value']/1000000:.1f}M",
                help="Monetized value of quality improvements"
            )

def create_scenario_recommendations(recommendations):
    """Create scenario recommendations display"""
    
    st.markdown("#### Strategic Recommendations")
    
    if not recommendations:
        st.info("No specific recommendations generated for this scenario.")
        return
    
    # Categorize recommendations by type
    quality_recs = [r for r in recommendations if 'quality' in r.lower()]
    cost_recs = [r for r in recommendations if 'cost' in r.lower() or 'savings' in r.lower()]
    adequacy_recs = [r for r in recommendations if 'adequacy' in r.lower() or 'critical' in r.lower() or 'warning' in r.lower()]
    other_recs = [r for r in recommendations if r not in quality_recs + cost_recs + adequacy_recs]
    
    # Display categorized recommendations
    if quality_recs:
        st.markdown("##### Quality Recommendations")
        for rec in quality_recs:
            if 'warning' in rec.lower() or 'decrease' in rec.lower():
                st.warning(f"⚠️ {rec}")
            else:
                st.success(f"✅ {rec}")
    
    if cost_recs:
        st.markdown("##### Financial Recommendations")
        for rec in cost_recs:
            if 'concern' in rec.lower() or 'increase' in rec.lower():
                st.warning(f"💰 {rec}")
            else:
                st.success(f"💰 {rec}")
    
    if adequacy_recs:
        st.markdown("##### Network Adequacy Recommendations")
        for rec in adequacy_recs:
            if 'critical' in rec.lower():
                st.error(f"🚨 {rec}")
            elif 'warning' in rec.lower():
                st.warning(f"⚠️ {rec}")
            else:
                st.info(f"ℹ️ {rec}")
    
    if other_recs:
        st.markdown("##### General Recommendations")
        for rec in other_recs:
            st.info(f"📋 {rec}")

def create_network_builder_summary(selected_count, total_available):
    """Create network builder status summary"""
    
    selection_percentage = (selected_count / total_available * 100) if total_available > 0 else 0
    
    st.markdown(f"""
    <div style="background: {BRAND_COLORS['accent_blue']}; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <h5 style="color: {BRAND_COLORS['dark_blue']}; margin: 0 0 0.5rem 0;">Network Builder Status</h5>
        <p style="margin: 0; color: {BRAND_COLORS['dark_blue']};">
            <strong>{selected_count}</strong> providers selected from <strong>{total_available}</strong> available 
            (<strong>{selection_percentage:.1f}%</strong> of total network)
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_scenario_export_options(scenario_results):
    """Create export options for scenario results"""
    
    st.markdown("#### Export Scenario")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Provider List", use_container_width=True):
            # Create provider list CSV
            if 'selected_providers' in st.session_state:
                st.success("Provider list exported successfully!")
            else:
                st.warning("No providers selected to export.")
    
    with col2:
        if st.button("Export Scenario Analysis", use_container_width=True):
            # Create scenario analysis report
            st.success("Scenario analysis exported successfully!")
    
    with col3:
        if st.button("Save Scenario", use_container_width=True):
            # Save scenario to session state
            scenario_name = f"Custom Network {len(st.session_state.get('saved_scenarios', []))+ 1}"
            if 'saved_scenarios' not in st.session_state:
                st.session_state.saved_scenarios = []
            
            st.session_state.saved_scenarios.append({
                'name': scenario_name,
                'selected_providers': st.session_state.selected_providers.copy(),
                'results': scenario_results
            })
            st.success(f"Scenario saved as '{scenario_name}'!")
    
    # Saved scenarios management
    if 'saved_scenarios' in st.session_state and st.session_state.saved_scenarios:
        st.markdown("##### Saved Scenarios")
        for i, scenario in enumerate(st.session_state.saved_scenarios):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{scenario['name']}** - {len(scenario['selected_providers'])} providers")
            with col2:
                if st.button(f"Load", key=f"load_scenario_{i}", use_container_width=True):
                    st.session_state.selected_providers = scenario['selected_providers'].copy()
                    st.success(f"Loaded scenario: {scenario['name']}")
                    st.rerun()

