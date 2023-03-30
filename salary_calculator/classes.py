import calendar
from dataclasses import dataclass, field
from datetime import time
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Tuple

from salary_calculator.exceptions import StartGreaterThanEndError
from salary_calculator.utils import (get_abbrev_by_calendar_day, normalize,
                                     substract_time_values)


class IntersectionTypes(Enum):
    NO_INTERSECTION = 1
    FITS_IN_CURRENT = 2
    EXCEEDS_CURRENT = 3
    START_BOUNDED = 4
    END_BOUNDED = 5


@dataclass
class TimeSpan:
    start: time
    end: time
    raw_end: time

    def __init__(self, start: time, end: time) -> None:
        _, normalized_end = normalize(end)
        if start > normalized_end:
            raise StartGreaterThanEndError(
                f"start time({start}) should be greather or equal to end time({end})"
            )
        self.raw_end = end
        self.start, self.end = start, normalized_end

    def __eq__(self, other):
        return (self.start, self.end) == (other.start, other.end)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.start, self.end) < (other.start, other.end)

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return (self.start, self.end) > (other.start, other.end)

    def __ge__(self, other):
        return self > other or self == other

    def __str__(self):
        return "%s-%s[%s]" % (
            self.start.strftime("%H:%M"),
            self.end.strftime("%H:%M"),
            self.raw_end.strftime("%H:%M"),
        )

    def __repr__(self):
        return "%s-%s[%s]" % (
            self.start.strftime("%H:%M"),
            self.end.strftime("%H:%M"),
            self.raw_end.strftime("%H:%M"),
        )

    def get_simple_format(self) -> str:
        return "%s-%s" % (self.start.strftime("%H:%M"), self.raw_end.strftime("%H:%M"))

    def get_intersection(self, other) -> Tuple[IntersectionTypes, int]:
        intersection_mins = 0
        start_is_bounded = self.start <= other.start <= self.end
        end_is_bounded = self.start <= other.end <= self.end
        other_span_exceeds_current = (
            other.start <= self.start <= other.end
            and other.start <= self.end <= other.end
        )
        other_span_fits_in_current = start_is_bounded and end_is_bounded

        current_case = IntersectionTypes.NO_INTERSECTION

        if other_span_fits_in_current:
            intersection_mins = (
                substract_time_values(other.end, other.start).total_seconds() // 60
            )
            current_case = IntersectionTypes.FITS_IN_CURRENT
        elif other_span_exceeds_current:
            intersection_mins = (
                substract_time_values(self.end, self.start).total_seconds() // 60
            )
            current_case = IntersectionTypes.EXCEEDS_CURRENT
        elif start_is_bounded:
            intersection_mins = (
                substract_time_values(self.end, other.start).total_seconds() // 60
            )
            current_case = IntersectionTypes.START_BOUNDED
        elif end_is_bounded:
            intersection_mins = (
                substract_time_values(other.end, self.start).total_seconds() // 60
            )
            current_case = IntersectionTypes.END_BOUNDED
        return current_case, intersection_mins


@dataclass
class WorkingDaySpan:
    weekday: int
    span: TimeSpan

    def __init__(self, *, weekday: int, start: time, end: time) -> None:
        self.span = TimeSpan(start, end)
        self.weekday = weekday

    def __str__(self) -> str:
        abbrev_weekday = get_abbrev_by_calendar_day(self.weekday)
        formated_span = self.span.get_simple_format()
        return f"{abbrev_weekday} -> {formated_span}"


@dataclass
class PaymentTimeSlot:
    span: TimeSpan
    hour_amount: Decimal

    def __init__(self, *, start: time, end: time, hour_amount: Decimal) -> None:
        self.span = TimeSpan(start, end)
        self.hour_amount = hour_amount


