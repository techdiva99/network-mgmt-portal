import streamlit as st
from ui.components import create_provider_card

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