#Author: G.R. Hettiarachchi
#Date: 23/12/2024
#Student ID: w2120296

import csv
import math
import tkinter as tk

# Task A: Input Validation
# To handle the entire process of validating and processing the date input
def validate_date_input():

    def input_day():#This validates and get the day input from the user
        while True: #To repeatedly ask the input if user enters invalid date
            try:
                day = int(input("\nPlease enter the day of the survey in the format dd: "))
                if day < 1 or day > 31: #If day is outside the 1-31 range, user has to try again
                    print('Out of range - values must be in the range 1 and 31.')
                else:
                    return day #To send the value to the main program (if valid)
            except ValueError: #If the input isnt a number this handle the case
                print('Integer required')



    def input_month():#This validates and get the month input from the user
        while True: #To repeatedly ask the input if user enters invalid month 
            try:
                month = int(input("Please enter the month of the survey in the format MM: "))
                if month < 1 or month > 12: #If day is outside the 1-12 range, user has to try again
                    print('Out of range - values must be in the range 1 to 12.')
                else:
                    return month #To send the value to the main program 
            except ValueError: #If the input isnt a number this handle the case
                print('Integer required')
            


    def input_year():#This validates and get the year input from the user
        while True: #To repeatedly ask the input if user enters invalid year
            try:
                year = int(input("Please enter the year of the survey in the format YYYY: "))
                if year < 2000 or year > 2024: #If year is outside the 2000-2024 range, user has to try again
                    print('Out of range - values must range from 2000 and 2024.')
                else:
                    return year # To send the value to the main program 
            except ValueError: #If the input isnt a number this handle the case
                print('Integer required')


    #Leap year calculation
    #should be divisible by 4 and not divisible by 100 OR divisible by 400
    def leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) #return true or false
            


    while True: # Outer loop to keep asking for input until valid
        #Call the functions to get day, month and year
        day = input_day()
        month = input_month()
        year = input_year()


        if month == 2: # Check if the month is February
            if leap_year(year) and day > 29: 
                print("February has only 29 days in a leap year.") #print this if the user enters a day greater than 29 
                continue #restart loop
            elif not leap_year(year) and day > 28:
                print("February has only 28 days in a non leap year.") #print this if the user enters a day greater than 28
                continue #restart loop


        #To put a 0 in front
        if day < 10:
            day = f"0{day}"
        if month < 10:
            month = f"0{month}"


        #Create a formatted string combining day, month, and year
        day_as_string = f"{day}{month}{year}"

        #Create the name of the file based on the date entered by user
        file_path = f"traffic_data{day_as_string}.csv"
        
        #Check if the date matches one of our known data files
        if day_as_string in ['15062024', '16062024', '21062024']:
            print(f"\n***************************\ndata file selected is {file_path}\n***************************\n")
            return file_path, f"{day}/{month}/{year}"  #  Return both file_path (name of the file) and formatted_date
        else:
            print("Invalid date entered. No data file.")

#Function to let the user decide if they want another file or exit
def validate_continue_input():
    while True:
        user_input = input("Do you want to load another file? (Y/N): ").lower()
        if user_input == "y":
            return True  #Go back to the main loop and let the user pick another date
        elif user_input == "n":
            print("Exiting program..")
            exit()  #Exit the program completely
        else:
            print("Invalid. Please enter 'Y' or 'N'.")


# Task B: Processed Outcomes

