from datetime import date

import requests

from src.database.serializers import UserDeserializer

USERS_TABLE_URL = "https://api.baserow.io/api/database/rows/table/230779/"


def get_all_users(database_token: str):
    response = requests.get(
        USERS_TABLE_URL,
        params={"user_field_names": "true"},
        headers={"Authorization": f"Token {database_token}"})
    response.raise_for_status()
    all_users = response.json()["results"]
    return [UserDeserializer(all_users[i]).user for i in range(len(all_users))]


def get_active_users(database_token: str):
    all_users = get_all_users(database_token)
    return list(filter(lambda user: user.is_active, all_users))


def get_active_users_by_birthdate(database_token: str, birthdate: date):
    # TODO: переписать с фильтрацией на этапе запроса к БД
    active_users = get_active_users(database_token)
    birthday_match_users = []
    for user in active_users:
        if not user.birthdate:
            continue
        if user.birthdate.strftime("%d.%m") == birthdate.strftime("%d.%m"):
            birthday_match_users.append(user)
    return birthday_match_users
