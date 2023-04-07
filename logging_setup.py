import logging

import telebot

from apikeys import logging_bot_token, admin_chat_id

logging.basicConfig(
    format="%(asctime)s => %(filename)s => %(levelname)s => %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs.txt"
)

main_formatter = logging.Formatter("%(asctime)s => %(filename)s => %(levelname)s => %(message)s")

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(main_formatter)

file_handler = logging.FileHandler(filename="important.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(main_formatter)


# Telegram bot handler
class TelegramBotHandler(logging.Handler):
    def __init__(self, api_key, chat_id):
        super().__init__()
        self.api_key = api_key
        self.chat_id = chat_id

    def emit(self, record):
        bot = telebot.TeleBot(self.api_key)
        bot.send_message(self.chat_id, self.format(record))


telegram = TelegramBotHandler(logging_bot_token, admin_chat_id)
telegram.setLevel(logging.CRITICAL)
telegram.setFormatter(main_formatter)

root_logger = logging.getLogger("")

root_logger.addHandler(console)
root_logger.addHandler(file_handler)
root_logger.addHandler(telegram)

logging.critical("Test")