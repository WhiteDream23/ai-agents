"""
LLM management and configuration
"""
from langchain_ollama import OllamaLLM
from config import OLLAMA_HOST, DEFAULT_MODEL, MODEL_TEMPERATURE, ENABLE_STREAMING

class LLMManager:
    """Manages LLM instances and configurations"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or DEFAULT_MODEL
        self._llm = None
        
    @property
    def llm(self) -> OllamaLLM:
        """Get or create LLM instance"""
        if self._llm is None:
            self._llm = OllamaLLM(
                model=self.model_name,
                temperature=MODEL_TEMPERATURE,
                streaming=ENABLE_STREAMING,
                base_url=OLLAMA_HOST
            )
        return self._llm
    
    def update_model(self, new_model: str):
        """Update the model and recreate LLM instance"""
        self.model_name = new_model
        self._llm = None
    
    def stream_response(self, prompt: str):
        """Stream response from LLM"""
        return self.llm.stream(prompt)
    
    def invoke(self, prompt: str):
        """Get complete response from LLM"""
        return self.llm.invoke(prompt)

# Global LLM instance
llm_manager = LLMManager()
