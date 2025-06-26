# ui/sidebar_manager.py
"""
Complete sidebar rendering and filter management
"""

import streamlit as st

def create_sidebar_header(title):
    """Create styled sidebar header"""
    return f"""
    <div class="sidebar-header">
        <h3 style="margin: 0;">{title}</h3>
    </div>
    """
    
def render_sidebar():
    """Render the sidebar with all controls"""
    with st.sidebar:
        st.markdown(create_sidebar_header("Network Analysis Controls"), unsafe_allow_html=True)
        
        # Primary filters
        st.subheader("Primary Controls")
        
        tin_search = st.text_input("TIN Number Search", placeholder="Enter Tax ID Number")
        
        st.markdown("**Geographic:**")
        all_states = ['NY', 'CA', 'IL', 'TX', 'FL', 'VA', 'PA', 'GA', 'MA', 'OH']
        state_filter = st.selectbox("State", ["All States"] + all_states)
        
        all_cbsas = [
            'New York-Newark-Jersey City, NY-NJ-PA',
            'Los Angeles-Long Beach-Anaheim, CA',
            'Chicago-Naperville-Elgin, IL-IN-WI'
        ]
        cbsa_filter = st.selectbox("CBSA (Metro Area)", ["All CBSAs"] + all_cbsas)
        
        clinical_groups = [
            "Behavioral Health",
            "Wounds", 
            "Complex Nursing Interventions",
            "MMTA_Cardiac_and_Circulatory",
            "MMTA_Endocrine",
            "MMTA_Infectious_Disease"
        ]
        clinical_group_filter = st.selectbox("Clinical Group", ["All Clinical Groups"] + clinical_groups)
        
        st.markdown("---")
        
        # Advanced filters
        st.subheader("Advanced Controls")
        
        volume_filter = st.selectbox(
            "Volume", 
            ["All Volumes", "High Volume (>3000)", "Medium Volume (1000-3000)", "Low Volume (<1000)"]
        )
        
        quality_filter = st.selectbox(
            "Quality",
            ["All Quality", "High Quality (>4.5)", "Medium Quality (3.5-4.5)", "Low Quality (<3.5)"]
        )
        
        cost_filter = st.selectbox(
            "Cost",
            ["All Costs", "High Cost (>$700)", "Medium Cost ($400-700)", "Low Cost (<$400)"]
        )
        
        adequacy_filter = st.selectbox(
            "Network Adequacy Risk",
            ["All Risk Levels", "High Risk", "Medium Risk", "Low Risk"]
        )
        
        # Network status checkboxes
        st.markdown("**Network Status:**")
        col1, col2 = st.columns(2)
        with col1:
            in_network_check = st.checkbox("In-Network", value=True)
        with col2:
            out_network_check = st.checkbox("Out-of-Network", value=True)
        
        st.markdown("---")
        
        # Analysis controls
        st.subheader("Analysis Actions")
        
        run_analysis = st.button("Deploy AI Agents", type="primary", use_container_width=True)
        
        if st.button("Reset Agent Status", use_container_width=True):
            st.session_state.agent_status = {
                "Data Specialist": "waiting",
                "Quadrant Analyst": "waiting", 
                "Competitive Intelligence": "waiting",
                "Executive Strategist": "waiting"
            }
            st.rerun()
    
    return {
        'run_analysis': run_analysis,
        'filters': {
            "network_statuses": ([s for s in ["In-Network", "Out-of-Network"] 
                                if (s == "In-Network" and in_network_check) or 
                                   (s == "Out-of-Network" and out_network_check)]),
            "volume_filter": volume_filter,
            "quality_filter": quality_filter,
            "cost_filter": cost_filter,
            "state_filter": state_filter,
            "cbsa_filter": cbsa_filter,
            "clinical_group_filter": clinical_group_filter,
            "adequacy_filter": adequacy_filter,
            "tin_search": tin_search
        }
    }

