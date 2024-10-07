from openai import OpenAI
from constants import *

import sys

# create an openai client
client = OpenAI(api_key=API_KEY)

def get_model(prompt):
    '''
    Figures out which model to use.
    '''
    messages = [
        {'role': 'system', 'content': GET_MODEL_CONTEXT},
        {'role': 'user', 'content': prompt}
    ]
    response = client.chat.completions.create(
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        model=GPT_MODELS['GPT-3']
    )
    
    return response.choices[0].message.content

response = get_model(sys.argv[1])
print(response)
