# config/settings.py
"""
Application configuration settings
"""

# Streamlit page configuration
PAGE_CONFIG = {
    'page_title': "Network Optimization Portal",
    'page_icon': "⚕",
    'layout': "wide",
    'initial_sidebar_state': "expanded",
    'menu_items': {
        'Get Help': 'https://docs.networkoptimizer.com',
        'Report a bug': 'https://github.com/yourorg/network-optimizer/issues',
        'About': """
        # Network Optimization Portal
        
        **Version:** 2.0.0 (CrewAI Enhanced)
        **Built with:** Streamlit, Plotly, Pandas, CrewAI  
        **Theme:** OneHome & Humana  
        
        Advanced provider network optimization with AI agent intelligence.
        """
    }
}

# Analysis thresholds
ANALYSIS_THRESHOLDS = {
    'quality_threshold': 4.0,
    'cost_threshold': 600,
    'high_volume_threshold': 3000,
    'medium_volume_threshold': 1000,
    'high_quality_threshold': 4.5,
    'medium_quality_threshold': 3.5,
    'high_cost_threshold': 700,
    'medium_cost_threshold': 400
}

# Data generation constants
DATA_CONSTANTS = {
    'home_health_episodes': [
        'Post-Acute Care', 'Chronic Disease Management', 'Wound Care', 
        'Cardiac Care', 'Diabetes Management', 'COPD Management', 
        'Medication Management', 'Rehabilitation'
    ],
    'cbsas': [
        'New York-Newark-Jersey City, NY-NJ-PA',
        'Los Angeles-Long Beach-Anaheim, CA',
        'Chicago-Naperville-Elgin, IL-IN-WI',
        'Dallas-Fort Worth-Arlington, TX',
        'Houston-The Woodlands-Sugar Land, TX',
        'Washington-Arlington-Alexandria, DC-VA-MD-WV',
        'Miami-Fort Lauderdale-West Palm Beach, FL',
        'Philadelphia-Camden-Wilmington, PA-NJ-DE-MD',
        'Atlanta-Sandy Springs-Roswell, GA',
        'Boston-Cambridge-Newton, MA-NH'
    ],
    'states': ['NY', 'CA', 'IL', 'TX', 'FL', 'VA', 'PA', 'GA', 'MA', 'OH', 
              'MI', 'NC', 'NJ', 'AZ', 'WA', 'TN', 'IN', 'MO', 'MD', 'WI'],
    'clinical_groups': [
        "Behavioral Health",
        "Wounds", 
        "Complex Nursing Interventions",
        "MMTA_Cardiac_and_Circulatory",
        "MMTA_Endocrine",
        "MMTA_Infectious_Disease",
        "Neoplasm_and_Blood_Forming_Diseases",
        "MMTA_Gastrointestinal_Tract_and_Genitourinary_System",
        "MMTA_Respiratory",
        "MMTA_Surgical_Aftercare",
        "Musculoskeletal_Rehabilitation",
        "Neurological_Rehabilitation"
    ],
    'provider_names': [
        "MetroHealth Medical Center", "Riverside Healthcare", "Summit Medical Group",
        "Valley Health System", "Coastal Family Medicine", "Mountain View Specialists", 
        "Downtown Urgent Care", "Northside Hospital", "Lakeside Mental Health",
        "Central OB/GYN Clinic", "Advanced Home Care", "Premier Health Services",
        "Optimal Care Partners", "Elite Home Health", "Comprehensive Care Network",
        "Quality First Healthcare", "Regional Care Providers", "Integrated Health Solutions",
        "Community Care Alliance", "Specialized Home Services", "Unity Health Partners",
        "Excellence in Care", "Advanced Medical Solutions", "Preferred Care Network",
        "Superior Health Services", "Innovative Care Group", "Total Care Solutions",
        "Professional Health Partners", "Dynamic Care Network", "Complete Care Services",
        "Strategic Health Alliance", "Premier Care Solutions", "Advanced Care Network",
        "Integrated Care Partners", "Quality Care Alliance", "Comprehensive Health Group",
        "Optimal Health Solutions", "Excellence Care Network", "Superior Care Partners",
        "Professional Care Group", "Elite Health Services", "Premier Health Alliance",
        "Advanced Care Solutions", "Quality Health Partners", "Comprehensive Care Alliance",
        "Superior Health Network", "Professional Care Solutions", "Elite Care Group",
        "Premier Care Network", "Advanced Health Partners"
    ]
}

