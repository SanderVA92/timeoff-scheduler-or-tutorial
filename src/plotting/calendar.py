from datetime import date

import pandas as pd
import calplot
import matplotlib.pyplot as plt
import matplotlib.colors as colors


__COLORMAP = colors.ListedColormap(['red', 'green', 'yellow'])


def holiday_calendar_plot(bank_holidays: list[date], weekend_days: list[date], days_off: list[date]) -> None:
    bank_holiday_series = pd.Series(100, index=bank_holidays)

    weekend_days = list(set(weekend_days) - set(bank_holidays))
    print(weekend_days)
    weekend_days_series = pd.Series(300, index=weekend_days)

    days_off = list(set(days_off) - set(weekend_days) - set(bank_holidays))
    days_off_series = pd.Series(200, index=days_off)

    combined = pd.concat([bank_holiday_series, days_off_series, weekend_days_series])
    combined.index = combined.index.astype('datetime64[ns]')

    calplot.calplot(
        combined,
        cmap=__COLORMAP,
        linecolor='black',
        linewidth=0.5,
        edgecolor='red',
        colorbar=False,
        dropzero=True
    )

    plt.savefig('calendar_plot.png')
