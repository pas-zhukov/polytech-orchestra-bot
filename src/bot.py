from datetime import datetime

from telebot import TeleBot

from src.utils.messages import get_message_for_next_rehearsal, get_message_for_today, get_monthly_forecast


class OrchestraBot:
    def __init__(self, token: str, group_id: str):
        self.bot = TeleBot(token)
        self.group_id = group_id

        @self.bot.message_handler(commands=['start', 'today'])
        def send_start(message):
            self.bot.send_message(message.chat.id, get_message_for_today(), allow_sending_without_reply=True)

        @self.bot.message_handler(commands=['poll'])
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

        @self.bot.message_handler(commands=['help'])
        def help_mes(message):
            self.bot.send_message(message.chat.id,
                                  message.from_user.first_name + ', привет!\n'
                                                                      '/start или /today - Проверить доступность Белого Зала сегодня.\n'
                                                                      '/next - Проверить доступность Белого Зала на следующей репетиции.\n'
                                                                      '/poll - Запустить опрос: явка сегодня.\n'
                                                                      '')

        @self.bot.message_handler(commands=['forecast'])
        def forecast(message):
            self.bot.send_message(message.chat.id, get_monthly_forecast())

    def start(self):
        self.bot.infinity_polling()
