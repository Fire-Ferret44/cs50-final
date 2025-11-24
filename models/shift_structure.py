"""
Defines a ShiftStructure class that manages shifts for different days.
"""

from pathlib import Path
import csv
from collections import defaultdict
from typing import List, Dict

from models.shift import Shift


class ShiftStructure:
    """Class to manage shifts for different days of the week."""

    DAY_BEHAVIOUR_TO_TEMPLATE_DAY = {
        "weekday": "monday",
        "friday": "friday",
        "saturday": "saturday",
        "sunday": "sunday",
        "public_holiday_behaves_like_saturday": "saturday",
        "public_holiday_behaves_like_sunday": "sunday",
    }

    def __init__(self):
        # Dictionary: day_type (str) -> list of Shift objects
        self.shifts_by_day: Dict[str, List[Shift]] = defaultdict(list)

    def load_from_csv(self, filepath: Path):
        """Loads shift attritubutes"""
        with open(filepath, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                day = row['day'].lower()  # e.g. "monday"
                shift_type = row['shift_type']
                start_time = row['start_time']
                end_time = row['end_time']
                hours = row['hours']
                base_required_staff = int(row['required_staff'])

                shift = Shift(
                    day=day,
                    shift_type=shift_type,
                    start_time=start_time,
                    end_time=end_time,
                    hours=hours,
                    base_required_staff=base_required_staff,
                    required_staff=0  # Placeholder, will be set in calendar
                    )
                self.shifts_by_day[day].append(shift)

    def add_shift(self, shift: Shift):
        """ Adds a shift """
        self.shifts_by_day[shift.day.lower()].append(shift)

    def get_shifts_for_day(self, dt) -> List[Shift]:
        """Return the list of shifts for the given day_type string."""
        dow = dt.strftime('%A').lower()
        return self.shifts_by_day.get(dow.lower(), [])

    def get_shift_duration(self, shift_type: str) -> float:
        """Returns the duration of a shift by its type."""
        for shifts in self.shifts_by_day.values():
            for shift in shifts:
                if shift.shift_type == shift_type:
                    return shift.hours
        raise ValueError(f"Shift type '{shift_type}' not found in the structure.")

    def all_shifts(self) -> List[Shift]:
        """Returns a flat list of all shifts across all days."""
        return [shift for shifts in self.shifts_by_day.values() for shift in shifts]

    def __repr__(self):
        """ShiftStructure representation"""
        return f"ShiftStructure({dict(self.shifts_by_day)})"
