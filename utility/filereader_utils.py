"""
Helper functions that read the files in the test folder and return the highest
value x where the test file names would be test_x_schedule.txt and test_x_metadata.txt.
This will be used to determine the next file name.
"""

from pathlib import Path
import re

def get_next_file_number(output_dir: Path) -> int:
    """
    Get the next test file number based on existing test files in the folder.
    Args: test_folder (Path)
    Returns: int
    """
    pattern = re.compile(r'test_(\d+)_schedule\.txt')
    max_number = 0
    
    for file in output_dir.iterdir():
        if file.is_file() and pattern.match(file.name):
            match = pattern.search(file.name)
            if match:
                number = int(match.group(1))
                max_number = max(max_number, number)
    
    return max_number + 1
