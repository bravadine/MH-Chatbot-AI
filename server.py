from bot import Bot
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/bot", methods=["GET","POST"])
def get_reply():
    bot = Bot("Charles")

    if request.method == "GET":
        data = {
            "bot_name": bot.bot_name,
            "response": bot.greet()
        }
        return jsonify(data)

    if request.method == "POST":
        content = request.json
        response = bot.chat_respond(content["message"])
        context = bot.chat_context()
        data = {
            "bot_name": bot.bot_name,
            "response": response,
            "context": context
        }
        return jsonify(data)
