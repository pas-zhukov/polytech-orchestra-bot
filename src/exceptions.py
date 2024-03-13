class ConcertosNotFoundException(Exception):
    def __init__(self, mes):
        super().__init__(mes)
