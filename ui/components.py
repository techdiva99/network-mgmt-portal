# ui/components.py
"""
Reusable UI components for the Network Optimization Platform
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from config.brand_colors import BRAND_COLORS
from utils.metrics_calculator import calculate_network_metrics

def display_metrics_row(metrics):
    """Display the 6-column metrics row matching original design"""
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card-compact">
            <h4>Total Providers</h4>
            <h2 style="color: {BRAND_COLORS['primary_blue']};">{metrics['total_providers']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card-compact metric-card-compact-green">
            <h4>In-Network</h4>
            <h2 style="color: {BRAND_COLORS['primary_green']};">{metrics['in_network_providers']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card-compact">
            <h4>Avg Cost/Utilizer</h4>
            <h2 style="color: {BRAND_COLORS['primary_blue']};">${metrics['avg_cost_per_utilizer']:.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card-compact metric-card-compact-green">
            <h4>Network Quality</h4>
            <h2 style="color: {BRAND_COLORS['primary_green']};">{metrics['avg_quality_score']:.1f}/5.0</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card-compact">
            <h4>Network Savings</h4>
            <h2 style="color: {BRAND_COLORS['success']};">${metrics['network_savings']/1000000:.1f}M</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="metric-card-compact">
            <h4>High Risk Removals</h4>
            <h2 style="color: {BRAND_COLORS['error']};">{metrics['high_risk_removals']}</h2>
        </div>
        """, unsafe_allow_html=True)

def display_agent_status(agent_name, status, message=""):
    """Display agent status with brand styling"""
    status_class = {
        "waiting": "agent-status",
        "working": "agent-status agent-working", 
        "complete": "agent-status agent-complete"
    }
    
    status_text = {
        "waiting": "READY",
        "working": "WORKING",
        "complete": "COMPLETE"
    }
    
    st.markdown(f"""
    <div class="{status_class.get(status, 'agent-status')}">
        <strong>[{status_text.get(status, "")}] {agent_name}</strong><br>
        <small>{message}</small>
    </div>
    """, unsafe_allow_html=True)

def create_provider_card(provider, card_type="removal"):
    """Create provider recommendation cards"""
    if card_type == "removal":
        card_class = "provider-card-removal"
        color = BRAND_COLORS['error']
        quality_concern = "Poor" if provider['quality_score'] < 3.5 else "Below Average"
        
        return f"""
        <div class="{card_class}">
            <strong style="color: {color};">{provider['name']}</strong><br>
            <small style="color: #666;">
                <strong>Performance:</strong> {quality_concern} quality score ({provider['quality_score']:.1f}/5.0)<br>
                <strong>Cost Impact:</strong> High cost at ${provider['cost_per_utilizer']:.0f} per utilizer<br>
                <strong>Financial Opportunity:</strong> ${provider['termination_value']:,.0f} annual savings<br>
                <strong>Service Line:</strong> {provider['clinical_group']} • <strong>Volume:</strong> {provider['utilizers']:,} members<br>
                <strong>Market:</strong> {provider['primary_cbsa'][:40]}...<br>
                <strong>Network Risk:</strong> {provider['adequacy_risk']} adequacy impact
            </small>
        </div>
        """
    
    elif card_type == "addition":
        card_class = "provider-card-addition"
        color = BRAND_COLORS['success']
        quality_strength = "Excellent" if provider['quality_score'] >= 4.5 else "Good"
        
        return f"""
        <div class="{card_class}">
            <strong style="color: {color};">{provider['name']}</strong><br>
            <small style="color: #666;">
                <strong>Performance:</strong> {quality_strength} quality score ({provider['quality_score']:.1f}/5.0)<br>
                <strong>Cost Efficiency:</strong> Competitive at ${provider['cost_per_utilizer']:.0f} per utilizer<br>
                <strong>Market Position:</strong> {provider['market_position_percentile']:.0f}th percentile performance<br>
                <strong>Service Line:</strong> {provider['clinical_group']} • <strong>Capacity:</strong> {provider['utilizers']:,} members<br>
                <strong>Market:</strong> {provider['primary_cbsa'][:40]}...<br>
                <strong>Geographic Coverage:</strong> {', '.join(provider['operating_states'][:3])}
            </small>
        </div>
        """

def create_info_box(content, box_type="blue"):
    """Create styled info boxes"""
    box_class = f"info-box-{box_type}"
    color = BRAND_COLORS['dark_blue'] if box_type == "blue" else BRAND_COLORS['dark_green']
    
    return f"""
    <div class="{box_class}">
        <div style="color: {color};">
            {content}
        </div>
    </div>
    """

