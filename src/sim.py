from constants import *

import base64
import platform
import subprocess
import os

import random

IMAGES = ['data/img1.png', 'data/img2.png'] # for testing

def delete_history():
    '''
    Deletes the the chat history.
    '''
    if os.path.exists(HISTORY_PATH):
        os.remove(HISTORY_PATH)

def speak(text):
    '''
    Let's NAO speak a given text.
    '''
    print("Speaking: {}.".format(text))

def move(x, y, r):
    '''
    Moves NAO to specific position:
    x - distance along X axis in meters
    y - distance along Y axis in meters
    r - rotation around Z axis in radians.
    '''
    print("Moving x={}m, y={}m and rotating {}.".format(x, y, r))

def stop():
    '''
    Stops the current action of NAO.
    '''
    print("Stopping current action.")

def recognize_sentence():
    '''
    Captures human voice and convert it to readable text.
    '''
    # Running the script and capturing its output
    command = [PYTHON_3_9_PATH, SCRIPT_NAME_STT]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode == 0:
            return output

        print("An error occurred: {}".format(error))
    except Exception as e:
        print("An exception occurred: {}".format(e))

def get_gpt_model(prompt):
    '''
    Figures out which model the user wants to use.
    '''
    command = [PYTHON_3_9_PATH, SCRIPT_NAME_GET_GPT_MODEL, prompt]
    # Run the command
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Get the output and error (if any)
        output, error = process.communicate()
        if process.returncode == 0:
            # decide which model to use
            model = output.strip()
            return "GPT-4" if model == "GPT-4" else "GPT-3"
        
        print("An error occurred: {}".format(error))
    # catch any exception
    except Exception as e:
        print("An exception occurred: {}".format(e))

def send_request_to_gpt(prompt, model, image=""):
    '''
    Sends http requests to GPT server and get a text/commands.
    '''
    # Command to run Python 3 script. Adjust the Python 3 path as necessary.
    command = [PYTHON_3_9_PATH, SCRIPT_NAME_GPT_PROXY, prompt, model, image]
    # Run the command
    try:
        print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Get the output and error (if any)
        output, error = process.communicate()
        if process.returncode == 0:
            return output

        print("An error occurred: {}".format(error))
    # catch any exception
    except Exception as e:
        print("An exception occurred: {}".format(e))

def process_response(response):
    '''
    Processes the response from gpt into text and moves.
    '''
    sentences, moves = [], []
    entries = response.splitlines()
    for entry in entries:
        entry = entry.strip()
        if not entry: continue
        if entry[0] == '(' and entry[-1] == ')' and entry.count(',') == 2:
            moves.append(eval(entry))
        else:
            sentences.append(entry)

    return sentences, moves

def main():
    '''
    Main loop that handles text and 
    voice prompts/commands and executes 
    them on NAO robot using GPT-4 Model.
    '''
    host = platform.node()
    speak("Connecting to {}".format(host))

    image_made = False # flag for model selection
    text_mode = True # True - text | False - speech
    delete_history()

    while True:

        if text_mode:
            command = raw_input("Input command: ") # raw_input is python2 function to get input as text. Otherwise it tries to evaluate the text as a python expression...
        else:
            print("Wating for voice command...")
            command = recognize_sentence()
        
        command = command.strip()
        
        if not command or command == "[Not understood]": 
            speak("Command not understood.")
            continue

        elif command in ["stop", "kill"]:
            speak("Stopping current action.")
            stop()
            continue

        elif command in ["exit", "quit"]:
            speak("Disconnecting from {}".format(host))
            stop()
            break
        
        ## communicate with gpt ##
        if PHOTO_KEYWORD in command:
            image_made = True
            img_path = random.choice(IMAGES)
            with open(img_path, "rb") as img_file:
                img = base64.b64encode(img_file.read()).decode("utf-8")
                response = send_request_to_gpt(command, "GPT-4", image=img)
        elif not image_made:
            response = send_request_to_gpt(command, "GPT-3", "False")
        else:
            model = get_gpt_model(command)
            print("Decision: {}".format(model))
            response = send_request_to_gpt(command, model, "True")
        
        sentences, moves = process_response(response)
        for sentence in sentences:
            speak(sentence)
        for mv in moves:
            move(mv[0], mv[1], mv[2])

# run main loop
main()