@dataclass
class EmployeeSchedule:
    username: Optional[str] = None
    working_days_spans: List[WorkingDaySpan] = field(default_factory=list)

    """
    |                | M  | T  | W  | Th | F  | Sa | Su |
    |----------------|----|----|----|----|----|----|----|
    | 00:01 -> 09:00 | 25 | 25 | 25 | 25 | 25 | 30 | 30 |
    | 09:01 -> 18:00 | 15 | 15 | 15 | 15 | 15 | 20 | 20 |
    | 18:01 -> 00:00 | 20 | 20 | 20 | 20 | 20 | 25 | 25 |

    """

    __weekday_time_payments = {
        calendar.SUNDAY: [
            PaymentTimeSlot(
                start=time(0, 1, 0), end=time(9, 0, 0), hour_amount=Decimal(30.0)
            ),
            PaymentTimeSlot(
                start=time(9, 1, 0), end=time(18, 0, 0), hour_amount=Decimal(20.0)
            ),
            PaymentTimeSlot(
                start=time(18, 1, 0), end=time(0, 0, 0), hour_amount=Decimal(25.0)
            ),
        ],
        calendar.MONDAY: [
            PaymentTimeSlot(
                start=time(0, 1, 0), end=time(9, 0, 0), hour_amount=Decimal(25.0)
            ),
            PaymentTimeSlot(
                start=time(9, 1, 0), end=time(18, 0, 0), hour_amount=Decimal(15.0)
            ),
            PaymentTimeSlot(
                start=time(18, 1, 0), end=time(0, 0, 0), hour_amount=Decimal(20.0)
            ),
        ],
        calendar.TUESDAY: [
            PaymentTimeSlot(
                start=time(0, 1, 0), end=time(9, 0, 0), hour_amount=Decimal(25.0)
            ),
            PaymentTimeSlot(
                start=time(9, 1, 0), end=time(18, 0, 0), hour_amount=Decimal(15.0)
            ),
            PaymentTimeSlot(
                start=time(18, 1, 0), end=time(0, 0, 0), hour_amount=Decimal(20.0)
            ),
        ],
        calendar.WEDNESDAY: [
            PaymentTimeSlot(
                start=time(0, 1, 0), end=time(9, 0, 0), hour_amount=Decimal(25.0)
            ),
            PaymentTimeSlot(
                start=time(9, 1, 0), end=time(18, 0, 0), hour_amount=Decimal(15.0)
            ),
            PaymentTimeSlot(
                start=time(18, 1, 0), end=time(0, 0, 0), hour_amount=Decimal(20.0)
            ),
        ],
        calendar.THURSDAY: [
            PaymentTimeSlot(
                start=time(0, 1, 0), end=time(9, 0, 0), hour_amount=Decimal(25.0)
            ),
            PaymentTimeSlot(
                start=time(9, 1, 0), end=time(18, 0, 0), hour_amount=Decimal(15.0)
            ),
            PaymentTimeSlot(
                start=time(18, 1, 0), end=time(0, 0, 0), hour_amount=Decimal(20.0)
            ),
        ],
        calendar.FRIDAY: [
            PaymentTimeSlot(
                start=time(0, 1, 0), end=time(9, 0, 0), hour_amount=Decimal(25.0)
            ),
            PaymentTimeSlot(
                start=time(9, 1, 0), end=time(18, 0, 0), hour_amount=Decimal(15.0)
            ),
            PaymentTimeSlot(
                start=time(18, 1, 0), end=time(0, 0, 0), hour_amount=Decimal(20.0)
            ),
        ],
        calendar.SATURDAY: [
            PaymentTimeSlot(
                start=time(0, 1, 0), end=time(9, 0, 0), hour_amount=Decimal(30.0)
            ),
            PaymentTimeSlot(
                start=time(9, 1, 0), end=time(18, 0, 0), hour_amount=Decimal(20.0)
            ),
            PaymentTimeSlot(
                start=time(18, 1, 0), end=time(0, 0, 0), hour_amount=Decimal(25.0)
            ),
        ],
    }

    def __str__(self) -> str:
        weekday_grouped_spans = {}
        for span in self.working_days_spans:
            if span.weekday not in weekday_grouped_spans:
                weekday_grouped_spans[span.weekday] = []
            sorted_list = list(
                sorted(
                    weekday_grouped_spans[span.weekday] + [span], key=lambda s: s.span
                )
            )
            weekday_grouped_spans[span.weekday] = sorted_list

        formated_spans = "\t"
        formated_spans += "\n\t".join(
            [
                (get_abbrev_by_calendar_day(weekday) + "\n\t\t")
                + "\n\t\t".join(
                    [s.span.get_simple_format() for s in weekday_grouped_spans[weekday]]
                )
                for weekday in weekday_grouped_spans.keys()
            ]
        )
        return f"{self.username}\n{formated_spans}"

    def calculate_salary(self) -> Decimal:
        decimal_two_places = Decimal("0.01")
        salary = Decimal(0.0)
        for employee_slot in self.working_days_spans:
            for payment_slot in self.__weekday_time_payments[employee_slot.weekday]:
                (
                    intersection_result,
                    intersection_mins,
                ) = payment_slot.span.get_intersection(employee_slot.span)
                if intersection_result != IntersectionTypes.NO_INTERSECTION:
                    intersection_hours = Decimal(intersection_mins / 60).quantize(
                        decimal_two_places
                    )
                    slot_amount = payment_slot.hour_amount * intersection_hours
                    salary += slot_amount
        return salary.quantize(decimal_two_places)
