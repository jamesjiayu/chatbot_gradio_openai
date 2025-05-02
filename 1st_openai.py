import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") 

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-4.1-nano",
    #"gpt-4.1",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
