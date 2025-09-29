#Author: Bashith Ratnaweera
#Date: 25.11.2024
#Student ID: w2119832 (UoW) 20240031 (IIT ID)

import csv

# Task A: Input Validation
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    date  = date_input()  
    month = month_input()  
    year  = year_input()   

    # To Check if the Year is a Leap Year
    while month == 2:                         # Check if it's February
        leap_year = check_leap_year(year)     # Check if it's a leap using the function check_leap_year(year)
        if not leap_year == True:             
            if date == 29:                    # Checks if it's February 29th of the given year which is not a leap year.
                print(f"{year} is not a leap year! Please Re-enter the date.")

                # Asks the user to Re-enter the Date
                date = date_input()           
                month = month_input()         
                year = year_input()           
                continue                      # Loops again to check if the new year entered is a leap year
            else:
                break
        else:
            break                             
    return date,month,year



def date_input(): # This function validates the user input for date format and range.
    while True:
        try:
            
            dd = int(input("Please enter the Day of the survey in the format DD (1-31) : "))
            if not (1 <= dd <= 31):
                print("Out of range - values must be in the range 1 and 31!")
                continue     
        except ValueError:
            print("Integer Required!")
            continue         
        else:
            break            
    return dd

def month_input(): # This function validates the user input for month format and range.
    while True:
        try:
            
            mm = int(input("Please enter the Month of the survey in the format MM (1-12) : "))
            if not (1 <= mm <= 12): 
                print("Out of range - values must be in the range 1 and 12!")
                continue    
        except ValueError:
            print("Integer Required!")
            continue        
        else:
            break           
    return mm

def year_input(): # This function validates the user input for year format and range.
    while True:
        try:
           
            yy = int(input("Please enter the Year of the survey in the format YY (2000-2024) : "))
            if not (2000 <= yy <= 2024):
                print("Out of range - values must be in the range 2000 and 2024!")
                continue   
        except ValueError:
            print("Integer Required!")
            continue       
        else:
            break          
    return yy

def check_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        user_input = input("Do you want to load another dataset? (Y/N): ").strip().upper()
        # .strip() removes unwanted spaces from the input and .upper() converts all strings to uppercase

        if user_input == 'Y': # Loops the main program if the user wants to select another dataset
            return True
        elif user_input == 'N':
            return False
        else:
            print("Invalid Input! Please Enter 'Y' for yes or 'N' for no.")
            continue


# Task B: Processed Outcomes

def process_csv_data(file_name):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    data = []
    try:
        with open(file_name,'r') as file:       # Open the csv file in Read mode and closes the file after executing
            file_reader = csv.DictReader(file)  # Reads the CSV file and parses it into a Dictionary format
            for row in file_reader:
                data.append(row)   # Appends each row of the csv file as a list of dictionaries in the list named "data"
    except FileNotFoundError:      # checks if the file is available
            print(f"Error: The file {file_name} does not exist.\nNo data is Available for this file.")
    return data

"""
Functions for analysing the data from the Dictionary named "data"
"""
def total_vehicles(data): # To count the number of Total vehicles
    return len(data)      # Calculates the number of rows in the "data" list

def total_trucks(data):   # To count the number of Total Trucks
    return sum(1 for row in data if row['VehicleType'] == 'Truck') # Counts every row with the 'VehicleType' as 'Truck'

def total_electric_vehicles(data): # To count the number of Total Trucks
    return sum(1 for row in data if row['elctricHybrid'].upper() == 'TRUE') # Counts every row with the 'True'

def total_two_wheeled_vehicles(data): # To count the Number of Two-Wheeled Vehicles (Motorcycles, Scooters, Bicycles)
    # Counts every row with the 'VehicleType' as 'Motorcycle' or 'Scooter' or 'Bicycle'
    return sum(1 for row in data if row['VehicleType'] in ['Motorcycle', 'Scooter', 'Bicycle'])

def total_busses_north(data):
    """
    Calculates the total number of Buses leaving Elm Avenue/Rabbit Road junction heading North.
    Returns The total number of buses meeting the criteria as an integer value
    """
    return sum(
        1 for row in data
        if row['JunctionName'] == "Elm Avenue/Rabbit Road"
        and row['VehicleType'] == "Buss"
        and row['travel_Direction_out'] == "N"
    )

