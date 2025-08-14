"""
Health Agent workflow management
"""
from langgraph.graph import StateGraph, END, START
from core.state import HealthAgentState
from agents.health_metrics_agent import HealthMetricsAgent
from agents.medical_knowledge_agent import MedicalKnowledgeAgent
from agents.recommendation_agent import RecommendationAgent

def build_health_workflow():
    """
    Build a workflow that connects specialized health agents.
    """ 
    graph = StateGraph(HealthAgentState)
    
    # Initialize agents
    health_agent = HealthMetricsAgent()
    knowledge_agent = MedicalKnowledgeAgent()
    recommendation_agent = RecommendationAgent()
    
    # Add nodes
    graph.add_node("health_metrics", health_agent.process)
    graph.add_node("medical_knowledge", knowledge_agent.process) 
    graph.add_node("generate_recommendations", recommendation_agent.process)
    
    # Add edges
    graph.add_edge(START, "health_metrics")
    graph.add_edge("health_metrics", "medical_knowledge")
    graph.add_edge("medical_knowledge", "generate_recommendations")
    graph.add_edge("generate_recommendations", END)
    
    return graph.compile()
