import streamlit as st
from ui.components import create_provider_card

def render_optimization_summary_tab(df, results):
    """Render Network Optimization Summary tab"""
    st.markdown("### Network Optimization Summary")
    st.markdown("**AI-driven clinical and financial analysis for network optimization**")

    # Get recommendations from quadrant analysis (if available)
    removal_candidates = []
    addition_candidates = []
    if 'quadrant_analysis' in results and 'removal_candidates' in results['quadrant_analysis']:
        removal_candidates = results['quadrant_analysis']['removal_candidates']
        addition_candidates = results['quadrant_analysis']['addition_candidates']

    # Calculate overall impact ONCE at the top
    total_current_providers = len(df[df['network_status'] == 'In-Network'])
    total_removal_candidates = len(removal_candidates)
    total_addition_candidates = len(addition_candidates)
    net_change = total_addition_candidates - total_removal_candidates

    # Executive Summary Section (move to top, use calculated values)
    st.markdown("### Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Network Size", f"{total_current_providers}", help="Total in-network providers in current analysis")
    with col2:
        st.metric("Recommended Removals", f"{total_removal_candidates}", help="Providers recommended for contract termination")
    with col3:
        st.metric("Recommended Additions", f"{total_addition_candidates}", help="Out-of-network providers recommended for recruitment")
    with col4:
        st.metric("Net Network Change", f"{net_change:+d}", help="Overall change in provider count")

    

    st.markdown("---")

    # Clinical and Business Impact Summary
    # st.markdown("#### Key Performance Indicators")
    # if 'quadrant_analysis' in results and 'financial_impact' in results['quadrant_analysis']:
    #     financial_impact = results['quadrant_analysis']['financial_impact']
    #     # Prepare KPI values (multi-line, detailed)
    #     kpi_1 = f"""
    #     <b>Financial Impact</b><br>
    #     Projected annual cost savings: <b>${financial_impact['total_removal_savings']/1000000:.1f}M</b> from contract optimizations<br>
    #     Network efficiency improvement through strategic provider mix optimization
    #     """
    #     kpi_2 = f"""
    #     <b>Quality Enhancement</b><br>
    #     Expected network quality score improvement: <b>+{financial_impact['avg_quality_improvement']:.2f} points</b><br>
    #     Enhanced member access to high-performing providers
    #     """
    #     kpi_3 = f"""
    #     <b>Operational Benefits</b><br>
    #     Streamlined provider network reducing administrative complexity<br>
    #     Improved contract negotiation leverage with performance-based partnerships<br>
    #     Enhanced member satisfaction through quality-focused network composition
    #     """
    #     kpi_4 = f"""
    #     <b>Risk Mitigation</b><br>
    #     All removal recommendations maintain adequate network coverage<br>
    #     Strategic additions strengthen market position and member choice<br>
    #     Balanced approach ensuring regulatory compliance and member access standards
    #     """
    #     # Display KPIs in a 2x2 grid
    #     kpi_col1, kpi_col2 = st.columns(2)
    #     with kpi_col1:
    #         st.markdown(f"<div style='background: #E1F5FE; border-left: 4px solid #00B4D8; padding: 1rem; margin: 0.5rem 0; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); min-height: 120px;'>{kpi_1}</div>", unsafe_allow_html=True)
    #         st.markdown(f"<div style='background: #E8F5E8; border-left: 4px solid #7CB342; padding: 1rem; margin: 0.5rem 0; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); min-height: 120px;'>{kpi_3}</div>", unsafe_allow_html=True)
    #     with kpi_col2:
    #         st.markdown(f"<div style='background: #E1F5FE; border-left: 4px solid #00B4D8; padding: 1rem; margin: 0.5rem 0; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); min-height: 120px;'>{kpi_2}</div>", unsafe_allow_html=True)
    #         st.markdown(f"<div style='background: #E8F5E8; border-left: 4px solid #7CB342; padding: 1rem; margin: 0.5rem 0; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); min-height: 120px;'>{kpi_4}</div>", unsafe_allow_html=True)
    # else:
    #     st.info("Detailed financial impact analysis will be available after quadrant analysis completion.")

    # st.markdown("---")
    st.markdown("### Provider Quadrants")
    # Display some basic results in an expandable 2x2 grid
    if 'quadrant_summary' in results.get('quadrant_analysis', {}):
        #st.markdown('#### Provider Quadrants')
        quadrant_colors = {
            'Preferred Partners': '#E8F5E9',
            'Strategic Opportunities': '#FFFDE7',
            'Performance Focus': '#E3F2FD',
            'Optimization Candidates': '#FFEBEE',
        }
        quadrant_descriptions = {
            'Preferred Partners': '⭐️ Best value providers: maintain and prioritize.',
            'Strategic Opportunities': '💰 High performers but expensive: consider for negotiation.',
            'Performance Focus': '⚖️ Low cost but quality concerns: monitor closely.',
            'Optimization Candidates': '⚠️ Underperformers and costly: primary candidates for removal.',
        }
        quadrant_items = list(results['quadrant_analysis']['quadrant_summary'].items())
        grid = st.columns(2)
        for i, (quadrant, count) in enumerate(quadrant_items):
            color = quadrant_colors.get(quadrant, '#E8F5E9')  # fallback to a visible color
            description = quadrant_descriptions.get(quadrant, '')
            with grid[i // 2]:
                st.markdown(f"""
                    <div style='background-color: {color}; padding: 1rem; margin: 0.5rem 0; min-height: 100px; border-left: 5px solid #2196F3;'>
                        <b>{quadrant}</b><br>
                        <span style='font-size:1.3em;'><b>{count}</b> providers</span><br>
                        <span style='font-size:1em;'>{description}</span>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown("---")                        
    # Show recommendations if available
    if removal_candidates or addition_candidates:
        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.markdown("#### Priority Network Removals")
            st.markdown("*Providers recommended for contract termination based on performance and cost analysis:*")
             # Summary for removals
            if removal_candidates:
                total_removal_savings = sum(p['termination_value'] for p in removal_candidates)
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("Total Annual Savings", f"${total_removal_savings/1000000:.1f}M", help="Projected annual financial benefit from contract terminations")
                with col_metric2:
                    avg_quality = sum(p['quality_score'] for p in removal_candidates) / len(removal_candidates)
                    quality_improvement = 4.0 - avg_quality
                    st.metric("Network Quality Impact", f"+{quality_improvement:.2f}", help="Expected improvement in average network quality score")
            for provider in removal_candidates[:5]:
                provider_card_html = create_provider_card(provider, "removal")
                st.markdown(provider_card_html, unsafe_allow_html=True)
           
        with col_right:
            st.markdown("#### Strategic Network Additions")
            st.markdown("*High-performing out-of-network providers recommended for contract negotiation:*")
            # Summary for additions
            if addition_candidates:
                current_in_network = df[df['network_status'] == 'In-Network']
                addition_quality = sum(p['quality_score'] for p in addition_candidates) / len(addition_candidates)
                current_quality = current_in_network['quality_score'].mean() if not current_in_network.empty else 0
                network_quality_improvement = addition_quality - current_quality
                potential_volume = sum(p['utilizers'] for p in addition_candidates)
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("Network Quality Impact", f"+{network_quality_improvement:.2f}", help="Expected quality score improvement from adding high-performing providers")
                with col_metric2:
                    st.metric("Additional Capacity", f"{potential_volume:,}", help="Additional member capacity from new provider partnerships")
            for provider in addition_candidates[:5]:
                provider_card_html = create_provider_card(provider, "addition")
                st.markdown(provider_card_html, unsafe_allow_html=True)
            

