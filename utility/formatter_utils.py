"""
Formats the schedule and metadata from variables into strings that can be saved
to txt files for test runs or printed to terminal screen.
"""

def format_roster_output(rostered_calendar) -> str:
#formats schedule to txt
    output = []
    for date, info in rostered_calendar.calendar.items():
        output.append(f"{date} ({info['dow']}):")
        for shift_type, doctors in info['assigned'].items():
            formatted_doctors = ', '.join(doctors) if doctors else 'None'
            output.append(f"  - {shift_type}: {formatted_doctors}")
        output.append("")
    return "\n".join(output)

def format_metadata_output(metadata) -> str:
 #formats metadata to txt
    output = []
    for doctor_name, data in metadata.items():
        output.append(f"Doctor: {doctor_name}")
        output.append(f"  Total Shifts Worked: {data.total_shifts_worked}")
        output.append(f"  Total Hours Worked: {data.total_hours_worked:.2f}")
        output.append(f"  Weekday Shifts Worked: {data.weekday_shifts_worked}")
        output.append(f"  Weekend Shifts Worked: {data.weekend_shifts_worked}")
        output.append(f"  Friday Shifts Worked: {data.fri_shifts_worked}")
        output.append(f"  Saturday Shifts Worked: {data.sat_shifts_worked}")
        output.append(f"  Sunday Shifts Worked: {data.sun_shifts_worked}")
        output.append(f"  Public Holidays Worked: {data.total_public_holidays_worked}")
        output.append(f"  Preferences Granted: {data.preferences_granted:.2f}")
        output.append("\n")
    return ", ".join(output)
