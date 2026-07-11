import gradio as gr
from speech_to_text import *

def audioLs(audioPath):
    return audioPath

demo = gr.Interface(
    fn = speechToText,
    inputs = gr.Audio(
        sources = ["microphone"],
        type = "filepath"
    ),
    outputs = "text"
)

demo.launch()