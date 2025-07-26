"""Main entry point for workings of app."""

from datetime import datetime
from pathlib import Path
from scheduler.random_scheduler import run_random_scheduler
from services.load_inputs import (
    load_doctors,
    load_shift_structure,
    load_schedule_period,
    load_public_holidays,
    load_shift_calendar,
)
from services.metadata_generator import generate_metadata
from utility.filereader_utils import get_next_file_number
from utility.formatter_utils import format_roster_output, format_metadata_output

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
    # for name, doctor in doctors.items():
    #     print(f"{name}: {doctor}\n")


    data_path = Path("data/input")
    shift_calendar = load_shift_calendar(data_path)

    # Run the scheduling algorithm
    rostered_calendar = run_random_scheduler(list(doctors.values()), shift_calendar)

    # Output / export the result
    output_dir = Path("tests/output/random_scheduler_output")
    file_number = get_next_file_number(output_dir)

    # Create filenames for schedule output
    schedule_filename = output_dir / f"test_{file_number}_schedule.txt"
    schedule_text = format_roster_output(rostered_calendar)

    # Save schedule with timestamp
    with open(schedule_filename, 'w', encoding='utf-8') as s_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s_file.write(f"Generated on: {timestamp}\n\n")
        s_file.write(schedule_text)

    # Print the schedule to terminal
    # print(f"Following schedule saved to {schedule_filename}:\n")
    # print(schedule_text)

    # Run the metadata generation
    metadata = generate_metadata(rostered_calendar, list(doctors.values()), shift_structure)

    # Create filename for metadata output
    metadata_filename = output_dir / f"test_{file_number}_metadata.txt"
    metadata_text = format_metadata_output(metadata)
   
    # Save metadata with timestamp
    with open(metadata_filename, 'w', encoding='utf-8') as m_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        m_file.write(f"Generated on: {timestamp}\n\n")
        m_file.write(metadata_text)
    
    # Print the metadata to terminal
    # print(f"Following metadata saved to {metadata_filename}:\n")
    # print(metadata_text)

if __name__ == "__main__":
    main()