# Function to process data from a CSV file
def process_csv_data(file_path):
    #initialize counters to track vehicle statistics
    total_vehicles = 0
    total_trucks = 0
    total_electric_vehicles = 0
    two_wheeled_vehicles = 0
    bus_went_north = 0
    one_direction_vehicles = 0
    over_speedlimit_vehicles = 0
    elm_avenue = 0
    hanley_highway = 0
    total_hours = 24
    total_bicycles = 0
    total_scooters = 0
    vehicle_count_per_hour = [0] * 24 #Creates a list with 24 zeros, Each zero represents the number of vehicles for each hour of the day
    peak_hours = []
    rain_hours = []



    try:
        # Open the CSV file
        with open(file_path, mode='r') as file:
            csvreader = csv.DictReader(file)  #Create a CSV reader that reads each row as a dictionary
            
            #Loop through each row in the CSV file
            for row in csvreader: 
                
                #To calculate total number of vehicles
                total_vehicles += 1  #increment the total vehicle count by 1
                
                #To calculate total number of Trucks
                #Check if the 'VehicleType' column contains "truck", and if true, increment the truck counter
                if "truck" in row["VehicleType"].lower():
                    total_trucks += 1
                
                #To calculate total number of Electric vehicles
                #Check if the 'elctricHybrid' column for this row has the value 'TRUE'
                if row["elctricHybrid"].strip().upper() == "TRUE":  
                    total_electric_vehicles += 1


                #Check if the vehicle is a two-wheeled vehicle 
                if (
                    "bicycle" in row["VehicleType"].lower().strip() or 
                    "scooter" in row["VehicleType"].lower().strip() or 
                    "motorcycle" in row["VehicleType"].lower().strip()
                    ):
                    #if true increment the counter
                    two_wheeled_vehicles += 1

                #Calculate total number of busses leaving Elm Avenue/Rabbit Road 
                if (
                    row["JunctionName"] == "Elm Avenue/Rabbit Road" and #check if the vehicle at elm avn/rabbit rd.
                    row["travel_Direction_out"].strip().lower() == "n" and #check if the bus is towards north (n)
                    row["VehicleType"].strip().lower() == "buss" # Check if the vehicle type is 'bus'
                    ):
                    #if true increment the counter
                    bus_went_north += 1
                
                #Calculate total number of vehicles that went in one direction
                if row["travel_Direction_in"] == row["travel_Direction_out"]:
                    one_direction_vehicles += 1 #if the two rows are the same it travels in only 1 direction
                
                #Calculate total number of vehicles recorded as over the speed limit 
                if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]): #Check if a vehicle's speed exceeds the junction's speed limit
                    over_speedlimit_vehicles += 1
                
                #Total number of vehicles recorded through Elm Avenue/Rabbit Road junction 
                if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                    elm_avenue += 1

                #Total number of vehicles recorded through Hanley Highway/Westway junction  
                elif row["JunctionName"] == "Hanley Highway/Westway":
                    hanley_highway += 1
                
                #Total number of bicycles 
                if row["VehicleType"] == "Bicycle" and not (
                row["VehicleType"] == "Scooter" and 
                row["VehicleType"] == "Motorcycle"
                ):
                    total_bicycles += 1
                
                #Total number of bicycles recorded through Elm Avenue/Rabbit Road
                if row["JunctionName"] == "Elm Avenue/Rabbit Road" and "Scooter" in row["VehicleType"]:
                    total_scooters += 1

                #This is for the 'highest number of vehicles in an hour' calculation
                
                if row["JunctionName"] == "Hanley Highway/Westway":
                    # get the hour part from the 'timeOfDay' column by splitting the string at ':' and converting the first part to an integer
                    hour = int(row["timeOfDay"].split(":")[0])  
                    if 0 <= hour < total_hours: #make sure that the extracted hour is within the valid range (0-23)
                        vehicle_count_per_hour[hour] += 1 #Takes the value in the list at the index hour and increases it by 1.
                
                
                #Calculate total number of hours of rain on the selected date
                if "rain" in row["Weather_Conditions"].lower(): #Check if the 'Weather_Conditions' column contains the word "rain"
                    # get the hour part from the 'timeOfDay' column by splitting the string at ':' and converting the first part to an integer
                    rain_hour = int(row["timeOfDay"].split(":")[0])  
                    # if this hour not already recorded to the list, add the hour to the rain hours list 
                    if rain_hour not in rain_hours:  
                        rain_hours.append(rain_hour)

        #Calculate the average number of Bicycles per hour
        avg_bicycles= total_bicycles/total_hours


        #Calculate the percentage of trucks out of all recorded vehicles
        if total_vehicles > 0: # Check if any vehicles were recorded to avoid division by zero
            truck_percentage = (total_trucks/total_vehicles)*100
        else:
            truck_percentage = 0  #If no vehicles are recorded, set the percentage of trucks to 0


        # Calculate the percentage of scooters passing through Elm Avenue/Rabbit Road
        if elm_avenue > 0: # Check if any vehicles were recorded in elm avenue to avoid division by zero
            scooter_percentage = math.floor((total_scooters/elm_avenue)*100)  # Calculate and round down to the nearest integer
        else:
            scooter_percentage = 0 #If no vehicles are recorded, set the percentage to 0



#Calculate the highest number of vehicles in an hour on Hanley Highway/Westway 
        max_hour_vehicles = 0
        # Loop through the list of vehicle counts for each hour (vehicle_count_per_hour)
        for count in vehicle_count_per_hour:
            #check if the current hour's vehicle count is greater than the current maximum
            if count > max_hour_vehicles:
                max_hour_vehicles = count #Update the maximum



