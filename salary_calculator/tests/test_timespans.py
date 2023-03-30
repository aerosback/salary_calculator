from datetime import datetime
from typing import List, Tuple
from unittest import TestCase

from salary_calculator.classes import IntersectionTypes, TimeSpan
from salary_calculator.exceptions import StartGreaterThanEndError


def create_timespan(value: str) -> TimeSpan:
    start_token, end_token = value.split("-")
    start = datetime.strptime(start_token, "%H:%M").time()
    end = datetime.strptime(end_token, "%H:%M").time()
    return TimeSpan(start, end)


class TimespanTestCase(TestCase):
    def setUp(self) -> None:
        self.input_ouput_dataset = {
            "start_greather_than_end_error_case": [
                "08:39-05:20",
                "10:29-09:00",
                "23:00-12:00",
                "11:11-10:00",
                "00:05-00:02",
            ],
            "not_intersected_span_case": [
                ("10:00-15:30", "09:30-09:40"),
                ("05:30-10:00", "23:30-23:40"),
                ("04:20-12:00", "14:00-16:00"),
                ("23:50-23:55", "12:40-12:50"),
                ("11:00-15:00", "18:00-22:00"),
            ],
            "fits_in_span_case": [
                ("10:00-20:00", "13:30-15:27"),
                ("00:01-20:00", "15:00-19:00"),
                ("15:00-16:30", "15:30-15:35"),
                ("05:00-10:00", "09:00-09:01"),
                ("23:30-23:59", "23:32-23:35"),
            ],
            "exceeds_length_span_case": [
                ("10:00-11:00", "09:00-12:00"),
                ("12:00-13:00", "10:00-13:03"),
                ("05:30-08:20", "05:00-10:00"),
                ("14:35-18:40", "12:00-23:11"),
                ("01:30-12:00", "00:01-13:00"),
            ],
            "start_bounded_span_case": [
                ("10:00-13:00", "12:00-14:00"),
                ("09:45-14:00", "10:00-14:05"),
                ("22:00-23:00", "22:50-23:30"),
                ("05:30-13:00", "10:12-14:20"),
                ("11:35-13:28", "11:40-14:00"),
            ],
            "end_bounded_span_case": [
                ("11:45-14:00", "10:30-11:50"),
                ("14:22-16:40", "13:00-14:30"),
                ("09:30-12:55", "08:00-10:00"),
                ("17:30-19:00", "13:00-18:00"),
                ("20:30-22:30", "19:00-22:00"),
            ],
        }
        return super().setUp()

    def create_spans_from_case(self, case: str) -> List[Tuple[TimeSpan, TimeSpan]]:
        return [
            (create_timespan(span_tuple[0]), create_timespan(span_tuple[1]))
            for span_tuple in self.input_ouput_dataset[case]
        ]

    def get_entries_by_case(self, case: str) -> List[str]:
        return self.input_ouput_dataset[case]

    def test_error_spans_having_start_greater_than_end(self):
        current_case = "start_greather_than_end_error_case"
        for span_str in self.get_entries_by_case(current_case):
            with self.assertRaises(StartGreaterThanEndError):
                create_timespan(span_str)

    def test_not_intersected_span_case(self):
        current_case = "not_intersected_span_case"
        target_intersection_type = IntersectionTypes.NO_INTERSECTION
        list_pairs = self.create_spans_from_case(current_case)
        for pair_entry in list_pairs:
            first_timespan, second_timespan = pair_entry
            intersection_result, _ = first_timespan.get_intersection(second_timespan)
            self.assertEqual(intersection_result, target_intersection_type)

    def test_fits_in_span_case(self):
        current_case = "fits_in_span_case"
        target_intersection_type = IntersectionTypes.FITS_IN_CURRENT
        list_pairs = self.create_spans_from_case(current_case)
        for pair_entry in list_pairs:
            first_timespan, second_timespan = pair_entry
            intersection_result, _ = first_timespan.get_intersection(second_timespan)
            self.assertEqual(intersection_result, target_intersection_type)

    def test_exceeds_length_span_case(self):
        current_case = "exceeds_length_span_case"
        target_intersection_type = IntersectionTypes.EXCEEDS_CURRENT
        list_pairs = self.create_spans_from_case(current_case)
        for pair_entry in list_pairs:
            first_timespan, second_timespan = pair_entry
            intersection_result, _ = first_timespan.get_intersection(second_timespan)
            self.assertEqual(intersection_result, target_intersection_type)

    def test_start_bounded_span_case(self):
        current_case = "start_bounded_span_case"
        target_intersection_type = IntersectionTypes.START_BOUNDED
        list_pairs = self.create_spans_from_case(current_case)
        for pair_entry in list_pairs:
            first_timespan, second_timespan = pair_entry
            intersection_result, _ = first_timespan.get_intersection(second_timespan)
            self.assertEqual(intersection_result, target_intersection_type)

    def test_end_bounded_span_case(self):
        current_case = "end_bounded_span_case"
        target_intersection_type = IntersectionTypes.END_BOUNDED
        list_pairs = self.create_spans_from_case(current_case)
        for pair_entry in list_pairs:
            first_timespan, second_timespan = pair_entry
            intersection_result, _ = first_timespan.get_intersection(second_timespan)
            self.assertEqual(intersection_result, target_intersection_type)
