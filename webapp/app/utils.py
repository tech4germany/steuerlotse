import datetime as dt


def get_first_day_of_tax_period():
    return dt.date(dt.date.today().year - 1, 1, 1)
