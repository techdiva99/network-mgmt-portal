# ui/styling.py
"""
CSS styling and visual components for the Network Optimization Platform
"""

import streamlit as st
from config.brand_colors import BRAND_COLORS, get_logo_html

def apply_custom_css():
    """Apply the complete CSS styling from the original platform"""
    st.markdown(f"""
    <style>
        /* Hide Streamlit header and menu */
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Hide default sidebar toggle */
        .css-1544g2n {{display: none;}}
        button[title="Close sidebar"] {{display: none;}}
        .css-79elbk {{display: none;}}
        
        /* Custom header that stays visible */
        .custom-header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: {BRAND_COLORS['white']};
            border-bottom: 4px solid {BRAND_COLORS['primary_blue']};
            padding: 1rem 1.5rem;
            z-index: 1001;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: margin-left 0.3s ease;
            min-height: 80px;
        }}
        
        .header-content {{
            display: flex;
            align-items: center;
            justify-content: flex-start;
            transition: all 0.3s ease;
            padding-left: 0;
            width: 100%;
        }}
        
        @media (min-width: 768px) {{
            .custom-header.sidebar-open .header-content {{
                padding-left: 140px;
            }}
        }}
        
        .header-title {{
            font-size: 1.8rem;
            font-weight: 700;
            color: {BRAND_COLORS['dark_blue']};
            margin: 0;
            display: flex;
            align-items: center;
        }}
        
        .header-subtitle {{
            font-size: 1rem;
            color: {BRAND_COLORS['secondary_blue']};
            margin: 0;
            font-weight: 500;
        }}
        
        /* Add padding to main content */
        .main .block-container {{
            padding-top: 120px;
        }}
        
        /* Sidebar positioning */
        .css-1d391kg {{
            padding-top: 100px;
            z-index: 1000;
        }}
        
        /* Compact metrics styling */
        .metric-card-compact {{
            background: {BRAND_COLORS['white']};
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid {BRAND_COLORS['primary_blue']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
            text-align: center;
        }}
        
        .metric-card-compact:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }}
        
        .metric-card-compact-green {{
            border-left-color: {BRAND_COLORS['primary_green']};
        }}
        
        .metric-card-compact h4 {{
            font-size: 1rem;
            font-weight: 600;
            margin: 0 0 0.3rem 0;
            color: {BRAND_COLORS['dark_blue']};
        }}
        
        .metric-card-compact h2 {{
            font-size: 2.2rem;
            margin: 0;
            font-weight: 700;
        }}
        
        /* Agent status indicators */
        .agent-status {{
            background: {BRAND_COLORS['white']};
            border-radius: 8px;
            padding: 1rem;
            border-left: 4px solid {BRAND_COLORS['primary_green']};
            margin: 0.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .agent-working {{
            border-left-color: {BRAND_COLORS['warning']};
            animation: pulse 2s infinite;
        }}
        
        .agent-complete {{
            border-left-color: {BRAND_COLORS['success']};
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        /* Tab styling - Enhanced */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: {BRAND_COLORS['light_gray']};
            padding: 8px;
            border-radius: 12px;
            margin-bottom: 2rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: {BRAND_COLORS['white']};
            border-radius: 8px;
            color: {BRAND_COLORS['dark_blue']};
            font-weight: 600;
            font-size: 1.1rem;
            padding: 12px 24px;
            border: 2px solid transparent;
            transition: all 0.2s ease;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            border-color: {BRAND_COLORS['primary_blue']};
            background: {BRAND_COLORS['accent_blue']};
        }}
        
        .stTabs [aria-selected="true"] {{
            background: {BRAND_COLORS['primary_blue']};
            color: white;
            border-color: {BRAND_COLORS['secondary_blue']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        /* Button styling */
        .stButton > button {{
            background: {BRAND_COLORS['primary_blue']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        
        .stButton > button:hover {{
            background: {BRAND_COLORS['secondary_blue']};
            transform: translateY(-1px);
        }}
        
        .green-button > button {{
            background: {BRAND_COLORS['primary_green']} !important;
        }}
        
        .green-button > button:hover {{
            background: {BRAND_COLORS['secondary_green']} !important;
        }}
        
        /* Sidebar styling */
        .sidebar-header {{
            background: {BRAND_COLORS['primary_green']};
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            text-align: center;
        }}
        
        /* Provider cards */
        .provider-card-removal {{
            background: #fff5f5;
            border-left: 4px solid {BRAND_COLORS['error']};
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 4px;
        }}
        
        .provider-card-addition {{
            background: #f0fff4;
            border-left: 4px solid {BRAND_COLORS['success']};
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 4px;
        }}
        
        /* Info boxes */
        .info-box-blue {{
            background: {BRAND_COLORS['accent_blue']};
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        .info-box-green {{
            background: {BRAND_COLORS['accent_green']};
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .custom-header {{
                padding: 0.8rem 0.8rem;
                min-height: 70px;
            }}
            .header-title {{
                font-size: 1.4rem;
            }}
            .header-subtitle {{
                font-size: 0.9rem;
            }}
            .main .block-container {{
                padding-top: 100px;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

def render_custom_header():
    """Render the custom header with branding"""
    st.markdown(f"""
    <div class="custom-header" id="main-header">
        <div class="header-content">
            {get_logo_html("logo.png", 50, 50)}
            <div>
                <h1 class="header-title">Network Optimization Portal</h1>
                <p class="header-subtitle">Advanced Provider Analytics & AI Agent Intelligence</p>
            </div>
        </div>
        <div style="color: {BRAND_COLORS['primary_blue']}; font-weight: 700; font-size: 1.1rem;">
            OneHome × Humana
        </div>
    </div>

    <script>
    function checkSidebar() {{
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const header = document.getElementById('main-header');
        if (sidebar && header) {{
            if (sidebar.style.display !== 'none' && window.innerWidth > 768) {{
                header.classList.add('sidebar-open');
            }} else {{
                header.classList.remove('sidebar-open');
            }}
        }}
    }}
    window.addEventListener('load', checkSidebar);
    window.addEventListener('resize', checkSidebar);
    setInterval(checkSidebar, 500);
    </script>
    """, unsafe_allow_html=True)

