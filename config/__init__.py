# config/__init__.py
"""
Configuration package for Network Optimization Platform
"""
from .brand_colors import BRAND_COLORS, QUADRANT_COLORS, STATUS_COLORS, get_logo_html
from .settings import PAGE_CONFIG, ANALYSIS_THRESHOLDS, DATA_CONSTANTS

__all__ = [
    'BRAND_COLORS', 
    'QUADRANT_COLORS', 
    'STATUS_COLORS', 
    'get_logo_html',
    'PAGE_CONFIG', 
    'ANALYSIS_THRESHOLDS', 
    'DATA_CONSTANTS'
]

