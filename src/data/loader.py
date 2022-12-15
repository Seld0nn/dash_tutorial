import pandas as pd
from functools import reduce, partial
from typing import Callable
import datetime as dt
import i18n
import babel.dates

class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]

def create_year_column(data: pd.DataFrame) -> pd.DataFrame:
    data[DataSchema.YEAR] = data[DataSchema.DATE].dt.year.astype(str)
    return data

def create_month_column(data: pd.DataFrame) -> pd.DataFrame:
    data[DataSchema.MONTH] = data[DataSchema.DATE].dt.month.astype(str)
    return data

def translate_date(data: pd.DataFrame, locale: str) -> pd.DataFrame:
    def date_repr(date: dt.date) -> str:
        return babel.dates.format_date(date, format="MMMM", locale=locale)

    data[DataSchema.MONTH] = data[DataSchema.DATE].apply(date_repr)
    return data

def translate_category(data: pd.DataFrame) -> pd.DataFrame:
    def translate(category: str) -> str:
        return i18n.t(f"category.{category}")
    data[DataSchema.CATEGORY] = data[DataSchema.CATEGORY].apply(translate)
    return data

def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def load_transaction_data(path: str, locale: str) -> pd.DataFrame:
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.CATEGORY: str
        },
        parse_dates=[DataSchema.DATE]
    )
    preprocessor = compose(
        create_year_column,
        partial(translate_date, locale = locale),
        translate_category
    )
    return preprocessor(data)