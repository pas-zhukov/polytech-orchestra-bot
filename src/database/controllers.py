import logging
from datetime import date

import requests

from src.database.serializers import UserDeserializer

logger = logging.getLogger(__name__)

USERS_TABLE_URL = "https://api.baserow.io/api/database/rows/table/230779/"


def get_all_users(database_token: str):
    logger.info("Requesting users from Baserow")

    headers = {"Authorization": f"Token {database_token}"}
    params = {"user_field_names": "true", "size": 200}
    url = USERS_TABLE_URL

    all_users = []
    page = 1

    while url:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        results = data["results"]
        all_users.extend(results)

        logger.info(
            "Loaded Baserow page %d: rows=%d, total_loaded=%d, has_next=%s",
            page,
            len(results),
            len(all_users),
            bool(data.get("next")),
        )

        url = data.get("next")
        params = None  # Следующая страница уже содержит параметры в URL
        page += 1

    users = [UserDeserializer(row).user for row in all_users]

    logger.info(
        "Finished loading users: rows=%d, deserialized=%d",
        len(all_users),
        len(users),
    )

    return users


def get_active_users(database_token: str):
    all_users = get_all_users(database_token)
    active_users = [user for user in all_users if user.is_active]

    logger.info(
        "Filtered active users: total=%d, active=%d, inactive=%d",
        len(all_users),
        len(active_users),
        len(all_users) - len(active_users),
    )

    return active_users


def get_active_users_by_birthdate(database_token: str, birthdate: date):
    logger.info("Searching for birthdays on %s", birthdate.strftime("%d.%m.%Y"))

    active_users = get_active_users(database_token)
    birthday_match_users = []

    missing_birthdate = 0
    invalid_birthdate = 0

    for user in active_users:
        if not user.birthdate:
            missing_birthdate += 1
            logger.debug(
                "Skipping user without birthdate: %s",
                user,
            )
            continue

        try:
            user_birthdate = user.birthdate

            if isinstance(user_birthdate, str):
                logger.warning(
                    "Birthdate is a string instead of date: value=%r, type=%s",
                    user_birthdate,
                    type(user_birthdate).__name__,
                )
                invalid_birthdate += 1
                continue

            if user_birthdate.strftime("%d.%m") == birthdate.strftime("%d.%m"):
                logger.info(
                    "Birthday match found: birthdate=%s",
                    user_birthdate.strftime("%d.%m.%Y"),
                )
                birthday_match_users.append(user)

        except (AttributeError, ValueError, TypeError):
            invalid_birthdate += 1
            logger.exception("Failed to process user birthdate")

    logger.info(
        "Birthday search completed: active=%d, matched=%d, "
        "missing_birthdate=%d, invalid_birthdate=%d",
        len(active_users),
        len(birthday_match_users),
        missing_birthdate,
        invalid_birthdate,
    )

    return birthday_match_users
