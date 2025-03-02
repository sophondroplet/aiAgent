from __future__ import annotations as _annotations

import os
import asyncio

from httpx import AsyncClient
import gradio as gr

from weather_agent import Deps, weather_agent

async def get_weather_response(user_input: str) -> str:
    latkey = os.getenv("GEOLOC_API_KEY")
    weatherkey = os.getenv("WEATHER_API_KEY")
    result = await weather_agent.run(user_input, deps=Deps(client=AsyncClient(), latlong_key=latkey, weather_key=weatherkey))
    return result.data

def respond(user_input, history):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(get_weather_response(user_input))
    history.append((user_input, response))
    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(show_label=False, placeholder="Ask about the weather...").style(container=False)
        with gr.Column():
            submit_btn = gr.Button("Send")
    submit_btn.click(respond, [user_input, chatbot], [chatbot, chatbot])

demo.launch(share=True)
