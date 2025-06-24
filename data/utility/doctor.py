"""
Defines a Doctor class with attributes.
Includes name, experience, leave dates, pairing constraints, and shift preferences. 
"""

from datetime import date
from typing import List, Dict, Union

class Doctor:

    def __init__(self, name: str, experience_level: str):
        self.name: str = name
        self.experience_level: str = experience_level
        self.leave_dates: List[date] = []
        self.no_leave_dates: int = 0
        self.requires_pair: List[str] = []
        self.avoid_pair: List[str] = []
        self.preferences: Dict [str, str] = {
            "avoid_day": None,  # single date string or datetime.date
            "avoid_weekend": None,  # single weekend identifier
            "prefer_distribution_weekend": None,
            "prefer_distribution_month": None,
            "notes": None,
        }
 
    def add_leave_date(self, leave_date: Union[date, List[date]]) -> None:
        if isinstance(leave_date, list):
            self.leave_dates.extend(leave_date)
        else:
            self.leave_dates.append(leave_date)

    def set_preferences(self, preferences: Dict[str, str]) -> None:
        for key, value in preferences.items():
            if key in self.preferences:
                self.preferences[key] = value
            else:
                print(f"Unknown preference key: '{key}'")


    def add_pairing_constraint(self, doctor_2: str, constraint_type: str) -> None:
        constraint_type = constraint_type.lower().strip()

        if constraint_type == "avoid_pair":
            if doctor_2 not in self.avoid_pair:
                self.avoid_pair.append(doctor_2)

        elif constraint_type == "requires_pair":
            if doctor_2 not in self.requires_pair:
                self.requires_pair.append(doctor_2)

        else:
            raise ValueError(f"Invalid constraint type: {constraint_type}")