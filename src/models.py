from datetime import datetime as dt
from datetime import date, timedelta
from enum import Enum


class Location(Enum):
    WHITEHALL = 0
    ROOM206 = 1


class Concerto:
    def __init__(self, title: str, date_: dt):
        self.title: str = title
        self.datetime: dt = date_

    def get_stringed_time(self):
        return self.datetime.strftime("%H:%M")


class User:
    def __init__(self, name: str, birthdate: date, instrument: str,
                 tg: str, vk: str, is_active: bool,
                 activity_start: date, activity_end: date):
        self.name: str = name
        self.birthdate: date = birthdate
        self.instrument: str = instrument
        self.tg: str = tg
        self.vk: str = vk
        self.is_active: bool = is_active
        self.activity_start: date = activity_start
        self.activity_end: date = activity_end


class Rehearsal:
    def __init__(self, datetime: dt, place: Location = Location.WHITEHALL):
        self.datetime = datetime
        self.place = place

    @staticmethod
    def get_next_rehearsal(from_date: dt = dt.now()):
        next_rehearsal_days_mapping = {
            0: 4,  # MON
            1: 3,  # TUE
            2: 2,  # WED
            3: 1,  # THU
            4: 3,  # FRI
            5: 2,  # SAT
            6: 1  # SUN
        }
        next_rehearsal_date = from_date + timedelta(days=next_rehearsal_days_mapping[from_date.weekday()])
        return Rehearsal(next_rehearsal_date)
