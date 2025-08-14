"""
Main application entry point for Smart Health Agent
"""
from ui.gradio_interface import create_gradio_layout
from ui.event_handlers import event_handlers
from config import SERVER_NAME, SERVER_PORT, ENABLE_SHARE, ENABLE_DEBUG

def create_ui():
    """
    Creates the Gradio interface with streaming support
    """
    # Create layout with event bindings
    demo = create_gradio_layout(event_handlers)
    
    return demo

def main():
    """Main application entry point"""
    print("Starting Smart Health Agent...")
    
    demo = create_ui()
    
    demo.queue(
        max_size=20,
        default_concurrency_limit=2
    )
    
    demo.launch(
        server_name=SERVER_NAME,
        server_port=SERVER_PORT,
        share=ENABLE_SHARE,
        debug=ENABLE_DEBUG,
        show_error=True,
        inbrowser=True
    )

if __name__ == "__main__":
    main()
