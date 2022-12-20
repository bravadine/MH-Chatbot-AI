from bot import Bot
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/bot-reply", methods=["GET","POST"])
def get_reply():
    bot = Bot("Khennet")
    if request.method == "POST":
        content = request.json
        response = bot.get_bot_response(content["message"])
        context = bot.get_current_context()
        data = {
            "status": "ok",
            "response": response,
            "context": context
        }
        return jsonify(data)