def total_vehicles_not_turning(data):
    """
    Calculates the total number of vehicles passing through both junctions without turning left or right.

    Checks whether the travel direction is the same as the travel direction out,
    and if it's the same it shows that the vehicle didn't turn left or right and "1" is added to the sum.

    Returns the total number of vehicles meeting the criteria as an integer value
    """
    return sum(1 for row in data if row['travel_Direction_in'] == row['travel_Direction_out'])


def percentage_of_trucks(data):
    """
    Calculates the percentage of all vehicles recorded that are trucks.
    Returns the percentage of trucks, rounded to the nearest integer.
    """
    total_vehicles = len(data)  # Calculates the number of elements in the list "data"
    if total_vehicles == 0:     # Checks if there are no elements in the list "data"
        return 0                # Avoid division by zero

    total_trucks = sum(1 for row in data if row['VehicleType'] == 'Truck') # Calculates the number of Trucks
    percentage = (total_trucks / total_vehicles) * 100  # Calculates the percentage of trucks to the number of vehicles
    return round(percentage) # rounds off the percentage to an integer

def average_bicycles_per_hour(data):
    """
    Calculates the average number of bicycles per hour for the selected date.
    Returns the average number of bicycles per hour, rounded to the nearest integer.
    """
    bicycles_per_hour = {}  # Dictionary to count bicycles per hour

    # Loop through each row to filter bicycles and group by hour
    for row in data:
        if row['VehicleType'] == 'Bicycle':        # Filters rows where the VehicleType is 'Bicycle'
            hour = row['timeOfDay'].split(':')[0]  # Extract the hour from 'timeOfDay'

            # Increment the count for this hour
            if hour in bicycles_per_hour:
                """
                If the hour is already a key in the dictionary, increment its value by 1 
                (a new bicycle is recorded for that hour).
                """
                bicycles_per_hour[hour] += 1
            else:
                """
                If the hour is not already in the dictionary, add it as a key and set its value to 1 
                (the first bicycle is recorded for that hour).
                """
                bicycles_per_hour[hour] = 1

    # Calculate the total number of bicycles and the number of unique hours
    """
    Sums all the values in the dictionary (the counts of bicycles for each hour) to get the total number of bicycles.
    """
    total_bicycles = sum(bicycles_per_hour.values())
    """
    Counts the number of keys in the dictionary (the number of unique hours during which bicycles were recorded).
    """
    total_hours = len(bicycles_per_hour)

    if total_hours == 0: # Avoid division by zero and calculate the average
        return 0
    average = total_bicycles / total_hours # Calculates the average number of bicycles per hour.

    return round(average) # Return the rounded average

def total_vehicles_over_speed_limit(data):
    """
    Calculates the total number of vehicles recorded as over the speed limit for the selected date.
    Returns the Total number of vehicles exceeding the speed limit.
    """
    over_speed_limit_count = 0      # Initialize Counter

    for row in data:
        # Convert speed fields to integers for comparison
        try:
            vehicle_speed = int(row['VehicleSpeed']) # Converts the VehicleSpeed value from the row into an integer.
            junction_speed_limit = int(row['JunctionSpeedLimit']) # Converts the value from the row into an integer.

            # Check if the vehicle is over the speed limit
            if vehicle_speed > junction_speed_limit:
                over_speed_limit_count += 1  # Increments the Counter by 1 for each vehicle exceeding the speed limit.
        except ValueError:
            # In case of any data conversion issue it will skip that row
            continue

    return over_speed_limit_count # Returns the value of the Counter

def total_vehicles_elm_avenue(data):
    """
    Calculates the total number of vehicles recorded through only Elm Avenue/Rabbit Road junction
    for the selected date.
    Returns the Total number of vehicles recorded through Elm Avenue/Rabbit Road on that date.
    """
    elm_avenue_count = 0            # Initialize Counter

    for row in data:
        # Check if the junction is Elm Avenue/Rabbit Road
        if row['JunctionName'] == "Elm Avenue/Rabbit Road":
            elm_avenue_count += 1   # Increments the Counter by 1

    return elm_avenue_count         # Returns the value of the Counter

