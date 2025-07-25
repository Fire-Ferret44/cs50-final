"""
Loads data from csv files into the classes for doctors and shifts.
"""

from pathlib import Path
from calendar import monthrange
import csv
from datetime import date, datetime, timedelta

from models.shift_structure import ShiftStructure
from models.shift_calendar import ShiftCalendar
