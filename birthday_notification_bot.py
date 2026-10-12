"""
Скрипт для проверки, у кого сегодня день рождения из оркестрантов.
Отправляет сообщение в личку Даше/Паше и завершает работу.
Регулярный запуск предполагается настраивать при помощи systemd.
"""
import logging

from environs import Env
from telebot import TeleBot, apihelper

from src.database.controllers import get_active_users_by_birthdate
from src.utils.messages import get_birthday_message

logger = logging.getLogger(__name__)


def main():
    env = Env()
    env.read_env()

    bot_token = env.str("TG_BOT_TOKEN")
    database_token = env.str("DATABASE_TOKEN")
    admin_ids = env.list("ADMIN_IDS")

    # Настройка SOCKS5-прокси для Telegram Bot API
    proxy_host = env.str("TG_PROXY_HOST")
    proxy_port = env.int("TG_PROXY_PORT")
    proxy_username = env.str("TG_PROXY_USERNAME", default="")
    proxy_password = env.str("TG_PROXY_PASSWORD", default="")

    proxy_auth = ""
    if proxy_username:
        proxy_auth = f"{proxy_username}:{proxy_password}@"

    proxy_url = (
        f"socks5h://{proxy_auth}"
        f"{proxy_host}:{proxy_port}"
    )

    apihelper.proxy = {
        "http": proxy_url,
        "https": proxy_url,
    }

    bot = TeleBot(bot_token)

    birthday_today_users = get_active_users_by_birthdate(
        database_token,
        __import__("datetime").datetime.now().date(),
    )

    for user in birthday_today_users:
        message = get_birthday_message(user)

        for admin in admin_ids:
            bot.send_message(admin, message)

    logger.info("Birthday notifications sent successfully")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    try:
        main()
    except Exception:
        logger.exception("Birthday notification bot failed")
        raise
        
