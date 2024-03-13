from datetime import datetime

from src.models import User
from src.database.exceptions import SerializationFailedError


class UserDeserializer:
    date_format = "%Y-%m-%d"

    def __init__(self, user_json: dict):
        self.user_raw = user_json
        self.user_true = {}
        try:
            self.user = self.__deserialize()
        except ValueError as ex:
            raise SerializationFailedError(ex)
        except KeyError as ex:
            raise SerializationFailedError(ex)

    def __deserialize(self):
        self.user_true = {
            "name": self.user_raw["ФИО"],
            "birthdate": datetime.strptime(self.user_raw["Дата рождения"], UserDeserializer.date_format).date(),
            "instrument": self.user_raw["Инструмент"][0]["value"],
            "tg": self.user_raw["Телеграм"],
            "vk": self.user_raw["ВКонтакте"],
            "is_active": bool(self.user_raw["Активен"]),
            "activity_start": datetime.strptime(self.user_raw["Старт активности"], UserDeserializer.date_format).date(),
            "activity_end": datetime.strptime(self.user_raw["Конец активности"], UserDeserializer.date_format).date()
        }
        return self.__create_user()

    def __create_user(self):
        return User(self.user_true["name"], self.user_true["birthdate"], self.user_true["instrument"], self.user_true["tg"],
                    self.user_true["vk"], self.user_true["is_active"], self.user_true["activity_start"], self.user_true["activity_end"])
