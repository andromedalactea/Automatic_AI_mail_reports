# Standar imports
import os
import tempfile
from io import BytesIO

# Third-party imports
import pandas as pd
import requests
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv(override=True)

def leads_report_info(query_date: str, end_date: str):
    """"
    This function logs into the CRM system and downloads the leads report.
    
    """
    # Define the environment variables
    PHP_AUTH_USER = os.getenv("PHP_AUTH_USER")
    PHP_AUTH_PW = os.getenv("PHP_AUTH_PW")
    DOMAIN = os.getenv("DOMAIN")

    # Login and report URLs
    login_url = f"{DOMAIN}/main/main.php"
    export_url = f"{DOMAIN}/main/lead_report_export.php"

    # Credentials for login
    payload = {
        "PHP_AUTH_USER": PHP_AUTH_USER,  # Username
        "PHP_AUTH_PW": PHP_AUTH_PW,      # Password
    }

    # Start a session
    session = requests.Session()

    # Send login credentials
    login_response = session.post(login_url, data=payload)

    # Check if login was successful
    if "Authentication Error" not in login_response.text:

        # If login is successful, send the request to download the report
        response = session.post(export_url, data={
            "run_export": "1",
            "query_date": query_date,  
            "end_date": end_date,    
            "date_field": "call_date",
            "header_row": "YES",
            "rec_fields": "ALL",
            "custom_fields": "NO",
            "call_notes": "NO",
            "did_filter": "NO",
            "export_fields": "STANDARD",
            "search_archived_data": "NO",
            "campaign[]": ["100"],
            "group[]": ["---NONE---"],
            "list_id[]": ["---ALL---"],
            "status[]": ["SALE"],
            "user_group[]": ["---ALL---"],
            "dids[]": [""],
        })

        # Check the response status
        if response.status_code == 200:
            try:
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
                    temp_file.write(response.content)  # Write the response content to the temp file
                    temp_file_path = temp_file.name    # Store the path to the temp file

                # Read the temporary file into a DataFrame
                df = pd.read_csv(temp_file_path, sep='\t')  # Using tab as separator
                os.remove(temp_file_path)  # Remove the temporary file

                return df
            
            except pd.errors.ParserError as e:
                print("ParserError:", e)
                print(response.content.decode('utf-8', errors='replace')[:1000])  # Print first 1000 chars for inspection
                return None
        else:
            print(f"Error downloading the report: {response.status_code}")
            print(response.text)
            return None
    else:
        print("Authentication Error: Please verify the credentials.")
        return None

# Example usage
if __name__ == "__main__":
    df = leads_report_info()
    if df is not None:
        print(df.head())  # Print the first few rows of the DataFrame