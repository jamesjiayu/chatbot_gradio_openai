import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

demo = gr.Interface(
    fn=greet,  # Function to wrap UI around
    inputs=["text", "slider"],  # Input components matching function arguments
    outputs=["text"],  # Output component matching function return
)

demo.launch()
