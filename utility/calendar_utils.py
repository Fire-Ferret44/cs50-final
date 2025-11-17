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

    def get_day_type(self, dt: date) -> dict:
        """
        Determines what kind of day this is based on:
        - Calendar weekday
        - Public holidays
        - Surrounding context (day before or after public holidays)
        """

        weekday = dt.weekday()  # Monday = 0, Sunday = 6
        dow_name = dt.strftime("%A").lower()

        # Check public holiday status
        is_today_ph = dt in self.public_holidays
        is_yesterday_ph = dt - timedelta(days=1) in self.public_holidays
        is_tomorrow_ph = dt + timedelta(days=1) in self.public_holidays

        day_description = None
        day_type = None

        # Today is public holiday
        if is_today_ph:
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

        # Tomorrow is public holiday
        elif is_tomorrow_ph:
            if weekday <= 3:  # Monday to Thursday
                day_type = 'friday'
                day_description = 'pre_holiday_behaves_like_friday'
            elif weekday == 6:
                day_type = 'saturday'
                day_description = 'pre_holiday_behaves_like_saturday'

        # Yesterday was public holiday
        elif is_yesterday_ph:
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
