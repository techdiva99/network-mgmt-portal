# tools/competitive_analysis_tool.py
"""
Competitive analysis tool for market intelligence and positioning
"""

from typing import Dict, List, Any
import pandas as pd
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

class CompetitiveAnalysisTool(BaseTool):
    name: str = "Competitive Analysis Tool"
    description: str = "Analyze competitive positioning and market intelligence for provider networks"
    
    def _run(self, provider_data: List[Dict], target_provider: str = None) -> Dict[str, Any]:
        """Perform comprehensive competitive analysis"""
        df = pd.DataFrame(provider_data)
        
        if target_provider:
            return self._analyze_specific_provider(df, target_provider)
        else:
            return self._analyze_market_position(df)
    
    def _analyze_market_position(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze overall market positioning"""
        # Market position analysis
        top_performers = df[df['market_position_percentile'] >= 75]
        poor_performers = df[df['market_position_percentile'] <= 25]
        
        # Market distribution analysis
        market_stats = {
            "total_providers": len(df),
            "top_quartile_count": len(top_performers),
            "bottom_quartile_count": len(poor_performers),
            "median_quality": df['quality_score'].median(),
            "median_cost": df['cost_per_utilizer'].median(),
            "avg_market_position": df['market_position_percentile'].mean()
        }
        
        # Competitive insights by clinical group
        clinical_group_analysis = self._analyze_by_clinical_group(df)
        
        # Network vs out-of-network comparison
        network_comparison = self._compare_network_status(df)
        
        # Geographic market analysis
        geographic_analysis = self._analyze_geographic_competition(df)
        
        return {
            "market_statistics": market_stats,
            "market_leaders": top_performers[['name', 'market_position_percentile', 'quality_score', 'cost_per_utilizer', 'clinical_group']].head(10).to_dict('records'),
            "improvement_targets": poor_performers[['name', 'market_position_percentile', 'quality_score', 'cost_per_utilizer', 'clinical_group']].head(10).to_dict('records'),
            "clinical_group_analysis": clinical_group_analysis,
            "network_comparison": network_comparison,
            "geographic_analysis": geographic_analysis,
            "competitive_threats": self._identify_competitive_threats(df),
            "market_opportunities": self._identify_market_opportunities(df)
        }
    
    def _analyze_specific_provider(self, df: pd.DataFrame, provider_name: str) -> Dict[str, Any]:
        """Analyze specific provider vs competitors"""
        target_data = df[df['name'] == provider_name]
        if target_data.empty:
            return {"error": f"Provider {provider_name} not found"}
        
        target = target_data.iloc[0]
        
        # Get direct competitors (same clinical group and geographic overlap)
        same_clinical_group = df[df['clinical_group'] == target['clinical_group']]
        
        # Find geographic competitors
        geographic_competitors = self._find_geographic_competitors(df, target)
        
        # Performance comparison
        performance_comparison = self._compare_provider_performance(target, same_clinical_group)
        
        # Market share analysis
        market_share_analysis = self._analyze_market_share(target, df)
        
        return {
            "target_provider": {
                "name": target['name'],
                "quality_score": target['quality_score'],
                "cost_per_utilizer": target['cost_per_utilizer'],
                "market_position": target['market_position_percentile'],
                "clinical_group": target['clinical_group'],
                "network_status": target['network_status']
            },
            "clinical_group_competitors": same_clinical_group[same_clinical_group['name'] != provider_name].head(10).to_dict('records'),
            "geographic_competitors": geographic_competitors,
            "performance_comparison": performance_comparison,
            "market_share_analysis": market_share_analysis,
            "competitive_advantages": self._identify_competitive_advantages(target, df),
            "competitive_threats": self._identify_provider_threats(target, df),
            "strategic_recommendations": self._generate_provider_recommendations(target, df)
        }
    
    def _analyze_by_clinical_group(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze competition by clinical group"""
        clinical_group_stats = {}
        
        for group in df['clinical_group'].unique():
            group_data = df[df['clinical_group'] == group]
            
            clinical_group_stats[group] = {
                "provider_count": len(group_data),
                "avg_quality": group_data['quality_score'].mean(),
                "avg_cost": group_data['cost_per_utilizer'].mean(),
                "avg_market_position": group_data['market_position_percentile'].mean(),
                "in_network_count": len(group_data[group_data['network_status'] == 'In-Network']),
                "out_network_count": len(group_data[group_data['network_status'] == 'Out-of-Network']),
                "top_performer": group_data.loc[group_data['market_position_percentile'].idxmax()]['name'] if not group_data.empty else None,
                "network_adequacy_risk": len(group_data[group_data['adequacy_risk'] == 'High'])
            }
        
        return clinical_group_stats
    
    def _compare_network_status(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compare in-network vs out-of-network providers"""
        in_network = df[df['network_status'] == 'In-Network']
        out_network = df[df['network_status'] == 'Out-of-Network']
        
        return {
            "in_network_stats": {
                "count": len(in_network),
                "avg_quality": in_network['quality_score'].mean(),
                "avg_cost": in_network['cost_per_utilizer'].mean(),
                "avg_market_position": in_network['market_position_percentile'].mean()
            },
            "out_network_stats": {
                "count": len(out_network),
                "avg_quality": out_network['quality_score'].mean(),
                "avg_cost": out_network['cost_per_utilizer'].mean(),
                "avg_market_position": out_network['market_position_percentile'].mean()
            },
            "quality_gap": out_network['quality_score'].mean() - in_network['quality_score'].mean(),
            "cost_gap": in_network['cost_per_utilizer'].mean() - out_network['cost_per_utilizer'].mean(),
            "high_quality_out_network": len(out_network[out_network['quality_score'] >= 4.0])
        }
    
    def _analyze_geographic_competition(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze competition by geographic market"""
        cbsa_analysis = {}
        
        for cbsa in df['primary_cbsa'].unique():
            cbsa_data = df[df['primary_cbsa'] == cbsa]
            
            cbsa_analysis[cbsa] = {
                "provider_count": len(cbsa_data),
                "avg_quality": cbsa_data['quality_score'].mean(),
                "avg_cost": cbsa_data['cost_per_utilizer'].mean(),
                "competition_intensity": len(cbsa_data) / df['primary_cbsa'].value_counts().max(),
                "market_leader": cbsa_data.loc[cbsa_data['market_position_percentile'].idxmax()]['name'] if not cbsa_data.empty else None,
                "network_penetration": len(cbsa_data[cbsa_data['network_status'] == 'In-Network']) / len(cbsa_data) if len(cbsa_data) > 0 else 0
            }
        
        return cbsa_analysis
    
    def _find_geographic_competitors(self, df: pd.DataFrame, target: pd.Series) -> List[Dict]:
        """Find geographic competitors for a specific provider"""
        # Providers in same CBSA
        same_cbsa = df[df['primary_cbsa'] == target['primary_cbsa']]
        
        # Providers in overlapping states
        overlapping_states = df[df['operating_states'].apply(
            lambda x: bool(set(x) & set(target['operating_states']))
        )]
        
        geographic_competitors = pd.concat([same_cbsa, overlapping_states]).drop_duplicates()
        geographic_competitors = geographic_competitors[geographic_competitors['name'] != target['name']]
        
        return geographic_competitors.head(10).to_dict('records')
    
    def _compare_provider_performance(self, target: pd.Series, competitors: pd.DataFrame) -> Dict[str, Any]:
        """Compare target provider performance against competitors"""
        if competitors.empty:
            return {"error": "No competitors found"}
        
        return {
            "quality_rank": (competitors['quality_score'] < target['quality_score']).sum() + 1,
            "cost_rank": (competitors['cost_per_utilizer'] > target['cost_per_utilizer']).sum() + 1,
            "market_position_rank": (competitors['market_position_percentile'] < target['market_position_percentile']).sum() + 1,
            "total_competitors": len(competitors),
            "quality_percentile": ((competitors['quality_score'] < target['quality_score']).sum() / len(competitors)) * 100,
            "cost_percentile": ((competitors['cost_per_utilizer'] > target['cost_per_utilizer']).sum() / len(competitors)) * 100,
            "better_quality_competitors": len(competitors[competitors['quality_score'] > target['quality_score']]),
            "lower_cost_competitors": len(competitors[competitors['cost_per_utilizer'] < target['cost_per_utilizer']])
        }
    
    def _analyze_market_share(self, target: pd.Series, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze market share for target provider"""
        # Market share by volume (utilizers)
        total_utilizers_cbsa = df[df['primary_cbsa'] == target['primary_cbsa']]['utilizers'].sum()
        provider_market_share = target['utilizers'] / total_utilizers_cbsa if total_utilizers_cbsa > 0 else 0
        
        # Market share by clinical group
        clinical_group_utilizers = df[df['clinical_group'] == target['clinical_group']]['utilizers'].sum()
        clinical_group_share = target['utilizers'] / clinical_group_utilizers if clinical_group_utilizers > 0 else 0
        
        return {
            "cbsa_market_share": provider_market_share * 100,
            "clinical_group_share": clinical_group_share * 100,
            "utilizer_volume": target['utilizers'],
            "relative_size": "Large" if target['utilizers'] > 3000 else "Medium" if target['utilizers'] > 1000 else "Small"
        }
    
    def _identify_competitive_threats(self, df: pd.DataFrame) -> List[Dict]:
        """Identify competitive threats in the market"""
        threats = []
        
        # High-performing out-of-network providers
        high_quality_out_network = df[
            (df['network_status'] == 'Out-of-Network') & 
            (df['quality_score'] >= 4.0) & 
            (df['cost_per_utilizer'] <= 600)
        ]
        
        for _, provider in high_quality_out_network.head(5).iterrows():
            threats.append({
                "provider_name": provider['name'],
                "threat_type": "High-Quality Out-of-Network",
                "threat_level": "High",
                "description": f"Excellent quality ({provider['quality_score']:.1f}) and competitive cost (${provider['cost_per_utilizer']:.0f})",
                "clinical_group": provider['clinical_group'],
                "market_position": provider['market_position_percentile']
            })
        
        return threats
    
    def _identify_market_opportunities(self, df: pd.DataFrame) -> List[Dict]:
        """Identify market opportunities"""
        opportunities = []
        
        # Underperforming in-network providers that could be replaced
        underperformers = df[
            (df['network_status'] == 'In-Network') & 
            (df['quality_score'] < 3.5) & 
            (df['cost_per_utilizer'] > 700)
        ]
        
        for _, provider in underperformers.head(5).iterrows():
            opportunities.append({
                "opportunity_type": "Provider Optimization",
                "description": f"Replace {provider['name']} with higher-performing alternative",
                "financial_impact": provider['termination_value'],
                "clinical_group": provider['clinical_group'],
                "current_performance": f"Quality: {provider['quality_score']:.1f}, Cost: ${provider['cost_per_utilizer']:.0f}"
            })
        
        return opportunities
    
    def _identify_competitive_advantages(self, target: pd.Series, df: pd.DataFrame) -> List[str]:
        """Identify competitive advantages for target provider"""
        advantages = []
        
        # Compare against clinical group average
        clinical_group_data = df[df['clinical_group'] == target['clinical_group']]
        avg_quality = clinical_group_data['quality_score'].mean()
        avg_cost = clinical_group_data['cost_per_utilizer'].mean()
        
        if target['quality_score'] > avg_quality:
            advantages.append(f"Above-average quality score ({target['quality_score']:.1f} vs {avg_quality:.1f} average)")
        
        if target['cost_per_utilizer'] < avg_cost:
            advantages.append(f"Below-average cost per utilizer (${target['cost_per_utilizer']:.0f} vs ${avg_cost:.0f} average)")
        
        if target['market_position_percentile'] > 75:
            advantages.append(f"Strong market position ({target['market_position_percentile']:.0f}th percentile)")
        
        if target['adequacy_risk'] == 'Low':
            advantages.append("Low network adequacy risk")
        
        return advantages
    
    def _identify_provider_threats(self, target: pd.Series, df: pd.DataFrame) -> List[str]:
        """Identify threats for specific provider"""
        threats = []
        
        # Find better-performing competitors in same clinical group
        competitors = df[
            (df['clinical_group'] == target['clinical_group']) & 
            (df['name'] != target['name'])
        ]
        
        better_competitors = competitors[
            (competitors['quality_score'] > target['quality_score']) & 
            (competitors['cost_per_utilizer'] < target['cost_per_utilizer'])
        ]
        
        if len(better_competitors) > 0:
            threats.append(f"{len(better_competitors)} competitors with better quality and lower cost")
        
        if target['market_position_percentile'] < 25:
            threats.append("Poor market position (bottom quartile)")
        
        if target['adequacy_risk'] == 'High':
            threats.append("High network adequacy risk")
        
        return threats
    
    def _generate_provider_recommendations(self, target: pd.Series, df: pd.DataFrame) -> List[str]:
        """Generate strategic recommendations for provider"""
        recommendations = []
        
        if target['quality_score'] < 4.0:
            recommendations.append("Implement quality improvement initiatives")
        
        if target['cost_per_utilizer'] > 700:
            recommendations.append("Negotiate cost reduction strategies")
        
        if target['market_position_percentile'] < 50:
            recommendations.append("Develop competitive positioning strategy")
        
        if target['network_status'] == 'Out-of-Network' and target['quality_score'] >= 4.0:
            recommendations.append("Consider for network inclusion")
        
        if target['network_status'] == 'In-Network' and target['quality_score'] < 3.5:
            recommendations.append("Evaluate for potential network removal")
        
        return recommendations

