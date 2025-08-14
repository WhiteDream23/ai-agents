"""
Weather Agent for retrieving and analyzing weather conditions
"""
import json
import requests
from core.llm_manager import llm_manager

class WeatherAgent:
    """
    Agent: Retrieves and analyzes weather conditions to inform health recommendations.
    Provides insights on optimal exercise settings based on current weather.
    """
    
    def __init__(self):
        pass
    
    def get_weather_data(self, latitude: float, longitude: float) -> dict:
        """Get weather data and provide exercise recommendations"""
        base_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "weather_code"],
            "timezone": "America/Los_Angeles"
        }
        
        # Default values in case API fails
        weather_data = {"temperature": 20, "humidity": 50, "condition": "Unknown"}
        
        try:
            resp = requests.get(base_url, params=params, timeout=10)
            data = resp.json()
            if resp.status_code == 200 and "current" in data:
                current = data["current"]
                weather_descriptions = {
                    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy",
                    3: "Overcast", 45: "Foggy", 51: "Light drizzle",
                    53: "Moderate drizzle", 61: "Light rain",
                    63: "Moderate rain", 65: "Heavy rain"
                }
                weather_data = {
                    "temperature": current.get("temperature_2m", 20),
                    "humidity": current.get("relative_humidity_2m", 50),
                    "condition": weather_descriptions.get(current.get("weather_code", 0), "Unknown")
                }
        except Exception as e:
            print(f"[WEATHER_AGENT] Error retrieving weather data: {e}")
        
        # Add exercise recommendations
        return self._add_exercise_recommendations(weather_data)
    
    def _get_fallback_recommendations(self, weather_data):
        """Generate fallback recommendations based on simple rules"""
        temp = weather_data.get('temperature', 20)
        condition = weather_data.get('condition', 'Unknown')
        return {
            'exercise_recommendation': 'Indoor' if (temp > 30 or temp < 5) else 'Outdoor',
            'intensity_level': 'Moderate' if 15 <= temp <= 25 else 'Low',
            'weather_alert': condition.lower() in ['rain', 'drizzle', 'snow', 'storm', 'foggy'],
            'reasoning': f"Based on {temp}°C and {condition} conditions, recommend {'indoor' if (temp > 30 or temp < 5) else 'outdoor'} exercise at {'moderate' if 15 <= temp <= 25 else 'low'} intensity."
        }
    
    def _add_exercise_recommendations(self, weather_data):
        """Use LLM to generate exercise recommendations based on weather"""
        try:
            prompt = f"""Analyze weather conditions (Temperature: {weather_data['temperature']}°C, Condition: {weather_data['condition']}, Humidity: {weather_data['humidity']}%) and provide exercise recommendations in JSON format with these exact keys:
                - exercise_recommendation: "Indoor" or "Outdoor"
                - intensity_level: "Low", "Moderate", or "High"
                - weather_alert: true or false
                - reasoning: brief explanation
                Return only JSON."""
            
            response = llm_manager.invoke(prompt)
            llm_recommendations = json.loads(response)
            
            # Verify all required fields exist
            required_fields = ['exercise_recommendation', 'intensity_level', 'weather_alert', 'reasoning']
            if all(field in llm_recommendations for field in required_fields):
                weather_data.update(llm_recommendations)
            else:
                weather_data.update(self._get_fallback_recommendations(weather_data))
                
        except (json.JSONDecodeError, Exception) as e:
            print(f"[WEATHER_AGENT] LLM recommendation failed: {e}")
            weather_data.update(self._get_fallback_recommendations(weather_data))
        
        return weather_data
