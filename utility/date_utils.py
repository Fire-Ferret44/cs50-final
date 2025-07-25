"""
Defines utility functions for date manipulation
"""

from datetime import datetime, timedelta

def parse_date(date_str):
    """ Converts 'DD-MM-YYYY' to datetime.date """
    return datetime.strptime(date_str, "%d-%m-%Y").date()

def generate_date_range(start_date, end_date):
    """ Generates a list of all dates from start_date to end_date inclusive """
    current = start_date
    dates = []
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    return dates
