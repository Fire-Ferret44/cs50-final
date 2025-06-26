"""
Defines a ShiftStructure class that manages shifts for different days.
"""

from pathlib import Path
import csv
from collections import defaultdict
from typing import List

from utility.shift import Shift


class ShiftStructure:
    def __init__(self):
        # Dictionary: day_type (str) -> list of Shift objects
        self.shifts_by_day = defaultdict(list)

    def load_from_csv(self, filepath: Path):
        with open(filepath, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                day = row['day'].lower()  # e.g. "monday"
                shift_type = row['shift_type']
                start_time = row['start_time']
                end_time = row['end_time']
                hours = row['hours']
                required_staff = row['required_staff']

                shift = Shift(day, shift_type, start_time, end_time, hours, required_staff)
                self.shifts_by_day[day].append(shift)

    def add_shift(self, shift: Shift):
        self.shifts_by_day[shift.day.lower()].append(shift)

    def get_shifts_for_day(self, day_type: str) -> List[Shift]:
        """Return the list of shifts for the given day_type string."""
        return self.shifts_by_day.get(day_type.lower(), [])

    def all_shifts(self) -> List[Shift]:
        return [shift for shifts in self.shifts_by_day.values() for shift in shifts]

    def __repr__(self):
        return f"ShiftStructure({dict(self.shifts_by_day)})"
