import requests


USERS_TABLE_URL = "https://api.baserow.io/api/database/rows/table/230779/"


def get_all_users(database_token: str):
    response = requests.get(
        USERS_TABLE_URL,
        params={"user_field_names": "true"},
        headers={"Authorization": f"Token {database_token}"})
    response.raise_for_status()
    return response.json()["results"]