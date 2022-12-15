from re import LOCALE
from venv import create
from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
import i18n
from flask import Flask

from src.components.layout import create_layout
from src.data.loader import load_transaction_data

DATA_PATH = "./data/transactions.csv"
LOCALE = "es"


i18n.set("locale", LOCALE)
i18n.load_path.append("locale")
data = load_transaction_data(DATA_PATH, LOCALE)

server = Flask(__name__)
app = Dash(server=server, external_stylesheets=[BOOTSTRAP])
app.title = i18n.t("general.app_title")
app.layout = create_layout(app, data)

if __name__ == "__main__":
    app.run_server()
    