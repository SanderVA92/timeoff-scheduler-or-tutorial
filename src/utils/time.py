from datetime import date, timedelta
from enum import Enum

from src.mdl.period import HolidayPeriod


class Time:
    @staticmethod
    def is_weekend_day(day: date) -> bool:
        return day.isoweekday() in [6, 7]

    @staticmethod
    def get_all_weekend_days(all_dates: list[date]) -> list[date]:
        return [day for day in all_dates if Time.is_weekend_day(day)]


class PeriodFactory:
    @staticmethod
    def generate_all_possible_holiday_periods(
        all_dates: list[date], max_period_length: int
    ) -> list[HolidayPeriod]:
        planning_end_date = max(all_dates)
        all_dates.sort()

        all_periods = []
        for start_date in all_dates:
            for duration in range(1, max_period_length + 1):
                if start_date + timedelta(days=duration) > planning_end_date:
                    break

                new_period = HolidayPeriod(start_date, duration)
                all_periods.append(new_period)

        return all_periods
