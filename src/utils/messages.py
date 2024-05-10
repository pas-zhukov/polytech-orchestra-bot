from src.exceptions import ConcertosNotFoundException
from src.utils.parser import get_concerto_today, get_concerto_by_date
from src.models import User, Rehearsal


def get_message_for_today() -> str:
    try:
        concerto = get_concerto_today()
        message = (f"Согласно расписанию Белого Зала, сегодня там концерт.\n"
                   f"Название: {concerto.title}\n"
                   f"Начало концерта: {concerto.get_stringed_time()}\n\n")
    except ConcertosNotFoundException:
        message = f"Согласно расписанию Белого Зала, сегодня там концертов не запланировано."
    return message


def get_message_for_today_rehearsal() -> str:
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
    next_rehearsal = Rehearsal.get_next_rehearsal()
    next_rehearsal_date = next_rehearsal.datetime

    try:
        concerto = get_concerto_by_date(next_rehearsal_date)
        message = (f'Согласно расписанию Белого Зала, {next_rehearsal_date.strftime("%d.%m.%Y")} там концерт.\n'
                   f'Название: {concerto.title}\nНачало концерта: {concerto.get_stringed_time()}\n\n')
    except ConcertosNotFoundException:
        message = f'Согласно расписанию Белого Зала, {next_rehearsal_date.strftime("%d.%m.%Y")} там концертов не запланировано.'
    return message


def get_monthly_forecast() -> str:
    rehearsals = []
    rehearsal = Rehearsal.get_next_rehearsal()
    for _ in range(8):
        rehearsals.append(rehearsal)
        rehearsal = Rehearsal.get_next_rehearsal(rehearsal.datetime)
    concertos = []
    for rehearsal in rehearsals:
        try:
            concerto = get_concerto_by_date(rehearsal.datetime)
        except ConcertosNotFoundException:
            concerto = None
        concertos.append(concerto)
    message = "Прогноз места проведения репетиций, основанный на расписании Белого зала:\n"
    for i in range(len(concertos)):
        message += f"{rehearsals[i].datetime.strftime('%d.%m.%Y')}: {'206' if concertos[i] else 'БЗ'}\n"
    return message



def get_birthday_message(user: User) -> str:
    message = (f"Привет! Сегодня день рождения у {user.name}. Дата рождения: {user.birthdate.strftime('%d.%m.%Y')}\n"
               f"Он/она играет в оркестре на {user.instrument} с {user.activity_start.strftime('%d.%m.%Y')}.\n"
               f"Контактные данные: Телеграм[{user.tg}], ВКонтакте[{user.vk}]")
    return message
