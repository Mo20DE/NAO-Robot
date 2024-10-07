from naoqi import ALProxy
from constants import *

import threading
import base64
import platform
import subprocess
import os

# initialize necessary modules
photoProxy = ALProxy("ALPhotoCapture", IP, PORT)
tts = ALProxy("ALTextToSpeech", IP, PORT)
#tts.setVoice("Kenny22Enhanced")

motion = ALProxy("ALMotion", IP, PORT)
motion.setStiffnesses("Body", 1.0)
motion.moveInit()

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
    global tts
    tts.say(text)
    print("Speaking: {}.".format(text))

def move(x, y, r):
    '''
    Moves NAO to specific position:
    x - distance along X axis in meters
    y - distance along Y axis in meters
    r - rotation around Z axis in radians.
    '''
    global motion
    motion.moveTo(x, y, r) # blocking function
    print("Moving x={}m, y={}m and rotating {}.".format(x, y, r))

def move_sequence(mvs):
    '''
    Executes a sequence of moves.
    '''
    for mv in mvs:
        move(mv[0], mv[1], mv[1])

def stop():
    '''
    Stops the current action of NAO.
    '''
    global tts, motion
    tts.stopAll()
    motion.stopMove()
    speak("Stopping current action.")

def takeImage():
    '''
    Captures an image from NAO robot, 
    saves it and encodes it to base64.
    '''
    global photoProxy
    resolution = 1    # VGA
    colorSpace = 11   # RGB

    photoProxy.setResolution(resolution)
    photoProxy.setColorSpace(colorSpace)
    
    # get a camera image and save it
    print(IMAGE_PATH)
    photoProxy.takePicture(IMAGE_PATH)
    # encode image to base64
    with open(IMAGE_PATH, 'rb') as img_file:
        image = base64.b64encode(img_file.read()).decode('utf-8')

    return image

def recognize_sentence():
    '''
    Captures human voice and convert it to readable text.
    '''
    command = [PYTHON_3_9_PATH, SCRIPT_NAME_STT]
    # Run the command
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode == 0:
            return output

        print("An error occurred: {}".format(error))
    # catch any exception
    except Exception as e:
        print("An error occurred: {}".format(e))

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
    command = [PYTHON_3_9_PATH, SCRIPT_NAME_GPT_PROXY, prompt, model, image]
    # Run the command
    try:
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
    global motion
    host = platform.node()
    #speak("Connecting to {}".format(host))

    image_made = False # flag for model selection
    text_mode = False # True - text | False - speech
    delete_history()

    while True:

        speak("Awaiting command.")
        if text_mode:
            command = raw_input("Input command: ") # raw_input is python2 function to get input as text. Otherwise it tries to evaluate the text as a python expression...
        else:
            print("Wating for voice command...")
            command = recognize_sentence()
        
        command = command.strip()
        #print(command)

        if not command or command == "[Not understood]": 
            speak("Command not understood.")
            continue
        #else:
        #    speak(command)

        if command in ["stop", "kill"]:
            speak("Stopping current action.")
            stop()
            continue

        elif command in ["exit", "quit"]:
            stop()
            speak("Disconnecting from {}".format(host))
            delete_history()
            break
        
        ## communicate with gpt ##
        if PHOTO_KEYWORD in command:
            image_made = True
            img = takeImage()
            response = send_request_to_gpt(command, "GPT-4", image=img)
        elif not image_made:
            response = send_request_to_gpt(command, "GPT-3", "False")
        else:
            model = get_gpt_model(command) # decide which model to use
            #print("Decision: {}".format(model))
            response = send_request_to_gpt(command, model, "True")

        sentences, moves = process_response(response)
        # check if nao is moving
        if not motion.moveIsActive():
            for sentence in sentences:
                speak(sentence)
            # run the moves in a thread
            if moves:
                t = threading.Thread(target=move_sequence, args=(moves,))
                t.run() 
                # for mv in moves:
                #     move(mv[0], mv[1], mv[2])
        else:
            speak("I am moving at the moment. Please wait.")

# run main loop
main()
    