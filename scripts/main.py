# Local imports
from extract_leads_report import leads_report_info
from auxiliar_fucntions import get_ny_time_and_start_of_day, schedule_report

# Third-party imports
import pandas as pd

# Define the main function
def main_automatic_report():
    try:
        # Extract the timing information
        current_time_ny, start_of_day_ny = get_ny_time_and_start_of_day()
        
        ## DELETE THIS LINE IN PRODUCTION
        current_time_ny, start_of_day_ny = "2024-09-13 18:33", "2024-09-08 00:30"
        
        # Get the leads report
        leads_report = leads_report_info(start_of_day_ny, current_time_ny)

        # Print the first 5 rows of the DataFrame
        print(leads_report.head())

        # Success message
        return "success"
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Schedule the report to run between 6:00 PM and 6:30 PM
if __name__ == "__main__":
    main_automatic_report()
    # Schedule the report to run between 6:00 PM and 6:30 PM
    # schedule_report(main_automatic_report, start_hour=18, start_minute=0, end_hour=18, end_minute=30)