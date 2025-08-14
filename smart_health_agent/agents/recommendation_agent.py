"""
Recommendation Agent for generating personalized health recommendations
"""
from langchain_core.messages import AIMessage
from core.state import HealthAgentState
from core.llm_manager import llm_manager

class RecommendationAgent:
    """
    Agent: Generates personalized health recommendations based on all collected data.
    """
    
    def __init__(self):
        pass
    
    def process(self, state: HealthAgentState) -> HealthAgentState:
        """Generate personalized health recommendations"""
        print("\n[RECOMMENDATION_AGENT] Generating personalized health plan...")
        weather_data = state.weather_data
        
        context = f"""
        Medical Knowledge: {state.rag_context.get('retrieved_knowledge', 'No medical context available')}
        
        Current Health Metrics:
        - Heart Rate: {state.health_data.get('heart_rate')} bpm - Status: {state.health_data.get('vitals_status', {}).get('heart_rate', 'Unknown')}
        - Sleep: {state.health_data.get('sleep_hours')} hours - Status: {state.health_data.get('vitals_status', {}).get('sleep', 'Unknown')}
        - Steps: {state.health_data.get('steps')} - Status: {state.health_data.get('vitals_status', {}).get('activity', 'Unknown')}
        
        Weather Analysis:
        - Current Weather: {weather_data.get('condition')} at {weather_data.get('temperature')}°C
        - Recommended Location: {weather_data.get('exercise_recommendation')}
        - Suggested Intensity: {weather_data.get('intensity_level')}
        - Weather Alerts: {"Yes" if weather_data.get('weather_alert') else "None"}
        - Weather Assessment: {weather_data.get('reasoning', '')}
        """
        
        prompt = f"""As the Health Recommendation Agent, generate personalized health advice:
        
        1. Consider the user's metrics (HR: {state.health_data.get('heart_rate')}, Sleep: {state.health_data.get('sleep_hours')}, Steps: {state.health_data.get('steps')})
        2. Factor in weather data from Weather Agent ({weather_data.get('temperature')}°C, {weather_data.get('condition')})
        3. Incorporate medical knowledge from documents
        
        Provide actionable recommendations for activity, nutrition, and sleep, with special focus on {weather_data.get('exercise_recommendation')} activities at {weather_data.get('intensity_level')} intensity.
        """
        
        response = ""
        for chunk in llm_manager.stream_response(prompt):
            response += chunk
            state.streaming_response = response
        
        state.recommendations.append(AIMessage(content=response))
        state.agent_reasoning["Recommendations"] = f"Generated personalized health plan (recommending {weather_data.get('exercise_recommendation')} activities)"
        print("[RECOMMENDATION_AGENT] Generated recommendations successfully")
        print(f"[RECOMMENDATION_AGENT] Recommendations: {response[:100]}...")  # Print first 100 chars
        return state
