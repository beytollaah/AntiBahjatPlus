"""
Women, Life, Liberty
A pipeline and UI to blur human faces in videos, and change the audio
Contact me: twitter.com/beytollaah

"""
import gradio as gr
from utils import get_gradio_ui


ui = get_gradio_ui()
ui.launch(inbrowser=True, quiet=True)

