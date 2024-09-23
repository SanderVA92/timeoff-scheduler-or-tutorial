from datetime import date, timedelta


class HolidayPeriod:
    __start_date: date
    __duration: int

    def __init__(self, start_date: date, duration: int) -> None:
        self.__start_date = start_date
        self.__duration = duration

    def start_date(self) -> date:
        return self.__start_date

    def end_date(self) -> date:
        return self.__start_date + timedelta(days=self.__duration - 1)

    def duration(self) -> int:
        return self.__duration

    def contains(self, datestamp: date) -> bool:
        return self.start_date() <= datestamp <= self.end_date()

    def all_days(self) -> list[date]:
        all_days = []
        for i in range(self.duration()):
            all_days.append(self.start_date() + timedelta(days=i))
        return all_days

    def __str__(self) -> str:
        return f'{self.start_date()} - {self.end_date()}'

    def __repr__(self) -> str:
        return str(self)
