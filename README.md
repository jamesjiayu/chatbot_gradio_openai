🚀 Chatbot Quickstart Guide: Building with Gradio and OpenAI
This guide empowers you to create a chatbot using Gradio for an intuitive user interface and OpenAI for intelligent, human-like responses. Designed for beginners and seasoned developers alike, it offers clear steps and insights for students, professors, and peers.

🛠️ Part 0: Managing Secrets with python-dotenv
Securely handle sensitive data like API keys using python-dotenv, a Python library that loads environment variables from a .env file into your application.
📋 What is python-dotenv and .env?
python-dotenv: Loads environment variables from a .env file into os.environ.
.env file: A text file with KEY=VALUE pairs, kept out of version control for security.
⚙️ Setup Instructions
Install python-dotenv
pip install python-dotenv


Create a .env File
In your project’s root, create .env and add:
OPENAI_API_KEY=sk-your-api-key
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DEBUG_MODE=true
 Notes: Avoid quotes unless needed; keep .env secure.
Load .env Variables in Python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set")
print(f"API Key: {api_key}")
 How it works: load_dotenv() sets variables in os.environ; os.getenv("KEY") retrieves values.
Test the Setup
Run: python app.py
Expected output: API Key: sk-your-api-key
🔒 Best Practices
Load Early: Call load_dotenv() at script start.
Set Defaults: debug_mode = os.getenv("DEBUG_MODE", "false")
Validate: Ensure critical variables exist:
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is required")


Specify Paths: Use load_dotenv(dotenv_path="path/to/.env") if needed.
Secure .env: Add .env to .gitignore.

🎨 Part 1: Crafting Interfaces with Gradio
Gradio is an open-source Python package for rapidly building and sharing web-based demos for any Python function, machine learning model, or API—no JavaScript or hosting expertise required!
📦 Installation
Prerequisite: Python 3.10 or higher.
pip install --upgrade gradio

🖼️ Building Your First Gradio Demo
Create a simple app in your editor, notebook, or Colab:
import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)

demo.launch()

