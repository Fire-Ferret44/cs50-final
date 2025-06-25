"""
Defines a DayType class with attributes.
Sees how a day would behave.
Adds public holiday logic.
"""

# utility/day_types.py

from datetime import date, timedelta

class DayType:
    def __init__(self, public_holidays: list[date]):
        self.public_holidays = set(public_holidays)

    def get_day_type(self, dt: date) -> str:
        """
        Determines what kind of day this is based on:
        - Calendar weekday
        - Public holidays
        - Surrounding context (day before or after public holidays)
        """

        weekday = dt.weekday()  # Monday = 0, Sunday = 6

        is_today_ph = dt in self.public_holidays
        is_yesterday_ph = (dt - timedelta(days=1)) in self.public_holidays
        is_tomorrow_ph = (dt + timedelta(days=1)) in self.public_holidays

        if is_today_ph:
            if weekday <= 3:  # Monday to Thursday
                return 'public_holiday_behaves_like_sunday'
            elif weekday == 4:
                return 'public_holiday_behaves_like_saturday'
            elif weekday == 5:
                return 'public_holiday_saturday'
            elif weekday == 6:
                return 'public_holiday_sunday'

        elif is_tomorrow_ph:
            if weekday <= 3:  # Monday to Thursday
                return 'pre_holiday_behaves_like_friday'
            elif weekday == 6:
                return 'pre_holiday_behaves_like_saturday'

        elif is_yesterday_ph:
            if weekday == 5:
                return 'post_holiday_saturday'

        # Regular days
        if 0 <= weekday <= 3:  # Monday to Thursday
            return 'weekday'
        elif weekday == 4:
            return 'friday'
        elif weekday == 5:
            return 'saturday'
        elif weekday == 6:
            return 'sunday'
        return 'unknown_day_type'
