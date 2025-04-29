import gradio as gr

def yes_man(message, history):
    if message.endswith("?"):
        return "Yes"
    else:
        return "Ask me anything!"

gr.ChatInterface(
    yes_man,
    type="messages",
    chatbot=gr.Chatbot(height=300, type="messages"),#300px
    textbox=gr.Textbox(placeholder="Ask me a yes or no question",  container=False, # No border or padding around Textbox 
scale=7, # Takes up significant width in layout 
max_length=100 # Limits input to 100 characters 
),
    title="Yes Man",
    description="Ask Yes Man any question",
    theme="ocean",
    examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
    cache_examples=True,
    css="""
        .gr-textbox {
            border: 2px solid #4a90e2 !important;
            background-color: #f0f8ff !important;
            border-radius: 8px !important;
            padding: 10px !important;
        }
        .gr-chatbot .message {
            background-color: #e6f3ff !important;
            color: #333 !important;
            border-radius: 10px !important;
        }
        .gr-title {
            font-size: 24px !important;
            color: #004aad !important;
        }
        .gr-description {
            font-size: 16px !important;
            color: #0066cc !important;
        }
    """
).launch()
