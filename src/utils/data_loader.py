import os

import pandas as pd

from src.config import Location


class CSVDataLoader:
    __base_path_datasets: str

    def __init__(self, base_path: str) -> None:
        self.__base_path_datasets = base_path

    def load_public_holidays(self, year: int, location: Location) -> pd.DataFrame:
        filename_public_holidays = f"{year}_public_holidays_{location.value}.csv"

        filepath_public_holidays = os.path.join(
            self.__base_path_datasets, filename_public_holidays
        )

        df_public_holidays = pd.read_csv(
            filepath_public_holidays,
            delimiter=",",
            usecols=["Date", "Holiday"],
            dtype={"Holiday": str, "Date": str},
        )

        df_public_holidays.sort_values(by="Date", inplace=True)
        df_public_holidays["Date"] = pd.to_datetime(df_public_holidays["Date"]).dt.date
        df_public_holidays = self.__add_weekday_column(df_public_holidays)

        return df_public_holidays

    @staticmethod
    def __add_weekday_column(
        df: pd.DataFrame, date_column: str = "Date"
    ) -> pd.DataFrame:
        df["Weekday"] = pd.to_datetime(df[date_column]).dt.day_name()
        return df
