import logging

from telebot import TeleBot
from environs import Env

from src.bot import OrchestraBot


def main():
    try:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.WARN)
        env = Env()
        env.read_env()
        bot_token = env.str("TG_BOT_TOKEN")
        group_id = env.str("GROUP_ID")
        bot = OrchestraBot(bot_token, group_id)
        bot.start()
    except Exception as ex:
        logging.error(ex)


if __name__ == "__main__":
    main()
