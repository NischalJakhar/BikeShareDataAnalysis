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
        #diff = stoptime - starttime
        #hour = int((diff.total_seconds()) / (60**2))
        hour = starttime.hour
        month = starttime.month
        day = starttime.day
        day_of_week_int = calendar.weekday(starttime.year, month, day)
        day_of_week = calendar.day_name[day_of_week_int]

    elif city == "Chicago":
        stoptime = datetime.strptime(datum['stoptime'], '%m/%d/%Y %H:%M')
        starttime = datetime.strptime(datum['starttime'], '%m/%d/%Y %H:%M')
        #diff = stoptime - starttime
        #hour = int((diff.total_seconds()) / (60 ** 2))
        hour = starttime.hour
        month = starttime.month
        day = starttime.day
        day_of_week_int = calendar.weekday(starttime.year, month, day)
        day_of_week = calendar.day_name[day_of_week_int]

    else:
        stoptime = datetime.strptime(datum['End date'], '%m/%d/%Y %H:%M')
        starttime = datetime.strptime(datum['Start date'], '%m/%d/%Y %H:%M')
        #diff = stoptime - starttime
        #hour = int((diff.total_seconds()) / (60 ** 2))
        hour = starttime.hour
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
    
def type_of_user(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the type of system user that made the
    trip.
    
    Remember that Washington has different category names compared to Chicago
    and NYC. 
    """
    
    # YOUR CODE HERE
    if city == "Washington":
        value = datum['Member Type']
        if value == "Registered":
            user_type = "Subscriber"
        elif value == "Casual":
            user_type = "Customer"

    elif city == "Chicago":
        user_type = datum['usertype']
    else:
        user_type = datum['usertype']
    return user_type


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 'Customer',
         'Chicago': 'Subscriber',
         'Washington': 'Subscriber'}

for city in tests:
    assert type_of_user(example_trips[city], city) == tests[city]
    
def condense_data(in_file, out_file, city):
    """
    This function takes full data from the specified input file
    and writes the condensed data to a specified output file. The city
    argument determines how the input file will be parsed.
    
    HINT: See the cell below to see how the arguments are structured!
    """
    
    with open(out_file, 'w') as f_out, open(in_file, 'r') as f_in:
        # set up csv DictWriter object - writer requires column names for the
        # first row as the "fieldnames" argument
        out_colnames = ['duration', 'month', 'hour', 'day_of_week', 'user_type']        
        trip_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
        trip_writer.writeheader()
        
        ## TODO: set up csv DictReader object ##
        trip_reader = csv.DictReader(f_in)

        # collect data from and process each row
        for row in trip_reader:
            # set up a dictionary to hold the values for the cleaned and trimmed
            # data point
            new_point = {}

            ## TODO: use the helper functions to get the cleaned data from  ##
            ## the original data dictionaries.                              ##
            ## Note that the keys for the new_point dictionary should match ##
            ## the column names set in the DictWriter object above.         ##
            new_point['duration'] = duration_in_mins(row, city)
            new_point['month'], new_point['hour'], new_point['day_of_week'] = time_of_trip(row, city)
            new_point['user_type'] = type_of_user(row, city)
            

            ## TODO: write the processed information to the output file.     ##
            ## see https://docs.python.org/3/library/csv.html#writer-objects ##
            trip_writer.writerow(new_point)
            
# Run this cell to check your work
city_info = {'Washington': {'in_file': './data/Washington-CapitalBikeshare-2016.csv',
                            'out_file': './data/Washington-2016-Summary.csv'},
             'Chicago': {'in_file': './data/Chicago-Divvy-2016.csv',
                         'out_file': './data/Chicago-2016-Summary.csv'},
             'NYC': {'in_file': './data/NYC-CitiBike-2016.csv',
                     'out_file': './data/NYC-2016-Summary.csv'}}

for city, filenames in city_info.items():
    condense_data(filenames['in_file'], filenames['out_file'], city)
    print_first_point(filenames['out_file'])
    

    
    
def number_of_trips(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        
        # initialize count variables
        n_subscribers = 0
        n_customers = 0
        
        # tally up ride types
        for row in reader:
            if row['user_type'] == 'Subscriber':
                n_subscribers += 1
            else:
                n_customers += 1
        
        # compute total number of rides
        n_total = n_subscribers + n_customers
        
        # return tallies as a tuple
        return(n_subscribers, n_customers, n_total)
   

## Modify this and the previous cell to answer Question 4a. Remember to run ##
## the function on the cleaned data files you created from Question 3.      ##

#data_file = './examples/BayArea-Y3-Summary.csv'
data_file = './data/NYC-2016-Summary.csv'
print(number_of_trips(data_file))

#**Question 4b**: Bike-share systems are designed for riders to take short trips. Most of the time, users are allowed to take trips of 30 minutes or less with no additional charges, with overage charges made for trips of longer than that duration. What is the average trip length for each city? What proportion of rides made in each city are longer than 30 minutes?

##**Answer**: **Average trip length for each city are following:**


##1._Washington_ : 18 minutes


##2._NYC_ : 15 minutes


##3._Chicago_ : 16 minutes


##**Proportion of rides in each city longer than 30 minutes are following:**


##1._Washington_ : 10.84%


#2._NYC_ : 7.3%


##3._Chicago_ : 8.33%


## Use this and additional cells to answer Question 4b.                 ##
##                                                                      ##
## HINT: The csv module reads in all of the data as strings, including  ##
## numeric values. You will need a function to convert the strings      ##
## into an appropriate numeric type before you aggregate data.          ##
## TIP: For the Bay Area example, the average trip length is 14 minutes ##
## and 3.5% of trips are longer than 30 minutes.                        ##
def average_trip_length(filename):
    """
    This function reads the file and answers the average
    trip length of a city and the proportion of rides > 30 minutes.
    
    filename : input file
    """
    with open(filename, 'r') as f_in:
        reader = csv.DictReader(f_in)
        
        #Calculates total number of trips and gets value from tuple returned 
        number_of_trip = number_of_trips(filename)[2]
        
        #record the total duration sum
        duration_sum = 0
        
        #records number of rides greater than 30 minutes
        no_of_rides_larger_thirty = 0
        
        for row in reader:
            if float(row['duration'])>30:
                no_of_rides_larger_thirty +=1
                
            duration_sum += float(row['duration'])
        
        return int(duration_sum/number_of_trip), no_of_rides_larger_thirty, number_of_trip
    
#Let' call the function with a file
avg,thirty,total_trip = average_trip_length('./data/Chicago-2016-Summary.csv')

#Total proportion in % calculated
proportion = (thirty*100)/total_trip

#Print values 
print(proportion)
print(avg)

## Use this and additional cells to answer Question 4c. If you have    ##
## not done so yet, consider revising some of your previous code to    ##
## make use of functions for reusability.                              ##
##                                                                     ##
## TIP: For the Bay Area example data, you should find the average     ##
## Subscriber trip duration to be 9.5 minutes and the average Customer ##
## trip duration to be 54.6 minutes. Do the other cities have this     ##
## level of difference? 

def long_avg_rides_users(filename):
    """
    Calculates the average time by customer/Subscriber
    
    """
    
    with open(filename, 'r') as f_in:
        reader = csv.DictReader(f_in)
        
        customer_duration = 0
        subscriber_duration = 0
        
        
        for row in reader:
            
            if row['user_type'] == "Customer":
                customer_duration +=float(row['duration'])
            else:
                subscriber_duration +=float(row['duration'])
              
                
        return customer_duration, subscriber_duration
        
        
filename = './data/NYC-2016-Summary.csv'

#Calling the function
customer_duration, subscriber_duration = long_avg_rides_users(filename)

#Called number_of_trips method defined previously
total_trip_done = number_of_trips(filename)

print(subscriber_duration/total_trip_done[0])
print(customer_duration/total_trip_done[1])

## Use this and additional cells to collect all of the trip times as a list ##
## and then use pyplot functions to generate a histogram of trip times.     ##
import matplotlib.pyplot as plt

%matplotlib inline 

def get_data(filename):
    
    with open(filename, 'r') as f_in:
        reader = csv.DictReader(f_in)
        
        data = []
        
        for row in reader:
            data.append(float(row['duration']))
        
        return data
data = get_data('./data/Washington-2016-Summary.csv')
plt.hist(data)
plt.title('Distribution of Trip Durations')
plt.xlabel('Duration (m)')
plt.show()


