from datetime import date, timedelta

from src.utils.enums import Weekday


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
        start_weekday = Weekday(self.start_date().isoweekday()).name
        end_weekday = Weekday(self.end_date().isoweekday()).name
        return f"{start_weekday[:3].capitalize()} {self.start_date()} - {end_weekday[:3].capitalize()} {self.end_date()}"

    def __repr__(self) -> str:
        return str(self)
