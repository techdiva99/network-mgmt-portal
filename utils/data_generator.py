# utils/data_generator.py
"""
Enhanced sample data generation for provider network analysis
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from config.settings import DATA_CONSTANTS

def generate_provider_data():
    """Generate comprehensive provider data matching original functionality"""
    
    providers_data = []
    
    for i, name in enumerate(DATA_CONSTANTS['provider_names']):
        # Determine network status (70% in-network, 30% out-of-network)
        network_status = "In-Network" if random.random() < 0.7 else "Out-of-Network"
        
        # Generate performance data
        base_quality = random.uniform(3.0, 5.0)
        base_cost = random.uniform(250, 1200)
        
        # Calculate termination value (higher for poor performers)
        if base_quality < 3.5 and base_cost > 800:
            termination_value = random.uniform(500000, 2000000)
        elif base_quality < 4.0 or base_cost > 700:
            termination_value = random.uniform(200000, 800000)
        else:
            termination_value = random.uniform(0, 300000)
        
        # Generate state performance
        operating_states = random.sample(DATA_CONSTANTS['states'], random.randint(1, 5))
        state_performance = {}
        for state in operating_states:
            state_performance[state] = random.choice(['Excellent', 'Good', 'Poor'])
        
        # Generate home health episode performance
        episode_performance = {}
        for episode in random.sample(DATA_CONSTANTS['home_health_episodes'], random.randint(3, 7)):
            episode_performance[episode] = random.choice(['Leader', 'Average', 'Needs Improvement'])
        
        # Generate CBSA performance
        operating_cbsas = random.sample(DATA_CONSTANTS['cbsas'], random.randint(1, 3))
        cbsa_performance = {}
        for cbsa in operating_cbsas:
            cbsa_performance[cbsa] = {
                'market_share': random.uniform(5, 25),
                'quality_rank': random.randint(1, 10),
                'cost_rank': random.randint(1, 10)
            }
        
        # Market position (percentile vs competitors)
        market_position = random.uniform(10, 90)
        
        # Network adequacy risk
        adequacy_risk = "High" if termination_value > 1000000 else "Medium" if termination_value > 500000 else "Low"
        
        provider = {
            'provider_id': f'PROV_{i+1:03d}',  # ADD THIS LINE - CRITICAL FIX
            'name': name,
            'network_status': network_status,
            'clinical_group': random.choice(DATA_CONSTANTS['clinical_groups']),
            'primary_cbsa': random.choice(operating_cbsas),
            'cost_per_utilizer': base_cost,
            'quality_score': base_quality,
            'utilizers': random.randint(500, 5000),
            'satisfaction': random.uniform(3.5, 5.0),
            'utilization': random.uniform(0.6, 0.95),
            'contract_expiry': (datetime.now() + timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
            'termination_value': termination_value,
            'operating_states': operating_states,
            'state_performance': state_performance,
            'episode_performance': episode_performance,
            'cbsa_performance': cbsa_performance,
            'market_position_percentile': market_position,
            'adequacy_risk': adequacy_risk,
            'competitors': random.sample([f'PROV_{j+1:03d}' for j in range(50) if j != i], random.randint(2, 5))
        }
        providers_data.append(provider)
    
    return pd.DataFrame(providers_data)

def create_state_opportunity_data(df):
    """Calculate opportunity by state for map visualization"""
    state_data = {}
    
    for _, provider in df.iterrows():
        for state in provider['operating_states']:
            if state not in state_data:
                state_data[state] = {
                    'total_opportunity': 0,
                    'provider_count': 0,
                    'avg_quality': 0,
                    'recommendations': []
                }
            
            state_data[state]['total_opportunity'] += provider['termination_value']
            state_data[state]['provider_count'] += 1
            state_data[state]['avg_quality'] += provider['quality_score']
    
    # Calculate averages and recommendations
    for state in state_data:
        state_data[state]['avg_quality'] /= state_data[state]['provider_count']
        
        # Generate recommendations based on opportunity size
        if state_data[state]['total_opportunity'] > 1000000:
            state_data[state]['recommendations'] = [
                "Review high-cost, low-quality providers",
                "Negotiate better contract terms",
                "Consider network consolidation"
            ]
        elif state_data[state]['total_opportunity'] > 500000:
            state_data[state]['recommendations'] = [
                "Optimize provider mix",
                "Improve quality metrics"
            ]
        else:
            state_data[state]['recommendations'] = ["Monitor performance"]
    
    return state_data

