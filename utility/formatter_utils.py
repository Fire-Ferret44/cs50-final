"""
Formats the schedule and metadata from variables into strings that can be saved
to txt files for test runs or printed to terminal screen.
"""

def format_roster_output(solution, shift_by_id, shift_calendar) -> str:
    """formats schedule to txt"""

    output = []
    current_week = None
    current_date = None

    max_shift_id_len = max(len(str(shift_id)) for shift_id in solution.keys())

    sorted_shifts = sorted(
        solution.keys(), key=lambda s: (shift_by_id[s].date, s)
    )

    for shift_id in sorted_shifts:
        shift = shift_by_id[shift_id]
        doctor = solution[shift_id]
        shift_date = shift.date

        week_number = shift_date.isocalendar()[1]
        if current_week is not None and week_number != current_week:
            output.append("")
        current_week = week_number

        if shift_date != current_date:
            day_info = shift_calendar.calendar[shift_date]

            dow = day_info['dow'][:3].upper()
            act = day_info['day_type'].lower()

            header = f"{shift_date} {dow} {act}"

            is_weekend_acting = act in ("friday", "saturday", "sunday")
            is_public_holiday = (
                day_info.get("description") is not None
                and "public_holiday" in day_info["description"]
            )

            if is_weekend_acting and is_public_holiday:
                header = f"<b><i>{header}</i></b>"
            elif is_weekend_acting:
                header = f"<b>{header}</b>"
            elif is_public_holiday:
                header = f"<i>{header}</i>"

            output.append(header)
            current_date = shift_date

        output.append(f"  | {shift.shift_id:<{max_shift_id_len}} | Doctor {doctor}")

    return "\n".join(output)

def format_metadata_output(doctor_stats) -> str:
    """formats metadata to txt"""

    output = []

    for doctor, stats in sorted(doctor_stats.items()):
        output.append(f"Doctor: {doctor}")
        output.append(f"  Total Shifts Worked: {stats['shifts']}")
        output.append(f"  Total Hours Worked: {stats['hours']:.2f}")
        output.append(f"  Weekend Shifts Worked: {stats['weekend_shifts']}")
        output.append("\n")
    return "\n".join(output)