def total_vehicles_hanley_highway(data):
    """
    Calculates the total number of vehicles recorded through only Hanley Highway/Westway junction
    for the selected date.
    Returns the total number of vehicles recorded through Hanley Highway/Westway.
    """
    hanley_highway_count = 0            # Initialize Counter

    for row in data:
        # Check if the junction is Hanley Highway/Westway
        if row['JunctionName'] == "Hanley Highway/Westway":
            hanley_highway_count += 1   # Increments the Counter by 1

    return hanley_highway_count         # Returns the value of the Counter

def percentage_scooters_elm_avenue(data):
    """
    Calculates the percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters.
    Returns the percentage of scooters through Elm Avenue/Rabbit Road, rounded to the nearest integer.
    """
    total_vehicles_elm_avenue = 0   # Initialize Counter
    total_scooters_elm_avenue = 0   # Initialize Counter

    for row in data:
        if row['JunctionName'] == "Elm Avenue/Rabbit Road": # Check if the vehicle is through Elm Avenue/Rabbit Road
            total_vehicles_elm_avenue += 1

            if row['VehicleType'] == 'Scooter':     # Check if the vehicle is a scooter
                total_scooters_elm_avenue += 1

    if total_vehicles_elm_avenue == 0:
        return 0  # Avoid division by zero if no vehicles at Elm Avenue/Rabbit Road

    # Calculate the percentage of scooters
    percentage = (total_scooters_elm_avenue / total_vehicles_elm_avenue) * 100

    return round(percentage)  # Round to the nearest integer and return the value

def peak_hour_vehicles_hanley_highway(data):
    """
    Calculates the number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway.
    Returns the number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway.
    """
    # Dictionary to store the number of vehicles per hour
    hour_vehicle_count = {}

    # Loop through each row to filter Hanley Highway/Westway vehicles and group by hour
    for row in data:
        if row['JunctionName'] == "Hanley Highway/Westway":
            hour = row['timeOfDay'].split(':')[0]  # Extract the hour from timeOfDay

            # Increment vehicle count for the corresponding hour
            if hour in hour_vehicle_count:
                hour_vehicle_count[hour] += 1
            else:
                hour_vehicle_count[hour] = 1

    # Find the hour with the maximum vehicles
    if hour_vehicle_count:
        peak_hour = max(hour_vehicle_count, key=hour_vehicle_count.get)
        return hour_vehicle_count[peak_hour]  # Return the number of vehicles in the peak hour
    else:
        return 0  # If no data for Hanley Highway/Westway, return 0


def peak_traffic_hours_hanley_highway(data):
    """
    Calculates the time(s) of the peak (busiest) traffic hour(s) on Hanley Highway/Westway.
    Returns a String representing the time(s) of the peak traffic hour(s) on Hanley Highway/Westway.
    """
    # Dictionary to store the number of vehicles per hour
    hour_vehicle_count = {}

    # Loop through each row to filter Hanley Highway/Westway vehicles and group by hour
    for row in data:
        if row['JunctionName'] == "Hanley Highway/Westway":
            hour = row['timeOfDay'].split(':')[0]  # Extract the hour from timeOfDay

            # Increment vehicle count for the corresponding hour
            if hour in hour_vehicle_count:
                """
                If the hour is already a key in the dictionary, increment its value by 1 
                (a new vehicle is recorded for that hour).
                """
                hour_vehicle_count[hour] += 1
            else:
                """
                If the hour is not already in the dictionary, add it as a key and set its value to 1 
                (the first vehicle is recorded for that hour).
                """
                hour_vehicle_count[hour] = 1

    # Find the maximum number of vehicles in any hour
    if hour_vehicle_count:      # Checks if the dictionary hour_vehicle_count is not empty.
        # Finds the maximum number of vehicles recorded in any hour by checking the values in the dictionary.
        max_vehicles = max(hour_vehicle_count.values())

        """
        Find all the hours that have the maximum number of vehicles
        Adds the hour to the list peak_hours if its count matches the max_vehicles value.
        """
        peak_hours = [hour for hour, count in hour_vehicle_count.items() if count == max_vehicles]

        # Format the peak hours in the required format (e.g., "Between 18:00 and 19:00")
        peak_times = [f"between {hour}:00 and {int(hour) + 1}:00" for hour in peak_hours]

        # Join multiple hours with commas if more than one
        return ", ".join(peak_times)
    else:
        return "No data for Hanley Highway/Westway" # Handles if there is no data

