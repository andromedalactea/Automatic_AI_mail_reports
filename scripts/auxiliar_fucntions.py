import time
from datetime import datetime
import pytz

def get_ny_time_and_start_of_day():
    # Define the New York timezone
    ny_tz = pytz.timezone('America/New_York')

    # Get the current time in New York
    ny_now = datetime.now(ny_tz)

    # Format the current New York time as a string
    ny_now_str = ny_now.strftime('%Y-%m-%d %H:%M')

    # Get the start of the same day (00:30)
    start_of_day = ny_now.replace(hour=0, minute=30, second=0, microsecond=0)
    start_of_day_str = start_of_day.strftime('%Y-%m-%d %H:%M')

    return ny_now_str, start_of_day_str

def schedule_report(report_function, start_hour: int=18, start_minute: int=0, end_hour: int=18, end_minute: int=30):
    """
    Function to schedule the report between specified time intervals and avoid running it multiple times within the same interval.

    Args:
        start_hour (int): Start hour of the interval (24-hour format). Default is 18 (6 PM).
        start_minute (int): Start minute of the interval. Default is 0.
        end_hour (int): End hour of the interval (24-hour format). Default is 18 (6 PM).
        end_minute (int): End minute of the interval. Default is 30.
    """
    while True:
        now = datetime.now()

        # Define the start and end times for the interval
        start_time = now.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
        end_time = now.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)

        # Check if the current time is within the specified interval
        if start_time <= now <= end_time:
            # Try to generate the report
            result = report_function()
            if result == "success":
                print("Report generated successfully. Sleeping for 20 hours.")
                # Sleep for 20 hours before checking the interval again
                time.sleep(20 * 3600)
            else:
                print("Error generating report. Retrying...")
                # Sleep a short time before checking the interval again to avoid busy waiting
                time.sleep(60)
        else:
            # If not within the interval, sleep for a while before checking again
            print("Not in the time interval. Checking again in 30 minutes.")
            time.sleep(15 * 60)
            
# Example usage
if __name__ == "__main__":
    current_time_ny, start_of_day_ny = get_ny_time_and_start_of_day()
    print("Current time in New York:", current_time_ny)
    print("Start of the day (00:30) in New York:", start_of_day_ny)
