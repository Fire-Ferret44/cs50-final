"""Check whether uploaded files are csv and have the correct headings."""

import csv
import io

REQUIRED_HEADINGS = {
    "doctors": ["doctor","level","requires_overlap"],
    "leave": ["doctor", "start_date","end_date"],
    "pairing_constraints": ["doctor_1","doctor_2","pair_type"],
    "schedule_period": ["start_date","end_date"],
    "shift_structure": ["day","shift_type","start_time","end_time","hours",
                        "required_staff","overlap"]
}

def validate_if_csv(file) -> bool:
    """Validate that the file is a csv file."""
    return file.filename.endswith(".csv") #currently not very robust but works for now.


def validate_headings(file, filename: str) -> tuple[bool, str]:
    """
    Validate that the CSV file has the expected headings.
    
    Args:
        file: A file-like object containing CSV data.
        expected_headings: A list of expected headings.
        
    Returns:
        bool: True if the headings match, False otherwise.
    """
    expected_headings = REQUIRED_HEADINGS.get(filename)
    if expected_headings is None:
        return False, f"No expected headers defined for '{filename}'"

    try:
        file.stream.seek(0)  # Reset file pointer to the beginning
        text = file.stream.read().decode('utf-8')
        reader = csv.reader(io.StringIO(text))
        actual_headings = next(reader)
    except Exception as e:
        return False, f"Could not read {filename}.csv: {e}"

    if sorted(actual_headings) != sorted(expected_headings):
        return False, (
            f"{filename}.csv has incorrect headers.\n"
            f"Expected: {expected_headings}\n"
            f"Found: {actual_headings}"
        )

    return True, ""
