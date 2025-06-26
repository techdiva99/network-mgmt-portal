# tools/quadrant_analysis_tool.py
"""
Quadrant analysis tool for provider performance categorization
"""

from typing import Dict, List, Any
import pandas as pd
from utils.metrics_calculator import (
    add_quadrant_analysis, 
    identify_removal_candidates, 
    identify_addition_candidates,
    calculate_financial_impact
)

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

class QuadrantAnalysisTool(BaseTool):
    name: str = "Quadrant Analysis Tool"
    description: str = "Analyze providers using quality-cost quadrant methodology for optimization opportunities"
    
    def _run(self, provider_data: List[Dict], quality_threshold: float = 4.0, cost_threshold: float = 600) -> Dict[str, Any]:
        """Perform comprehensive quadrant analysis matching original methodology"""
        df = pd.DataFrame(provider_data)
        
        # Add quadrant categories
        df = add_quadrant_analysis(df)
        
        # Identify optimization opportunities
        removal_candidates = identify_removal_candidates(df)
        addition_candidates = identify_addition_candidates(df)
        
        # Calculate financial impact
        financial_impact = calculate_financial_impact(removal_candidates, addition_candidates)
        
        # Generate quadrant insights
        quadrant_insights = self._generate_quadrant_insights(df)
        
        # Priority recommendations
        priority_recommendations = self._generate_priority_recommendations(removal_candidates, addition_candidates)
        
        return {
            "quadrant_summary": df['quadrant'].value_counts().to_dict(),
            "removal_candidates": removal_candidates.head(10).to_dict('records'),
            "addition_candidates": addition_candidates.head(10).to_dict('records'),
            "financial_impact": financial_impact,
            "quadrant_insights": quadrant_insights,
            "priority_recommendations": priority_recommendations,
            "processed_data": df.to_dict('records'),
            "analysis_metadata": {
                "quality_threshold": quality_threshold,
                "cost_threshold": cost_threshold,
                "total_providers_analyzed": len(df),
                "optimization_opportunities": len(removal_candidates) + len(addition_candidates)
            }
        }
    
    def _generate_quadrant_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate insights for each quadrant"""
        insights = {}
        
        for quadrant in df['quadrant'].unique():
            quadrant_data = df[df['quadrant'] == quadrant]
            
            insights[quadrant] = {
                "count": len(quadrant_data),
                "avg_quality": quadrant_data['quality_score'].mean(),
                "avg_cost": quadrant_data['cost_per_utilizer'].mean(),
                "total_utilizers": quadrant_data['utilizers'].sum(),
                "avg_market_position": quadrant_data['market_position_percentile'].mean(),
                "high_risk_count": len(quadrant_data[quadrant_data['adequacy_risk'] == 'High']),
                "recommendations": self._get_quadrant_recommendations(quadrant)
            }
        
        return insights
    
    def _get_quadrant_recommendations(self, quadrant: str) -> List[str]:
        """Get specific recommendations for each quadrant"""
        recommendations = {
            "Preferred Partners": [
                "Retain and expand partnerships",
                "Negotiate favorable contract renewals",
                "Use as benchmark for other providers",
                "Consider volume bonuses and incentives"
            ],
            "Strategic Opportunities": [
                "Negotiate cost reductions while maintaining quality",
                "Explore value-based payment models",
                "Consider selective contracting strategies",
                "Monitor for potential quality improvements"
            ],
            "Performance Focus": [
                "Implement quality improvement programs",
                "Provide additional training and support",
                "Set quality benchmarks and monitoring",
                "Consider performance-based incentives"
            ],
            "Optimization Candidates": [
                "Initiate performance improvement plans",
                "Consider contract termination if no improvement",
                "Identify alternative providers in market",
                "Ensure network adequacy before removal"
            ]
        }
        
        return recommendations.get(quadrant, ["Monitor performance"])
    
    def _generate_priority_recommendations(self, removal_candidates: pd.DataFrame, addition_candidates: pd.DataFrame) -> Dict[str, Any]:
        """Generate prioritized recommendations with implementation timelines"""
        
        # Immediate actions (30 days)
        immediate_actions = []
        if not removal_candidates.empty:
            top_removal = removal_candidates.iloc[0]
            immediate_actions.append({
                "action": "Begin contract termination process",
                "target": top_removal['name'],
                "rationale": f"Poor performance (Quality: {top_removal['quality_score']:.1f}, Cost: ${top_removal['cost_per_utilizer']:.0f})",
                "financial_impact": top_removal['termination_value']
            })
        
        # Short-term actions (90 days)
        short_term_actions = []
        if not addition_candidates.empty:
            top_addition = addition_candidates.iloc[0]
            short_term_actions.append({
                "action": "Initiate recruitment negotiations",
                "target": top_addition['name'],
                "rationale": f"High performance (Quality: {top_addition['quality_score']:.1f}, Cost: ${top_addition['cost_per_utilizer']:.0f})",
                "expected_benefit": "Quality improvement and cost efficiency"
            })
        
        # Medium-term actions (6 months)
        medium_term_actions = [
            {
                "action": "Complete network transition",
                "description": "Finalize all provider changes and measure outcomes",
                "success_metrics": ["Cost per utilizer reduction", "Quality score improvement", "Member satisfaction"]
            }
        ]
        
        return {
            "immediate_30_days": immediate_actions,
            "short_term_90_days": short_term_actions,
            "medium_term_6_months": medium_term_actions,
            "total_financial_opportunity": removal_candidates['termination_value'].sum() if not removal_candidates.empty else 0
        }

