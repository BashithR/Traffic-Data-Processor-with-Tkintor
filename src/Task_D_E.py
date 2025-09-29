#Author: Bashith Ratnaweera
#Date: 25.11.2024
#Student ID: w2119832 (UoW) 20240031 (IIT ID)

import tkinter as tk
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from idlelib.browser import file_open
import csv
import Task_A_B_C as abc

# Task D: Histogram Display

class HistogramApp:        # Defines a class named HistogramApp. This class is designed to create a histogram using the tkinter library.
    def __init__(self, traffic_data, file_path, date):
        # __init__ This is the constructor for the HistogramApp class.
        # It is called automatically when a new object of the class is created.
        """
        Initializes the histogram application with the traffic data and selected date.

        traffic data - A dictionary containing traffic data for each hour, where the key is the hour and the value is a list of counts
        for Junction 1 and Junction 2 (example -  {hour: [junction1_count, junction2_count]}).

        file_path - A string representing the name of the CSV file being processed.

        date - The date for the histogram (string format, example like "15/06/2024").
        """
        self.traffic_data = traffic_data                        # Stores the traffic data (making it accessible throughout the class).
        self.file_path = file_path                              # Stores the name of the file being processed.
        self.date = date                                        # Stores the selected date for the histogram (displayed in the histogram title).
        self.root = tk.Tk()                                     # Creates the main Tkinter window
        self.root.title(f"Histogram of Vehicle Frequency ({self.date})")    # Set the window title

        self.canvas = None   # Initializes a placeholder for the canvas object.
        """
        The canvas will later be used to draw the histogram bars, axes, and labels.
        Setting it to "None" so that the attribute exists, even though the canvas has not been created yet.
        """

    def setup_window(self):
        """
        This method is responsible for  -

        Setting up the window and canvas for the histogram application.
        Configuring the window size and packing the canvas into the window.

        """
        self.root.geometry("1400x720")                  # Specify the dimensions of the tkinter window. Set the window size (1400x720 pixels).
        self.canvas = tk.Canvas(self.root)              # Create a canvas to draw on (lines, shapes, or custom visuals)

        self.canvas.pack(fill=tk.BOTH, expand=True)     # Pack the canvas into the window and make it expandable
        """
        .pack() method is used to position and manage the Canvas within the window.
        
        fill=tk.BOTH -  Ensures that the Canvas stretches to fill both the width and height of the window.
        
        expand=True -  Allows the Canvas to grow or shrink dynamically when the window is resized.
                       This makes the application responsive to different screen sizes or user adjustments.
        """

    def draw_histogram(self):   # Creating and Displaying the Histogram on the Canvas.

        hours = list(self.traffic_data.keys()) # Extracts the hours from traffic_data
        """
        self.traffic_data is a Dictionary where the keys represent the hours
        and the values are lists of vehicle counts for the two junctions.
        
        list(self.traffic_data.keys()) converts the dictionary keys (hours) into a list, so they can be used for indexing.
        
        Example - traffic_data = {"08": [12, 15], "09": [10, 20]} >>>>>>>> hours = ["08", "09"]
        
        """

        junction1_counts = [self.traffic_data[hour][0] for hour in hours] # Extracts vehicle counts for Elm Avenue/ Rabbit Road junction
        """
        This is the first list comprehension that iterates over each hour in the hours list.
        For each hour, it gets the first value in the list of counts ([0]) from traffic_data.
        """
        junction2_counts = [self.traffic_data[hour][1] for hour in hours] # # Extracts vehicle counts for Hanley Highway/Westway junction
        """
        This is the second list comprehension that iterates over each hour in the hours list.
        For each hour, it gets the second value in the list of counts ([1]) from traffic_data.
        """

        bar_width = 20          # Sets the width of individual bars in the histogram
        bar_spacing = 10        # Spacing between hour groups

        # Calculate the highest vehicle count from both junctions
        max_count = max(max(junction1_counts), max(junction2_counts))
        margin = 80             # Sets a margin for the canvas

        # Define maximum allowable bar height (keeping it within the canvas space)
        max_bar_height = 520    # Leaving space for the title and axis

        # Calculate the scaling factor to ensure bars don't exceed the available space
        scaling_factor = max_bar_height / max_count if max_count > 0 else 1
        """
        The scaling factor adjusts the height of the bars so that the tallest bar corresponds to max_bar_height.
        If max_count is 0 (if no data), the scaling factor defaults to 1 to prevent division by zero.
        """

        # Draw X axis line on the canvas
        """
        The line starts at the point defined by 'margin' and (650) (vertical position), and ends at (1250, 650).
        'fill="gray"' specifies the color of the line.
        """
        self.canvas.create_line(margin, 650, 1250, 650, fill="gray")  # X-axis

        # Loop through each hour and draw the corresponding bars and labels
        for i, hour in enumerate(hours):  # Loop over hours list with index 'i' and value 'hour'
            """
            Calculate the x-coordinate for the start of the hour's bars
            The bars for each hour are placed next to each other, with 'bar_width' being the width of each bar
            and 'bar_spacing' being the space between the bars.
            The enumerate() function is used to get both the index (i) and the value (hour) from the list at the same time.
            """
            x_start = margin + i * (2 * bar_width + bar_spacing)  # x_start is the calculated position for the current bar

            # Green bar for Junction 1

            # Calculate the height of the bar for Junction 1 based on the count for the current hour (i)
            # 'scaling_factor' ensures the bars fit within the canvas by adjusting the height proportionally

            junction1_bar_height = junction1_counts[i] * scaling_factor  # Height of the bar for Junction 1

            # Draw a rectangle on the canvas to represent the bar for Junction 1
            """
            The coordinates (x_start, 650 - junction1_bar_height) specify the top-left corner of the rectangle.
            
            (x_start + bar_width, 650) defines the bottom-right corner.
            """
            self.canvas.create_rectangle(
                x_start, 650 - junction1_bar_height,    # Top-left corner (x_start, 650 - height)
                         x_start + bar_width, 650,      # Bottom-right corner (x_start + bar_width, 650)
                fill="light green",                     # Color of the bar is light green
                outline="green"                         # Border color is green
            )

            # Add a label above the green bar for Junction 1's vehicle count
            # The label is placed at the center of the bar horizontally, and slightly above the bar vertically
            self.canvas.create_text(
                x_start + bar_width / 2,                # x-coordinate at the center of the bar
                650 - junction1_bar_height - 10,        # y-coordinate slightly above the top of the bar
                text=str(junction1_counts[i]),          # The text shows the vehicle count for Junction 1 at this hour
                font=("Arial", 10)                      # Font style and size for the label
            )

            # Red bar for Junction 2

            # Calculate the height of the bar for Junction 2 in the same way as for Junction 1
            junction2_bar_height = junction2_counts[i] * scaling_factor  # Height of the bar for Junction 2

            # Draw a rectangle for Junction 2 next to the Junction 1 bar
            """
            The 'x_start + bar_width' shifts the rectangle to the right of the first bar.
            
            'x_start + 2 * bar_width' defines the end of the red bar.
            """
            self.canvas.create_rectangle(
                x_start + bar_width, 650 - junction2_bar_height,    # Top-left corner (shifted to the right by bar_width)
                x_start + 2 * bar_width, 650,                       # Bottom-right corner (further shifted by bar_width)
                fill="red",                                         # Color of the bar is red
                outline="black"                                     # Border color is black for better contrast
            )

            # Add a label above the red bar for Junction 2's vehicle count
            # The label is centered horizontally over the red bar, slightly above the bar vertically
            self.canvas.create_text(
                x_start + 1.5 * bar_width,                          # x-coordinate at the center of the red bar
                650 - junction2_bar_height - 10,                    # y-coordinate slightly above the top of the red bar
                text=str(junction2_counts[i]),                      # The text shows the vehicle count for Junction 2 at this hour
                font=("Arial", 10)                                  # Font style and size for the label
            )

        # Add hour labels at the bottom of each hour group
        for i, hour in enumerate(hours):  # Loop over hours again to add labels below each group of bars
            """
            Create a text label for each hour, placed below the corresponding bars
            
            The x-coordinate is calculated to place the label centered under the bars
            """
            self.canvas.create_text(
                margin + i * (2 * bar_width + bar_spacing) + bar_width,
                # x-coordinate at the center of each hour's bar group
                660,                                # y-coordinate positioned just below the bars (at y=660)
                text=hour,                          # The text displays the hour (e.g., "08:00")
                anchor=tk.N,                        # The label is anchored at the north (top) of the text
                font=("Arial", 10)                  # Font style and size for the label
            )

        # Add the title of the histogram at the top of the canvas, above the bars
        # The x-coordinate of 485 centers the title horizontally on the canvas
        self.canvas.create_text(
            485, 30,  # x-coordinate and y-coordinate for the title's position
            text=f"Histogram of Vehicle Frequency per Hour ({self.date})",  # The title text
            font=("Arial", 16)  # Font style and size for the title
        )

        # X-axis label indicating the time range
        self.canvas.create_text(
            700, 690,  # x-coordinate centered at the bottom of the canvas, y-coordinate placed below the X-axis line
            text="Hours 00:00 to 24:00",            # The label text for the X-axis
            font=("Arial black", 12)                # Font style and size for the X-axis label
        )

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which color represents which junction.
        """
        # Draw a green square for Junction 1
        self.canvas.create_rectangle(80, 60, 90, 70, fill="light green", outline="green") # Coordinates for x top , y top , x bottom , y bottom

        # Add legend text for Junction 1 (green color)
        self.canvas.create_text(186, 65, text="Elm Avenue/Rabbit Road", font=("Arial", 10)) # Coordinates for x and y

        # Draw a red square for Junction 2
        self.canvas.create_rectangle(80, 85, 90, 95, fill="red", outline="black")

        # Add legend text for Junction 2 (red color)
        self.canvas.create_text(190, 90, text="Hanley Highway/Westway", font=("Arial", 10))

    def run(self):
        """
        Runs the application by setting up the window, drawing the histogram,
        and adding the legend. This starts the Tkinter main loop.
        """
        # Set up the window and canvas for drawing
        self.setup_window()

        # Draw the histogram with the traffic data
        self.draw_histogram()

        # Add the legend to the histogram
        self.add_legend()

        # Start the Tkinter main loop, which keeps the window open continuously
        self.root.mainloop()


def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts hourly traffic counts -

    Counts vehicles for each hour at two junctions.
    Path to the CSV file.
    Dictionary with hour as the key and a list of two values [junction1_count, junction2_count].
    """
    hourly_traffic = {}

    try:
        with open(file_path, mode='r') as file:
            file_reader = csv.DictReader(file)

            # Iterate over rows to calculate hourly counts
            for row in file_reader:
                hour = row['timeOfDay'].split(':')[0]   # Extract the hour from 'timeOfDay'

                # Initialize the hour in the dictionary if not present
                if hour not in hourly_traffic:
                    hourly_traffic[hour] = [0, 0]       # [junction1_count, junction2_count]

                # Increment counts based on the junction name
                if row['JunctionName'] == "Elm Avenue/Rabbit Road":
                    hourly_traffic[hour][0] += 1
                elif row['JunctionName'] == "Hanley Highway/Westway":
                    hourly_traffic[hour][1] += 1

        print("Hourly traffic counts processed successfully.")
        return hourly_traffic

    except Exception as error:
        print(f"Error processing file: {error}")    # Notify the user that there was an error processing the data
        return {}


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple datasets based on user-entered dates.
        """
        self.current_data = None                    # Placeholder to store the current traffic data for processing
        self.date_to_data = None                    # Placeholder for mapping date to traffic data
        self.root = Tk()                            # Create the main Tkinter window
        self.root.title("Traffic Data Processor")   # Set the title of the Tkinter window

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None            # Reset the current data to None
        print("Previous data cleared.")     # Inform the user that data has been cleared

    def fetch_data_for_date(self, date):
        """
        Fetches traffic data for the given date from the dataset mapping.

        date - The user-entered date in string format ("DD/MM/YYYY").
        """
        self.date_to_data = process_csv_data(date)              # Call a function to process CSV data for the given date
        if self.date_to_data:
            self.current_data = self.date_to_data               # If data is found, store it in current_data
            print(f"Data for {date} retrieved successfully.")   # Notify successful data retrieval
        else:
            self.current_data = None                            # If no data is found, set current_data to None
            print(f"No data found for the date {date}.")        # Notify the user that no data was found

    def show_histogram(self, file_path, date):
        """
        Clears previous data, fetches data for the given date, and displays the histogram.

        file_path - Path to the CSV file being processed.
        date - The date for which to display the histogram. (It's a string value)
        """
        self.clear_previous_data()  # Clear any previously stored data
        self.fetch_data_for_date(file_path)  # Load the traffic data for the specified date

        if self.current_data:
            # If data is available, create a histogram using the HistogramApp class
            app = HistogramApp(self.current_data, file_path, date)
            app.run()  # Launch the Tkinter window for the histogram
        else:
            # If no data is available, show an error message
            messagebox.showerror("Error", f"No data available for the date {file_path}.")

    def handle_user_interaction(self):
        """
        Handles user interaction to process data for a user-entered date using a Tkinter window.
        """

        def process_date():
            """
            Inner function to process the user-entered date and file name.
            """
            date = f"{Date:02}/{Month:02}/{Year}"   # Format the date input as DD/MM/YYYY
            file_path = file_name                   # Assign the file path provided by the user
            self.root.destroy()                     # Close the Tkinter window after collecting inputs

            self.show_histogram(file_path, date)    # Display the histogram for the input date and file

        # Set the size of the main Tkinter window
        self.root.geometry("420x300")  # Set the window size (420x300 pixels)

        # Add a label to welcome the user
        Label(self.root,text="WELCOME TO TRAFFIC DATA PROCESSOR!",font=("Arial black", 10)).grid(row=0, column=0, padx=10, pady=10)

        # Add a button to start processing the data
        Button(self.root,text="Process Data",command=process_date).grid(row=1, column=0, padx=10, pady=10)

        # Add a button to quit the application and Destroy the Tkinter window when clicked
        Button(self.root,text="Quit",command=self.root.destroy).grid(row=2, column=0, padx=10, pady=10)

        Label(self.root, text="Close the histogram if you need "
                              "\nafter pressing 'Process' to load another dataset "
                              "\nor press 'Quit'.", font=("Arial black", 8)).grid(row=3, column=0,padx=10, pady=10)

        # Start the Tkinter main event loop to display the GUI and handle interactions
        self.root.mainloop()


# Main Program

if __name__ == "__main__":
    while True:
        print("<<< Welcome to Traffic Data Processor >>>")
        Date, Month, Year = abc.validate_date_input()  # Assign the date input to 3 variables Date , Month , Year

        file_name = f"data/traffic_data{Date:02}{Month:02}{Year}.csv"  # Generate the name of the file to Read
        
        """
        02 -
        "0" is to pad the numbers with leading zero if necessary
        "2" indicates the field width should be 2 digits
        """
        data = abc.process_csv_data(file_name)  # Creates a list of dictionaries after reading the csv file

        # Perform all calculations and assign the values to a list named "outcomes"
        outcomes = [abc.total_vehicles(data), abc.total_trucks(data), abc.total_electric_vehicles(data),
                    abc.total_two_wheeled_vehicles(data),
                    abc.total_busses_north(data), abc.total_vehicles_not_turning(data), abc.percentage_of_trucks(data),
                    abc.average_bicycles_per_hour(data), abc.total_vehicles_over_speed_limit(data), abc.total_vehicles_elm_avenue(data),
                    abc.total_vehicles_hanley_highway(data), abc.percentage_scooters_elm_avenue(data),
                    abc.peak_hour_vehicles_hanley_highway(data), abc.peak_traffic_hours_hanley_highway(data),
                    abc.total_hours_of_rain(data)]

        abc.display_outcomes(file_name,outcomes)  # Prints the Analysed Data to the IDLE shell

        # save the list as a text file named “results.txt”.
        abc.save_results_to_file(file_name, outcomes, file_to_write="results.txt")

        # Create an instance of the MultiCSVProcessor class to handle multiple datasets
        processor = MultiCSVProcessor()

        # Call the `handle_user_interaction` method to initiate user input handling via GUI
        processor.handle_user_interaction()

        # Check if the user wants to continue with another dataset or exit
        if abc.validate_continue_input():
            # If the user opts to continue, print a message indicating a new dataset is being processed
            print("<<< New Data Set Selected >>> ")
            continue  # Restart the loop to process a new dataset
        else:
            # If the user opts to exit, print an exit message and break the loop to end the program
            print("<<< Exiting the program >>> ")
            break  # Exit the loop and terminate the program