Tip: We use gr as shorthand for gradio for cleaner code.
Run with python app.py. The demo opens in a browser or notebook. Enter a name, adjust the slider, and click Submit to see a greeting.
Callback Function: A function executed on UI interaction (e.g., Submit). It’s central to Gradio’s event-driven design.
🧠 Understanding the Interface Class
The gr.Interface class creates demos for functions with inputs/outputs. Key arguments:
fn: The function to wrap with a UI.
inputs: Gradio components (e.g., ["text", "slider"]) matching function arguments.
outputs: Components (e.g., ["text"]) matching return values.
fn is versatile, supporting anything from calculators to ML models. Use lists for multiple inputs/outputs.
🏗️ Custom Demos with gr.Blocks (Optional)
gr.Blocks enables custom layouts and complex interactions, like dynamic component updates, all in Python. Not critical for this project but explore later if needed.
🤖 Chatbots with gr.ChatInterface
gr.ChatInterface simplifies chatbot UI creation with minimal code, supporting customization and multimodal inputs.
💬 Defining a Chat Function
A gr.ChatInterface chat function takes:
message: User’s latest input (string).
history: List of OpenAI-style dictionaries (e.g., [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"}].
Example history:
[
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris"}
]

Next message: "And what is its largest city?"
Returns: "Paris is also the largest city."
Example: Random Yes/No Chatbot
import random
import gradio as gr

def random_response(message, history):
    return random.choice(["Yes", "No"])

gr.ChatInterface(
    fn=random_response,
    type="messages"
).launch()

Tip: Use type="messages"; type="tuples" is deprecated.
Example: Alternating Agreement
import gradio as gr

def alternatingly_agree(message, history):
    if len([h for h in history if h["role"] == "assistant"]) % 2 == 0:
        return f"Yes, I do think that: {message}"
    else:
        return "I don't think so"

gr.ChatInterface(
    fn=alternatingly_agree,
    type="messages"
).launch()

The list comprehension [h for h in history if h["role"] == "assistant"] filters to assistant messages.
🎨 Customizing the Chat UI
gr.ChatInterface supports:
title, description: Add headers.
theme, css: Style the interface.
examples, cache_examples: Add preset inputs.
chatbot, textbox: Customize components.
Adding Examples
Use examples as strings or dictionaries (e.g., {"text": "What's in this image?", "files": ["cheetah.jpg"]}). Enable cache_examples=True for pre-computed results.
Customizing Chatbot/Textbox
import gradio as gr

def yes_man(message, history):
    if message.endswith("?"):
        return "Yes"
    else:
        return "Ask me anything!"

gr.ChatInterface(
    yes_man,
    type="messages",
    chatbot=gr.Chatbot(height=300, type="messages"),
    textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7, max_length=100),
    title="Yes Man",
    description="Ask Yes Man any question",
    theme="ocean",
    examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
    cache_examples=True,
    css="""
        .gr-textbox { border: 2px solid #4a90e2 !important; background-color: #f0f8ff !important; border-radius: 8px !important; padding: 10px !important; }
        .gr-chatbot .message { background-color: #e6f3ff !important; color: #333 !important; border-radius: 10px !important; }
        .gr-title { font-size: 24px !important; color: #004aad !important; }
        .gr-description { font-size: 16px !important; color: #0066cc !important; }
    """
).launch()

Layout Example:
scale=7: Textbox takes 70% width (7 / (7+2+1)).
container=False: No border/padding.
max_length=100: Limits input.
Placeholder Example:
gr.ChatInterface(
    yes_man,
    type="messages",
    chatbot=gr.Chatbot(placeholder="<strong>Your Personal Yes-Man</strong><br>Ask Me Anything"),
    ...
)

➕ Additional Inputs
Add inputs like sliders via additional_inputs:
import gradio as gr
import time

def echo(message, history, system_prompt, tokens):
    response = f"System prompt: {system_prompt}\n Message: {message}."
    for i in range(min(len(response), int(tokens))):
        time.sleep(0.05)
        yield response[: i + 1]

demo = gr.ChatInterface(
    echo,
    type="messages",
    additional_inputs=[
        gr.Textbox("You are helpful AI.", label="System Prompt"),
        gr.Slider(10, 100),
    ],
).launch()

Inputs appear in a gr.Accordion() unless pre-rendered in gr.Blocks.
📜 Collecting User Feedback
Enable feedback with flagging_mode="manual":
import time
import gradio as gr

def slow_echo(message, history):
    for i in range(len(message)):
        time.sleep(0.05)
        yield "You typed: " + message[: i + 1]

demo = gr.ChatInterface(
    slow_echo,
    type="messages",
    flagging_mode="manual",
    flagging_options=["Like", "Spam", "Inappropriate", "Other"],
).launch()

"Like" shows as thumbs-up; others appear in a dropdown.

🧠 Part 2: Powering Intelligence with OpenAI
🔑 1. Obtaining an OpenAI API Key
Prerequisites:
OpenAI account.
Email for verification.
Payment method (post-trial).
Basic environment variable knowledge.
📝 Step-by-Step Instructions
Create an OpenAI Account
Visit OpenAI.
Click Sign Up, use email or Google/Microsoft account.
Verify via email and log in.
Generate an API Key
Go to API Keys.
Click Create new secret key, name it (e.g., MyGPTProject), select Default project.
Copy the key (e.g., sk-proj-WOyfaLCiXq...). It’s shown once.
Store Securely
Add to .env:
OPENAI_API_KEY=sk-proj-WOyfaLCiXq...


Load in Python:
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set")


Set Up Billing
Go to Billing.
Add payment method, purchase $5 credits (expire in 1 year).
Verify in Credit grants.
Set usage limits to control spending.
Test the Key
Use OpenAI Playground to test prompts.
Check for errors (e.g., “exceeded quota”).
Best Practices:
Secure Key: Use .env, never hardcode.
Monitor Usage: Track credits in Billing.
Regenerate if Compromised: Create new key, delete old.
Note: Google AI API offers free keys for testing, unlike OpenAI’s post-trial billing.
⚡️ 2. OpenAI API Basics
🖥️ 2.1 First Demo
pip install openai

from openai import OpenAI

client = OpenAI(api_key="sk-proj-...")

response = client.responses.create(
    model="gpt-4o",  # Corrected from gpt-4.1
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)

Output:
As the moonlight sparkled over the enchanted forest, a gentle unicorn named Starbeam tiptoed through the dewdrops, leaving trails of shimmering dreams for all the sleeping creatures.

Response output:
[
    {
        "id": "msg_67b73f697ba4819183a15cc17d011509",
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "output_text",
                "text": "As the moonlight sparkled over the enchanted forest, a gentle unicorn named Starbeam tiptoed through the dewdrops, leaving trails of shimmering dreams for all the sleeping creatures.",
                "annotations": []
            }
        ]
    }
]

