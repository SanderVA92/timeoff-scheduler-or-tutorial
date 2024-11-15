from datetime import date, timedelta
from enum import Enum

from src.utils.enums import Weekday


class Location(Enum):
    BERLIN = "Berlin"
    MUNICH = "Munich"


class ModelConfig:
    PLANNING_PERIOD_START_DATE: date = date(2025, 1, 1)
    NUMBER_DAYS_IN_YEAR: int = 365
    PLANNING_PERIOD_END_DATE: date = PLANNING_PERIOD_START_DATE + timedelta(days=NUMBER_DAYS_IN_YEAR - 1)

    MAX_HOLIDAY_PERIOD_LENGTH: int = 20

    HOLIDAY_BUDGET: int = 30

    # Date-level utility parameters and preferences
    PREFERRED_WEEKDAYS_OFF: list[Weekday] = [Weekday.FRIDAY]
    PREFERRED_DATES_OFF: list[date] = [date(2025, 6, 19)]

    # Period-level utility parameters and preferences
    MIN_TIME_OFF_TO_GET_VALUE: int = 3
    PERIOD_LENGTH_GAIN_START: int = 4
    PERIOD_LENGTH_GAIN_CUTOFF: int = 20
    DURATION_COMPONENT_SCALER: float = 1.1

    BASELINE_MARGINAL_VALUE: float = 1
    BONUS_MARGINAL_VALUE: float = 0.5
