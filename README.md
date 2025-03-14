# NAO Robot Interaction System

This repository contains the code for a specialized interaction system for the NAO robot, utilizing OpenAI's GPT-3 and GPT-4 models.

## Overview

The system is designed to handle two primary types of tasks:
1. Conversational Responses
2. Movement Commands

### Architecture

A proxy receives voice commands and selects between GPT-3 (fast & text-based) and GPT-4 (capable of image processing). If needed, the robot captures an image and sends it along with the prompt to OpenAI’s backend. The response is processed and forwarded to the NAO robot, which then speaks and/or performs corresponding movements.

![Picture](Code%20Architecture.png)

### GET_MODEL_CONTEXT

The interaction system differentiates between text-based chat and image analysis requests to decide whether to use GPT-3 or GPT-4.

- **GPT-4**: Utilized for image-related requests. 
  Examples include analyzing images, describing visible elements, identifying obstacles, etc.
- **GPT-3**: Employed for conversational or command inquiries.
  Examples include general questions, trivia, movement instructions without images, etc.

### GPT_CONTEXT

For conversations, the system responds briefly and politely, avoiding repetitive answers. Examples include jokes, trivia, personal introductions, and more.

For movement commands, the system analyzes images or instructions and responds with succinct movement descriptions. The movement format is specified as `(x, y, r)`, representing distances and rotation.

The robot can also take images to e.g. describe their content, activated only when passing a keyword (default: 'snap') in the command.

## Examples

Below are some examples illustrating how the system responds to different types of queries:

### Conversational Examples

- "Tell me something about you" -> A brief self-introduction.
- "Tell me a funny joke?" -> A short joke.
- "What's the capital of France?" -> "It's Paris."

### Movement Command Examples

- "Move forward" -> move(0.5, 0, 0) -> [actual movement]
- "Turn around" -> move(0, 0, 3.14) -> [actual movement]
- "Go back" -> move(0, -0.5, 0) -> [actual movement]

## Usage

To use this system, ensure you have the appropriate model (GPT-3 or GPT-4) depending on the task type. The system is designed to be straightforward and intuitive, requiring minimal setup, considering it has to run scripts on 2 different python versions.

### Installation
- install Nao API
- install both Python 2.7 and 3.9
- install openai, speechrecognition for python 3.9

### Confuguration
File constants.py contains all the configurable parameters. The ones that have to be set up are:
- PYTHON_3_9_PATH (path to python 3.9 exe file)
- IP (Nao's IP address)
- MICROPHONE_ID (id of the deviced used for voice recognition, microphones and their IDs can be listed using list_microphones.py)

### Running
Run main.py file (using python 2.7!!)
