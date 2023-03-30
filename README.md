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

## Approach and methodology to build the solution

First, I decomposed the original problem into the smallest logical pieces, and realized that it all encompassed time ranges/spans intersections.\
Later, as to structure entities/classes presented in the original problem, I could abstract out logic into an schedule class(composed of a list of week day time segments/spans).
On the other hand, payment logic implied the use of another collection of time spans grouped by weekday.
As both collections were mutually iterated, calculating an employee's salary was achieved by summing up time intersections multiplied by the amount related to its corresponding hour range.
Once the prior steps were done, I had to decide on where to place operations & dataclasses.
As both were strongly connected, I put logic and dataclasses at classes.py file. 

Parsing text strings into dataclasses required an middleware class.Such rationale led me to create a serializer class, as it is usually done in Web APIs.

Finally, to put it all together, an entry point was needed, so I created a file named main.py.
As to guarantee all logic was coded properly, appropiate unit test were created:
Unit tests for entire schedules and salaries, and for timespans intersections.

## How to run locally main file with test input file?

Test input files are files which contain daily schedule input lines according to the format mentioned in the requirements.
At the file named main.py such lines are passed to obtain demo salaries given an specific week schedule.

To run main.py file:

`python main.py`

To test schedule lines of our own, modify the file named demo_dataset.txt at test_data_files directory.

## How to test locally?

Run the following line(and python will autodiscover our tests/ directory and run all files within):

`python -m unittest discover`

Inside each python test script there are customized datasets according to each case.
