from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from slm import SLM
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
     supports_credentials=False)

@app.route('/api/ask', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"],
              allow_headers=["Content-Type"],
              methods=["POST", "OPTIONS"])
              
def ask():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    question = data.get('question', '')
    model = SLM("Derek")
    response = model.respond(question)
    message = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            try:
                # Parse line as JSON object
                json_data = json.loads(line)
                if "message" in json_data and "content" in json_data["message"]:
                        message += json_data["message"]["content"]
            except json.JSONDecodeError:
                message += f"\nFailed to parse line: {line}"
    return jsonify({
        'question': question,
        'answer': f"{message}"
    })

if __name__ == '__main__':
    app.run(host="localhost", port=5050, debug=True)
