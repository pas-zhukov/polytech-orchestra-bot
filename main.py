from telebot import TeleBot
from environs import Env

from src.bot import OrchestraBot


def main():
    env = Env()
    env.read_env()
    bot_token = env.str("TG_BOT_TOKEN")
    group_id = env.str("GROUP_ID")
    bot = TeleBot(bot_token)


if __name__ == "__main__":
    main()
