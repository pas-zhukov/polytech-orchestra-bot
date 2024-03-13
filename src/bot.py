from telebot import TeleBot

from src.utils.messages import get_message_for_today


class OrchestraBot:
    def __init__(self, token: str, group_id: str):
        self.bot = TeleBot(token)
        self.group_id = group_id

        @self.bot.message_handler(commands=['start'])
        async def send_start(message):
            self.bot.send_message(message.chat.id, get_message_for_today(), allow_sending_without_reply=True)

        self.bot.infinity_polling()
