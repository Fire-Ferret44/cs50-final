"""
Loads data from csv files into the classes for doctors and shifts.
"""

from pathlib import Path
from calendar import monthrange
import csv
from datetime import date, datetime, timedelta

from utility.calendar_utils import DayType, is_valid_weekend_range
from utility.date_utils import parse_date, generate_date_range
from models.doctor import Doctor
from models.shift import Shift
from models.shift_structure import ShiftStructure
from models.shift_calendar import ShiftCalendar

def get_month_distribution_dates(tag: str, start: date, end: date) -> list[date] | str | None:
    """ Gets range of dates based on preference """
    tag = tag.lower()
    if tag in ("even"):
        return "even"

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
    #Loads doctors and their attributes
    doctors_path: Path,
    leave_path: Path,
    preferences_path: Path,
    pairing_constraints_path: Path
) -> dict:
    doctors = {}
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

    with open(leave_path, newline='', encoding='utf-8') as file:
        #Loads leave dates
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

    with open(preferences_path, newline='', encoding='utf-8') as file:
        #Loads preferences
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
                        print(f"Invalid weekend range for {name}: {start_date} to {end_date}")
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

    # Loads pairing constraints
    with open(pairing_constraints_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            doc1 = row["doctor_1"]
            doc2 = row["doctor_2"]
            constraint = row["type"].strip().lower()

            if doc1 not in doctors:
                print(f"Doctor {doc1} not found in doctors list. Skipping constraint.")
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
    """Loads shift structure from csv"""
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
    """Loads public holidays form csv"""
    holidays = []
    with open(public_holidays_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None) # skip header
        for row in reader:
            if row and row[0].strip():
                holidays.append(datetime.strptime(row[0].strip(), "%d-%m-%Y").date())
    return holidays

def load_schedule_period(schedule_period_path: Path) -> tuple[date, date]:
    """Loads schedule period from csv"""
    with open(schedule_period_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header
        line = next(file).strip()
        start_str, end_str = line.split(',')
        start_date = datetime.strptime(start_str, "%d-%m-%Y").date()
        end_date = datetime.strptime(end_str, "%d-%m-%Y").date()
        return start_date, end_date

def build_schedule_calendar(start_date, end_date, shift_structure, public_holidays):
    """Builds a schedule calendar i.e. calendar of schedule period"""
    resolver = DayType(public_holidays)
    calendar = ShiftCalendar(start_date, end_date, shift_structure, resolver)
    calendar.build_calendar()
    return calendar


def load_shift_calendar(data_path: Path) -> ShiftCalendar:
    """Builds a shift calendar i.e. number and type of shifts that need to be filled"""
    with open(data_path / 'schedule_period.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        row = next(reader)
        start_date = datetime.strptime(row['start_date'], '%d-%m-%Y').date()
        end_date = datetime.strptime(row['end_date'], '%d-%m-%Y').date()

    shift_structure = ShiftStructure()
    shift_structure.load_from_csv(data_path / 'shift_structure.csv')

    public_holidays = []
    with open(data_path / 'public_holidays_2025.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            public_holidays.append(datetime.strptime(row['date'], '%d-%m-%Y').date())

    day_type = DayType(public_holidays)

    shift_calendar = ShiftCalendar(
        start_date=start_date,
        end_date=end_date,
        shift_structure=shift_structure,
        day_type=day_type
    )

    return shift_calendar
