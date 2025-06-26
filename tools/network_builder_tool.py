# tools/network_builder_tool.py
"""
Network Builder Tool for custom network scenario analysis
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

class NetworkBuilderTool(BaseTool):
    name: str = "Network Builder Tool"
    description: str = "Build and analyze custom provider network scenarios with real-time metrics"
    
    def _run(self, 
             all_providers: List[Dict], 
             selected_provider_ids: List[str],
             scenario_name: str = "Custom Network") -> Dict[str, Any]:
        """Calculate metrics for a custom network scenario"""
        
        df = pd.DataFrame(all_providers)
        
        # Current network (in-network providers)
        current_network = df[df['network_status'] == 'In-Network']
        
        # Proposed network (selected providers)
        proposed_network = df[df['provider_id'].isin(selected_provider_ids)]
        
        # Calculate scenario metrics
        scenario_metrics = self._calculate_scenario_metrics(
            current_network, proposed_network, df
        )
        
        # Assess network adequacy
        adequacy_assessment = self._assess_network_adequacy(proposed_network, df)
        
        # Calculate financial impact
        financial_impact = self._calculate_financial_impact(
            current_network, proposed_network
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            scenario_metrics, adequacy_assessment, financial_impact
        )
        
        return {
            "scenario_name": scenario_name,
            "current_network_metrics": self._get_network_metrics(current_network),
            "proposed_network_metrics": self._get_network_metrics(proposed_network),
            "scenario_metrics": scenario_metrics,
            "adequacy_assessment": adequacy_assessment,
            "financial_impact": financial_impact,
            "recommendations": recommendations,
            "provider_changes": self._calculate_provider_changes(
                current_network, proposed_network
            ),
            "success": True
        }
    
    def _get_network_metrics(self, network_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate basic network metrics"""
        if network_df.empty:
            return {
                "provider_count": 0,
                "avg_quality": 0,
                "avg_cost": 0,
                "total_utilizers": 0,
                "total_savings_opportunity": 0,
                "clinical_groups": 0,
                "states_covered": 0,
                "cbsas_covered": 0
            }
        
        return {
            "provider_count": len(network_df),
            "avg_quality": network_df['quality_score'].mean(),
            "avg_cost": network_df['cost_per_utilizer'].mean(),
            "total_utilizers": network_df['utilizers'].sum(),
            "total_savings_opportunity": network_df['termination_value'].sum(),
            "clinical_groups": network_df['clinical_group'].nunique(),
            "states_covered": len(set([state for states in network_df['operating_states'] for state in states])),
            "cbsas_covered": network_df['primary_cbsa'].nunique()
        }
    
    def _calculate_scenario_metrics(self, 
                                  current_network: pd.DataFrame, 
                                  proposed_network: pd.DataFrame,
                                  all_providers: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comparative scenario metrics"""
        
        current_metrics = self._get_network_metrics(current_network)
        proposed_metrics = self._get_network_metrics(proposed_network)
        
        # Calculate changes
        quality_change = proposed_metrics['avg_quality'] - current_metrics['avg_quality']
        cost_change = proposed_metrics['avg_cost'] - current_metrics['avg_cost']
        provider_change = proposed_metrics['provider_count'] - current_metrics['provider_count']
        utilizer_change = proposed_metrics['total_utilizers'] - current_metrics['total_utilizers']
        
        # Calculate quality improvement score
        quality_improvement_score = self._calculate_quality_improvement_score(
            current_network, proposed_network
        )
        
        # Calculate cost efficiency score
        cost_efficiency_score = self._calculate_cost_efficiency_score(
            current_network, proposed_network
        )
        
        return {
            "quality_change": quality_change,
            "cost_change": cost_change,
            "provider_change": provider_change,
            "utilizer_change": utilizer_change,
            "quality_improvement_score": quality_improvement_score,
            "cost_efficiency_score": cost_efficiency_score,
            "network_performance_score": (quality_improvement_score + cost_efficiency_score) / 2
        }
    
    def _assess_network_adequacy(self, 
                               proposed_network: pd.DataFrame,
                               all_providers: pd.DataFrame) -> Dict[str, Any]:
        """Assess network adequacy for proposed network"""
        
        adequacy_issues = []
        adequacy_warnings = []
        coverage_gaps = {}
        
        # Clinical group adequacy assessment
        clinical_coverage = self._assess_clinical_group_coverage(proposed_network)
        
        # Geographic adequacy assessment  
        geographic_coverage = self._assess_geographic_coverage(proposed_network)
        
        # High-risk provider assessment
        high_risk_assessment = self._assess_high_risk_providers(proposed_network)
        
        # Overall adequacy score (0-100)
        adequacy_score = self._calculate_adequacy_score(
            clinical_coverage, geographic_coverage, high_risk_assessment
        )
        
        # Generate adequacy level
        if adequacy_score >= 80:
            adequacy_level = "Safe"
            adequacy_color = "green"
        elif adequacy_score >= 60:
            adequacy_level = "Warning"
            adequacy_color = "yellow"
        else:
            adequacy_level = "Critical"
            adequacy_color = "red"
        
        return {
            "adequacy_score": adequacy_score,
            "adequacy_level": adequacy_level,
            "adequacy_color": adequacy_color,
            "clinical_coverage": clinical_coverage,
            "geographic_coverage": geographic_coverage,
            "high_risk_assessment": high_risk_assessment,
            "adequacy_issues": adequacy_issues,
            "adequacy_warnings": adequacy_warnings,
            "coverage_gaps": coverage_gaps
        }
    
    def _assess_clinical_group_coverage(self, network_df: pd.DataFrame) -> Dict[str, Any]:
        """Assess clinical group coverage adequacy"""
        
        if network_df.empty:
            return {"coverage_score": 0, "gaps": [], "coverage_by_group": {}}
        
        # Required clinical groups (from your data constants)
        required_groups = [
            "Behavioral Health", "Wounds", "Complex Nursing Interventions",
            "MMTA_Cardiac_and_Circulatory", "MMTA_Endocrine", "MMTA_Infectious_Disease"
        ]
        
        covered_groups = set(network_df['clinical_group'].unique())
        missing_groups = [group for group in required_groups if group not in covered_groups]
        
        # Calculate coverage by state for each clinical group
        coverage_by_group = {}
        for group in required_groups:
            group_providers = network_df[network_df['clinical_group'] == group]
            if not group_providers.empty:
                states_covered = len(set([state for states in group_providers['operating_states'] for state in states]))
                coverage_by_group[group] = {
                    "provider_count": len(group_providers),
                    "states_covered": states_covered,
                    "adequacy_status": "Adequate" if len(group_providers) >= 2 else "Limited"
                }
            else:
                coverage_by_group[group] = {
                    "provider_count": 0,
                    "states_covered": 0,
                    "adequacy_status": "Missing"
                }
        
        # Calculate overall coverage score
        coverage_score = (len(covered_groups) / len(required_groups)) * 100
        
        return {
            "coverage_score": coverage_score,
            "covered_groups": list(covered_groups),
            "missing_groups": missing_groups,
            "coverage_by_group": coverage_by_group,
            "required_groups": required_groups
        }
    
    def _assess_geographic_coverage(self, network_df: pd.DataFrame) -> Dict[str, Any]:
        """Assess geographic coverage adequacy"""
        
        if network_df.empty:
            return {"coverage_score": 0, "state_coverage": {}, "cbsa_coverage": {}}
        
        # State coverage analysis
        all_states = set([state for states in network_df['operating_states'] for state in states])
        
        # CBSA coverage analysis
        covered_cbsas = set(network_df['primary_cbsa'].unique())
        
        # Calculate state adequacy (minimum 2 providers per state)
        state_coverage = {}
        for state in all_states:
            state_providers = network_df[network_df['operating_states'].apply(lambda x: state in x)]
            provider_count = len(state_providers)
            clinical_groups_covered = len(state_providers['clinical_group'].unique())
            
            state_coverage[state] = {
                "provider_count": provider_count,
                "clinical_groups_covered": clinical_groups_covered,
                "adequacy_status": "Adequate" if provider_count >= 2 else "Limited" if provider_count == 1 else "Missing"
            }
        
        # Calculate overall geographic coverage score
        adequate_states = len([s for s, data in state_coverage.items() if data['adequacy_status'] == 'Adequate'])
        coverage_score = (adequate_states / len(state_coverage)) * 100 if state_coverage else 0
        
        return {
            "coverage_score": coverage_score,
            "states_covered": len(all_states),
            "cbsas_covered": len(covered_cbsas),
            "state_coverage": state_coverage,
            "cbsa_coverage": {cbsa: {"provider_count": len(network_df[network_df['primary_cbsa'] == cbsa])} 
                            for cbsa in covered_cbsas}
        }
    
    def _assess_high_risk_providers(self, network_df: pd.DataFrame) -> Dict[str, Any]:
        """Assess high-risk providers in network"""
        
        if network_df.empty:
            return {"risk_score": 100, "high_risk_count": 0, "risk_details": []}
        
        # Count high-risk providers
        high_risk_providers = network_df[network_df['adequacy_risk'] == 'High']
        high_risk_count = len(high_risk_providers)
        
        # Calculate risk score (lower is better)
        total_providers = len(network_df)
        risk_ratio = high_risk_count / total_providers if total_providers > 0 else 0
        risk_score = max(0, 100 - (risk_ratio * 100))
        
        # Risk details
        risk_details = []
        for _, provider in high_risk_providers.iterrows():
            risk_details.append({
                "provider_name": provider['name'],
                "clinical_group": provider['clinical_group'],
                "primary_cbsa": provider['primary_cbsa'],
                "risk_reason": "High network adequacy risk"
            })
        
        return {
            "risk_score": risk_score,
            "high_risk_count": high_risk_count,
            "total_providers": total_providers,
            "risk_ratio": risk_ratio,
            "risk_details": risk_details
        }
    
    def _calculate_adequacy_score(self, 
                                clinical_coverage: Dict, 
                                geographic_coverage: Dict, 
                                high_risk_assessment: Dict) -> float:
        """Calculate overall network adequacy score"""
        
        # Weighted adequacy score
        clinical_weight = 0.4
        geographic_weight = 0.4
        risk_weight = 0.2
        
        adequacy_score = (
            clinical_coverage['coverage_score'] * clinical_weight +
            geographic_coverage['coverage_score'] * geographic_weight +
            high_risk_assessment['risk_score'] * risk_weight
        )
        
        return round(adequacy_score, 1)
    
    def _calculate_financial_impact(self, 
                                  current_network: pd.DataFrame,
                                  proposed_network: pd.DataFrame) -> Dict[str, Any]:
        """Calculate financial impact of network changes"""
        
        # Identify additions and removals
        current_ids = set(current_network['provider_id'].tolist()) if not current_network.empty else set()
        proposed_ids = set(proposed_network['provider_id'].tolist()) if not proposed_network.empty else set()
        
        additions = proposed_ids - current_ids
        removals = current_ids - proposed_ids
        
        # Calculate savings from removals
        if removals and not current_network.empty:
            removal_providers = current_network[current_network['provider_id'].isin(removals)]
            removal_savings = removal_providers['termination_value'].sum()
        else:
            removal_savings = 0
        
        # Calculate costs from additions (estimate recruitment/setup costs)
        addition_costs = len(additions) * 50000  # Estimated $50k per new provider
        
        # Net financial impact
        net_savings = removal_savings - addition_costs
        
        # Quality impact value (monetize quality improvements)
        if not current_network.empty and not proposed_network.empty:
            quality_improvement = proposed_network['quality_score'].mean() - current_network['quality_score'].mean()
            quality_value = quality_improvement * len(proposed_network) * 25000  # $25k per provider per quality point
        else:
            quality_improvement = 0
            quality_value = 0
        
        # Total value
        total_value = net_savings + quality_value
        
        return {
            "removal_savings": removal_savings,
            "addition_costs": addition_costs,
            "net_savings": net_savings,
            "quality_improvement": quality_improvement,
            "quality_value": quality_value,
            "total_value": total_value,
            "providers_added": len(additions),
            "providers_removed": len(removals),
            "roi_percentage": (total_value / max(addition_costs, 1)) * 100 if addition_costs > 0 else 0
        }
    
    def _calculate_provider_changes(self, 
                                  current_network: pd.DataFrame,
                                  proposed_network: pd.DataFrame) -> Dict[str, List]:
        """Calculate specific provider additions and removals"""
        
        current_ids = set(current_network['provider_id'].tolist()) if not current_network.empty else set()
        proposed_ids = set(proposed_network['provider_id'].tolist()) if not proposed_network.empty else set()
        
        additions = proposed_ids - current_ids
        removals = current_ids - proposed_ids
        retained = current_ids & proposed_ids
        
        return {
            "additions": list(additions),
            "removals": list(removals),
            "retained": list(retained),
            "additions_count": len(additions),
            "removals_count": len(removals),
            "retained_count": len(retained)
        }
    
    def _calculate_quality_improvement_score(self, 
                                           current_network: pd.DataFrame,
                                           proposed_network: pd.DataFrame) -> float:
        """Calculate quality improvement score (0-100)"""
        
        if current_network.empty or proposed_network.empty:
            return 0
        
        current_quality = current_network['quality_score'].mean()
        proposed_quality = proposed_network['quality_score'].mean()
        
        # Normalize to 0-100 scale
        quality_improvement = ((proposed_quality - current_quality) / 5.0) * 100
        return min(100, max(0, 50 + quality_improvement))  # Base 50, adjust by improvement
    
    def _calculate_cost_efficiency_score(self, 
                                       current_network: pd.DataFrame,
                                       proposed_network: pd.DataFrame) -> float:
        """Calculate cost efficiency score (0-100)"""
        
        if current_network.empty or proposed_network.empty:
            return 0
        
        current_cost = current_network['cost_per_utilizer'].mean()
        proposed_cost = proposed_network['cost_per_utilizer'].mean()
        
        # Normalize to 0-100 scale (lower cost = higher score)
        cost_improvement = ((current_cost - proposed_cost) / current_cost) * 100
        return min(100, max(0, 50 + cost_improvement))  # Base 50, adjust by improvement
    
    def _generate_recommendations(self, 
                                scenario_metrics: Dict,
                                adequacy_assessment: Dict,
                                financial_impact: Dict) -> List[str]:
        """Generate strategic recommendations for the network scenario"""
        
        recommendations = []
        
        # Quality-based recommendations
        if scenario_metrics['quality_change'] > 0.2:
            recommendations.append(f"Excellent quality improvement: +{scenario_metrics['quality_change']:.2f} points")
        elif scenario_metrics['quality_change'] < -0.2:
            recommendations.append(f"Warning: Quality decrease of {abs(scenario_metrics['quality_change']):.2f} points")
        
        # Cost-based recommendations
        if scenario_metrics['cost_change'] < -50:
            recommendations.append(f"Significant cost savings: ${abs(scenario_metrics['cost_change']):.0f} per utilizer")
        elif scenario_metrics['cost_change'] > 50:
            recommendations.append(f"Cost increase: +${scenario_metrics['cost_change']:.0f} per utilizer")
        
        # Financial impact recommendations
        if financial_impact['total_value'] > 1000000:
            recommendations.append(f"Strong financial case: ${financial_impact['total_value']/1000000:.1f}M total value")
        elif financial_impact['total_value'] < 0:
            recommendations.append(f"Financial concern: -${abs(financial_impact['total_value'])/1000000:.1f}M total cost")
        
        # Adequacy-based recommendations
        if adequacy_assessment['adequacy_level'] == 'Critical':
            recommendations.append("Critical: Address network adequacy issues before implementation")
        elif adequacy_assessment['adequacy_level'] == 'Warning':
            recommendations.append("Warning: Monitor network adequacy during implementation")
        else:
            recommendations.append("Network adequacy maintained")
        
        # Network size recommendations
        if scenario_metrics['provider_change'] < -10:
            recommendations.append("Significant network reduction - ensure adequate coverage")
        elif scenario_metrics['provider_change'] > 10:
            recommendations.append("Network expansion - monitor integration costs")
        
        return recommendations

