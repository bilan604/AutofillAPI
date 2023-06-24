
import optparse
import openai
from dotenv import load_dotenv
load_dotenv()


def askGPT4(api_key, query):
    print("ASK GPT 4 CALLED")
    query = "This is a test message. Can you confirm?"
    message=[{"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages = message,
        temperature=0.2,
        max_tokens=1000,
        frequency_penalty=0.0
    ).choices[0]

    return response

openai.api_key = "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"
print(askGPT4("", ""))