#Calculate the busiest traffic hours on Hanley Highway/Westway       
        for hour in range(total_hours):
            # Check if this hour has the highest number of vehicles
            if vehicle_count_per_hour[hour] == max_hour_vehicles:
                # If true, append the hour to the list of peak hours in the desired format
                peak_hours.append(f"between {hour}:00 and {int(hour)+1}:00")


        

        # Create a summary of results to display and save
        results = ( # Combine all statistics into a single string
            f"The total number of vehicles recorded for this date is: {total_vehicles}\n"
            f"The total number of trucks recorded for this date is: {total_trucks}\n"
            f"The total number of electric vehicles for this date is: {total_electric_vehicles}\n"
            f"The total number of two-wheeled vehicles for this date is: {two_wheeled_vehicles}\n"
            f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is: {bus_went_north}\n"
            f"The total number of Vehicles through both junctions not turning left or right is: {one_direction_vehicles}\n"
            f"The percentage of total vehicles recorded that are trucks for this date is: {round(truck_percentage)}%\n"
            f"The average number of Bikes per hour for this date is: {round(avg_bicycles)}\n"
            f"The total number of Vehicles recorded as over the speed limit for this date is: {over_speedlimit_vehicles}\n"
            f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is: {elm_avenue}\n"
            f"The total number of vehicles recorded through Hanley Highway/Westway junction is: {hanley_highway}\n"
            f"{scooter_percentage}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n"
            f"The highest number of vehicles in an hour on Hanley Highway/Westway is: {max_hour_vehicles}\n"
            f"The most vehicles through Hanley Highway/Westway were recorded: {', '.join(peak_hours)}\n" #Use join to combine multiple hours into a single readable string
            f"The number of hours of rain for this date is: {len(rain_hours)}\n" #len counts total number of hours in the rain hours list
        )
        
        # Create a header to display before the results
        file_info = f"***************************\ndata file selected is {file_path}\n***************************\n"
        
        #Call the function to show results on the console
        display_outcomes(results)
        
        # Call to save the combined header and results to 'result.txt'
        save_results_to_file(file_info + results) #(file_info + results is the actual data)
        
    # Handle the case where the file doesn't exist
    except FileNotFoundError:
        print(f"File {file_path} not found.")

# Function to display results on the console
def display_outcomes(results):
    print(results)


# Task C: Save Results to Text File

# Function to save the results into a file (outcomes is the placeholder)
def save_results_to_file(outcomes):
    
    with open("results.txt", "a") as file: # Open results.txt in append mode
        file.write(outcomes)  #Write the results to the file



