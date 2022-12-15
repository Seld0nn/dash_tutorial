import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import i18n

from . import ids
from ..data.loader import DataSchema

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_months = data[DataSchema.MONTH].tolist()
    unique_months = sorted(set(all_months))

    @app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        [Input(ids.YEAR_DROPDOWN, "value"), Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks")],
    )
    def update_months(years: list, _: int) -> list:
        filtered_data = data.query("year in @years")
        return sorted(set(filtered_data[DataSchema.MONTH].tolist()))

    return html.Div(
        children=[
            html.H6(i18n.t("general.month")),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=[{"label": month, "value": month} for month in unique_months],
                value=unique_months,
                multi=True
            ), 
            html.Button(
                className="dropdown-button", 
                children=[i18n.t("general.select_all")], 
                id=ids.SELECT_ALL_MONTHS_BUTTON, 
                n_clicks=0,
            ),
        ]
    )
