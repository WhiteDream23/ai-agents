"""
Medical Knowledge Agent for searching and retrieving relevant health insights
"""
from core.state import HealthAgentState
from core.rag_system import rag_system

class MedicalKnowledgeAgent:
    """
    Agent: Searches medical documents for relevant health insights using RAG system.
    """
    
    def __init__(self):
        pass
    
    def process(self, state: HealthAgentState) -> HealthAgentState:
        """Search medical documents for relevant insights"""
        print("\n[KNOWLEDGE_AGENT] Processing medical knowledge...")

        relevant_docs = []
        num_docs = 0
        
        # Check if the vectorstore is initialized
        if rag_system.vectorstore:
            query = f"Health insights for: Heart rate: {state.health_data.get('heart_rate')}, Sleep: {state.health_data.get('sleep_hours')} hours, Steps: {state.health_data.get('steps')}"
            try:
                relevant_docs = rag_system.similarity_search(query)
                num_docs = len(relevant_docs)
            except Exception as e:
                print(f"[KNOWLEDGE_AGENT] Error during similarity search: {e}")
                relevant_docs = []
        else:
            print("[KNOWLEDGE_AGENT] Warning: Global vectorstore not initialized. Skipping document search.")

        state.rag_context["retrieved_knowledge"] = "\n".join([doc.page_content for doc in relevant_docs])
        state.rag_context["current_metrics"] = state.health_data
        
        state.agent_reasoning["MedicalKnowledge"] = f"Retrieved {num_docs} medical documents" if rag_system.vectorstore else "Skipped document retrieval (vectorstore not initialized)"
        
        print("[KNOWLEDGE_AGENT] Updated state with retrieved knowledge")
        return state
