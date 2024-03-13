from datetime import datetime


class Concerto:
    def __init__(self, title: str, date: datetime):
        self.title: str = title
        self.datetime: datetime = date

    def get_stringed_time(self):
        return self.datetime.strftime("%H:%M")
