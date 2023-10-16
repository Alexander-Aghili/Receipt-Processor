import base64
import os, glob
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage

from requests import HTTPError



# Set the path to your credentials JSON file
credentials_file = 'credentials.json'
SCOPES = ['https://mail.google.com/']

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Function to get all messages from a specific sender
def get_messages_from_sender(num_messages, sender_email="zlaclair@ucsc.edu"):
    try:
        # Use the Gmail API to search for messages from the specified sender
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', q=f'from:{sender_email}').execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
        else:
            for i in range(len(messages)):
                message = messages[i]
                messages[i] = service.users().messages().get(userId='me', id=message['id']).execute()

            messages=sorted(messages, key=lambda k: k['internalDate'], reverse=True)

            for i in range(len(message)):
                if i >= num_messages:
                    break
                for part in messages[i]['payload']['parts']:
                    if part['mimeType'] == 'application/pdf':
                        pdf = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=part['body']['attachmentId']).execute()
                        file_data = base64.urlsafe_b64decode(pdf['data'].encode('UTF-8'))
                        with open(part['filename'], 'wb') as f:
                            f.write(file_data)

    except Exception as e:
        print(f"An error occurred: {e}")


def send_message():
    try:
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()
        message['To'] = "zlaclair@ucsc.edu"
        message['From'] = "awaghili@ucsc.edu"
        message['Subject'] = "Renamed Files"

        for file in glob.glob("*.pdf"):
            with open(file, 'rb') as content_file:
                content = content_file.read()
                message.add_attachment(content, maintype='application', subtype='pdf', filename=file)
                

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(F'Message Id: {send_message["id"]}')
                # Specify the message ID of the email you want to mark as important
        message_id = send_message['id']

        # Specify the label to add (IMPORTANT label)
        labels_to_add = ['IMPORTANT']

        # Modify the message to add the label
        try:
            service.users().messages().modify(userId='me', id=message_id, body={'addLabelIds': labels_to_add}).execute()
            print(f"Email with Message ID {message_id} marked as important.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    except HTTPError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message

