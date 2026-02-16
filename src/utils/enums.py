from enum import Enum, IntEnum


class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class DayType(IntEnum):
    PUBLIC_HOLIDAY = 1
    WEEKEND = 2
    DAY_OFF = 3
    REGULAR = 0
