from salary_calculator.serializers import EmployeeScheduleSerializer

if __name__ == "__main__":
    with open("salary_calculator/test_data_files/demo_dataset.txt") as file:
        for line in file:
            line = line.replace("\n", "")
            serializer = EmployeeScheduleSerializer(line)
            schedule = serializer.serialize()
            print("------------------------------------------------------>>>>")
            print(schedule)
            salary = schedule.calculate_salary()
            print(f"The amount to pay {schedule.username} is: {salary} USD")
