from src.exceptions import ConcertosNotFoundException
from src.utils.parser import get_concerto_today
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


def get_birthday_message(user: User) -> str:
    message = (f"Привет! Сегодня день рождения у {user.name}. Дата рождения: {user.birthdate.strftime('%d.%m.%Y')}\n"
               f"Он/она играет в оркестре на {user.instrument} с {user.activity_start.strftime('%d.%m.%Y')}.\n"
               f"Контактные данные: Телеграм[{user.tg}], ВКонтакте[{user.vk}]")
    return message
