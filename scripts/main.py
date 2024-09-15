# Local imports
from extract_leads_report import leads_report_info
from auxiliar_fucntions import get_ny_time_and_start_of_day, schedule_report
from calificate_calls import calificate_calls_from_df
from df_to_pdf_calification import df_to_pdf
from send_emails import send_email_with_attachment

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

        # Check if the leads report is not empty
        if leads_report.empty:
            return "The leads report is empty"
        
        # Calificate the calls
        else:
            print(len(leads_report))
            leads_report = leads_report.head(5) # DELETE THIS LINE IN PRODUCTION
            leads_report = calificate_calls_from_df(leads_report)

        # Convert the DataFrame to a PDF
        df_to_pdf(leads_report, 'calificate_calls.pdf')

        ## Send the email with the attachment
        sender_email = "reports@salestrainerai.com"
        receiver_email = "bry3638@gmail.com"
        subject = f"Daily Leads Reports for the day {start_of_day_ny.split(' ')[0]}"
        body = "This email conatint a attached PDF with the repots for leads today"
        attachment_path = "calificate_calls.pdf"

        send_email_with_attachment(sender_email, receiver_email, subject, body, attachment_path)

        # Print the first 5 rows of the DataFrame
        leads_report.to_csv('calificate_calls.csv', index=False)

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