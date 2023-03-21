
# https://platform.openai.com/docs/guides/chat



import openai
import os
from dotenv import load_dotenv
load_dotenv()

# Getting bearer token from .env file
open_ai_token = os.getenv("OPENAI_TOKEN")

openai.api_key = open_ai_token

def get_results( prompt = 'Say Working', max_tokens = 1000 ):

    return openai.ChatCompletion.create(
    max_tokens=max_tokens,
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are my assistant who writes tweets."},
            {"role": "user", "content": prompt}
        ],
    n=3
    )
def run(prompt, emojiOption):
    # print('Ctrl+C to quit.')
    # while True:
    # prompt = input('Prompt: ')
    if emojiOption == 'with-emojis':
        prompt_str = f'Write twitter post for keyword : {prompt} with emojis'
    else:
        prompt_str = f'Write twitter post for keyword : {prompt} without emojis'
    result = get_results(prompt_str)
    # print(result)
    results_arr = []
    for choice in result['choices']:
        results_arr.append(choice['message']['content'])
    return results_arr
def runThreads(prompt, emojiOption, description):
    # print('Ctrl+C to quit.')
    # while True:
    # prompt = input('Prompt: ')
    if emojiOption == 'with-emojis':
        prompt_str = f'Write twitter thread for keyword : {prompt} with emojis'
    else:
        prompt_str = f'Write twitter thread for keyword : {prompt} without emojis'
    if description != '' and description != None:
        prompt_str += f" including {description}"
    result = get_results(prompt_str)
    # print(result)
    results_arr = []
    for choice in result['choices']:
        results_arr.append(choice['message']['content'])
    return results_arr
# if __name__ == '__main__':
#     data = run()
#     print(data)