def create_quadrant_summary_metrics(quadrant_summary):
    """Create quadrant summary metrics in 4 columns"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        preferred_count = quadrant_summary.get('Preferred Partners', 0)
        st.metric("Preferred Partners", preferred_count, help="High Quality, Low Cost - Retain & Expand")
    
    with col2:
        strategic_count = quadrant_summary.get('Strategic Opportunities', 0)
        st.metric("Strategic Opportunities", strategic_count, help="High Quality, High Cost - Negotiate Terms")
    
    with col3:
        focus_count = quadrant_summary.get('Performance Focus', 0)
        st.metric("Performance Focus", focus_count, help="Low Quality, Low Cost - Quality Improvement")
    
    with col4:
        optimization_count = quadrant_summary.get('Optimization Candidates', 0)
        st.metric("Optimization Candidates", optimization_count, help="Low Quality, High Cost - Consider Alternatives")

def create_welcome_screen():
    """Create the welcome screen content"""
    return f"""
    ## Welcome to AI Agent Network Optimization
    
    <div style="background: {BRAND_COLORS['accent_blue']}; padding: 2rem; border-radius: 12px; margin: 2rem 0;">
    
    ### Your Specialized AI Agent Team:
    
    **Data Specialist Agent**
    - Advanced provider data processing and validation
    - Intelligent filtering with quality assessment
    - Comprehensive data insights and anomaly detection
    
    **Quadrant Analyst Agent**  
    - Sophisticated performance quadrant analysis
    - Optimization opportunity identification
    - Cost-quality balance recommendations with network adequacy assessment
    
    **Competitive Intelligence Agent**
    - Market positioning and competitive benchmarking
    - Industry standard comparisons and threat analysis
    - Strategic competitive advantage identification
    
    **Executive Strategist Agent**
    - Comprehensive analysis synthesis into executive insights
    - Strategic recommendations with ROI projections
    - Implementation roadmaps and success metrics
    
    </div>
    
    ### AI-Powered Network Optimization:
    1. **Configure Analysis Parameters** - Set your filters and criteria in the sidebar
    2. **Deploy AI Agents** - Click "Deploy AI Agents" to start the collaborative analysis
    3. **Monitor Agent Progress** - Watch real-time status updates as agents work together
    4. **Review AI Insights** - Examine comprehensive results across multiple analysis dimensions
    5. **Implement Recommendations** - Act on AI-generated strategic recommendations
    
    ### Key AI Agent Capabilities:
    - **Intelligent Data Processing** with quality validation and anomaly detection
    - **Advanced Quadrant Analysis** using AI-enhanced performance categorization
    - **Competitive Intelligence** with market positioning and benchmarking
    - **Strategic Synthesis** combining all analyses into actionable executive insights
    - **Real-time Collaboration** between specialized agents for comprehensive coverage
    
    <div style="background: {BRAND_COLORS['accent_green']}; padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0; text-align: center;">
    <strong style="color: {BRAND_COLORS['dark_green']}; font-size: 1.1rem;">
    Ready to experience AI agent-powered network optimization?
    </strong>
    </div>
    
    *Configure your analysis parameters and deploy your AI agent team to transform your provider network optimization process.*
    """

def create_footer(crewai_available=False):
    """Create the enhanced footer"""
    return f"""
    <div style="text-align: center; color: {BRAND_COLORS['dark_blue']}; 
                background: {BRAND_COLORS['light_gray']}; padding: 1.5rem; border-radius: 8px;">
        <h4 style="margin: 0 0 0.5rem 0;">AI Agent Network Optimization Portal</h4>
        <!--p style="margin: 0; opacity: 0.8;">
            Powered by <span style="color: {BRAND_COLORS['primary_green']}; font-weight: 600;">CrewAI Multi-Agent Intelligence</span> • 
            Advanced Provider Analytics • Built for Healthcare Excellence
        </p-->
        <!--p style="margin: 0.5rem 0; opacity: 0.8;">
            <span style="color: {BRAND_COLORS['primary_blue']};">OneHome</span> & 
            <span style="color: {BRAND_COLORS['primary_green']};">Humana</span> Partnership
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.6;">
            Version 2.0.0 (AI Enhanced) • {datetime.now().strftime("%Y-%m-%d")} • 
            CrewAI Framework: {"Available" if crewai_available else "Mock Mode"}
        </p-->
        <!--p style="margin: 0.3rem 0 0 0; font-size: 0.9rem; opacity: 0.7;">
            AI Team Contact: <strong>hsa_ai_team@humana.com</strong-->
        </p>
    </div>
    """

