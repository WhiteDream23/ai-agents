"""
Health Metrics Agent for analyzing fitness data and evaluating vitals
"""
import pandas as pd
from core.state import HealthAgentState
from agents.weather_agent import WeatherAgent
from config import DEFAULT_LATITUDE, DEFAULT_LONGITUDE, HEART_RATE_NORMAL_RANGE, SLEEP_OPTIMAL_RANGE, ACTIVITY_THRESHOLD

class HealthMetricsAgent:
    """
    Agent: Analyzes fitness data and evaluates vitals/status.
    """
    
    def __init__(self):
        self.weather_agent = WeatherAgent()
    
    def process(self, state: HealthAgentState) -> HealthAgentState:
        """Process health metrics and update state"""
        print("\n[HEALTH_AGENT] Processing health data...")
        vitals_status = {}
        
        # Check if we have 7-day averages or single values
        if 'heart_rate_avg_7d' in state.health_data:
            hr = state.health_data.get('heart_rate_avg_7d', 0)
            sleep_hrs = state.health_data.get('sleep_hours_avg_7d', 0)
            steps = state.health_data.get('steps_avg_7d', 0)
            # Store both 7d average and regular format for compatibility
            state.health_data['heart_rate'] = hr
            state.health_data['sleep_hours'] = sleep_hrs
            state.health_data['steps'] = steps
        else:
            hr = state.health_data.get('heart_rate', 0)
            sleep_hrs = state.health_data.get('sleep_hours', 0)
            steps = state.health_data.get('steps', 0)
        
        print(f"[HEALTH_AGENT] Current metrics - HR: {hr}, Sleep: {sleep_hrs}, Steps: {steps}")

        # Evaluate vitals using configuration
        hr_min, hr_max = HEART_RATE_NORMAL_RANGE
        sleep_min, sleep_max = SLEEP_OPTIMAL_RANGE
        
        vitals_status['heart_rate'] = 'Normal' if hr_min <= hr <= hr_max else 'Abnormal'
        vitals_status['sleep'] = 'Optimal' if sleep_min <= sleep_hrs <= sleep_max else 'Suboptimal'
        vitals_status['activity'] = 'Active' if steps >= ACTIVITY_THRESHOLD else 'Sedentary'
        
        # Get weather data if not available
        if not state.weather_data or 'exercise_recommendation' not in state.weather_data:
            state.weather_data = self.weather_agent.get_weather_data(DEFAULT_LATITUDE, DEFAULT_LONGITUDE)
        
        state.health_data['vitals_status'] = vitals_status
        state.health_data['weather_impact'] = state.weather_data
        state.health_data['last_processed'] = pd.Timestamp.now()
        
        # Simple reasoning
        state.agent_reasoning["HealthMetrics"] = f"Analyzed vitals: HR {vitals_status['heart_rate']}, Sleep {vitals_status['sleep']}, Activity {vitals_status['activity']}"
        
        print(f"[HEALTH_AGENT] Processed vitals status: {vitals_status}")
        return state
