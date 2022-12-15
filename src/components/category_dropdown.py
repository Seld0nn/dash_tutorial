import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import i18n

from . import ids
from ..data.loader import DataSchema

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_categories = data[DataSchema.CATEGORY].tolist()
    unique_categories = sorted(set(all_categories))

    @app.callback(
        Output(ids.CATEGORY_DROPDOWN, "value"),
        [Input(ids.YEAR_DROPDOWN, "value"),
        Input(ids.MONTH_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_CATEGORIES_BUTTON, "n_clicks")],
    )
    def select_all_categories(years: list, months: list, _: int) -> list:
        filtered_data = data.query("year in @years and month in @months")
        return sorted(set(filtered_data[DataSchema.CATEGORY].tolist()))

    return html.Div(
        children=[
            html.H6(i18n.t("general.category")),
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN,
                options=[{"label": category, "value": category} for category in unique_categories],
                value=unique_categories,
                multi=True
            ), 
            html.Button(
                className="dropdown-button", 
                children=[i18n.t("general.select_all")], 
                id=ids.SELECT_ALL_CATEGORIES_BUTTON, 
                n_clicks=0,
            ),
        ]
    )
