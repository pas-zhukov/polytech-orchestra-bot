"""
Скрипт для проверки, у кого сегодня день рождения из оркестрантов. Отправляет сообщение в личку Даше/Паше и завершает работу.
Регулярный запуск предполагается настраивать при помощи systemd.
"""

from telebot import TeleBot
from environs import Env

from src.utils.messages import get_message_for_today


def main():
    env = Env()
    env.read_env()
    bot_token = env.str("TG_BOT_TOKEN")
    admin_ids = env.list("ADMIN_IDS")
    bot = TeleBot(bot_token)


if __name__ == "__main__":
    main()
