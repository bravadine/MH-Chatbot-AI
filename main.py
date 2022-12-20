from bot import Bot

if __name__ == "__main__":
    bot = Bot("Charlie")
    print("Chatbot is ready to talk with you! Say goodbye to the bot to end the session.")

    while bot.chat_context() != "EXIT_PROGRAM":
        message = input("\nYou: ")
        response = bot.chat_respond(message)
        print("Bot:", response)
