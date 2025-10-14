Prompt
----------

## Role: You are an experienced single page application web developer with 10+ years of front end experience.  

## Context: I want to make a quick CLI command reference guide for LM Studio where I will be using LM Studio at the backend as my LLM.  

## Instructions: 
- I will have HTML page with JS as my front end 
- LMStudio  will be serving REST API at 1234 port 
- I want to use Javascript code on my html page that will send the API requests and get the API requests from LM Studio Backend.   

## Curl Command example to my endpoint - 

"""

curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen/qwen3-4b",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
      { "role": "user", "content": "What day is it today?" }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
}'

""" 


Task:
- Convert this curl command into Javascript code that will call and fetch the api content based on user prompted query    
- Have an input text field called "Question" and then a submit button.
- onSubmit we should send the user question as "content" in ''' { "role": "user", "content": "What day is it today?" } '''
- I want to have my system role's content to be
'''
Usage
lms <subcommand>

where <subcommand> can be one of:

- chat - Open an interactive chat with the currently loaded model.
- status - Prints the status of LM Studio
- server - Commands for managing the local server
- ls - List all downloaded models
- ps - List all loaded models
- get - Searching and downloading a model from online.
- load - Load a model
- unload - Unload a model
- create - Create a new project with scaffolding
- log - Log operations. Currently only supports streaming logs from LM Studio via `lms log stream`
- dev - Starts the development server for the plugin in the current folder.
- push - Uploads the plugin in the current folder to LM Studio Hub.
- clone - Clone an artifact from LM Studio Hub to a local folder.
- login - Authenticate with LM Studio
- import - Import a model file into LM Studio
- flags - Set or get experiment flags
- bootstrap - Bootstrap the CLI
- version - Prints the version of the CLI

For more help, try running `lms <subcommand> --help`
'''"
