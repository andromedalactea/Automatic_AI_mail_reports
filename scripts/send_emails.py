import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email_with_attachment(sender_email, receiver_email, subject, body, attachment_path):
    # Create the MIME object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the email body
    message.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    with open(attachment_path, 'rb') as attachment_file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(attachment_path)}',
        )
        message.attach(part)

    # Convert the message to a string
    email_text = message.as_string()

    # SMTP server configuration
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    sender_password = os.getenv("SMTP_PASSWORD")

    # Send the email
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, email_text)

        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Usage example
    sender_email = os.getenv("SENDER_EMAIL")  # Replace with your email
    receiver_email = os.getenv("RECEIVER_EMAIL")  # Replace with the recipient's email
    subject = "Report"
    body = "Please find the attached report."
    
    attachment_path = "/home/clickgreen/freelancers/Automatic_AI_mail_reports/calificate_calls.pdf"  # Replace with the path to your PDF file

    send_email_with_attachment(sender_email, receiver_email, subject, body, attachment_path)