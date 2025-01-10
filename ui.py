import gradio as gr
from ollama_mai import main

def chat(message, history):
    return main(message)

demo = gr.ChatInterface(
    fn=chat,
    title="😊 Friends of IxNetwork 😊",
    description="Let's talk about anything IxNetwork",
)

if __name__ == '__main__':
    demo.launch(debug=True)
