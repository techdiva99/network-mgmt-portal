# main.py
"""
Main Streamlit application for CrewAI Network Optimization Platform
Refactored modular architecture with proper separation of concerns
"""

import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Configuration imports
from config.settings import PAGE_CONFIG
from config.brand_colors import BRAND_COLORS

# UI imports
from ui.styling import apply_custom_css, render_custom_header
from ui.components import (
    display_metrics_row,
    create_welcome_screen,
    create_footer
)
from ui.sidebar_manager import render_sidebar
from ui.tab_manager import render_analysis_tabs

# Utils imports
from utils.metrics_calculator import calculate_network_metrics, add_quadrant_analysis
from utils.analysis_orchestrator import AnalysisOrchestrator

# CrewAI imports with fallback
try:
    from crews.network_optimization_crew import NetworkOptimizationCrew
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(**PAGE_CONFIG)

def initialize_session_state():
    """Initialize session state variables"""
    if 'agent_status' not in st.session_state:
        st.session_state.agent_status = {
            "Data Specialist": "waiting",
            "Quadrant Analyst": "waiting",   
            "Competitive Intelligence": "waiting",
            "Executive Strategist": "waiting"
        }
    
    if 'crew' not in st.session_state and CREWAI_AVAILABLE:
        st.session_state.crew = NetworkOptimizationCrew()

def render_main_content(sidebar_data):
    """Render main content based on sidebar interactions"""
    
    if sidebar_data['run_analysis']:
        # Initialize orchestrator
        orchestrator = AnalysisOrchestrator()
        
        # Execute analysis using orchestrator
        try:
            # Only show spinner while analysis is running
            with st.spinner("🤖 AI Agents are analyzing your provider network..."):
                results = orchestrator.execute_agent_analysis(sidebar_data['filters'])
            # After spinner, show results and UI
            df = pd.DataFrame(results["data_analysis"]["data"])
            df = add_quadrant_analysis(df)

            # Set all agent statuses to 'success' after run
            if 'agent_status' in st.session_state:
                for agent in st.session_state.agent_status:
                    st.session_state.agent_status[agent] = 'success'
            agent_status = st.session_state.get('agent_status', {})
            agent_names = list(agent_status.keys())
            agent_cols = st.columns(4)
            with st.expander('🤖 AI Agent Processing Status', expanded=False):
                for idx, agent in enumerate(agent_names):
                    with agent_cols[idx % 4]:
                        status = agent_status[agent]
                        # Only show status if not 'success', else show a checkmark and 'Complete'
                        if status == 'success':
                            icon = '✅'
                            status_text = 'Complete'
                        elif status == 'waiting':
                            icon = '⏳'
                            status_text = 'Waiting'
                        else:
                            icon = '❌'
                            status_text = status.capitalize()
                        st.markdown(f'<div style="border-radius: 5px; padding: 0.5em; text-align: center; margin-bottom: 0.5em;">{icon} <b>{agent}</b><br><span style="font-size:0.9em;">{status_text}</span></div>', unsafe_allow_html=True)

            # Calculate and display metrics
            metrics = calculate_network_metrics(df)
            display_metrics_row(metrics)
            
            # Render analysis tabs
            render_analysis_tabs(df, results, metrics)

            # # Collapsible section for analysis results and agent progress
            # with st.expander("AI Agent Processing & Results", expanded=False):
            #     # Two-column layout for agent progress and analysis results
            #     col1, col2 = st.columns(2)
            #     with col1:
            #         st.markdown("#### Agent Progress")
            #         agent_status = st.session_state.get('agent_status', {})
            #         for agent, status in agent_status.items():
            #             st.write(f"- **{agent}**: {status}")
            #     with col2:
            #         st.markdown("### Analysis Results")
            #         # st.write(f"✅ Processed {len(df)} providers")
            #         # st.write(f"✅ Analysis completed at {results['timestamp']}")
            #         # Display some basic results
            #         if 'quadrant_summary' in results['quadrant_analysis']:
            #             st.markdown("#### Provider Quadrants")
            #             for quadrant, count in results['quadrant_analysis']['quadrant_summary'].items():
            #                 st.write(f"• {quadrant}: {count} providers")
        
        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {str(e)}")
            st.stop()
    else:
        # Show welcome screen
        st.markdown(create_welcome_screen(), unsafe_allow_html=True)

def main():
    """Main application entry point"""
    # Configure page
    configure_page()
    
    # Apply styling and render header
    apply_custom_css()
    render_custom_header()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and get user inputs (using existing sidebar module)
    sidebar_data = render_sidebar()
    
    # Render main content
    render_main_content(sidebar_data)
    
    # Render footer
    st.markdown("---")
    st.markdown(create_footer(CREWAI_AVAILABLE), unsafe_allow_html=True)

if __name__ == "__main__":
    main()