# Task D: Histogram Display
class HistogramApp: #to handle making and showing a histogram graph.
    def __init__(self, traffic_data, date):
        # Initialize traffic data (how many cars per hour) and the date for the graph.
        self.traffic_data = traffic_data # store traffic data for later use (like an empty box)
        self.date = date
        self.root = tk.Tk()  # Create the Tkinter root window (setting up an empty page)
        self.root.title("Histogram") # Set the window title

    def setup_window(self):
        # Setup the canvas with appropriate dimensions
        self.canvas = tk.Canvas(self.root, width=1400, height=800, bg="white") # Adjust canvas dimensions for better view (drawing area)
        self.canvas.pack() #canvas appears in the window 
        self.canvas.create_line(100, 690, 1340, 690, width=2, fill="gray") #start at 100 steps from left, 690 down and end at 1340 steps from left, 690 down
        self.canvas.create_text(720, 720, text="Hours 00:00 to 24:00", font=("Arial", 12, "bold"), fill = "#4f5251") #first 720 in the middle, 2nd 720 at the botton
        self.canvas.create_text(
            330, 40, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", # will hold the date to label the histogram later.
            font=("Arial", 16, "bold"), fill="#4f5251") #330 at left ,40 on top (locate at top left corner)

    # Draw histogram bars for traffic data
    def draw_histogram(self):
        
        bar_width = 22  # Set the width for each bar
        gap_between_hours = 10  # Space between hour groups

        #Loop through each hour in the traffic data and get the hour and the traffic counts for Elm and Hanley
        for hour, (elm_count, hanley_count) in self.traffic_data.items():
            # Find where to 'start' drawing the bars for the current hour.
            x_start = 60 + hour * (2 * bar_width + gap_between_hours)

            # Elm Avenue bar (green)
            elm_x_end = x_start + bar_width  # End position for Elm bar
            self.canvas.create_rectangle(
                x_start, 
                690 - elm_count * 8, #Calculate the 'top position' of the Elm Avenue bar by subtracting it from the bottom (690)
                elm_x_end, 
                690, #Calculate the 'bottom position' of the Elm Avenue bar
                fill="#c8f577", outline="gray")  # green bar
            
            self.canvas.create_text(
                (x_start + elm_x_end) // 2, #finds the middle of the Elm Avenue bar so the number can be placed center
                690 - elm_count * 8 - 10, #place the number top of the bar (-10 helps to position it a little higher.)
                text=str(elm_count), #turns the number into a string to display
                font=("Arial", 8, "bold"), fill = "#a0d443") 
            
            # Hanley Highway bar (blue)
            hanley_x_start = elm_x_end  # Set the starting position after elm bar
            hanley_x_end = hanley_x_start + bar_width #where the bar will end
            self.canvas.create_rectangle(
                hanley_x_start, 
                690 - hanley_count * 8,  #Calculate the 'top position' of the Hanley Highway bar by subtracting it from the bottom (690)
                hanley_x_end, 
                690, #Calculate the 'bottom position' of the Hanley Highway bar
                fill="#a2c7de", outline="gray") #blue bar 
            
            self.canvas.create_text(
                (hanley_x_start + hanley_x_end) // 2, #finds the middle of the hanley highway bar so the number can be placed center
                690 - hanley_count * 8 - 10, #place the number top of the bar (-10 helps to position it a little higher.)
                text=str(hanley_count), #turns the number into a string to display
                font=("Arial", 8, "bold"), fill = "#7dafcf")
            # Format hour to two digits if its less than 10.
            if hour < 10:
                hour_label = f"0{hour}"
            else:
                hour_label = str(hour)
            self.canvas.create_text(
                (x_start + hanley_x_end) // 2, #finding the middle point between the Elm and Hanley bars to place the hour in center
                700, #places the hour below the bars
                text=hour_label, #with leading 0s
                font=("Arial", 8))
            
    #two small squares to understand what the colors of the bars mean
    def add_legend(self):
        self.canvas.create_rectangle(
            60, 60, #60 units to the right and 60 units down
            80, 80, #80 units to the right and 80 units down
            fill="#c8f577", outline="gray")  # Add green rectangle for Elm
        
        # label for elm bar legend
        self.canvas.create_text(
            90, 70,  # defines the position where the description text will be placed.
            text="Elm Avenue/Rabbit Road", 
            font=("Arial", 11), anchor="w")  # Label for Elm
        
        self.canvas.create_rectangle(
            60, 90, #60 units to the right and 90 units down
            80, 110, #80 units to the right and 110 units down
            fill="#a2c7de", outline="gray")  # Add blue rectangle for Hanley
        
        # label for henly bar legend
        self.canvas.create_text(
            90, 100, # defines the position where the description text will be placed.
            text="Hanley Highway/Westway",
            font=("Arial", 11), anchor="w")  # Label for Hanley

    def run(self):
        self.setup_window() # Set up the window and canvas
        self.draw_histogram() # Draw the histogram bars
        self.add_legend() # Add a legend for the colors
        self.root.mainloop() #  starts the Tkinter event loop, allowing the window to remain open and interactive

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        self.current_data = None #going to hold the traffic data loaded from the CSV file

    def load_csv_file(self, file_path): # to open a CSV file using its location.(just a placeholder)
        #a dictionary to track the traffic count for each hour (from 0 to 23)
        hourly_data = {hour: [0, 0] for hour in range(24)} #each hour has two counts: one for Elm (1st num) and one for Hanley(2nd num).
        try:
            with open(file_path, mode='r') as file: # open the file in read mode ('r')
                # Create a CSV reader that will treat each row as a dictionary
                csvreader = csv.DictReader(file)
                # Loop through each row in the CSV file (each row is a dictionary)
                for row in csvreader:
                    hour = int(row["timeOfDay"].split(":")[0])  # Extract the hour from the "timeOfDay" value (splitting at the colon)
                    if row["JunctionName"] == "Elm Avenue/Rabbit Road":# check If the junction is "Elm Avenue/Rabbit Road", 
                        hourly_data[hour][0] += 1 #elm avenue is first part of the list; increase its count by 1
                    elif row["JunctionName"] == "Hanley Highway/Westway": # check If the junction is "Hanley Highway/Westway", 
                        hourly_data[hour][1] += 1 #Hanley Highway is the 2nd part of the list; increase its count by 1
            self.current_data = hourly_data # Save the hourly data to 'current_data' (available to other parts of the program)
        except FileNotFoundError:
            print(f"File {file_path} not found.") # If the file isn't found

    #to handle the interaction with the user
    def handle_user_interaction(self):
        while True: #starts an infinite loop to keep asking the user for input until they choose to stop
            # Get the file path and formatted date by calling the validate_date_input function
            file_path, formatted_date = validate_date_input()
            process_csv_data(file_path) #call this to display the processes in task b before displaying the histogram
            self.load_csv_file(file_path)
            if self.current_data: #checks if self.current_data has anything in it.
                # Create a new HistogramApp object using the traffic data (self.current_data) and the date (formatted_date)
                histogram_app = HistogramApp(self.current_data, formatted_date)  #this data is assigned to self.traffic_data
                histogram_app.run() #runs the histogram app just created

            if not validate_continue_input(): # Ask the user if they want to continue, if they don't, break out of the loop
                break

if __name__ == "__main__": # runs when the file is executed directly, not when it's imported.
    processor = MultiCSVProcessor() #setting up everything needed to start processing CSV files
    processor.handle_user_interaction() #to begin processing the data and handling user input
