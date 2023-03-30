from decimal import Decimal
from unittest import TestCase

from salary_calculator.classes import EmployeeSchedule
from salary_calculator.serializers import EmployeeScheduleSerializer


class ScheduleTestCase(TestCase):
    def setUp(self) -> None:
        self.input_ouput_dataset = {
            "first_base_case": {
                "input_line": "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00",
                "output_value": Decimal("215.0"),
            },
            "second_base_case": {
                "input_line": "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
                "output_value": Decimal("85.0"),
            },
            "intersected_case1": {
                "input_line": "C1=MO08:35-09:45,MO12:50-18:30,SA03:32-09:50,SA17:59-20:00",
                "output_value": Decimal("339.0"),
            },
            "intersected_case2": {
                "input_line": "C2=MO10:12-20:30,TU07:36-10:55,FR12:30-19:45,SU09:11-20:35",
                "output_value": Decimal("587.85"),
            },
            "exceeding_length_case1": {
                "input_line": "EL1=MO08:00-18:30,WE00:01-09:30,SU08:59-18:02",
                "output_value": Decimal("581.70"),
            },
            "exceeding_length_case2": {
                "input_line": "EL2=TU00:15-18:45,SA07:32-20:40",
                "output_value": Decimal("658.0"),
            },
            "precisely_fitting_case1": {
                "input_line": "PF1=MO00:01-09:00,TU09:01-18:00,WE18:01-00:00,SA18:01-00:00",
                "output_value": Decimal("627.85"),
            },
            "precisely_fitting_case2": {
                "input_line": "PF2=FR18:01-00:00,SA09:01-18:00,SA18:01-00:00,SU09:01-18:00,SU18:01-00:00",
                "output_value": Decimal("777.10"),
            },
            "mixed_case1": {
                "input_line": "MX1=MO03:00-05:00,MO08:30-09:30,MO12:00-18:30,SU00:30-18:40",
                "output_value": Decimal("620.15"),
            },
            "mixed_case2": {
                "input_line": "MX2=WE05:55-08:30,WE08:40-9:50,WE10:00-12:00,WE14:00-18:45,SA09:10-17:30,SA18:20-23:50",
                "output_value": Decimal("493.75"),
            },
            "special_case_includes_midnight": {
                "input_line": "SC1=MO00:00-09:00,MO23:00-00:00,SU18:40-00:00",
                "output_value": Decimal("377.10"),
            },
            "special_case_entire_day": {
                "input_line": "SC2=MO00:01-00:00,SU18:00-00:00",
                "output_value": Decimal("627.85"),
            },
        }
        return super().setUp()

    def create_schedule_from_case(self, case: str) -> EmployeeSchedule:
        return EmployeeScheduleSerializer(
            self.input_ouput_dataset[case]["input_line"]
        ).serialize()

    def get_precalculated_salary_from_case(self, case: str) -> Decimal:
        return self.input_ouput_dataset[case]["output_value"]

    def test_base_cases(self):
        current_case = "first_base_case"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

        current_case = "second_base_case"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

    def test_cases_having_intersected_spans(self):
        current_case = "intersected_case1"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

        current_case = "intersected_case2"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

    def test_cases_having_exceeding_length_spans(self):
        current_case = "exceeding_length_case1"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

        current_case = "exceeding_length_case2"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

    def test_cases_having_precisely_fitting_spans(self):
        current_case = "precisely_fitting_case1"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

        current_case = "precisely_fitting_case2"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

    def test_mixed_cases(self):
        current_case = "mixed_case1"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

        current_case = "mixed_case2"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

    def test_empty_schedule(self):
        default_salary = Decimal("0.0")
        schedule = EmployeeSchedule()
        self.assertEqual(default_salary, schedule.calculate_salary())

    def test_special_bounded_cases(self):
        current_case = "special_case_includes_midnight"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())

        current_case = "special_case_entire_day"
        precalculated_salary = self.get_precalculated_salary_from_case(current_case)
        schedule = self.create_schedule_from_case(current_case)
        self.assertEqual(precalculated_salary, schedule.calculate_salary())
