from bot import Bot

if __name__ == "__main__":
    bot = Bot()
    print("Chatbot is ready to talk with you! Type \"quit\" to end the session.")
    while True:
        message = input("You:")
        if message.lower() == "quit":
            break
        response = bot.get_bot_response(message)
        print("Bot:", response)