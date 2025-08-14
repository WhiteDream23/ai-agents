"""
Event handlers for Gradio UI interactions
"""
import traceback
from langchain_core.messages import HumanMessage
from core.state import HealthAgentState
from core.workflow import build_health_workflow
from core.rag_system import rag_system
from core.llm_manager import llm_manager
from utils.health_data import get_health_data
from agents.weather_agent import WeatherAgent
from config import DEFAULT_LATITUDE, DEFAULT_LONGITUDE

class EventHandlers:
    """Handles all UI events and interactions"""
    
    def __init__(self):
        self.weather_agent = WeatherAgent()
    
    def on_initialize(self, fpath):
        """Handler for initialization button click"""
        print("[UI] Initialize button clicked.")
        print(f"[UI] Folder/File Path: {fpath}")
        
        messages = [{"role": "assistant", "content": ""}]
        
        try:
            if not fpath or not fpath.strip():
                yield "Error: Please enter a valid folder path.", [{"role": "assistant", "content": "Please enter a valid folder path."}]
                return
                
            rag_system.reset_vectorstore()
            lat, lon = DEFAULT_LATITUDE, DEFAULT_LONGITUDE
            
            # Setup RAG
            if isinstance(fpath, str) and fpath.strip():
                if fpath.lower().endswith('.pdf'):
                    import os
                    rag_folder_path = os.path.dirname(fpath)
                else:
                    rag_folder_path = fpath
                print(f"[UI] Using provided path for RAG: {rag_folder_path}")
                rag_system.setup_vectorstore(rag_folder_path)

            # Get data
            health_data = get_health_data()
            weather_data = self.weather_agent.get_weather_data(lat, lon)
            
            # Build workflow
            app = build_health_workflow()
            initial_state = HealthAgentState(
                health_data=health_data,
                weather_data=weather_data,
                messages=[HumanMessage(content="User requested initial health recommendations.")] 
            )

            # Run workflow
            final_state = app.invoke(initial_state)
            response_content = final_state.get('streaming_response')
            
            if not response_content and final_state.get('recommendations'):
                response_content = final_state['recommendations'][-1].content
            elif not response_content:
                response_content = "Agent workflow finished, but no recommendation message was generated."

            messages = [{"role": "assistant", "content": response_content}]
            yield "[UI] Initialization complete. Agents activated.", messages

        except Exception as e:
            error_msg = f"Error during initialization workflow: {str(e)}"
            print(f"[UI] Error: {error_msg}")
            traceback.print_exc()
            yield error_msg, [{"role": "assistant", "content": f"An error occurred: {error_msg}"}]
    
    def chat_interact(self, user_message, chat_history):
        """Chat function with streaming support"""
        print(f"\n[CHAT] Received message: {user_message}")
        
        if not user_message or not user_message.strip():
            return "", chat_history or []
        
        if chat_history is None:
            chat_history = []
        
        context = ""
        if rag_system.vectorstore:
            try:
                relevant_docs = rag_system.similarity_search(user_message)
                context = "\n".join([doc.page_content for doc in relevant_docs])
            except Exception as e:
                print(f"[CHAT] Error during similarity search: {e}")
                context = "Error retrieving relevant documents."
        
        history_str = ""
        for h in chat_history:
            if h and h.get('content'):
                if h['role'] == 'user':
                    history_str += f"User: {h['content']}\n"
                elif h['role'] == 'assistant':
                    history_str += f"AI: {h['content']}\n"
        
        prompt = f"""You are a helpful health assistant. Provide direct, clear answers.

Context from medical documents: {context}

Chat history:
{history_str}

User: {user_message}

Provide a direct answer:"""
        
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": "```"})
        
        try:
            for chunk in llm_manager.stream_response(prompt):
                if chunk:
                    chat_history[-1]["content"] += chunk
                    yield "", chat_history
        except Exception as e:
            print(f"[CHAT] Error during streaming: {e}")
            chat_history[-1]["content"] = f"Error generating response: {str(e)}"
            yield "", chat_history
        chat_history[-1]["content"] += "```"
        yield "", chat_history
        return "", chat_history

# Global event handlers instance
event_handlers = EventHandlers()