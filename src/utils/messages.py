from src.exceptions import ConcertosNotFoundException
from src.utils.parser import get_concerto_today


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
