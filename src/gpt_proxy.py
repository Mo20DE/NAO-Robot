from openai import OpenAI
from constants import *

import os
import sys 
import json

# create an openai client
client = OpenAI(api_key=API_KEY)

def send_request(prompt, model, img=None):
    '''
    Sends http requests to gpt server 
    and gets the response back.
    '''
    # load chat data
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'r') as json_file:
            original_messages = json.load(json_file)
    else:
        original_messages = [{'role': 'system', 'content': GPT_CONTEXT}]
    
    messages = original_messages.copy()
    if model == 'GPT-4' and 'True' != img != 'False':
        # check if image was provided
        prompt = [
            {'type': 'text', 'text': prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}", "detail": "low"}}
        ]
    elif model == 'GPT-3' and img == 'True':
        # filter data
        messages = [entry for entry in original_messages if not isinstance(entry['content'], list)]

    # add the user prompt to the history
    entry = {'role': 'user', 'content': prompt}
    messages.append(entry)
    original_messages.append(entry)

    response = client.chat.completions.create(
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        model=GPT_MODELS[model]
    )

    message = response.choices[0].message
    original_messages.append({'role': message.role, 'content': message.content})
    # save the chat history
    with open(HISTORY_PATH, 'w') as json_file:
        json.dump(original_messages, json_file, indent=2)
        
    #print(f"Current model: {model}")
    
    return message.content

response = send_request(sys.argv[1], sys.argv[2], sys.argv[3])
print(response)