Warning: output may include tool calls; use output_text for text.
OpenAI Client:
OpenAI() creates a client instance.
Parameters: api_key (required), max_retries (default 2), timeout (default 10 minutes).
Methods: responses.create (text generation), chat.completions.create (chat).
Note: Model "gpt-4.1" is likely a typo; use "gpt-4o". Your project’s "gpt-4.1-nano-2025-04-14" is non-standard—verify availability. See Models.
Responses are stored for 30 days (disable with store=False). OpenAI claims not to train on API data without consent.
✍️ 2.3 Text Generation and Prompting
Prompt Engineering: Crafting prompts is an art and science due to non-deterministic outputs. Techniques vary by model.
Message Roles:
Use instructions or roles:
response = client.responses.create(
    model="gpt-4o",
    instructions="Talk like a pirate.",
    input="Are semicolons optional in JavaScript?",
)
print(response.output_text)

Equivalent to:
response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "developer", "content": "Talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in JavaScript?"}
    ]
)
print(response.output_text)

developer: System rules.
user: Inputs.
instructions: Apply only to current request; reapply for multi-turn chats.
Prompt Caching: Place reusable content early:
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "system", "content": "You are a friendly assistant, answering concisely and accurately.\n"},
    {"role": "user", "content": "What's the weather like today?"}
  ]
}

📡 2.4 Response API
The responses endpoint supports text/image inputs and text/JSON outputs, with tools like file search.
Create a Response:
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "input": "Tell me a three sentence bedtime story about a unicorn."
  }'

In Python:
response = client.responses.create(
    model="gpt-4o",
    input="Tell me a three sentence bedtime story about a unicorn."
)
print(response)

Postman:
Method: POST
URL: https://api.openai.com/v1/responses
Auth: OpenAI API, Key: sk-proj-...
Body: JSON
{
    "model": "gpt-4o",
    "input": "Tell me a three sentence bedtime story about a unicorn."
}


Parameters:
input: Text/image/file (required).
model: E.g., gpt-4o (required).
instructions: System message.
max_output_tokens: Limits output tokens.
previous_response_id: Links multi-turn chats.
stream: Enable SSE streaming (default false).
temperature: 0–2 (default 1).
truncation: auto or disabled (default).
store: Store responses (default true).
Response Object:
{
  "id": "resp_67ccd2bed1ec8190b14f964abc0542670bb6a6b452d3795b",
  "object": "response",
  "created_at": 1741476542,
  "status": "completed",
  "model": "gpt-4o",
  "output": [
    {
      "type": "message",
      "id": "msg_67ccd2bf17f0819081ff3bb2cf6508e60bb6a6b452d3795b",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "In a peaceful grove beneath a silver moon, a unicorn named Lumina discovered a hidden pool that reflected the stars. As she dipped her horn into the water, the pool began to shimmer, revealing a pathway to a magical realm of endless night skies. Filled with wonder, Lumina whispered a wish for all who dream to find their own hidden magic, and as she glanced back, her hoofprints sparkled like stardust.",
          "annotations": []
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 36,
    "output_tokens": 87,
    "total_tokens": 123
  },
  ...
}

Fields:
output_text: Aggregated text (SDK-only).
previous_response_id: For multi-turn context.
usage: Token breakdown.

🤝 Part 3: Uniting Gradio and OpenAI for a Smart Chatbot
💬 3.1 Console-Based Interaction
A simple console chatbot:
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def chat():
    while True:
        print("-----type q to quit----------")
        user_input = input("please input: ")
        if user_input == "q":
            print("bye")
            break
        response = client.responses.create(
            model="gpt-4o",
            input=user_input
        )
        print("AI say: ", response.output_text)
        print(response.id)

chat()

Run to interact; type q to quit.
🌐 3.2 Building a Gradio + OpenAI Chatbot
A web-based chatbot:
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

def chat(current_msg, history_msg, max_output_tokens, temperature):
    instructions = "You are a friendly assistant chatbot. Answer directly and concisely."
    ans = ""
    try:
        response = client.responses.create(
            input=current_msg,
            instructions=instructions,
            model="gpt-4o",
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )
        logger.info(f"max_output_tokens: {max_output_tokens}. temperature: {temperature}")
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
    additional_inputs=[
        gr.Slider(minimum=1, maximum=2048, value=256, step=1, label="Max output tokens"),
        gr.Slider(minimum=0.1, maximum=2.0, value=1.0, step=0.1, label="Creativeness"),
    ],
)

