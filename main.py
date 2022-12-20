from bot import Bot

if __name__ == "__main__":
    bot = Bot()
    print("Chatbot is ready to talk with you! Say goodbye to the bot to end the session.")
    while bot.get_current_context() != "exit":
        message = input("You:")
        response = bot.get_bot_response(message)
        print("Bot:", response)