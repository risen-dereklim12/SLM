import ollama

client = ollama.Client()

# Define the model and the input prompt
model = "mistral-nemo"  # model name
prompt = "What is PDPA?"

# Send the query to the model
response = client.generate(model=model, prompt=prompt)

# Print the response from the model
print("Response from Derek:")
print(response.response)