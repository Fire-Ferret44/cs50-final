"""
Defines a ScheduleCalendar class.
Generates a calendar of shifts for a range of days.
"""

from datetime import date, timedelta
from typing import Dict

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
            #Get infor on day behaviour
            day_info = self.day_type.get_day_type(current)
            behaviour = day_info["day_type"]

            #Map behaviour to template day
            template_day = ShiftStructure.DAY_BEHAVIOUR_TO_TEMPLATE_DAY.get(behaviour)
            if template_day is None:
                template_day = current.strftime('%A').lower()

            #Get shifts for that template day
            shifts_for_day = self.shift_structure.shifts_by_day.get(template_day, [])

            date_string = current.strftime("%y%m%d")

            #Add actual dates
            dated_shifts = []
            for shift in shifts_for_day:
                #add slot number to id
                for slot_number in range(1, shift.base_required_staff + 1):
                    shift_id = (
                        f"{date_string}_{day_info['dow'].lower()}_"
                        f"{shift.shift_type}_{slot_number}"
                    )

                    new_shift = Shift(
                        day=shift.day,
                        shift_type=shift.shift_type,
                        start_time=shift.start_time,
                        end_time=shift.end_time,
                        hours=shift.hours,
                        base_required_staff=shift.base_required_staff,
                        required_staff=1, # Each dated shift represents one staff slot
                        slot_number=slot_number,
                        date=current, # Assign the current date to the shift
                        shift_id=shift_id, # Assign the unique shift ID
                        overlap=shift.overlap, # Carry over overlap attribute
                    )
                    dated_shifts.append(new_shift)

            self.calendar[current] = {
                "dow": day_info['dow'],
                "day_type": day_info['day_type'],
                "description": day_info['description'],
                "shifts": dated_shifts,
                "assigned": {shift.shift_id: [] for shift in dated_shifts}  # Initially empty
            }

            current += timedelta(days=1)

    def get_day(self, dt: date) -> Dict:
        """Returns calendar date"""
        return self.calendar.get(dt, {})

    def __repr__(self):
        """Shift calendar representation"""
        return f"ShiftCalendar({len(self.calendar)} days from {self.start_date} to {self.end_date})"
