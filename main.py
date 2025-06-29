import requests
import json

# Base URL for the local Ollama API
url = "http://localhost:11434/api/chat"

# Define the model and the input prompt
payload = {
    "model": "Derek",  # Replace with the model name
    "messages": [{"role": "user", "content": "What is PDPA?"}]
}

# To grab responses as they are retrieved, set streaming to true
response = requests.post(url, json=payload, stream=True)

# If response status is 200, print the response
if response.status_code == 200:
    print("Streaming response from Derek:")
    for line in response.iter_lines(decode_unicode=True):
        if line:  # Ignore empty lines
            try:
                # Parse line as JSON object
                json_data = json.loads(line)
                # Print message content
                if "message" in json_data and "content" in json_data["message"]:
                    print(json_data["message"]["content"], end="")
            except json.JSONDecodeError:
                print(f"\nFailed to parse line: {line}")
    print()  # Ends with a newline
# Catch the error if the response status is not 200
else:
    print(f"Error: {response.status_code}")
    print(response.text)