"""
Health data utilities and synthetic data generation
"""
import pandas as pd

def generate_synthetic_fitness_data() -> dict:
    """
    Generate synthetic health/fitness data for testing.
    """
    return {
        'heart_rate': 75,
        'steps': 8500,
        'sleep_hours': 7.5,
        'calories': 2100,
        'last_updated': pd.Timestamp.now().isoformat()
    }

def get_health_data() -> dict:
    """
    Get synthetic health data
    
    Returns:
        dict: Health data
    """
    return generate_synthetic_fitness_data()