def total_hours_of_rain(data):
    """
    Calculates the total number of hours of rain on the selected date.
    Returns the Total number of hours of rain on the selected date.
    """
    rain_hours = set()  # Use a set to store unique hours of rain
    """
    A set is used because it inherently keeps only unique values, so no duplicate hours are counted.
    """

    for row in data:                                    # Iterates over each dictionary (row) in the data list
        # Check if the weather condition is "Rain"
        if 'Rain' in row['Weather_Conditions']:         # Checks if "Rain" is in the Weather_Conditions field
            hour = row['timeOfDay'].split(':')[0]       # Extract the hour from "timeOfDay"
            rain_hours.add(hour)                        # Add the hour to the set (only unique hours will be kept)

    return len(rain_hours)  # The size of the set "rain_hours" shows the number of unique hours of rain

def display_outcomes(file_name,outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    print("\n*************************************************************************************************")
    print(f"Data file selected is {file_name}")
    print("*************************************************************************************************\n")
    print(f"The Total number of Vehicles recorded for this date is {outcomes[0]}")
    print(f"The Total number of Trucks recorded for this date is {outcomes[1]}")
    print(f"The Total number of Electric Vehicles recorded for this date is {outcomes[2]}")
    print(f"The Total number of Two-Wheeled Vehicles recorded for this date is {outcomes[3]}")
    print(f"The Total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[4]}")
    print(f"The Total number of Vehicles through both junctions not turning left or right is {outcomes[5]}")
    print(f"The Percentage of Total Vehicles recorded that are Trucks for this date is {outcomes[6]}%")
    print(f"The Average number of Bikes per hour for this date is {outcomes[7]}")
    print(f"The Total number of Vehicles recorded as over the speed limit for this date is {outcomes[8]}")
    print(f"The Total number of Vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[9]}")
    print(f"The Total number of Vehicles recorded through Hanley Highway/Westway junction is {outcomes[10]}")
    print(f"{outcomes[11]}% of Vehicles recorded through Elm Avenue/Rabbit Road are Scooters.")
    print(f"The Highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[12]}")
    print(f"The Most Vehicles through Hanley Highway/Westway were recorded between {outcomes[13]}")
    print(f"The number of hours of rain for this date is {outcomes[14]}")

# Task C: Save Results to Text File
def save_results_to_file(file_name, outcomes, file_to_write="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    # Create a list of lines to write
    lines_to_write = (
                      "********************************************************************************************\n",
                      f"Data file selected is {file_name}\n",
                      "********************************************************************************************\n",
                      f"\nThe Total number of Vehicles recorded for this date is {outcomes[0]}\n",
                      f"The Total number of Trucks recorded for this date is {outcomes[1]}\n",
                      f"The Total number of Electric Vehicles recorded for this date is {outcomes[2]}\n",
                      f"The Total number of Two-Wheeled Vehicles recorded for this date is {outcomes[3]}\n",
                      f"The Total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[4]}\n",
                      f"The Total number of Vehicles through both junctions not turning left or right is {outcomes[5]}\n"
                      f"The Percentage of Total Vehicles recorded that are Trucks for this date is {outcomes[6]}%\n",
                      f"The Average number of Bikes per hour for this date is {outcomes[7]}\n",
                      f"The Total number of Vehicles recorded as over the speed limit for this date is {outcomes[8]}\n",
                      f"The Total number of Vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[9]}\n",
                      f"The Total number of Vehicles recorded through Hanley Highway/Westway junction is {outcomes[10]}\n",
                      f"{outcomes[11]}% of Vehicles recorded through Elm Avenue/Rabbit Road are Scooters.\n"
                      f"The Highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[12]}\n",
                      f"The Most Vehicles through Hanley Highway/Westway were recorded {outcomes[13]}\n",
                      f"The number of hours of rain for this date is {outcomes[14]}\n",
                      "\n"
                      )

    with open(file_to_write, 'a') as file: # Use "a" to create a file if there's no file named "results.txt"
        file.writelines(lines_to_write)

# Main Program has been disabled to run everything in Part D and E

# if you have been contracted to do this assignment please do not remove this line