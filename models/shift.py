"""
Defines a Shift class with attributes.
Includes day, shift type, start time, end time, hours, required number of staff
"""

class Shift:
    """Represents a work shift with attributes such as day, type, start time, end time"""
    def __init__(self, day, shift_type, start_time, end_time, hours, required_staff):
        self.day = day  # e.g. "Monday"
        self.shift_type = shift_type  # e.g. "short", "long", "24h"
        self.start_time = start_time
        self.end_time = end_time
        self.hours = int(hours)
        self.required_staff = int(required_staff)

    def __repr__(self):
        return (f"Shift(day={self.day}, type={self.shift_type}, "
                f"start={self.start_time}, end={self.end_time}, "
                f"hours={self.hours}, staff={self.required_staff})")
