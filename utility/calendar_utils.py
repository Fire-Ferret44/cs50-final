"""
Defines a DayType class with attributes.
Sees how a day would behave.
Adds public holiday logic.
Checks if date range valid weekend range.
"""

# utility/day_types.py

from datetime import date, timedelta

class DayType:
    """Class to determine the type of day based on public holidays and weekdays."""
    def __init__(self, public_holidays: list[date]):
        self.public_holidays = set(public_holidays)
        self.day_type = {}

    def find_holiday_block(self, dt: date) -> tuple[date | None, date | None]:
        """Determine if there are consecutive public holidays"""

        if dt not in self.public_holidays:
            return None, None

        start = dt
        end = dt

        # Move backwards to find the start of the block
        while start - timedelta(days=1) in self.public_holidays:
            start -= timedelta(days=1)

        # Move forwards to find the end of the block
        while end + timedelta(days=1) in self.public_holidays:
            end += timedelta(days=1)

        return start, end

    def get_day_type(self, dt: date) -> dict:
        """
        Determines what kind of day this is based on:
        - Calendar weekday
        - Public holidays
        - Checks if there are consecutive public holidays
        - Surrounding context (day before or after public holidays)
        """

        weekday = dt.weekday()  # Monday = 0, Sunday = 6
        dow_name = dt.strftime("%A").lower()

        # Determine if today is a public holiday
        in_holiday = dt in self.public_holidays

        # Find block if today is a public holiday
        if in_holiday:
            holiday_start, holiday_end = self.find_holiday_block(dt)
        else:
            holiday_start = holiday_end = None

        # Determine boundaries of holiday block
        day_before_holiday = holiday_start - timedelta(days=1) if holiday_start else None
        day_after_holiday = holiday_end + timedelta(days=1) if holiday_end else None

        is_day_before_holiday = day_before_holiday == dt
        is_day_after_holiday = day_after_holiday == dt

        day_description = None
        day_type = None

        # Today is public holiday
        if in_holiday:
            day_type = 'public_holiday'

            #described like what day it behaves like:
            if weekday <= 3:  # Monday to Thursday
                day_description = 'public_holiday_behaves_like_sunday'
            elif weekday == 4:
                day_description = 'public_holiday_behaves_like_saturday'
            elif weekday == 5:
                day_description = 'public_holiday_saturday'
            else:
                day_description = 'public_holiday_sunday'

        # Day before public holiday(s)
        elif is_day_before_holiday:
            if weekday <= 3:  # Monday to Thursday
                day_type = 'friday'
                day_description = 'pre_holiday_behaves_like_friday'
            elif weekday == 6:
                day_type = 'saturday'
                day_description = 'pre_holiday_behaves_like_saturday'

        # Day after public holiday(s)
        elif is_day_after_holiday:
            if weekday == 5:
                day_type = 'saturday'
                day_description = 'post_holiday_saturday'

        #Regular days
        if day_type is None:
            day_type = self.weekday_to_type(weekday)

        return{
            "dow": dow_name,
            "day_type": day_type,
            "description": day_description
        }

    #day of week integer to type
    def weekday_to_type(self, weekday: int) -> str:
        """ Converts weekday integer to string type """
        if 0 <= weekday <= 3:
            return 'weekday'
        elif weekday == 4:
            return 'friday'
        elif weekday == 5:
            return 'saturday'
        elif weekday == 6:
            return 'sunday'
        return 'unknown_day_type'

def is_valid_weekend_range(start_date, end_date):
    """ Checks if Fri (4) to Sun (6) """
    return start_date.weekday() == 4 and end_date.weekday() == 6
