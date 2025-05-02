"""
Project: AI Chatbot
Date: 04/25
Author: James W.
Desc: chatbot with openai and gradio
"""

import os
import logging
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

previous_response_id = None

def chat(current_msg, history_msg, max_output_tokens, temperature):
    ans = ""
    global previous_response_id
    instructions = (
        "You are a friendly assistant chatbot. Answer directly and concisely."
    )
    # () for long string
    try:
        response = client.responses.create(
            input=current_msg,
            instructions=instructions,
            model="gpt-4.1-nano",
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            previous_response_id=previous_response_id,
        )
        ans = response.output_text
        previous_response_id = response.id
        logger.info(
            f"max_output_tokens:{max_output_tokens}. temperature: {temperature}"
        )
    except ConnectionError as e:
        logger.error(f"Network error: {e}")
        return None
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
    else:
        return ans
    finally:
        logger.info("Execution completed.")


try:
    with open("styles.css", "r", encoding="utf-8") as f:
        css_content = f.read()
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    css_content = ""

chatbot = gr.ChatInterface(
    fn=chat,
    css=css_content,
    type="messages",
    theme="default",
    title="AI Chatbot",
    description="🤖 Your friendly assistant in dark mode",
    flagging_mode="manual",
    chatbot=gr.Chatbot(height=350, type="messages"),
    flagging_options=["Like", "Spam", "Inappropriate", "Other"],
    textbox=gr.Textbox(
        placeholder="Ask me anything…",
        container=False,
        max_length=500,
    ),
    additional_inputs=[
        gr.Slider(1, 2048, value=256, step=1, label="Max Output Tokens"),
        gr.Slider(0.1, 2.0, value=1.0, step=0.1, label="Creativeness"),
    ],
)


if __name__ == "__main__":
    chatbot.launch()
