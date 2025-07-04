"""Class for metadata of shift."""

class DoctorMetadata:
    """Metadata for a doctor."""
    def __init__(self, name: str, total_shifts_worked: int, weekday_shifts_worked: int, fri_shifts_worked: int,
                 sat_shifts_worked: int, sun_shifts_worked: int, weekend_shifts_worked: int,
                 total_hours_worked: float, preferences_granted: float):
        self.name = name
        self.total_shifts_worked = total_shifts_worked
        self.weekday_shifts_worked = weekday_shifts_worked
        self.fri_shifts_worked = fri_shifts_worked
        self.sat_shifts_worked = sat_shifts_worked
        self.sun_shifts_worked = sun_shifts_worked
        self.weekend_shifts_worked = weekend_shifts_worked
        self.total_hours_worked = total_hours_worked
        self.preferences_granted = preferences_granted
    
    def __repr__(self):
        return (f"DoctorMetadata(name={self.name}, total_shifts_worked={self.total_shifts_worked}, "
                f"weekday_shifts_worked={self.weekday_shifts_worked}, "
                f"fri_shifts_worked={self.fri_shifts_worked}, "
                f"sat_shifts_worked={self.sat_shifts_worked}, "
                f"sun_shifts_worked={self.sun_shifts_worked}, "
                f"weekend_shifts_worked={self.weekend_shifts_worked}, "
                f"total_hours_worked={self.total_hours_worked}, "
                f"preferences_granted={self.preferences_granted})")
