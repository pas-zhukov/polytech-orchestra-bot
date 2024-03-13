import unittest
from datetime import datetime, date, time

from src.utils.parser import get_concerto_by_date, get_concerto_title_and_time


class TestParser(unittest.TestCase):
    def test_get_concerto_title_and_time(self):
        concerto_url = "https://whitehall.spbstu.ru/events/manfred-13032024/"

        title, concerto_time = get_concerto_title_and_time(concerto_url)

        assert title == "Манфред"
        assert concerto_time == time(hour=19, minute=0, second=0)

    def _addSkip_test_get_concerto_title_and_date(self):
        get_concerto_title_and_time("https://whitehall.spbstu")

    def test_get_concerto_by_date(self):
        concerto_date = date(2024, 3, 13)
        concerto = get_concerto_by_date(concerto_date)

        assert concerto.title == "Манфред"
        assert concerto.datetime == datetime.combine(concerto_date, time(hour=19, minute=0))