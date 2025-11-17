"""
Defines a Shift class with attributes.
Includes day, shift type, start time, end time, hours, required number of staff
"""

class Shift:
    """Represents a work shift with attributes such as day, type, start time, end time"""
    def __init__(
        self,
        day: str,
        shift_type: str,
        start_time,
        end_time,
        hours: int,
        base_required_staff: int,
        required_staff: int,
        date=None,
        shift_id=None,
        slot_number=None,
    ):
        self.day = day  # e.g. "Monday"
        self.shift_type = shift_type  # e.g. "short", "long", "24h"
        self.start_time = start_time
        self.end_time = end_time
        self.hours = int(hours)
        self.base_required_staff = int(base_required_staff)
        self.required_staff = int(required_staff) # In calendar this will be 1 per slot
        self.date = date  # Added date attribute if tied to calendar
        self.shift_id = shift_id  # Unique identifier for the shift
        self.slot_number = slot_number  # For shifts requiring multiple staff

    def __repr__(self):
        return (f"Shift(date={self.date}, "
                f"day={self.day},  "
                f"id={self.shift_id}, "
                f"slot={self.slot_number})")
