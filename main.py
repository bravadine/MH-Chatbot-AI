from bot import Bot

if __name__ == "__main__":
    bot = Bot()
    while True:
        message = input("You : ")
        response = bot.get_bot_response(message)
        print("Bot :",response)