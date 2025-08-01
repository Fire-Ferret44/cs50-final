"""Main entry point for workings of app.
function run_scheduler_from_paths for flask app and
function main for running scheduler from command line for testing
"""

from datetime import datetime
from pathlib import Path
from scheduler.random_scheduler import run_random_scheduler
from services.load_inputs import (
    load_doctors,
    load_shift_structure,
    # load_schedule_period,
    load_public_holidays,
    load_shift_calendar,
)
from services.metadata_generator import generate_metadata
from utility.filereader_utils import get_next_file_number
from utility.formatter_utils import format_roster_output, format_metadata_output

def run_scheduler_from_paths(input_path: Path, filenumber: int):
    """Function that can be used in with the flask app to run scheduler."""
    print("Running: run_scheduler_from_paths()")
    doctors = load_doctors(
        doctors_path=input_path / f"doctors_{filenumber}.csv",
        leave_path=input_path / f"leave_{filenumber}.csv",
        pairing_constraints_path=input_path / f"pairing_constraints_{filenumber}.csv",
        preferences_path=input_path / f"preferences_{filenumber}.csv"
    )
    
    shift_structure = load_shift_structure(input_path, filenumber)
    shift_calendar = load_shift_calendar(input_path, filenumber) # schedule period read within this function
    rostered_calendar = run_random_scheduler(list(doctors.values()), shift_calendar)
    public_holidays = load_public_holidays(input_path)
    metadata = generate_metadata(rostered_calendar, list(doctors.values()), shift_structure, public_holidays)

    schedule_text = format_roster_output(rostered_calendar)
    metadata_text = format_metadata_output(metadata)

    #file_number = get_next_file_number(output_dir)

    return {
        "schedule_text": schedule_text,
        "metadata_text": metadata_text,
    #    "file_number": file_number
    }

def main():
    """ Paths for input data """
    print("Running: main()")
    base_path = Path("data/input") # Defines path to input data folder

    doctors = load_doctors(
        doctors_path=base_path / "doctors.csv",
        leave_path=base_path / "leave.csv",
        pairing_constraints_path=base_path / "pairing_constraints.csv",
        preferences_path=base_path / "preferences.csv"
    )

    shift_structure = load_shift_structure(base_path / "shift_structure.csv", filenumber=0)
    # schedule_period = load_schedule_period(base_path / "schedule_period.csv")
    public_holidays = load_public_holidays(base_path / "public_holidays_2025.csv")

    print(f"Loaded {len(doctors)} doctors")
    # for name, doctor in doctors.items():
    #     print(f"{name}: {doctor}\n")


    data_path = Path("data/input")
    shift_calendar = load_shift_calendar(data_path, filenumber=0)  # Load shift calendar with schedule period read within this function

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
    metadata = generate_metadata(rostered_calendar, list(doctors.values()), shift_structure, public_holidays)

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
