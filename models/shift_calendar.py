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
            date_string = current.strftime("%d%m%y")
            shifts: List[Shift] = self.shift_structure.get_shifts_for_day(current)

            #Add actual dates
            dated_shifts = []
            type_count = {} #if there are 2 identical shifts we should numerate them to differentiate

            for shift in shifts:
                type_count[shift.shift_type] = type_count.get(shift.shift_type, 0) + 1
                slot = type_count[shift.shift_type]

                #add slot number to id if >1
                if slot > 1: 
                    shift_id = f"{date_string}_{dow}_{shift.shift_type}_{slot}"
                else:
                    shift_id = f"{date_string}_{dow}_{shift.shift_type}"

                dated_shift = Shift(
                    day=shift.day,
                    shift_type=shift.shift_type,
                    start_time=shift.start_time,
                    end_time=shift.end_time,
                    hours=shift.hours,
                    required_staff=shift.required_staff,
                    date=current, # Assign the current date to the shift
                    shift_id=shift_id  # Assign the unique shift ID
                )
                dated_shifts.append(dated_shift)

            shifts = dated_shifts # Replace with dated shifts

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
