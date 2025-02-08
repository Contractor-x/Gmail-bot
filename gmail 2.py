import base64
import logging
import os
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_credentials():
    try:
        creds, _ = google.auth.default()
        return creds
    except Exception as error:
        logging.error(f"Error obtaining credentials: {error}")
        raise

def create_message(sender, to, subject, body, html_body=None, attachment=None):
    message = EmailMessage()
    message.set_content(body)
    
    if html_body:
        message.add_alternative(html_body, subtype='html')
    
    message["To"] = to
    message["From"] = sender
    message["Subject"] = subject
    
    if attachment:
        with open(attachment, "rb") as file:
            message.add_attachment(file.read(), maintype="application", subtype="octet-stream", filename=os.path.basename(attachment))
    
    return message

def send_email(service, message):
    try:
        # Encode the message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"message": {"raw": encoded_message}}
        
        # Send the email
        sent_message = service.users().messages().send(userId="me", body=create_message).execute()
        
        logging.info(f"Message sent successfully with id: {sent_message['id']}")
        return sent_message
    except HttpError as error:
        logging.error(f"An error occurred while sending email: {error}")
        raise
    except Exception as error:
        logging.error(f"Unexpected error: {error}")
        raise

def gmail_send_email():
    logging.basicConfig(level=logging.INFO)
    
    # Retrieve credentials
    creds = get_credentials()
    
    # Create Gmail API client
    service = build("gmail", "v1", credentials=creds)
    
    sender = os.getenv('SENDER_EMAIL', 'sender@example.com')
    recipient = os.getenv('RECIPIENT_EMAIL', 'recipient@example.com')
    subject = "Automated Email"
    body = "This sends an email using the Gmail API."
    html_body = "<html><body><p>This is an <b>automated</b> email sent using the Gmail API.</p></body></html>"
    
    # Create the message
    message = create_message(sender, recipient, subject, body, html_body)
    
    # Send the email
    send_email(service, message)

if __name__ == "__main__":
    gmail_send_email()
