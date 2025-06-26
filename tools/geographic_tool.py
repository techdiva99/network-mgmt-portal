# tools/geographic_tool.py
"""
Geographic optimization tool for network analysis by location
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

class GeographicOptimizationTool(BaseTool):
    name: str = "Geographic Optimization Tool"
    description: str = "Analyze provider network optimization opportunities by geographic location"
    
    def _run(self, provider_data: List[Dict], analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Perform geographic analysis based on type requested"""
        df = pd.DataFrame(provider_data)
        
        if analysis_type == "state":
            return self._analyze_by_state(df)
        elif analysis_type == "cbsa":
            return self._analyze_by_cbsa(df)
        elif analysis_type == "network_adequacy":
            return self._analyze_network_adequacy(df)
        else:
            return self._comprehensive_geographic_analysis(df)
    
    def _comprehensive_geographic_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform comprehensive geographic analysis"""
        return {
            "state_analysis": self._analyze_by_state(df),
            "cbsa_analysis": self._analyze_by_cbsa(df),
            "network_adequacy": self._analyze_network_adequacy(df),
            "geographic_gaps": self._identify_geographic_gaps(df),
            "expansion_opportunities": self._identify_expansion_opportunities(df),
            "consolidation_opportunities": self._identify_consolidation_opportunities(df)
        }
    
    def _analyze_by_state(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze provider network by state"""
        state_analysis = {}
        
        # Create state-level data
        for _, provider in df.iterrows():
            for state in provider['operating_states']:
                if state not in state_analysis:
                    state_analysis[state] = {
                        'providers': [],
                        'total_opportunity': 0,
                        'total_utilizers': 0,
                        'quality_scores': [],
                        'costs': [],
                        'clinical_groups': set(),
                        'in_network_count': 0,
                        'out_network_count': 0,
                        'high_risk_count': 0
                    }
                
                state_analysis[state]['providers'].append(provider['name'])
                state_analysis[state]['total_opportunity'] += provider['termination_value']
                state_analysis[state]['total_utilizers'] += provider['utilizers']
                state_analysis[state]['quality_scores'].append(provider['quality_score'])
                state_analysis[state]['costs'].append(provider['cost_per_utilizer'])
                state_analysis[state]['clinical_groups'].add(provider['clinical_group'])
                
                if provider['network_status'] == 'In-Network':
                    state_analysis[state]['in_network_count'] += 1
                else:
                    state_analysis[state]['out_network_count'] += 1
                
                if provider['adequacy_risk'] == 'High':
                    state_analysis[state]['high_risk_count'] += 1
        
        # Calculate derived metrics
        for state in state_analysis:
            data = state_analysis[state]
            data['provider_count'] = len(data['providers'])
            data['avg_quality'] = np.mean(data['quality_scores'])
            data['avg_cost'] = np.mean(data['costs'])
            data['clinical_group_count'] = len(data['clinical_groups'])
            data['network_penetration'] = data['in_network_count'] / data['provider_count'] if data['provider_count'] > 0 else 0
            data['adequacy_risk_ratio'] = data['high_risk_count'] / data['provider_count'] if data['provider_count'] > 0 else 0
            
            # Generate recommendations
            data['recommendations'] = self._generate_state_recommendations(state, data)
            
            # Clean up lists for JSON serialization
            data['clinical_groups'] = list(data['clinical_groups'])
            del data['quality_scores']
            del data['costs']
        
        # Rank states by opportunity
        state_rankings = sorted(state_analysis.items(), 
                               key=lambda x: x[1]['total_opportunity'], 
                               reverse=True)
        
        return {
            "state_details": state_analysis,
            "state_rankings": [(state, data['total_opportunity']) for state, data in state_rankings],
            "total_states": len(state_analysis),
            "summary_stats": self._calculate_state_summary_stats(state_analysis)
        }
    
    def _analyze_by_cbsa(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze provider network by CBSA (metro area)"""
        cbsa_analysis = {}
        
        for _, provider in df.iterrows():
            cbsa = provider['primary_cbsa']
            
            if cbsa not in cbsa_analysis:
                cbsa_analysis[cbsa] = {
                    'providers': [],
                    'total_opportunity': 0,
                    'total_utilizers': 0,
                    'quality_scores': [],
                    'costs': [],
                    'clinical_groups': set(),
                    'in_network_count': 0,
                    'out_network_count': 0,
                    'market_positions': []
                }
            
            cbsa_analysis[cbsa]['providers'].append(provider['name'])
            cbsa_analysis[cbsa]['total_opportunity'] += provider['termination_value']
            cbsa_analysis[cbsa]['total_utilizers'] += provider['utilizers']
            cbsa_analysis[cbsa]['quality_scores'].append(provider['quality_score'])
            cbsa_analysis[cbsa]['costs'].append(provider['cost_per_utilizer'])
            cbsa_analysis[cbsa]['clinical_groups'].add(provider['clinical_group'])
            cbsa_analysis[cbsa]['market_positions'].append(provider['market_position_percentile'])
            
            if provider['network_status'] == 'In-Network':
                cbsa_analysis[cbsa]['in_network_count'] += 1
            else:
                cbsa_analysis[cbsa]['out_network_count'] += 1
        
        # Calculate derived metrics
        for cbsa in cbsa_analysis:
            data = cbsa_analysis[cbsa]
            data['provider_count'] = len(data['providers'])
            data['avg_quality'] = np.mean(data['quality_scores'])
            data['avg_cost'] = np.mean(data['costs'])
            data['avg_market_position'] = np.mean(data['market_positions'])
            data['clinical_group_count'] = len(data['clinical_groups'])
            data['network_penetration'] = data['in_network_count'] / data['provider_count'] if data['provider_count'] > 0 else 0
            data['competition_intensity'] = data['provider_count'] / df['primary_cbsa'].value_counts().max()
            
            # Generate recommendations
            data['recommendations'] = self._generate_cbsa_recommendations(cbsa, data)
            
            # Clean up for JSON serialization
            data['clinical_groups'] = list(data['clinical_groups'])
            del data['quality_scores']
            del data['costs']
            del data['market_positions']
        
        return {
            "cbsa_details": cbsa_analysis,
            "total_cbsas": len(cbsa_analysis),
            "most_competitive": max(cbsa_analysis.items(), key=lambda x: x[1]['competition_intensity']),
            "highest_opportunity": max(cbsa_analysis.items(), key=lambda x: x[1]['total_opportunity'])
        }
    
    def _analyze_network_adequacy(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze network adequacy by geography and clinical group"""
        adequacy_analysis = {}
        
        # Analyze by state and clinical group combination
        for _, provider in df.iterrows():
            for state in provider['operating_states']:
                clinical_group = provider['clinical_group']
                key = f"{state}_{clinical_group}"
                
                if key not in adequacy_analysis:
                    adequacy_analysis[key] = {
                        'state': state,
                        'clinical_group': clinical_group,
                        'in_network_providers': 0,
                        'total_providers': 0,
                        'high_risk_providers': 0,
                        'total_utilizers': 0,
                        'provider_names': []
                    }
                
                adequacy_analysis[key]['total_providers'] += 1
                adequacy_analysis[key]['total_utilizers'] += provider['utilizers']
                adequacy_analysis[key]['provider_names'].append(provider['name'])
                
                if provider['network_status'] == 'In-Network':
                    adequacy_analysis[key]['in_network_providers'] += 1
                
                if provider['adequacy_risk'] == 'High':
                    adequacy_analysis[key]['high_risk_providers'] += 1
        
        # Calculate adequacy metrics
        for key in adequacy_analysis:
            data = adequacy_analysis[key]
            data['adequacy_ratio'] = data['in_network_providers'] / data['total_providers'] if data['total_providers'] > 0 else 0
            data['risk_level'] = self._calculate_adequacy_risk_level(data)
            data['recommendations'] = self._generate_adequacy_recommendations(data)
        
        # Identify critical gaps
        critical_gaps = [
            data for data in adequacy_analysis.values()
            if data['adequacy_ratio'] < 0.6 or data['in_network_providers'] < 2
        ]
        
        return {
            "adequacy_details": adequacy_analysis,
            "critical_gaps": critical_gaps,
            "total_coverage_areas": len(adequacy_analysis),
            "areas_at_risk": len(critical_gaps),
            "overall_adequacy_score": self._calculate_overall_adequacy_score(adequacy_analysis)
        }
    
    def _identify_geographic_gaps(self, df: pd.DataFrame) -> List[Dict]:
        """Identify geographic gaps in network coverage"""
        gaps = []
        
        # Analyze clinical group coverage by state
        coverage_matrix = {}
        for _, provider in df.iterrows():
            clinical_group = provider['clinical_group']
            for state in provider['operating_states']:
                if state not in coverage_matrix:
                    coverage_matrix[state] = set()
                coverage_matrix[state].add(clinical_group)
        
        # Find all clinical groups
        all_clinical_groups = set(df['clinical_group'].unique())
        
        # Identify gaps
        for state, covered_groups in coverage_matrix.items():
            missing_groups = all_clinical_groups - covered_groups
            if missing_groups:
                gaps.append({
                    "state": state,
                    "missing_clinical_groups": list(missing_groups),
                    "coverage_percentage": len(covered_groups) / len(all_clinical_groups) * 100,
                    "gap_severity": "High" if len(missing_groups) > 3 else "Medium" if len(missing_groups) > 1 else "Low"
                })
        
        return sorted(gaps, key=lambda x: len(x['missing_clinical_groups']), reverse=True)
    
    def _identify_expansion_opportunities(self, df: pd.DataFrame) -> List[Dict]:
        """Identify geographic expansion opportunities"""
        opportunities = []
        
        # Find CBSAs with high out-of-network quality providers
        for cbsa in df['primary_cbsa'].unique():
            cbsa_data = df[df['primary_cbsa'] == cbsa]
            out_network = cbsa_data[cbsa_data['network_status'] == 'Out-of-Network']
            high_quality_out = out_network[out_network['quality_score'] >= 4.0]
            
            if len(high_quality_out) > 0:
                opportunities.append({
                    "cbsa": cbsa,
                    "expansion_type": "High-Quality Provider Recruitment",
                    "opportunity_count": len(high_quality_out),
                    "avg_quality": high_quality_out['quality_score'].mean(),
                    "potential_utilizers": high_quality_out['utilizers'].sum(),
                    "priority": "High" if len(high_quality_out) >= 3 else "Medium"
                })
        
        return sorted(opportunities, key=lambda x: x['opportunity_count'], reverse=True)
    
    def _identify_consolidation_opportunities(self, df: pd.DataFrame) -> List[Dict]:
        """Identify geographic consolidation opportunities"""
        opportunities = []
        
        # Find CBSAs with multiple underperforming providers
        for cbsa in df['primary_cbsa'].unique():
            cbsa_data = df[df['primary_cbsa'] == cbsa]
            in_network = cbsa_data[cbsa_data['network_status'] == 'In-Network']
            underperformers = in_network[
                (in_network['quality_score'] < 3.5) & 
                (in_network['cost_per_utilizer'] > 700)
            ]
            
            if len(underperformers) >= 2:
                opportunities.append({
                    "cbsa": cbsa,
                    "consolidation_type": "Underperformer Removal",
                    "provider_count": len(underperformers),
                    "total_savings": underperformers['termination_value'].sum(),
                    "affected_utilizers": underperformers['utilizers'].sum(),
                    "priority": "High" if len(underperformers) >= 3 else "Medium"
                })
        
        return sorted(opportunities, key=lambda x: x['total_savings'], reverse=True)
    
    def _generate_state_recommendations(self, state: str, data: Dict) -> List[str]:
        """Generate recommendations for state-level optimization"""
        recommendations = []
        
        if data['total_opportunity'] > 1000000:
            recommendations.append("High-priority state for network optimization")
        
        if data['network_penetration'] < 0.6:
            recommendations.append("Improve network penetration through provider recruitment")
        
        if data['adequacy_risk_ratio'] > 0.3:
            recommendations.append("Address network adequacy risks before provider removals")
        
        if data['avg_quality'] < 3.5:
            recommendations.append("Focus on quality improvement initiatives")
        
        if data['clinical_group_count'] < 8:
            recommendations.append("Expand clinical group coverage")
        
        return recommendations
    
    def _generate_cbsa_recommendations(self, cbsa: str, data: Dict) -> List[str]:
        """Generate recommendations for CBSA-level optimization"""
        recommendations = []
        
        if data['competition_intensity'] > 0.8:
            recommendations.append("Highly competitive market - focus on differentiation")
        
        if data['network_penetration'] < 0.5:
            recommendations.append("Significant out-of-network opportunity")
        
        if data['avg_market_position'] < 50:
            recommendations.append("Below-average market positioning - strategic review needed")
        
        if data['total_opportunity'] > 500000:
            recommendations.append("Significant financial optimization opportunity")
        
        return recommendations
    
    def _calculate_adequacy_risk_level(self, data: Dict) -> str:
        """Calculate network adequacy risk level"""
        if data['in_network_providers'] < 2 or data['adequacy_ratio'] < 0.4:
            return "High"
        elif data['in_network_providers'] < 3 or data['adequacy_ratio'] < 0.6:
            return "Medium"
        else:
            return "Low"
    
    def _generate_adequacy_recommendations(self, data: Dict) -> List[str]:
        """Generate network adequacy recommendations"""
        recommendations = []
        
        if data['risk_level'] == "High":
            recommendations.append("Critical: Recruit additional in-network providers immediately")
        elif data['risk_level'] == "Medium":
            recommendations.append("Monitor closely and consider provider recruitment")
        
        if data['high_risk_providers'] > 0:
            recommendations.append("Evaluate alternatives before removing high-risk providers")
        
        return recommendations
    
    def _calculate_overall_adequacy_score(self, adequacy_analysis: Dict) -> float:
        """Calculate overall network adequacy score"""
        if not adequacy_analysis:
            return 0.0
        
        total_score = sum(data['adequacy_ratio'] for data in adequacy_analysis.values())
        return (total_score / len(adequacy_analysis)) * 100
    
    def _calculate_state_summary_stats(self, state_analysis: Dict) -> Dict:
        """Calculate summary statistics across all states"""
        if not state_analysis:
            return {}
        
        total_opportunity = sum(data['total_opportunity'] for data in state_analysis.values())
        avg_quality = np.mean([data['avg_quality'] for data in state_analysis.values()])
        avg_cost = np.mean([data['avg_cost'] for data in state_analysis.values()])
        total_providers = sum(data['provider_count'] for data in state_analysis.values())
        
        return {
            "total_opportunity": total_opportunity,
            "avg_quality_across_states": avg_quality,
            "avg_cost_across_states": avg_cost,
            "total_providers_across_states": total_providers,
            "states_with_high_opportunity": len([s for s in state_analysis.values() if s['total_opportunity'] > 500000])
        }

