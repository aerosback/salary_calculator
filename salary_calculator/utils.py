import calendar
from datetime import date, datetime, time, timedelta
from typing import Tuple

__weekdays_mappings = {
    "SU": calendar.SUNDAY,
    "MO": calendar.MONDAY,
    "TU": calendar.TUESDAY,
    "WE": calendar.WEDNESDAY,
    "TH": calendar.THURSDAY,
    "FR": calendar.FRIDAY,
    "SA": calendar.SATURDAY,
}


def get_calendar_day_by_abbrev(abbrev: str) -> int:
    try:
        calendar_day = __weekdays_mappings[abbrev]
    except KeyError as exc:
        raise ValueError(f"week day prefix:{abbrev} is invalid") from exc
    return calendar_day


def get_abbrev_by_calendar_day(calendar_day: int) -> str:
    return list(__weekdays_mappings.keys())[
        list(__weekdays_mappings.values()).index(calendar_day)
    ]


def normalize(value: time) -> Tuple[bool, time]:
    """
    Return a tuple of whether normalization was performed on passed value, and the normalized value.
    A time value is normalized if it corresponds to the midnight time, which should be greater than any other
    time value according to the project logic.
    Hence, such value is converted into the time value "23:59:59" to allow sort and substraction logic.
    """
    requires_normalization = time(0, 0) <= value < time(0, 1)
    returned_value = value if not requires_normalization else time(23, 59, 59)
    return requires_normalization, returned_value


def substract_time_values(value: time, other_value: time) -> timedelta:
    first_value = datetime.combine(date.today(), value)
    second_value = datetime.combine(date.today(), other_value)
    return first_value - second_value
