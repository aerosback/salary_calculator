from datetime import datetime

from salary_calculator.classes import EmployeeSchedule, WorkingDaySpan
from salary_calculator.utils import get_calendar_day_by_abbrev


class EmployeeScheduleSerializer:
    def __init__(self, raw_str) -> None:
        self.raw_data = raw_str

    def serialize(self) -> EmployeeSchedule:
        spans = []
        equals_index = self.raw_data.index("=")
        username = self.raw_data[0:equals_index]
        spans_substr = self.raw_data[equals_index + 1 :]

        for span_token in spans_substr.split(","):
            weekday_token = span_token[0:2]
            start_token, end_token = span_token[2:].split("-")
            weekday = get_calendar_day_by_abbrev(weekday_token)
            start = datetime.strptime(start_token, "%H:%M").time()
            end = datetime.strptime(end_token, "%H:%M").time()
            span = WorkingDaySpan(weekday=weekday, start=start, end=end)
            spans.append(span)
        return EmployeeSchedule(working_days_spans=spans, username=username)
