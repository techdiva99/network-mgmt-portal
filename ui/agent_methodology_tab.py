# ui/agent_methodology_tab.py
"""
Agent Methodology tab implementation
"""
import streamlit as st
from config.brand_colors import BRAND_COLORS

def render_agent_methodology_tab():
    """Render Agent Methodology tab"""
    st.markdown("### AI Agent Methodology")
    
    st.markdown(f"""
    <div class="info-box-blue">
        <h5 style="color: {BRAND_COLORS['dark_blue']}; margin: 0 0 1rem 0;">AI Agent Architecture</h5>
        
        <h6 style="color: {BRAND_COLORS['dark_blue']}; margin: 1rem 0 0.5rem 0;">Agent Specializations:</h6>
        <ul style="margin: 0;">
            <li><strong>Data Specialist Agent:</strong> Advanced data processing, quality assessment, and filtering</li>
            <li><strong>Quadrant Analyst Agent:</strong> Performance categorization and optimization opportunity identification</li>
            <li><strong>Competitive Intelligence Agent:</strong> Market analysis and competitive positioning</li>
            <li><strong>Executive Strategist Agent:</strong> Strategic synthesis and executive reporting</li>
        </ul>
        
        <h6 style="color: {BRAND_COLORS['dark_blue']}; margin: 1rem 0 0.5rem 0;">Agent Collaboration:</h6>
        <p style="margin: 0.5rem 0;">Sequential workflow with data handoff between specialized agents, ensuring comprehensive analysis through AI collaboration.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box-green">
        <h5 style="color: {BRAND_COLORS['dark_green']}; margin: 0 0 1rem 0;">Quadrant Analysis Methodology</h5>
        
        <h6 style="color: {BRAND_COLORS['dark_green']}; margin: 1rem 0 0.5rem 0;">AI-Enhanced Categorization:</h6>
        <ul style="margin: 0;">
            <li><strong>Preferred Partners:</strong> AI identifies high-quality, cost-efficient providers for retention</li>
            <li><strong>Strategic Opportunities:</strong> High-performing providers flagged for contract optimization</li>
            <li><strong>Performance Focus:</strong> Cost-effective providers targeted for quality improvement programs</li>
            <li><strong>Optimization Candidates:</strong> AI recommends comprehensive performance review or removal</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

