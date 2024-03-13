from datetime import datetime, date


class Concerto:
    def __init__(self, title: str, date: datetime):
        self.title: str = title
        self.datetime: datetime = date

    def get_stringed_time(self):
        return self.datetime.strftime("%H:%M")


class User:
    def __init__(self, name: str, birthdate: date, instrument: str,
                 tg: str, vk: str, is_active: bool,
                 activity_start: date, activity_end: date) -> None:
        self.name: str = name
        self.birthdate: date = birthdate
        self.instrument: str = instrument
        self.tg: str = tg
        self.vk: str = vk
        self.is_active: bool = is_active
        self.activity_start: date = activity_start
        self.activity_end: date = activity_end
