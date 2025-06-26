# ui/tab_manager.py
"""
Centralized tab rendering and management
"""
import streamlit as st
from ui.layouts import render_network_intelligence_tab, render_optimization_summary_tab
from ui.competitive_analysis_tab import render_competitive_analysis_tab
from ui.geographic_optimization_tab import render_geographic_optimization_tab
from ui.network_builder import render_network_builder_tab
from ui.agent_methodology_tab import render_agent_methodology_tab
from ui.agent_dashboard_tab import render_ai_agent_dashboard

def render_analysis_tabs(df, results, metrics):
    """Render the main analysis tabs"""
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Optimization Summary",
        "Network Intelligence", 
        "Competitive Analysis", 
        "Geographic Optimization", 
        "Network Builder",
        "Agent Methodology",
        "AI Agent Dashboard"
    ])
    
    with tab1:
        render_optimization_summary_tab(df, results)
    
    with tab2:
        render_network_intelligence_tab(df, results)
    
    with tab3:
        render_competitive_analysis_tab(df, results)
    
    with tab4:
        render_geographic_optimization_tab(df, results)
    
    with tab5:
        render_network_builder_tab(df, results)
    
    with tab6:
        render_agent_methodology_tab()
    
    with tab7:
        render_ai_agent_dashboard(df, results)

