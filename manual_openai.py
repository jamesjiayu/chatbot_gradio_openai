
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def chat():
    previous_response_id=None
    while True:
        print("-----type q to quit----------")
        user_input = input("please input: ")
        if user_input == "q":
            print("bye")
            break
        response = client.responses.create(
            model="gpt-4.1-nano",
            input=user_input,
            previous_response_id=previous_response_id
        )
        print("AI say: ", response.output_text)
        print(response.id)
        previous_response_id=response.id

chat()

