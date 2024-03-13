"""
Скрипт для проверки, у кого сегодня день рождения из оркестрантов. Отправляет сообщение в личку Даше/Паше и завершает работу.
Регулярный запуск предполагается настраивать при помощи systemd.
"""
from datetime import datetime, date

from telebot import TeleBot
from environs import Env

from src.database.controllers import get_users_by_birthdate
from src.utils.messages import get_user_card


def main():
    env = Env()
    env.read_env()
    bot_token = env.str("TG_BOT_TOKEN")
    database_token = env.str("DATABASE_TOKEN")
    admin_ids = env.list("ADMIN_IDS")
    bot = TeleBot(bot_token)

    birthday_today_users = get_users_by_birthdate(database_token, datetime.now().date())

    for user in birthday_today_users:
        message = get_user_card(user)
        for admin in admin_ids:
            bot.send_message(admin, message)


if __name__ == "__main__":
    main()
