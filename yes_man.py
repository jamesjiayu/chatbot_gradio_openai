import gradio as gr
import random

def random_response(message, history):
    return random.choice(["Yes", "No"])

demo = gr.ChatInterface(
    fn=random_response,
    type="messages"  # Always use type="messages" (default "tuples" is deprecated)
).launch()