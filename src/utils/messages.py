from datetime import datetime, timedelta

from src.exceptions import ConcertosNotFoundException
from src.utils.parser import get_concerto_today, get_concerto_by_date
from src.models import User


def get_message_for_today() -> str:
    try:
        concerto = get_concerto_today()
        message = (f"Согласно расписанию Белого Зала, сегодня там концерт.\n"
                   f"Название: {concerto.title}\n"
                   f"Начало концерта: {concerto.get_stringed_time()}\n\n"
                   f"Репетируем в 206.")
    except ConcertosNotFoundException:
        message = f"Согласно расписанию Белого Зала, сегодня там концертов не запланировано. Репетируем в зале!"

    return message


def get_message_for_next_rehearsal() -> str:
    next_rehearsal_days_mapping = {
        0: 4,  # MON
        1: 3,  # TUE
        2: 2,  # WED
        3: 1,  # THU
        4: 3,  # FRI
        5: 2,  # SAT
        6: 1   # SUN
    }
    today_date = datetime.now()
    next_rehearsal_date = today_date + timedelta(days=next_rehearsal_days_mapping[today_date.weekday()])

    try:
        concerto = get_concerto_by_date(next_rehearsal_date)
        message = (f'Согласно расписанию Белого Зала, {next_rehearsal_date.strftime("%d.%m.%Y")} там концерт.\n'
                   f'Название: {concerto.title}\nНачало концерта: {concerto.get_stringed_time()}\n\n')
    except ConcertosNotFoundException:
        message = f'Согласно расписанию Белого Зала, {next_rehearsal_date.strftime("%d.%m.%Y")} там концертов не запланировано.'
    return message


def get_birthday_message(user: User) -> str:
    message = (f"Привет! Сегодня день рождения у {user.name}. Дата рождения: {user.birthdate.strftime('%d.%m.%Y')}\n"
               f"Он/она играет в оркестре на {user.instrument} с {user.activity_start.strftime('%d.%m.%Y')}.\n"
               f"Контактные данные: Телеграм[{user.tg}], ВКонтакте[{user.vk}]")
    return message
