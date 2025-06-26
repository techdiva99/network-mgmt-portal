# ui/__init__.py
"""
UI package for Network Optimization Platform
"""

# Import from config package (not ui package)
from config.brand_colors import BRAND_COLORS, QUADRANT_COLORS, STATUS_COLORS, get_logo_html
from config.settings import PAGE_CONFIG, ANALYSIS_THRESHOLDS, DATA_CONSTANTS

# Core UI components (existing)
from .styling import apply_custom_css, render_custom_header
from .components import (
    display_metrics_row,
    display_agent_status,
    create_provider_card,
    create_quadrant_summary_metrics,
    create_welcome_screen,
    create_footer
)
from .visualizations import (
    create_quadrant_visualization,
    create_competitive_positioning_chart,
    create_market_position_bell_curve,
    create_state_opportunity_bar_chart,
    create_episode_performance_chart,
    create_state_performance_chart,
    create_us_map_choropleth
)
from .network_intelligence_tab import (
    render_network_intelligence_tab
)
from .network_builder_components import *

# Existing sidebar (already created)
from .sidebar_manager import render_sidebar, create_sidebar_header

# New modular components (only import if they exist)
try:
    from .tab_manager import render_analysis_tabs
except ImportError:
    pass

try:
    from .agent_dashboard_tab import render_ai_agent_dashboard
except ImportError:
    pass

try:
    from .competitive_analysis_tab import render_competitive_analysis_tab
except ImportError:
    pass

try:
    from .geographic_optimization_tab import render_geographic_optimization_tab
except ImportError:
    pass

try:
    from .optimization_summary_tab import render_optimization_summary_tab
except ImportError:
    pass

try:
    from .agent_methodology_tab import render_agent_methodology_tab
except ImportError:
    pass

try:
    from .network_builder import render_network_builder_tab
except ImportError:
    pass

__all__ = [
    # Brand colors and config (imported from config package)
    'BRAND_COLORS',
    'QUADRANT_COLORS', 
    'STATUS_COLORS',
    'get_logo_html',
    'PAGE_CONFIG',
    'ANALYSIS_THRESHOLDS',
    'DATA_CONSTANTS',
    
    # Styling
    'apply_custom_css',
    'render_custom_header',
    
    # Core components
    'display_metrics_row',
    'display_agent_status', 
    'create_provider_card',
    'create_sidebar_header',
    'create_quadrant_summary_metrics',
    'create_welcome_screen',
    'create_footer',
    
    # Visualizations
    'create_quadrant_visualization',
    'create_competitive_positioning_chart',
    'create_market_position_bell_curve',
    'create_state_opportunity_bar_chart',
    'create_episode_performance_chart',
    'create_state_performance_chart',
    'create_us_map_choropleth',
    
    # Layouts
    'render_network_intelligence_tab',
    'render_optimization_summary_tab',
    
    # Sidebar (existing)
    'render_sidebar',
]


