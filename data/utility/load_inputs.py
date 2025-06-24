"""
Loads data from csv files into the classes for doctors and shifts.
"""

from pathlib import Path
import csv
from datetime import datetime, timedelta
from utility.doctor import Doctor

base_path = Path("data/input") # Defines path to input data folder

input_paths = {
    "doctors_csv": base_path / "doctors.csv",
    "leave": base_path / "leave.csv",
    "pairing_constraints": base_path / "pairing_constraints.csv",
    "preferences": base_path / "preferences.csv",
    "shift_structure": base_path / "shift_structure.csv"
}

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

# def doctors_by_experience_level(doctors: dict, level: str) -> list:
#     # Generates a list of doctors with certain experience level
#     return [name for name, doc in doctors.items() if doc.experience_level == level.lower()]

def load_doctors(path: Path) -> dict:
    doctors = {}
    # Load doctors and experience level
    seniors = []
    juniors = []

    with open(path["doctors_csv"], newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["doctor"]
            experience_level = row["experience_level"].lower()
            doctors[name] = Doctor(name=name, experience_level=experience_level)
            if experience_level == "senior":
                seniors.append(name)
            elif experience_level == "junior":
                juniors.append(name)
    
    # Load leave dates
    with open(path["leave"], newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["doctor"]
            start_date = parse_date(row["start_date"])
            end_date = parse_date(row["end_date"])
            leave_dates = generate_date_range(start_date, end_date)
            if leave_dates:
                no_leave_dates = len(leave_dates)
            else:
                no_leave_dates = 0
            if name in doctors:
                doctors[name].add_leave_date(leave_dates)
                doctors[name].no_leave_dates = no_leave_dates


    # Load preferences
    with open(path["preferences"], newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["doctor"]
            if name not in doctors:
                continue
            doctor = doctors[name]

            # Simple fields
            doctor.preferences["prefer_weekday_off"] = row["prefer_weekday_off"]
            doctor.preferences["prefer_not_weekend_dates"] = row["prefer_not_weekend_dates"]
            doctor.preferences["prefer_not_weekend_range"] = row["prefer_not_weekend_range"]
            doctor.preferences["prefer_distribution_weekend"] = row["prefer_distribution_weekend"]
            doctor.preferences["prefer_distribution_month"] = row["prefer_distribution_month"]
            doctor.preferences["notes"] = row["notes"]

    # Load pairing constraints
    with open(path["pairing_constraints"], newline='', encoding='utf-8') as file:
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