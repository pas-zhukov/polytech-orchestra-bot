"""
Скрипт для разовой проверки занятости Белого Зала. Отправляет сообщение в общий чат и завершает работу.
Регулярный запуск предполагается настраивать при помощи systemd.
"""

from telebot import TeleBot
from environs import Env

from src.utils.messages import get_message_for_today_rehearsal


def main():
    env = Env()
    env.read_env()
    bot_token = env.str("TG_BOT_TOKEN")
    group_id = env.str("GROUP_ID")
    bot = TeleBot(bot_token)
    message = get_message_for_today_rehearsal()
    bot.send_message(group_id, message)


if __name__ == "__main__":
    main()
