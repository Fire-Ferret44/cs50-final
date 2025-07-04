"""Main entry point for workings of app."""

from pathlib import Path
from utility.load_inputs import (
    load_doctors,
    load_shift_structure,
    load_schedule_period,
    load_public_holidays,
    load_shift_calendar,
)
from scheduler.random_scheduler import run_random_scheduler

def main():
    """ Paths for input data """
    base_path = Path("data/input") # Defines path to input data folder

    doctors = load_doctors(
        doctors_path=base_path / "doctors.csv",
        leave_path=base_path / "leave.csv",
        pairing_constraints_path=base_path / "pairing_constraints.csv",
        preferences_path=base_path / "preferences.csv"
    )

    shift_structure = load_shift_structure(base_path / "shift_structure.csv")
    schedule_period = load_schedule_period(base_path / "schedule_period.csv")
    public_holidays = load_public_holidays(base_path / "public_holidays_2025.csv")

    print(f"Loaded {len(doctors)} doctors")
    for name, doctor in doctors.items():
        print(f"{name}: {doctor}\n")



    data_path = Path("data/input")
    shift_calendar = load_shift_calendar(data_path)

    # Run the scheduling algorithm
    print("Running scheduling algorithm...") # Placeholder
    rostered_calendar = run_random_scheduler(list(doctors.values()), shift_calendar)

    # Output / export the result
    print("Schedule generated successfully:") # Placeholder

    for day, info in rostered_calendar.calendar.items():
        print(f"\n{day} ({info['dow']})")
        for shift_type, assigned in info["assigned"].items():
            print(f"  - {shift_type}: {', '.join(assigned) or 'None'}")

if __name__ == "__main__":
    main()