if __name__ == "__main__":
    chatbot.launch()

Callback Function: chat must include current_msg and history_msg for gr.ChatInterface, even if history_msg is unused.
Parameters:
temperature: Controls randomness (0.1–2.0, default 1.0).
max_output_tokens: Limits output (1–2048, default 256).
🎨 3.3 Customizing with CSS and Conversation State
Create styles.css:
body {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}
.gradio-container, .gradio-app {
    border-radius: 16px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4) !important;
}
.gr-title {
    font-size: 2.2rem !important;
    color: #f4d35e !important;
    text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5) !important;
    margin-bottom: 8px !important;
}
.gr-description {
    font-size: 1.1rem !important;
    color: #d4c9e1 !important;
    margin-bottom: 16px !important;
}
.gr-textbox textarea {
    background: #3a2f4a !important;
    color: #f2e9e4 !important;
    border: 2px solid #7b5ea7 !important;
    border-radius: 12px !important;
    padding: 12px !important;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.3) !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
.gr-textbox textarea:focus {
    border-color: #f4d35e !important;
    box-shadow: 0 0 10px rgba(244, 211, 94, 0.5) !important;
    outline: none !important;
}
.gr-chatbot .message.user {
    background: linear-gradient(135deg, #4a3b5a, #6b5b95) !important;
    color: #f2e9e4 !important;
    border-radius: 18px 4px 18px 4px !important;
    padding: 12px 16px !important;
    margin: 8px 0 !important;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3) !important;
}
.gr-chatbot .message.bot {
    background: linear-gradient(135deg, #6b5b95, #9b89b3) !important;
    color: #f2e9e4 !important;
    border-radius: 4px 18px 4px 18px !important;
    padding: 12px 16px !important;
    margin: 8px 0 !important;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3) !important;
}
.gr-slider .wrap {
    color: #d4c9e1 !important;
}
.gr-slider .slider {
    accent-color: #f4d35e !important;
    height: 6px !important;
    border-radius: 3px !important;
}
.gr-slider .slider::-webkit-slider-thumb {
    background: #f4d35e !important;
    border: 2px solid #3a2f4a !important;
    border-radius: 50% !important;
    width: 18px !important;
    height: 18px !important;
    cursor: pointer !important;
}
.gr-button, button.gr-button {
    background: #f4d35e !important;
    color: #2b1d3a !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.2s ease !important;
}
.gr-button:hover, button.gr-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 12px rgba(0, 0, 0, 0.5) !important;
    background: #f7e084 !important;
}
button[aria-label='Retry'] {
    display: none !important;
}

Enhanced chatbot with CSS and previous_response_id:
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
    global previous_response_id
    instructions = "You are a friendly assistant chatbot. Answer directly and concisely."
    ans = ""
    try:
        response = client.responses.create(
            input=current_msg,
            instructions=instructions,
            model="gpt-4o",
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            previous_response_id=previous_response_id,
        )
        ans = response.output_text
        previous_response_id = response.id
        logger.info(f"max_output_tokens: {max_output_tokens}. temperature: {temperature}")
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

Conversation State:
previous_response_id: Chains responses for threaded conversations.
Context Window: Total tokens (input + output + reasoning). E.g., gpt-4o-2024-08-06 has 128k tokens, max 16,384 output tokens.
Large prompts risk truncation; monitor token usage.

