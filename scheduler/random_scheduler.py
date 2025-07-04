"""
Scheduler that randomly assigns shifts to available doctors.
Output creater to work on the metadata creator & general input --> output interface.
"""

import random
from datetime import date

from utility.shift_calendar import ShiftCalendar
from utility.doctor import Doctor

def is_doctor_available(doctor: Doctor, day: date) -> bool:
    
    return day not in doctor.leave_dates

def run_random_scheduler(doctors: list[Doctor], calendar: ShiftCalendar) -> ShiftCalendar:
    for day, info in calendar.calendar.items():
        assigned_today = set()

        for shift in info["shifts"]:
            needed = shift.required_staff
            candidates = [doc for doc in doctors if is_doctor_available(doc, day) and doc.name not in assigned_today]

            selected = random.sample(candidates, k=min(needed, len(candidates)))

            calendar.calendar[day]["assigned"][shift.shift_type] = [doc.name for doc in selected]

            for doc in selected:
                assigned_today.add(doc.name)

    return calendar
