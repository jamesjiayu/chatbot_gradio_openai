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

"""history_msg:
[
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris"}
]"""


def chat(current_msg, history_msg, max_output_tokens, temperature):
    instructions = "You are a friendly assistant chatbot. Answer directly and concisely."
    ans = ""
    try:
        response = client.responses.create(
            input=current_msg,
            instructions=instructions,
            model="gpt-4.1-nano-2025-04-14",
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            stream=False,
        )
        logger.info(f"max_output_tokens:{max_output_tokens}. temperature: {temperature}")
        ans = response.output_text
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


chatbot = gr.ChatInterface(
    fn=chat,
    type="messages",
    # save_history=True,
    additional_inputs=[
        gr.Slider(
            minimum=1, maximum=2048, value=256, step=1, label="Max output tokens"
        ),
        gr.Slider(minimum=0.1, maximum=2.0, value=0.2, step=0.1, label="Creativeness"),
    ],
)

# if __name__ == "__main__":
chatbot.launch()
