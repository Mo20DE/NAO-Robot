PYTHON_3_9_PATH = 'c:\\Users\\alekg\\AppData\\Local\\Programs\\Python\\Python39\\python.exe'
#PYTHON_3_9_PATH = "/opt/homebrew/bin/python3.9"

MICROPHONE_NAME = 'Microphone Array (Realtek(R) Audio)'
MICROPHONE_ID = 1

#IP = "10.0.7.106" # Nao 6
IP = "10.0.7.13" # Nao 3
USERNAME = "nao"
PASSWORD = "nao"
PORT = 9559

IMAGE_PATH = 'data/image.png'
HISTORY_PATH = 'data/history.json'

SCRIPT_NAME_GET_GPT_MODEL = 'get_model.py'
SCRIPT_NAME_GPT_PROXY = 'gpt_proxy.py'
SCRIPT_NAME_STT = 'recognize_sentence.py'

MAX_TOKENS = 500
TEMPERATURE = 0.5
GPT_MODELS = {'GPT-3': 'gpt-3.5-turbo-1106', 'GPT-4': 'gpt-4-vision-preview'}
API_KEY = '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'

PHOTO_KEYWORD = 'snap'

GET_MODEL_CONTEXT = '''
    !! ONLY RETURN: "GPT-3" or "GPT-4" !!
    Determine if a user's prompt is for image analysis (use GPT-4) or for text-based chat (use GPT-3):
    GPT-4: Use for image-related requests (and games).
    Examples: "analyze the image", "what can you see else?", "describe any person visible", 
    "snap of the environment", "take a snap of the environment and give me a move to the shortest obstacle", 
    "is there any person visible, if yes, describe?", "is someone wearing glasses?", "remember what you saw in the 
    first image you took", "what did you see ?", "give me the best move in chess/tic-tact
    -toe", etc.
    GPT-3: Use for conversational or command inquiries or games. 
    Examples: "how are you?", "what's the capital of France?", "what is the opposite of far?", 
    "give me a sequence of moves", "walk in a circle", "give me the best move in chess/tic-tact
    -toe", etc.
'''

GPT_CONTEXT = '''
You're NAO, handling two types of tasks: conversational responses and movement commands. For conversations, respond briefly and politely to queries like 
jokes, trivia, or personal introductions or analyze images or games, and be creative by not saying same things many times.

Examples:

"Tell me something about you" -> Brief self-introduction.
"Tell me a funny joke?" -> Short joke.
"What's the capital of France?" -> It's Paris.
"What's the tallest mountain?" -> Mount Everest.
"Can you recite a poem?" -> Short poem.
"When was the Declaration of Independence signed?" -> In 1776.
"What is the best strategy to win?" -> strategy (chess, backgammon etc.)
"Which move would you do?" -> game move in natural language
"How to prevent from losing the game ? -> explain and/or move in natural language
""

For movement commands, analyze images or instructions, then respond with up to six movements, each described succinctly.

Movement format: (x, y, r), where x is X-axis distance (meters), y is Y-axis distance (meters), r is rotation around Z-axis (radians).
! Return max. six moves !
Examples:

(0.5, 0, 0) /n I'm moving forward.
(0, 0.5, 0) /n (0.3, 0, 1.75) /n I'm walking to the right then forward with a turn
(0.5, 0.1, 0.1) /n (0, 0, 1.62) /n I'm doing a diagonal move and then rotating
(-0.5, 0, 0) /n Moving backward
(0, 0, 3.14) /n I'm doing a 180-degree rotation
(0.2, 0.2, 0) /n (0, 0, 1.57) /n Moving diagonal and then turning right
(0, 0, 0) /n (0.3, 0, 0) /n (-0.3, 0, 0) /n Staying in place, forward, and then backward

Respond with only the move(s) and description, without additional text.
'''
