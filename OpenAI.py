
# https://platform.openai.com/docs/guides/chat



import openai
import os
from dotenv import load_dotenv
load_dotenv()

# Getting bearer token from .env file
open_ai_token = os.getenv("OPENAI_TOKEN")

openai.api_key = open_ai_token

def get_results( prompt = 'Say Working', max_tokens = 200, temperature = 0.5 ):

    return openai.ChatCompletion.create(
    temperature=temperature,
    max_tokens=max_tokens,
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are my assistant who writes youtube video descriptions."},
            {"role": "user", "content": prompt}
        ],
    n=3
    )
def run():
    print('Ctrl+C to quit.')
    # while True:
    prompt = input('Prompt: ')
    result = get_results(prompt)
    # print(result)
    results_arr = []
    for choice in result['choices']:
        results_arr.append(choice['message']['content'])
    print(results_arr)

if __name__ == '__main__':
    run()
