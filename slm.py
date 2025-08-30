import requests
from vector.client import VectorClient
from embedding.embedding import Embedding
import json

class SLM:
    def __init__(self, model_name):
        # Base URL for the local Ollama API
        self.url = "http://localhost:11434/api/chat"
        self.model_name = model_name

    def respond(self, question): 
        # Query vector database for context
        vector_db = VectorClient()
        # embed question
        embedding = Embedding()
        question_embedding = embedding.encode(question)
        context_result = vector_db.search(question_embedding["embeddings"][0], limit=7)
        context = ""
        for cr in context_result:
            # print(cr)
            context += cr.payload['text']
        print(context)
        # Add the context to the question
        question = f"Answer the {question} as PDPA Chatbot based on this: {context}. Do not answer anything out of the context. Do not hallucinate.\
            If the answer is not from the context, say 'I cannot find the answer in my knowledge base. Kindly reach out to a human for support'.\
            If the reply from this the context provided is beyond your context window limit, reply 'I shall summarize the reply as it has exceeded \
                my context window' and then reply with summary of the rest of the reply."
        # print(question)
        payload = {
            "model": self.model_name,  # Replace with the model name
            "messages": [{"role": "user", "content": f"{question}"}]
        }
        # Ask the model
        response = requests.post(self.url, json=payload, stream=True)
        
        # Return the model's response
        return response

        # # Define the model and the input prompt
        # payload = {
        #     "model": self.model_name,  # Replace with the model name
        #     "messages": [{"role": "user", "content": f"{question}"}]
        # }

        # # To grab responses as they are retrieved, set streaming to true
        # response = requests.post(self.url, json=payload, stream=False)

        return response

if __name__ == "__main__":
    slm = SLM("mistral-nemo")
    response = slm.respond("What is the advisory committee of the PDPA?")
    message = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            try:
                obj = json.loads(line)
                if "message" in obj and "content" in obj["message"]:
                    chunk = obj["message"]["content"]
                    print(chunk, end="", flush=True) 
            except json.JSONDecodeError:
                message += f"\nFailed to parse line: {line}"
                print(message, end="", flush=True)
    
    
        