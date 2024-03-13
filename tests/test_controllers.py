from datetime import date

import pytest
from environs import Env

from src.database.controllers import get_active_users_by_birthdate


class TestControllers:

    #  Returns an empty list when there are no active users with the given birthdate
    def test_empty_list_no_active_users_with_given_birthdate(self, mocker):
        # Arrange
        self.env = Env()
        self.env.read_env()
        self.database_token = self.env.str('DATABASE_TOKEN')
        birthdate = date(1999, 3, 3)
        mocker.patch("src.database.controllers.get_active_users", return_value=[])
    
        # Act
        result = get_active_users_by_birthdate(self.database_token, birthdate)
    
        # Assert
        assert result == []

    #  Returns an empty list when the birthdate is None
    def test_empty_list_birthdate_is_none(self, mocker):
        # Arrange
        self.env = Env()
        self.env.read_env()
        self.database_token = self.env.str('DATABASE_TOKEN')
        birthdate = None
        mocker.patch("src.database.controllers.get_active_users", return_value=[])
    
        # Act
        result = get_active_users_by_birthdate(self.database_token, birthdate)
    
        # Assert
        assert result == []
