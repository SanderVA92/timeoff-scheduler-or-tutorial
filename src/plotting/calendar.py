from datetime import date

import pandas as pd
from plotly_calplot import calplot
import plotly.graph_objects as go

from src.config import ModelConfig
from src.utils.enums import DayType


def _extract_highest_prio_type_per_date(
    dates_by_type: dict[DayType, list[date]], ascending_prio: list[DayType]
) -> dict[date, DayType]:
    type_by_date = {}
    for date_type in ascending_prio:
        new_types = {d: date_type for d in dates_by_type.get(date_type, [])}
        type_by_date.update(new_types)

    return type_by_date


def holiday_calendar_plot(dates_by_type: dict[DayType, list[date]]) -> go.Figure:
    def make_hover_text(d: date, type_name: DayType) -> str:
        week = d.isocalendar()[1]
        hover_text = f"Date: {d}<br>Week: {week}"
        if type_name != DayType.REGULAR:
            type_string = type_name.name.replace("_", " ").capitalize()
            hover_text += f"<br>Type: {type_string}"

        return hover_text

    all_dates_in_period = pd.date_range(
        ModelConfig.PLANNING_PERIOD_START_DATE,
        ModelConfig.PLANNING_PERIOD_END_DATE,
        freq="D",
    )
    dates_by_type[DayType.REGULAR] = [d.date() for d in all_dates_in_period]

    ascending_prio_for_visual = [
        DayType.REGULAR,
        DayType.DAY_OFF,
        DayType.WEEKEND,
        DayType.PUBLIC_HOLIDAY,
    ]
    type_by_date = _extract_highest_prio_type_per_date(
        dates_by_type, ascending_prio_for_visual
    )

    # Create records for all dates
    records = []
    for d, d_type in type_by_date.items():
        records.append(
            {"date": d, "value": d_type.value, "text": make_hover_text(d, d_type)}
        )

    df = pd.DataFrame(records)
    df["date"] = df["date"].astype("datetime64[ns]")

    # Discrete colorscale for 4 categories (0=empty, 1=holiday, 2=weekend, 3=day off)
    colorscale = [
        [0.0, "#ebedf0"],  # Light gray for empty days
        [0.25, "#ebedf0"],
        [0.25, "#e74c3c"],  # Red for public holidays
        [0.5, "#e74c3c"],
        [0.5, "#f1c40f"],  # Yellow for weekends
        [0.75, "#f1c40f"],
        [0.75, "#2ecc71"],  # Green for days off
        [1.0, "#2ecc71"],
    ]

    fig = calplot(
        df,
        x="date",
        y="value",
        text="text",
        colorscale=colorscale,
        cmap_min=0,
        cmap_max=3,
        gap=1,
        total_height=300,
        month_lines_width=3,
        showscale=False,
    )

    # Add legend
    legend_items = [
        ("Public Holiday", "#e74c3c"),
        ("Weekend", "#f1c40f"),
        ("Day Off", "#2ecc71"),
    ]

    for label, color in legend_items:
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=12, color=color, symbol="square"),
                name=label,
                showlegend=True,
            )
        )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(t=80),
    )

    fig.update_xaxes(tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))

    # Update hovertemplate to only show custom text
    for trace in fig.data:
        if hasattr(trace, "hovertemplate"):
            trace.hovertemplate = "%{text}<extra></extra>"

    return fig
