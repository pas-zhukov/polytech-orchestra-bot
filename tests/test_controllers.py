from datetime import date

import pytest
from environs import Env

from src.database.controllers import get_active_users_by_birthdate, get_active_users


class TestControllers:

    def test_get_active_users(self):
        env = Env()
        env.read_env()
        database_token = env.str('DATABASE_TOKEN')
        users = get_active_users(database_token)
        for user in users:
            assert user.is_active is True

    def test_active_user_by_birthdate(self):
        env = Env()
        env.read_env()
        database_token = env.str('DATABASE_TOKEN')
        birthdate = date(1999, 3, 3)

        result = get_active_users_by_birthdate(database_token, birthdate)

        assert result != []

    def test_inactive_user_by_birthdate(self):
        env = Env()
        env.read_env()
        database_token = env.str('DATABASE_TOKEN')
        birthdate = date(1995, 2, 24)

        result = get_active_users_by_birthdate(database_token, birthdate)

        assert result == []

    def _addSkip_test_empty_list_birthdate_is_none(self):
        # Arrange
        env = Env()
        env.read_env()
        database_token = env.str('DATABASE_TOKEN')
        birthdate = None

        result = get_active_users_by_birthdate(database_token, birthdate)

        assert result == []
