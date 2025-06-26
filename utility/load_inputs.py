"""
Loads data from csv files into the classes for doctors and shifts.
"""

from pathlib import Path
from calendar import monthrange
import csv
from datetime import date, datetime, timedelta

from utility.doctor import Doctor
from utility.shift import Shift
from utility.day_type import DayType
from utility.shift_structure import ShiftStructure
from utility.shift_calendar import ShiftCalendar

def parse_date(date_str):
    # Converts 'DD-MM-YYYY' to datetime.date
    return datetime.strptime(date_str, "%d-%m-%Y").date()

def generate_date_range(start_date, end_date):
    # Generates a list of all dates from start_date to end_date inclusive
    current = start_date
    dates = []
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    return dates

def is_valid_weekend_range(start_date, end_date):
    return start_date.weekday() == 4 and end_date.weekday() == 6  # Fri to Sun

def get_month_distribution_dates(tag: str, start: date, end: date) -> list[date] | str | None:
    tag = tag.lower()
    if tag in ("even", "balanced"):
        return "balanced"

    distribution_dates = []
    current = start

    while current <= end:
        last_day = monthrange(current.year, current.month)[1]
        match tag:
            case "beg":
                if 1 <= current.day <= 15:
                    distribution_dates.append(current)
            case "mid":
                if 8 <= current.day <= 23:
                    distribution_dates.append(current)
            case "end":
                if 16 <= current.day <= last_day:
                    distribution_dates.append(current)
        current += timedelta(days=1)

    return distribution_dates if distribution_dates else None

# def doctors_by_experience_level(doctors: dict, level: str) -> list:
#     # Generates a list of doctors with certain experience level
#     return [name for name, doc in doctors.items() if doc.experience_level == level.lower()]

def load_doctors(
    doctors_path: Path,
    leave_path: Path,
    preferences_path: Path,
    pairing_constraints_path: Path
) -> dict:
    doctors = {}
    # Load doctors and experience level
    seniors = []
    juniors = []

    with open(doctors_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["doctor"]
            experience_level = row["level"].lower()
            doctors[name] = Doctor(name=name, experience_level=experience_level)
            doctors[name].no_leave_dates = 0  # Initialize leave dates count here outside leave def
            if experience_level == "senior":
                seniors.append(name)
            elif experience_level == "junior":
                juniors.append(name)
    
    # Load leave dates
    with open(leave_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["doctor"]
            start_date = parse_date(row["start_date"])
            end_date = parse_date(row["end_date"])
            leave_dates = generate_date_range(start_date, end_date)
            no_leave_dates = len(leave_dates)
            if name in doctors:
                doctors[name].add_leave_date(leave_dates)
                doctors[name].no_leave_dates = no_leave_dates


    # Load preferences
    with open(preferences_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["doctor"]
            if name not in doctors:
                continue
            doctor = doctors[name]

            # Prefer to avoid a specific weekend
            if row["avoid_weekend"]:
                try:
                    date_str = row["avoid_weekend"].strip()
                    start_date = parse_date(date_str.strip())
                    end_date = start_date + timedelta(days=2)

                    if not is_valid_weekend_range(start_date, end_date):
                        print(f"Warning: Invalid weekend range for {name}: {start_date} to {end_date}")
                    else:
                        doctor.preferences["avoid_weekend"] = generate_date_range(start_date, end_date)

                except ValueError as e:
                    print(f"Invalid date format for avoid_weekend in {name}: {e}")
                except KeyError as e:
                    print(f"Missing expected column while parsing avoid_weekend for {name}: {e}")

            # Prefer to avoid one specific weekday
            if row["avoid_day"]:
                try:
                    doctor.preferences["avoid_day"] = parse_date(row["avoid_day"].strip())
                except ValueError as e:
                    print(f"Invalid date format for avoid_day in {name}: {e}")
                except KeyError as e:
                    print(f"Missing expected column while parsing avoid_day for {name}: {e}")

            # Prefer how weekends are distributed (as string: "fri-sun", "sat", "none")
            doctor.preferences["prefer_distribution_weekend"] = row["prefer_distribution_weekend"].strip().lower()

            # Prefer distribution over the month
            month_pref = row["prefer_distribution_month"].strip().lower()
            if month_pref:
                doctor.preferences["prefer_distribution_month"] = get_month_distribution_dates(month_pref, start_date, end_date)
            else:
                doctor.preferences["prefer_distribution_month"] = None

            # Notes
            doctor.preferences["notes"] = row["notes"]

    # Load pairing constraints
    with open(pairing_constraints_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            doc1 = row["doctor_1"]
            doc2 = row["doctor_2"]
            constraint = row["type"].strip().lower()

            if doc1 not in doctors:
                continue

            if constraint == "avoid_pair":
                if doc1 in doctors:
                    doctors[doc1].avoid_pair.append(doc2)
            elif constraint == "requires_pair":
                if doc2 == "senior":
                    doctors[doc1].requires_pair.extend(seniors)
                else:
                    doctors[doc1].requires_pair.append(doc2)

    return doctors

def load_shift_structure(shift_structure_path: Path) -> ShiftStructure:
    # Load shift structure from csv
    shift_structure = ShiftStructure()

    with open(shift_structure_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            shift = Shift(
                day=row["day"],
                shift_type=row["shift_type"],
                start_time=row["start_time"],
                end_time=row["end_time"],
                hours=int(row["hours"]),
                required_staff=int(row["required_staff"])
            )
            shift_structure.add_shift(shift)

    return shift_structure

def load_public_holidays(public_holidays_path: Path) -> list[date]:
    holidays = []
    with open(public_holidays_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None) # skip header
        for row in reader:
            if row and row[0].strip():
                holidays.append(datetime.strptime(row[0].strip(), "%d-%m-%Y").date())
    return holidays

def load_schedule_period(schedule_period_path: Path) -> tuple[date, date]:
    with open(schedule_period_path, newline='', encoding='utf-8') as file:
        line = next(file).strip()
        start_str, end_str = line.split(',')
        start_date = datetime.strptime(start_str, "%d-%m-%Y").date()
        end_date = datetime.strptime(end_str, "%d-%m-%Y").date()
        return start_date, end_date

def build_schedule_calendar(start_date, end_date, shift_structure, public_holidays):
    resolver = DayType(public_holidays)
    calendar = ShiftCalendar(start_date, end_date, shift_structure, resolver)
    calendar.build_calendar()
    return calendar
