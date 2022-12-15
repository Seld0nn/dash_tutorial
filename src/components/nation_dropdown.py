from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import i18n

from . import ids


def render(app: Dash) -> html.Div:
    all_nations = ["South Korea", "China", "Canada"]

    @app.callback(
        Output(ids.NATION_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_NATIONS_BUTTON, "n_clicks"),
    )
    def select_all_nations(_: int) -> list:
        return all_nations

    return html.Div(
        children=[html.H6(i18n.t("general.nation")), 
        dcc.Dropdown(
            id=ids.NATION_DROPDOWN,
            options=[{"label": nation, "value": nation} for nation in all_nations],
            value=all_nations,
            multi=True
            ), 
            
            html.Button(
                className="dropdown-button", 
                children=[i18n.t("general.select_all")], 
                id=ids.SELECT_ALL_NATIONS_BUTTON, 
                n_clicks=0,
            ),
        ]
    )