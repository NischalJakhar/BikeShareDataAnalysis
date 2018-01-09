# import all necessary packages and functions.
import csv # read and write csv files
from datetime import datetime # operations to parse dates
from pprint import pprint


def print_first_point(filename):
    """
    This function prints and returns the first data point (second row) from
    a csv file that includes a header row.
    """
    # print city name for reference
    city = filename.split('-')[0].split('/')[-1]
    print('\nCity: {}'.format(city))

    with open(filename, 'r') as f_in:
        ## TODO: Use the csv library to set up a DictReader object. ##
        ## see https://docs.python.org/3/library/csv.html           ##
        trip_reader = csv.DictReader(f_in)

        ## TODO: Use a function on the DictReader object to read the     ##
        ## first trip from the data file and store it in a variable.     ##
        ## see https://docs.python.org/3/library/csv.html#reader-objects ##
        first_trip = next(trip_reader)

        ## TODO: Use the pprint library to print the first trip. ##
        ## see https://docs.python.org/3/library/pprint.html     ##

        pprint(first_trip)

    # output city name and first trip for later testing
    return (city, first_trip)


# list of files for each city
data_files = ['./data/NYC-CitiBike-2016.csv',
              './data/Chicago-Divvy-2016.csv',
              './data/Washington-CapitalBikeshare-2016.csv', ]

# print the first trip from each file, store in dictionary
example_trips = {}
for data_file in data_files:
    city, first_trip = print_first_point(data_file)
    example_trips[city] = first_trip
    
    
def duration_in_mins(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the trip duration in units of minutes.

    Remember that Washington is in terms of milliseconds while Chicago and NYC
    are in terms of seconds.

    HINT: The csv module reads in all of the data as strings, including numeric
    values. You will need a function to convert the strings into an appropriate
    numeric type when making your transformations.
    see https://docs.python.org/3/library/functions.html
    """

    # YOUR CODE HERE
    if city == "Washington":
        duration = float(datum['Duration (ms)']) / (60 * 1000)
    elif city == "NYC" or "Chicago":
        duration = float(datum['tripduration']) / 60
    

    return duration


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 13.9833,
         'Chicago': 15.4333,
         'Washington': 7.1231}

for city in tests:
    assert abs(duration_in_mins(example_trips[city], city) - tests[city]) < .001
    
 def time_of_trip(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the month, hour, and day of the week in
    which the trip was made.
    
    Remember that NYC includes seconds, while Washington and Chicago do not.
    
    HINT: You should use the datetime module to parse the original date
    strings into a format that is useful for extracting the desired information.
    see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """
    
    # YOUR CODE HERE
        if city == 'NYC':

        stoptime = datetime.strptime(datum['stoptime'], '%m/%d/%Y %H:%M:%S')
        starttime = datetime.strptime(datum['starttime'], '%m/%d/%Y %H:%M:%S')
        diff = stoptime - starttime
        hour = int((diff.total_seconds()) / (60**2))
        month = starttime.month
        day = starttime.day
        day_of_week_int = calendar.weekday(starttime.year, month, day)
        day_of_week = calendar.day_name[day_of_week_int]

    elif city == "Chicago":
        stoptime = datetime.strptime(datum['stoptime'], '%m/%d/%Y %H:%M')
        starttime = datetime.strptime(datum['starttime'], '%m/%d/%Y %H:%M')
        diff = stoptime - starttime
        hour = int((diff.total_seconds()) / (60 ** 2))
        month = starttime.month
        day = starttime.day
        day_of_week_int = calendar.weekday(starttime.year, month, day)
        day_of_week = calendar.day_name[day_of_week_int]

    else:
        stoptime = datetime.strptime(datum['End date'], '%m/%d/%Y %H:%M')
        starttime = datetime.strptime(datum['Start date'], '%m/%d/%Y %H:%M')
        diff = stoptime - starttime
        hour = int((diff.total_seconds()) / (60 ** 2))
        month = starttime.month
        day = starttime.day
        day_of_week_int = calendar.weekday(starttime.year, month, day)
        day_of_week = calendar.day_name[day_of_week_int]
        
        
    
    return (month, hour, day_of_week)


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': (1, 0, 'Friday'),
         'Chicago': (3, 23, 'Thursday'),
         'Washington': (3, 22, 'Thursday')}

for city in tests:
    assert time_of_trip(example_trips[city], city) == tests[city]
