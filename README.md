# salary-calculator

## Python Version
`python:3.8.10`

## Project Architecture Description

Most script files are stored at inner salary_calculator folder.\
This solution was built having in mind Clean Architecture principles.\
Functional programming guidelines were also taken into account to structure functions.\

Flake8 tool was run onto the current project as to follow PEP8 guidelines.\

Key script files are the following:

Filename       | Contains
-------------- | -------------
classes.py     | Business Logic/Data classes and related operations on them
exceptions.py  | Custom exceptions
serializers.py | Classes to convert formated strings into data classes
utils.py       | Utility miscelaneous functions

## How to run main file with test input file?

Test input files are files which contain daily schedule input lines according to the format mentioned in the requirements.
At the file named main.py such lines are passed to obtain demo salaries given an specific week schedule.

To run main.py file:

`python main.py`

To test schedule lines of our own, modify the file named demo_dataset.txt at test_data_files directory.

## How to test?

Run the following line(and python will autodiscover our tests/ directory and run all files within):

`python -m unittest discover`

Inside each python test script there are customized datasets according to each case.
