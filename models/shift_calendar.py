"""
Defines a ScheduleCalendar class.
Generates a calendar of shifts for a range of days.
"""

from datetime import date, timedelta
from typing import Dict, List

from utility.calendar_utils import DayType
from models.shift_structure import ShiftStructure
from models.shift import Shift


class ShiftCalendar:
    """Class for shifts over schedule period in calendar dates"""
    def __init__(self, start_date: date, end_date: date,
                 shift_structure: ShiftStructure,
                 day_type: DayType):
        self.start_date = start_date
        self.end_date = end_date
        self.shift_structure = shift_structure
        self.day_type = day_type
        self.calendar: Dict[date, Dict] = {}

        self.build_calendar()

    def build_calendar(self) -> None:
        """Builds the calendar for the given date range"""
        current = self.start_date
        while current <= self.end_date:
            day_type = self.day_type.get_day_type(current)
            dow = current.strftime("%A").lower()
            shifts: List[Shift] = self.shift_structure.get_shifts_for_day(current)

            self.calendar[current] = {
                "day_type": day_type,
                "dow" : dow,
                "shifts": shifts,
                "assigned": {shift.shift_type: [] for shift in shifts}  # Initially empty
            }

            current += timedelta(days=1)

    def get_day(self, dt: date) -> Dict:
        """Returns calendar date"""
        return self.calendar.get(dt, {})

    def __repr__(self):
        """Shift calendar representation"""
        return f"ShiftCalendar({len(self.calendar)} days from {self.start_date} to {self.end_date})"
