from datetime import datetime

from telebot import TeleBot

from src.utils.messages import get_message_for_today, get_message_for_next_rehearsal


class OrchestraBot:
    def __init__(self, token: str, group_id: str):
        self.bot = TeleBot(token)
        self.group_id = group_id

        @self.bot.message_handler(commands=['start'])
        def send_start(message):
            self.bot.send_message(message.chat.id, get_message_for_today(), allow_sending_without_reply=True)

        @self.bot.message_handler(commands=['опрос', 'poll'])
        def rehearsal_today(message):
            self.bot.send_poll(message.chat.id,
                               question=f'Репетиция сегодня, {datetime.now().strftime("%d.%m")}',
                               options=['Буду', 'Не смогу и т/д'], is_anonymous=False)

        @self.bot.message_handler(commands=['time'])
        def time_now(message):
            self.bot.send_message(message.chat.id, 'Время на сервере ' + datetime.now().strftime('%H:%M'))

        @self.bot.message_handler(commands=['next'])
        def next_rehearsal(message):
            self.bot.send_message(message.chat.id, get_message_for_next_rehearsal())

    def start(self):
        self.bot.infinity_polling()
