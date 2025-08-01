"""
Loads data from csv files into the classes for doctors and shifts.
"""

from models.metadata import DoctorMetadata
from utility.calendar_utils import DayType

def generate_metadata(rostered_calendar, doctors, shift_structure, public_holidays) -> dict[str, DoctorMetadata]:
    """
    Generates metadata for each doctor based on the rostered calendar.
    """
    metadata_info = {}
    
    for doctor in doctors:
        metadata_info[doctor.name] = DoctorMetadata(
            name=doctor.name,
            total_shifts_worked=0,
            weekday_shifts_worked=0,
            fri_shifts_worked=0,
            sat_shifts_worked=0,
            sun_shifts_worked=0,
            weekend_shifts_worked=0,
            public_holidays_worked=0,
            total_hours_worked=0.0,
            preferences_granted=0.0
        )

    for day, info in rostered_calendar.calendar.items():
        day_type_instance = DayType(public_holidays=public_holidays)
        day_type_str = day_type_instance.get_day_type(day)
        # Get the metadata for the day type
        for shift_type, assigned in info["assigned"].items():
            for doctor_name in assigned:
                if doctor_name in metadata_info:
                    metadata_info[doctor_name].total_shifts_worked += 1
                    metadata_info[doctor_name].total_hours_worked += shift_structure.get_shift_duration(shift_type)
                if day_type_str == 'weekday':
                    metadata_info[doctor_name].weekday_shifts_worked += 1
                elif day_type_str == 'friday':
                    metadata_info[doctor_name].fri_shifts_worked += 1
                elif day_type_str == 'saturday':
                    metadata_info[doctor_name].sat_shifts_worked += 1
                elif day_type_str == 'sunday':
                    metadata_info[doctor_name].sun_shifts_worked += 1
                elif 'public_holiday' in day_type_str:
                    metadata_info[doctor_name].public_holidays_worked += 1
                # Optionally handle public holiday types. Yes to be worked on!
                    pass

        # For weekend shifts (Friday, Saturday, Sunday, and public holiday weekends)
        if day_type_str in ('friday', 'saturday', 'sunday') or 'public_holiday' in day_type_str:
            metadata_info[doctor_name].weekend_shifts_worked += 1
    
    return metadata_info
