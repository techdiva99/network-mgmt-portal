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

import base64
import os

def get_logo_html(logo_path="logo.png", width=60, height=60, type='header_right'):
    """Generate HTML for logo display using base64 encoding for Streamlit compatibility"""
    if type=='header_left':
        return f'<div style="width: {width}px; height: {height}px; background: {BRAND_COLORS["primary_blue"]}; border-radius: 8px; margin-right: 15px; display: inline-flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">NMX</div>'
    else:
        logo_full_path = os.path.join(os.path.dirname(__file__), "..", "data", logo_path)
        try:
            with open(logo_full_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()
            return f'<img src="data:image/png;base64,{encoded}" width="{width}" height="{height}" style="margin-right: 15px; border-radius: 8px; display: inline-flex; vertical-align: middle;" alt="Logo" />'
        except Exception as e:
            # fallback to text if image not found
            return f'<div style="width: {width}px; height: {height}px; background: {BRAND_COLORS["primary_blue"]}; border-radius: 8px; margin-right: 15px; display: inline-flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">NMX</div>'

