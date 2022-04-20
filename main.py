import CONFIG

from telebot import TeleBot


bot = TeleBot(CONFIG.TOKEN)


def main():
    bot.infinity_polling(True)


if __name__ == '__main__':
    main()
