from datetime import datetime, timedelta  # Module for working with dates and times
import os  # Module for working with the file system

# These two functions save the time_log file in the same directory as this file. If you would like to specify a specific path, you may get rid of the get_script_path() function and you will need to alter the get_log_file_path()
# Function to get the path of the current script
def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

# Function to construct the full path for the log file
def get_log_file_path():
    script_path = "C:\\Users\\Name\\Desktop" # Replace this with the path where you would like to save your log file in quotations, make sure to use 2 slash characters
    script_path = get_script_path() # Delete this if you are saving the log file to your own directory instead
    return os.path.join(script_path, "time_log.txt") 

            
# Write log entry to file
def write_log_entry(f, date, start_time_str, end_time_str, duration, total_duration):
    f.write(f"{date} | {start_time_str} | {end_time_str} | {format_duration(duration)} | {total_duration}\n")

# Format duration to HH:MM:SS format
def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02d}:{seconds:02d}"

# Calculate duration string from duration in seconds
def calculate_duration_str(duration):
    return format_duration(duration)

# Get previous data from the log file
def get_previous_data():
    with open(get_log_file_path(), 'a+') as f:
        f.seek(0)
        previous_data = f.readlines()
    return previous_data



# Get the start time in HH:MM:SS format
start_time_str = datetime.now().strftime("%H:%M:%S")


# Put your script here
input("Press enter to end...")


# Get the end time in HH:MM:SS format
end_time_str = datetime.now().strftime("%H:%M:%S")

# Calculate duration in seconds
date = datetime.now().strftime("%Y-%m-%d")
start_time = datetime.strptime(start_time_str, "%H:%M:%S")
end_time = datetime.strptime(end_time_str, "%H:%M:%S")
duration = int((end_time - start_time).total_seconds())
duration_str = str(duration).split('.')[0]

# Read the previous total duration from the file, if it exists
previous_data = get_previous_data()
total_duration_str = calculate_duration_str(duration)

with open(get_log_file_path(), 'a+') as f:
    if len(previous_data) == 0:
        # If no data found, create a new file with headers
        f.write("Date | Start time | End Time | Duration | Total Duration\n")
        f.write("--------------------------------------------------------\n")

        write_log_entry(f, date, start_time_str, end_time_str, duration, total_duration_str)
    else:
        # If data found, update the file with new record
        previous_duration_str = previous_data[-1].split("|")[4].strip()  # Get the last record's total duration
        previous_duration = datetime.strptime(previous_duration_str, "%H:%M:%S")

        # Calculate total duration
        total_duration = timedelta(hours=previous_duration.hour, minutes=previous_duration.minute, seconds=previous_duration.second)  # Creates timedelta object with desired format
        total_duration += timedelta(seconds=duration)  # Add the current duration
        total_duration_str = calculate_duration_str(total_duration.seconds)

        write_log_entry(f, date, start_time_str, end_time_str, duration, total_duration_str)