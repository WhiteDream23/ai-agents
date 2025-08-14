"""
Gradio UI interface components and layout
"""
import gradio as gr

def create_gradio_components():
    """Create and return all Gradio UI components"""
    
    # Header
    title = gr.Markdown("# Smart Health Agent")
    subtitle = gr.Markdown("### GPU-accelerated personalized health recommendations with specialized agents")
    
    # Input components
    folder_path = gr.Textbox(
        label="Medical Knowledge Base",
        placeholder="Enter path to folder containing medical PDF documents",
        scale=1,
        container=True
    )
    
    # Action components
    init_button = gr.Button("Activate Agent System", scale=1)
    init_output = gr.Textbox(label="Initialization Status", visible=False)
    
    # Chat components
    chatbot = gr.Chatbot(
        label="Smart Health Agent Chat",
        height=400,
        container=True,
        show_copy_button=True,
        render_markdown=False,
        type='messages',
        elem_id="health-chatbot"
    )
    
    msg = gr.Textbox(
        label="Ask your health-related questions",
        placeholder="Type your message here...",
        show_label=True,
        lines=2,
        container=True,
        scale=4
    )
    
    submit = gr.Button("Send Message", scale=2)
    clear_button = gr.Button("Clear Chat", scale=1)
    
    return {
        'title': title,
        'subtitle': subtitle,
        'folder_path': folder_path,
        'init_button': init_button,
        'init_output': init_output,
        'chatbot': chatbot,
        'msg': msg,
        'submit': submit,
        'clear_button': clear_button
    }

def create_gradio_layout(event_handlers):
    """Create the Gradio interface layout"""
    
    with gr.Blocks(
        theme=gr.themes.Soft(),
        title="Smart Health Agent"
    ) as demo:
        
        # Header
        gr.Markdown("# Smart Health Agent")
        gr.Markdown("### GPU-accelerated personalized health recommendations with specialized agents")
        
        with gr.Column(scale=1):
            # Input components
            folder_path = gr.Textbox(
                label="Medical Knowledge Base",
                placeholder="Enter path to folder containing medical PDF documents",
                scale=1,
                container=True
            )
            
            # Action components
            init_button = gr.Button("Activate Agent System", scale=1)
            init_output = gr.Textbox(label="Initialization Status", visible=False)
            
            # Chat components
            chatbot = gr.Chatbot(
                label="Smart Health Agent Chat",
                height=400,
                container=True,
                show_copy_button=True,
                render_markdown=False,
                type='messages',
                elem_id="health-chatbot"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Ask your health-related questions",
                    placeholder="Type your message here...",
                    show_label=True,
                    lines=2,
                    container=True,
                    scale=4
                )
            
            with gr.Row():
                submit = gr.Button("Send Message", scale=2)
                clear_button = gr.Button("Clear Chat", scale=1)
        
        # Bind events within the Blocks context
        init_button.click(
            fn=event_handlers.on_initialize,
            inputs=[folder_path],
            outputs=[init_output, chatbot],
        )
        
        msg.submit(
            fn=event_handlers.chat_interact,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot],
        )
        
        submit.click(
            fn=event_handlers.chat_interact,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot],
        )
        
        clear_button.click(
            lambda: ([], ""), 
            inputs=None, 
            outputs=[chatbot, msg]
        )
    
    return demo
