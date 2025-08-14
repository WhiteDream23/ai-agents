"""
Core state management for Health Agent workflow
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage

class HealthAgentState(BaseModel):
    """
    State object for the health agent workflow
    """
    messages: List[BaseMessage] = Field(default_factory=list)
    health_data: Dict[str, Any] = Field(default_factory=dict)
    weather_data: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[BaseMessage] = Field(default_factory=list)
    rag_context: Dict[str, Any] = Field(default_factory=dict)
    streaming_response: str = Field(default="")
    # Simple agent reasoning storage
    agent_reasoning: Dict[str, str] = Field(default_factory=dict)
