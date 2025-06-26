# tools/visualization_tool.py
"""
Visualization tool for generating charts and graphs for network analysis
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# CrewAI imports with fallback
try:
    from crewai.tools import BaseTool
except ImportError:
    try:
        from crewai_tools import BaseTool
    except ImportError:
        class BaseTool:
            name: str = ""
            description: str = ""
            def _run(self, *args, **kwargs):
                raise NotImplementedError

class VisualizationTool(BaseTool):
    name: str = "Visualization Tool"
    description: str = "Generate interactive charts and visualizations for network optimization analysis"
    
    def __init__(self):
        super().__init__()
        # Brand colors for consistent styling
        self.brand_colors = {
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
        
        self.quadrant_colors = {
            'Preferred Partners': self.brand_colors['success'],
            'Strategic Opportunities': self.brand_colors['warning'],
            'Performance Focus': self.brand_colors['primary_blue'],
            'Optimization Candidates': self.brand_colors['error']
        }
    
    def _run(self, 
             chart_type: str, 
             data: List[Dict], 
             title: str = "", 
             **kwargs) -> Dict[str, Any]:
        """Generate visualization based on chart type and data"""
        
        df = pd.DataFrame(data)
        
        if chart_type == "quadrant_analysis":
            return self._create_quadrant_chart(df, title, **kwargs)
        elif chart_type == "competitive_positioning":
            return self._create_competitive_chart(df, title, **kwargs)
        elif chart_type == "geographic_heatmap":
            return self._create_geographic_heatmap(df, title, **kwargs)
        elif chart_type == "performance_trends":
            return self._create_performance_trends(df, title, **kwargs)
        elif chart_type == "clinical_group_analysis":
            return self._create_clinical_group_chart(df, title, **kwargs)
        elif chart_type == "network_adequacy":
            return self._create_network_adequacy_chart(df, title, **kwargs)
        elif chart_type == "financial_impact":
            return self._create_financial_impact_chart(df, title, **kwargs)
        elif chart_type == "market_position_distribution":
            return self._create_market_distribution_chart(df, title, **kwargs)
        else:
            return {"error": f"Chart type '{chart_type}' not supported"}
    
    def _create_quadrant_chart(self, df: pd.DataFrame, title: str, **kwargs) -> Dict[str, Any]:
        """Create quadrant analysis scatter plot"""
        quality_threshold = kwargs.get('quality_threshold', 4.0)
        cost_threshold = kwargs.get('cost_threshold', 600)
        
        # Add quadrant categories if not present
        if 'quadrant' not in df.columns:
            df['quadrant'] = df.apply(
                lambda row: self._get_quadrant_category(
                    row['quality_score'], 
                    row['cost_per_utilizer'], 
                    quality_threshold, 
                    cost_threshold
                ), axis=1
            )
        
        fig = px.scatter(
            df,
            x='cost_per_utilizer',
            y='quality_score',
            size='utilizers',
            color='quadrant',
            hover_data=['name', 'network_status', 'clinical_group'],
            title=title or "Provider Performance Quadrants",
            labels={
                'cost_per_utilizer': 'Cost per Utilizer ($)',
                'quality_score': 'Quality Score',
                'utilizers': 'Utilizer Count'
            },
            color_discrete_map=self.quadrant_colors
        )
        
        # Add threshold lines
        fig.add_hline(y=quality_threshold, line_dash="dash", line_color="gray", 
                      annotation_text="Quality Threshold")
        fig.add_vline(x=cost_threshold, line_dash="dash", line_color="gray", 
                      annotation_text="Cost Threshold")
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title_font_color=self.brand_colors['dark_blue'],
            height=500
        )
        
        return {
            "chart_type": "quadrant_analysis",
            "figure": fig.to_json(),
            "insights": self._generate_quadrant_insights(df),
            "data_points": len(df)
        }
    
    def _create_competitive_chart(self, df: pd.DataFrame, title: str, **kwargs) -> Dict[str, Any]:
        """Create competitive positioning chart"""
        color_by = kwargs.get('color_by', 'network_status')
        
        color_map = {
            'In-Network': self.brand_colors['primary_green'],
            'Out-of-Network': self.brand_colors['error']
        }
        
        fig = px.scatter(
            df,
            x='cost_per_utilizer',
            y='quality_score',
            size='utilizers',
            color=color_by,
            hover_data=['name', 'market_position_percentile', 'clinical_group'],
            title=title or "Competitive Market Positioning",
            labels={
                'cost_per_utilizer': 'Cost per Utilizer ($)',
                'quality_score': 'Quality Score',
                color_by: color_by.replace('_', ' ').title()
            },
            color_discrete_map=color_map
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title_font_color=self.brand_colors['dark_blue'],
            height=500
        )
        
        return {
            "chart_type": "competitive_positioning",
            "figure": fig.to_json(),
            "insights": self._generate_competitive_insights(df),
            "data_points": len(df)
        }
    
    def _create_geographic_heatmap(self, df: pd.DataFrame, title: str, **kwargs) -> Dict[str, Any]:
        """Create geographic heatmap by state"""
        metric = kwargs.get('metric', 'total_opportunity')
        
        # Aggregate data by state
        state_data = self._aggregate_by_geography(df, 'state')
        
        # Create choropleth map
        fig = go.Figure(data=go.Choropleth(
            locations=list(state_data.keys()),
            z=[data[metric] for data in state_data.values()],
            locationmode='USA-states',
            colorscale=[
                [0, self.brand_colors['light_gray']],
                [0.3, self.brand_colors['accent_blue']],
                [0.6, self.brand_colors['primary_blue']],
                [1.0, self.brand_colors['dark_blue']]
            ],
            colorbar_title=metric.replace('_', ' ').title(),
            showscale=True
        ))
        
        fig.update_layout(
            title_text=title or f'{metric.replace("_", " ").title()} by State',
            title_font_color=self.brand_colors['dark_blue'],
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'
            ),
            height=500
        )
        
        return {
            "chart_type": "geographic_heatmap",
            "figure": fig.to_json(),
            "insights": self._generate_geographic_insights(state_data),
            "data_points": len(state_data)
        }
    
    def _create_performance_trends(self, df: pd.DataFrame, title: str, **kwargs) -> Dict[str, Any]:
        """Create performance trends over time or by category"""
        group_by = kwargs.get('group_by', 'clinical_group')
        
        # Aggregate performance metrics by group
        performance_data = df.groupby(group_by).agg({
            'quality_score': 'mean',
            'cost_per_utilizer': 'mean',
            'utilizers': 'sum',
            'termination_value': 'sum'
        }).reset_index()
        
        # Create dual-axis chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(
                x=performance_data[group_by],
                y=performance_data['quality_score'],
                name='Average Quality Score',
                marker_color=self.brand_colors['primary_blue']
            ),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(
                x=performance_data[group_by],
                y=performance_data['cost_per_utilizer'],
                mode='lines+markers',
                name='Average Cost per Utilizer',
                line=dict(color=self.brand_colors['primary_green'], width=3)
            ),
            secondary_y=True,
        )
        
        fig.update_xaxes(title_text=group_by.replace('_', ' ').title())
        fig.update_yaxes(title_text="Quality Score", secondary_y=False)
        fig.update_yaxes(title_text="Cost per Utilizer ($)", secondary_y=True)
        
        fig.update_layout(
            title_text=title or f"Performance Trends by {group_by.replace('_', ' ').title()}",
            title_font_color=self.brand_colors['dark_blue'],
            height=500
        )
        
        return {
            "chart_type": "performance_trends",
            "figure": fig.to_json(),
            "insights": self._generate_trend_insights(performance_data, group_by),
            "data_points": len(performance_data)
        }
    
    def _create_clinical_group_chart(self, df: pd.DataFrame, title: str, **kwargs) -> Dict[str, Any]:
        """Create clinical group analysis chart"""
        chart_style = kwargs.get('style', 'bar')
        
        clinical_analysis = df.groupby('clinical_group').agg({
            'quality_score': 'mean',
            'cost_per_utilizer': 'mean',
            'utilizers': 'sum',
            'termination_value': 'sum'
        }).reset_index()
        
        if chart_style == 'bar':
            fig = px.bar(
                clinical_analysis,
                x='clinical_group',
                y='quality_score',
                title=title or "Quality Score by Clinical Group",
                color='quality_score',
                color_continuous_scale=[
                    [0, self.brand_colors['error']],
                    [0.5, self.brand_colors['warning']],
                    [1, self.brand_colors['success']]
                ]
            )
        else:
            fig = px.scatter(
                clinical_analysis,
                x='cost_per_utilizer',
                y='quality_score',
                size='utilizers',
                hover_data=['clinical_group', 'termination_value'],
                title=title or "Clinical Group Performance Analysis"
            )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title_font_color=self.brand_colors['dark_blue'],
            height=500,
            xaxis_tickangle=-45
        )
        
        return {
            "chart_type": "clinical_group_analysis",
            "figure": fig.to_json(),
            "insights": self._generate_clinical_group_insights(clinical_analysis),
            "data_points": len(clinical_analysis)
        }
    
    def _create_network_adequacy_chart(self, df: pd.DataFrame, title: str, **kwargs) -> Dict[str, Any]:
        """Create network adequacy visualization"""
        adequacy_data = df.groupby(['adequacy_risk', 'network_status']).size().reset_index(name='count')
        
        fig = px.sunburst(
            adequacy_data,
            path=['adequacy_risk', 'network_status'],
            values='count',
            title=title or "Network Adequacy Risk Distribution",
            color='adequacy_risk',
            color_discrete_map={
                'High': self.brand_colors['error'],
                'Medium': self.brand_colors['warning'],
                'Low': self.brand_colors['success']
            }
        )
        
        fig.update_layout(
            title_font_color=self.brand_colors['dark_blue'],
            height=500
        )
        
        return {
            "chart_type": "network_adequacy",
            "figure": fig.to_json(),
            "insights": self._generate_adequacy_insights(adequacy_data),
            "data_points": len(adequacy_data)
        }
    
    def _create_financial_impact_chart(self, df: pd.DataFrame, title: str, **kwargs) -> Dict[str, Any]:
        """Create financial impact waterfall chart"""
        # Calculate financial impacts by quadrant
        financial_data = df.groupby('quadrant')['termination_value'].sum().reset_index()
        
        fig = go.Figure(go.Waterfall(
            name="Financial Impact",
            orientation="v",
            measure=["relative"] * len(financial_data),
            x=financial_data['quadrant'],
            y=financial_data['termination_value'],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title=title or "Financial Impact by Provider Quadrant",
            title_font_color=self.brand_colors['dark_blue'],
            showlegend=False,
            height=500
        )
        
        return {
            "chart_type": "financial_impact",
            "figure": fig.to_json(),
            "insights": self._generate_financial_insights(financial_data),
            "data_points": len(financial_data)
        }
    
    def _create_market_distribution_chart(self, df: pd.DataFrame, title: str, **kwargs) -> Dict[str, Any]:
        """Create market position distribution (bell curve)"""
        # Create bell curve data
        x_values = np.linspace(0, 100, 100)
        mean_position = 50
        std_dev = 20
        y_values = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_values - mean_position) / std_dev) ** 2)
        
        fig = go.Figure()
        
        # Add bell curve
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines',
            fill='tonexty',
            name='Market Distribution',
            line=dict(color=self.brand_colors['primary_blue'], width=2),
            fillcolor=f"rgba(0, 180, 216, 0.3)"
        ))
        
        # Add provider positions
        for _, provider in df.iterrows():
            fig.add_trace(go.Scatter(
                x=[provider['market_position_percentile']],
                y=[0.002],
                mode='markers',
                marker=dict(
                    size=8,
                    color=self.brand_colors['primary_green'] if provider['network_status'] == 'In-Network' else self.brand_colors['error'],
                    symbol='diamond'
                ),
                name=provider['name'],
                showlegend=False
            ))
        
        fig.update_layout(
            title=title or "Provider Market Position Distribution",
            xaxis_title="Market Position Percentile",
            yaxis_title="Distribution Density",
            title_font_color=self.brand_colors['dark_blue'],
            height=400
        )
        
        return {
            "chart_type": "market_position_distribution",
            "figure": fig.to_json(),
            "insights": self._generate_distribution_insights(df),
            "data_points": len(df)
        }
    
    def _get_quadrant_category(self, quality: float, cost: float, quality_threshold: float, cost_threshold: float) -> str:
        """Categorize provider into quadrant"""
        if quality >= quality_threshold and cost <= cost_threshold:
            return "Preferred Partners"
        elif quality >= quality_threshold and cost > cost_threshold:
            return "Strategic Opportunities"
        elif quality < quality_threshold and cost <= cost_threshold:
            return "Performance Focus"
        else:
            return "Optimization Candidates"
    
    def _aggregate_by_geography(self, df: pd.DataFrame, geo_level: str) -> Dict[str, Dict]:
        """Aggregate data by geographic level"""
        geographic_data = {}
        
        for _, provider in df.iterrows():
            if geo_level == 'state':
                geo_units = provider['operating_states']
            else:
                geo_units = [provider['primary_cbsa']]
            
            for geo_unit in geo_units:
                if geo_unit not in geographic_data:
                    geographic_data[geo_unit] = {
                        'total_opportunity': 0,
                        'provider_count': 0,
                        'avg_quality': 0,
                        'total_utilizers': 0
                    }
                
                geographic_data[geo_unit]['total_opportunity'] += provider['termination_value']
                geographic_data[geo_unit]['provider_count'] += 1
                geographic_data[geo_unit]['avg_quality'] += provider['quality_score']
                geographic_data[geo_unit]['total_utilizers'] += provider['utilizers']
        
        # Calculate averages
        for geo_unit in geographic_data:
            if geographic_data[geo_unit]['provider_count'] > 0:
                geographic_data[geo_unit]['avg_quality'] /= geographic_data[geo_unit]['provider_count']
        
        return geographic_data
    
    def _generate_quadrant_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate insights for quadrant analysis"""
        insights = []
        quadrant_counts = df['quadrant'].value_counts()
        
        if 'Optimization Candidates' in quadrant_counts:
            insights.append(f"{quadrant_counts['Optimization Candidates']} providers identified for optimization")
        
        if 'Preferred Partners' in quadrant_counts:
            insights.append(f"{quadrant_counts['Preferred Partners']} high-performing providers to retain")
        
        return insights
    
    def _generate_competitive_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate competitive analysis insights"""
        insights = []
        
        out_network_high_quality = len(df[(df['network_status'] == 'Out-of-Network') & (df['quality_score'] >= 4.0)])
        if out_network_high_quality > 0:
            insights.append(f"{out_network_high_quality} high-quality out-of-network providers available")
        
        return insights
    
    def _generate_geographic_insights(self, geographic_data: Dict) -> List[str]:
        """Generate geographic analysis insights"""
        insights = []
        
        top_opportunity = max(geographic_data.items(), key=lambda x: x[1]['total_opportunity'])
        insights.append(f"{top_opportunity[0]} has highest optimization opportunity: ${top_opportunity[1]['total_opportunity']:,.0f}")
        
        return insights
    
    def _generate_trend_insights(self, performance_data: pd.DataFrame, group_by: str) -> List[str]:
        """Generate trend analysis insights"""
        insights = []
        
        best_quality = performance_data.loc[performance_data['quality_score'].idxmax()]
        insights.append(f"{best_quality[group_by]} has highest average quality: {best_quality['quality_score']:.1f}")
        
        return insights
    
    def _generate_clinical_group_insights(self, clinical_analysis: pd.DataFrame) -> List[str]:
        """Generate clinical group insights"""
        insights = []
        
        top_group = clinical_analysis.loc[clinical_analysis['quality_score'].idxmax()]
        insights.append(f"{top_group['clinical_group']} shows highest quality performance")
        
        return insights
    
    def _generate_adequacy_insights(self, adequacy_data: pd.DataFrame) -> List[str]:
        """Generate network adequacy insights"""
        insights = []
        
        high_risk_count = adequacy_data[adequacy_data['adequacy_risk'] == 'High']['count'].sum()
        if high_risk_count > 0:
            insights.append(f"{high_risk_count} high-risk network adequacy areas identified")
        
        return insights
    
    def _generate_financial_insights(self, financial_data: pd.DataFrame) -> List[str]:
        """Generate financial impact insights"""
        insights = []
        
        total_opportunity = financial_data['termination_value'].sum()
        insights.append(f"Total financial opportunity: ${total_opportunity/1000000:.1f}M")
        
        return insights
    
    def _generate_distribution_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate market distribution insights"""
        insights = []
        
        top_quartile = len(df[df['market_position_percentile'] >= 75])
        insights.append(f"{top_quartile} providers in top performance quartile")
        
        return insights

