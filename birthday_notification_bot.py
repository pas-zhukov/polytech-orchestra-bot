"""
Скрипт для проверки, у кого сегодня день рождения из оркестрантов.
Отправляет сообщение в личку Даше/Паше и завершает работу.
Регулярный запуск предполагается настраивать при помощи systemd.
"""
import logging
from datetime import datetime

from telebot import TeleBot
from environs import Env

from src.database.controllers import get_active_users_by_birthdate
from src.utils.messages import get_birthday_message


logger = logging.getLogger(__name__)


def main():
    logger.info("Starting birthday notification check")

    env = Env()
    env.read_env()

    bot_token = env.str("TG_BOT_TOKEN")
    database_token = env.str("DATABASE_TOKEN")
    admin_ids = env.list("ADMIN_IDS")

    logger.info("Configuration loaded. Admins count: %d", len(admin_ids))

    bot = TeleBot(bot_token)
    today = datetime.now().date()

    logger.info("Checking birthdays for %s", today)

    birthday_today_users = get_active_users_by_birthdate(
        database_token,
        today,
    )

    logger.info("Found %d birthday(s)", len(birthday_today_users))

    if not birthday_today_users:
        logger.info("No birthdays today. Finishing")
        return

    sent_count = 0

    for user in birthday_today_users:
        message = get_birthday_message(user)

        for admin in admin_ids:
            logger.info(
                "Sending birthday notification to admin %s",
                admin,
            )
            bot.send_message(admin, message)
            sent_count += 1

    logger.info(
        "Birthday notification check completed. Messages sent: %d",
        sent_count,
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    try:
        main()
    except Exception:
        logger.exception("Birthday notification check failed")
        raise
        
