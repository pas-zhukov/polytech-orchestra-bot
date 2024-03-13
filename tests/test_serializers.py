import pytest
from datetime import datetime

from src.database.serializers import UserDeserializer
from src.database.exceptions import SerializationFailedError
from src.models import User


class TestUserDeserializer:

    #  Deserialize a valid user JSON object and create a User instance.
    def test_deserialize_valid_user(self):
        # Arrange
        user_json = {
            "ФИО": "John Doe",
            "Дата рождения": "1990-01-01",
            "Инструмент": [{"value": "Guitar"}],
            "Телеграм": "@johndoe",
            "ВКонтакте": "johndoe",
            "Активен": True,
            "Старт активности": "2022-01-01",
            "Конец активности": "2022-12-31"
        }

        # Act
        deserializer = UserDeserializer(user_json)

        # Assert
        assert isinstance(deserializer.user, User)
        assert deserializer.user.name == "John Doe"
        assert deserializer.user.birthdate == datetime.strptime("1990-01-01", "%Y-%m-%d").date()
        assert deserializer.user.instrument == "Guitar"
        assert deserializer.user.tg == "@johndoe"
        assert deserializer.user.vk == "johndoe"
        assert deserializer.user.is_active is True
        assert deserializer.user.activity_start == datetime.strptime("2022-01-01", "%Y-%m-%d").date()
        assert deserializer.user.activity_end == datetime.strptime("2022-12-31", "%Y-%m-%d").date()

    #  Deserialize a user JSON object with invalid birthdate and raise SerializationFailedError.
    def test_deserialize_invalid_name(self):
        # Arrange
        user_json = {
            "ФИО": "",
            "Дата рождения": "190-01-01",
            "Инструмент": [{"value": "Guitar"}],
            "Телеграм": "@johndoe",
            "ВКонтакте": "johndoe",
            "Активен": True,
            "Старт активности": "2022-01-01",
            "Конец активности": "2022-12-31"
        }

        # Act & Assert
        with pytest.raises(SerializationFailedError):
            UserDeserializer(user_json)

    #  Deserialize a user JSON object with invalid json key and raise SerializationFailedError.
    def test_deserialize_invalid_key(self):
        # Arrange
        user_json = {
            "Имя": "",
            "Дата рождения": "190-01-01",
            "Инструмент": [{"value": "Guitar"}],
            "Телеграм": "@johndoe",
            "ВКонтакте": "johndoe",
            "Активен": True,
            "Старт активности": "2022-01-01",
            "Конец активности": "2022-12-31"
        }

        # Act & Assert
        with pytest.raises(SerializationFailedError):
            UserDeserializer(user_json)