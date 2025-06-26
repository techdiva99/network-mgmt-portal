# ui/competitive_analysis_tab.py
"""
Competitive Analysis tab implementation
"""
import streamlit as st
from ui.visualizations import create_competitive_positioning_chart

def render_competitive_analysis_tab(df, results):
    """Render Competitive Analysis tab"""
    st.markdown("### Competitive Analysis")
    
    # Market position analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Market Leaders")
        top_performers = df[df['market_position_percentile'] >= 75].head(5)
        for _, leader in top_performers.iterrows():
            st.markdown(f"• **{leader['name']}** - {leader['market_position_percentile']:.0f}th percentile")
    
    with col2:
        st.markdown("#### Improvement Targets")
        poor_performers = df[df['market_position_percentile'] <= 25].head(5)
        for _, target in poor_performers.iterrows():
            st.markdown(f"• **{target['name']}** - {target['market_position_percentile']:.0f}th percentile")
    
    # Competitive positioning chart
    if len(df) > 0:
        fig_comp = create_competitive_positioning_chart(df)
        st.plotly_chart(fig_comp, use_container_width=True)

