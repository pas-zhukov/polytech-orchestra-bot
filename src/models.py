from datetime import datetime, date

from src.database.controllers import get_all_users
from src.database.serializers import UserDeserializer


class Concerto:
    def __init__(self, title: str, date: datetime):
        self.title: str = title
        self.datetime: datetime = date

    def get_stringed_time(self):
        return self.datetime.strftime("%H:%M")


class User:
    def __init__(self, name: str, birthdate: date, instrument: str,
                 tg: str, vk: str, is_active: bool,
                 activity_start: date, activity_end: date):
        self.name: str = name
        self.birthdate: date = birthdate
        self.instrument: str = instrument
        self.tg: str = tg
        self.vk: str = vk
        self.is_active: bool = is_active
        self.activity_start: date = activity_start
        self.activity_end: date = activity_end

    @staticmethod
    def get_all_users(database_token: str):
        all_users = get_all_users(database_token)
        return [UserDeserializer(all_users[i]).user for i in range(len(all_users))]