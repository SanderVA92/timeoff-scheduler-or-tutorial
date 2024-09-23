from datetime import date

import pandas as pd
import calplot
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches


__COLORMAP = colors.ListedColormap(['red', 'yellow', 'green'])


def holiday_calendar_plot(public_holidays: list[date], weekend_days: list[date], days_off: list[date]) -> None:
    public_holiday_series = pd.Series(1, index=public_holidays)

    actual_weekend_days = list(set(weekend_days).difference(set(public_holidays)))
    weekend_days_series = pd.Series(2, index=actual_weekend_days)

    days_off = list(set(days_off) - set(weekend_days) - set(public_holidays))
    days_off_series = pd.Series(3, index=days_off)

    combined = pd.concat([public_holiday_series, days_off_series, weekend_days_series])
    combined.index = combined.index.astype('datetime64[ns]')

    calplot.calplot(
        combined,
        cmap=__COLORMAP,
        linecolor='black',
        linewidth=0.5,
        edgecolor='red',
        colorbar=False,
        dropzero=True,
    )

    public_holiday_patch = mpatches.Patch(color='red', label='Public Holiday')
    weekend_days_patch = mpatches.Patch(color='yellow', label='Weekend')
    days_off_patch = mpatches.Patch(color='green', label='Day Off')

    plt.legend(handles=[public_holiday_patch, weekend_days_patch, days_off_patch], loc='right', bbox_to_anchor=(1.22, 1))

    plt.savefig('calendar_plot.png')
