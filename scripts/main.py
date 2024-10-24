# Import python libraries
import os

# Local imports
from extract_leads_report import leads_report_info
from auxiliar_functions import get_ny_time_and_start_of_day, schedule_report, absolute_path
from calificate_calls import calificate_calls_from_df
from df_to_pdf_calification import df_to_pdf
from send_emails import send_email_with_attachment

# Third-party imports
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)
pd.set_option('display.max_columns', None) 

# Define the main function
def main_automatic_report():
    try:
        # If not exist files directory create it
        os.makedirs(absolute_path('../files'), exist_ok=True)

        # Extract the timing information
        current_time_ny, start_of_day_ny = get_ny_time_and_start_of_day()
        
        ## DELETE NEXT LINE IN PRODUCTION
        # current_time_ny, start_of_day_ny = "2024-09-13 18:33", "2024-09-08 00:30"

        print(f"Current time in New York: {current_time_ny}")
        print(f"Start of the day in New York: {start_of_day_ny}")

        # Get the leads report
        leads_report = leads_report_info(start_of_day_ny, current_time_ny)

        # Check if the leads report is not empty
        if leads_report.empty:
            return "The leads report is empty"
        
        # Calificate the calls
        else:
            print(len(leads_report))
            # leads_report = leads_report.head(3) # DELETE THIS LINE IN PRODUCTION
            leads_report = calificate_calls_from_df(leads_report)

        # Name for the pdf
        pdf_name = f"{os.getenv('ATTACHMENT_NAME')}_{current_time_ny.split(' ')[0]}.pdf"
        pdf_path = absolute_path(f"../files/{pdf_name}")

        # Convert the DataFrame to a PDF
        css_path = absolute_path('../css/style_report.css')
        df_to_pdf(leads_report, pdf_path, css_path)

        ## Send the email with the attachment
        sender_email = os.getenv("SENDER_EMAIL")
        receiver_emails = os.getenv("RECEIVER_EMAIL")
        receiver_email_list = receiver_emails.split(',')

        # Email information
        subject = f"Daily Leads Reports for the day {start_of_day_ny.split(' ')[0]}"
        body = "This email contains an attached PDF with today's lead reports."

        for receiver_email in receiver_email_list:
            send_email_with_attachment(sender_email, receiver_email, subject, body, pdf_path)

        # # Print the first 5 rows of the DataFrame
        # leads_report.to_csv('calificate_calls.csv', index=False)

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