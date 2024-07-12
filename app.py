from flask import Flask, request, jsonify
from flask_cors import CORS
from chat import get_response  # This imports from your chat.py file

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
