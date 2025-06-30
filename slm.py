import requests
import json

class SLM:
    def __init__(self, model_name):
        # Base URL for the local Ollama API
        self.url = "http://localhost:11434/api/chat"
        self.model_name = model_name

    def respond(self, question): 
        # Define the model and the input prompt
        payload = {
            "model": "Derek",  # Replace with the model name
            "messages": [{"role": "user", "content": f"{question}"}]
        }

        # To grab responses as they are retrieved, set streaming to true
        response = requests.post(self.url, json=payload, stream=False)

        return response
        