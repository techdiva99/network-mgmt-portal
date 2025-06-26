# config/brand_colors.py
"""
OneHome × Humana Brand Color Scheme
Extracted from original Network Optimization Platform
"""

# Brand colors from OneHome (cyan/blue) and Humana (green)
BRAND_COLORS = {
    'primary_blue': '#00B4D8',
    'primary_green': '#7CB342', 
    'secondary_blue': '#0077BE',
    'secondary_green': '#4CAF50',
    'accent_blue': '#E1F5FE',
    'accent_green': '#E8F5E8',
    'dark_blue': '#003F5C',
    'dark_green': '#2E7D32',
    'white': '#FFFFFF',
    'light_gray': '#F5F5F5',
    'warning': '#FF9800',
    'error': '#F44336',
    'success': '#4CAF50'
}

# Quadrant color mapping
QUADRANT_COLORS = {
    'Preferred Partners': BRAND_COLORS['success'],
    'Strategic Opportunities': BRAND_COLORS['warning'],
    'Performance Focus': BRAND_COLORS['primary_blue'],
    'Optimization Candidates': BRAND_COLORS['error']
}

# Status color mapping
STATUS_COLORS = {
    'In-Network': BRAND_COLORS['primary_green'],
    'Out-of-Network': BRAND_COLORS['error'],
    'High': BRAND_COLORS['error'],
    'Medium': BRAND_COLORS['warning'],
    'Low': BRAND_COLORS['success']
}

def get_logo_html(logo_path="logo.png", width=60, height=60):
    """Generate HTML for logo display"""
    return f'<div style="width: {width}px; height: {height}px; background: {BRAND_COLORS["primary_blue"]}; border-radius: 8px; margin-right: 15px; display: inline-flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">HSA</div>'

