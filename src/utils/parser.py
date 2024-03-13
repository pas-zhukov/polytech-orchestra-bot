from datetime import datetime, date, time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup as bs

from src.models import Concerto
from src.exceptions import ConcertosNotFoundException

WHITEHALL_URL = "https://whitehall.spbstu.ru/"
WHITEHALL_EVENTS_URL = "https://whitehall.spbstu.ru/events/"


def get_concerto_today():
    return get_concerto_by_date(datetime.now())


def get_concerto_by_date(date: date) -> Concerto:
    formatted_date = date.strftime("%Y-%m-%d")
    response = requests.get(WHITEHALL_EVENTS_URL, params={"date": formatted_date})
    response.raise_for_status()
    events_page_soup = bs(response.text, "lxml")
    # TODO: собирать не только первый концерт, но и остальные
    # TODO: заменить парсинг на парсинг через css-селектор
    try:
        first_event_url = (events_page_soup
                           .find('ul', {'class': 'scedule'})
                           .find('div', {'class': 'col-md-11 col-xs-9'})
                           .find('div', {'class': 'text'})
                           .find('a', {'class': 'title'})
                           .get('href'))
    except AttributeError:
        raise ConcertosNotFoundException("No concertos found for the given date")
    full_event_url = urljoin(WHITEHALL_URL, first_event_url)
    concerto_title, concerto_time = get_concerto_title_and_time(full_event_url)
    concerto_datetime = datetime.combine(date, concerto_time)
    return Concerto(concerto_title, concerto_datetime)


def get_concerto_title_and_time(concerto_url: str) -> (str, time):
    response = requests.get(concerto_url)
    response.raise_for_status()
    soup = bs(response.text, "lxml")
    # TODO: заменить парсинг на парсинг через css-селектор
    concerto_title = soup.find('head').find('title').text
    concerto_time = soup.find('div', {'class': 'col-md-7 col-sm-8 con-inf-sect'}).findAll('div')[3].text
    concerto_time = datetime.strptime(concerto_time, "%H:%M").time()
    return concerto_title, concerto_time


if __name__ == "__main__":
    get_concerto_by_date(datetime.strptime("15.03.2024", "%d.%m.%Y"))
