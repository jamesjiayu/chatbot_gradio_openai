
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def chat():
    while True:
        print("-----type q to quit----------")
        user_input = input("please input: ")
        if user_input == "q":
            print("bye")
            break
        response = client.responses.create(
            model="gpt-4.1-nano-2025-04-14",
            input=user_input
        )
        print("AI say: ", response.output_text)
        print(response.id)

chat()
