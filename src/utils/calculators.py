from datetime import date

from src.config import ModelConfig
from src.mdl.period import HolidayPeriod
from src.utils.enums import Weekday
from src.utils.time import Time


class CalculateCost:
    @staticmethod
    def generate_single_date_cost_lookup(
        all_dates_in_period: list[date], cost_free_dates: list[date]
    ) -> dict[date, int]:
        dict_cost = {}

        for datestamp in all_dates_in_period:
            if Time.is_weekend_day(datestamp):
                dict_cost[datestamp] = 0
                continue

            if datestamp in cost_free_dates:
                dict_cost[datestamp] = 0
                continue

            dict_cost[datestamp] = 1

        return dict_cost

    @staticmethod
    def for_holiday_period(
        period: HolidayPeriod, daily_cost_lookup: dict[date, int]
    ) -> int:
        total_cost = 0
        for day in period.all_days():
            total_cost += daily_cost_lookup[day]

        return total_cost


class CalculateUtility:
    @staticmethod
    def duration_dependent_component(duration_in_days: int) -> float:
        duration_component_scaler = ModelConfig.DURATION_COMPONENT_SCALER

        min_duration = ModelConfig.PERIOD_LENGTH_GAIN_START
        max_duration = ModelConfig.PERIOD_LENGTH_GAIN_CUTOFF
        if duration_in_days < min_duration:
            return 0

        # Above the minimum holiday period length, we accumulate a linearly-increasing value for the time off.
        if duration_in_days > max_duration:
            additional_value = (
                max_duration - min_duration + 1
            ) * duration_component_scaler
            return additional_value

        additional_value = (
            duration_in_days - min_duration + 1
        ) * duration_component_scaler
        return additional_value

    @staticmethod
    def marginal_value_of_a_single_day(
        date_to_check: date,
        preferred_weekdays_off: list[Weekday],
        preferred_dates_off: list[date],
    ) -> float:
        utility = ModelConfig.BASELINE_MARGINAL_VALUE

        if Weekday(date_to_check.isoweekday()) in preferred_weekdays_off:
            utility += ModelConfig.BONUS_MARGINAL_VALUE
            return utility

        if date_to_check in preferred_dates_off:
            utility += ModelConfig.BONUS_MARGINAL_VALUE
            return utility

        return utility

    @staticmethod
    def summed_marginal_value_for_period(
        period: HolidayPeriod,
        preferred_weekdays_off: list[Weekday],
        preferred_dates_off: list[date],
    ) -> float:
        total_value = 0
        for day in period.all_days():
            total_value += CalculateUtility.marginal_value_of_a_single_day(
                day, preferred_weekdays_off, preferred_dates_off
            )

        return total_value

    @staticmethod
    def total_value_for_period(
        period: HolidayPeriod,
        preferred_weekdays_off: list[Weekday],
        preferred_dates_off: list[date],
    ) -> float:
        if period.duration() < ModelConfig.MIN_TIME_OFF_TO_GET_VALUE:
            return 0

        summed_marginal = CalculateUtility.summed_marginal_value_for_period(period, preferred_weekdays_off, preferred_dates_off)
        period_based = CalculateUtility.duration_dependent_component(period.duration())
        return summed_marginal + period_based
