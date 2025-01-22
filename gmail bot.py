
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def gmail_send_email():
    """Send an email using the Gmail API.
    
    Print the returned message's id.
    
    Returns:
        Message object, including message id and meta data.
    """
    creds, _ = google.auth.default()
    
    try:
        # Create Gmail API client
        service = build("gmail", "v1", credentials=creds)
        
        message = EmailMessage()
        message.set_content("This is an automated email sent using the Gmail API.")
        message["To"] = "recipient@example.com"
        message["From"] = "sender@example.com"
        message["Subject"] = "Automated Email"
        
        # Encode the message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        create_message = {"message": {"raw": encoded_message}}
        
        # Send the email
        sent_message = (service.users().messages().send(userId="me", body=create_message).execute())
        
        print(f"Message Id: {sent_message['id']}")
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        
if __name__ == "__main__":
    gmail_send_email()
