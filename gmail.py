import os, json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Set the path to your credentials JSON file
credentials_file = 'credentials.json'
sender_email = "zlaclair@ucsc.edu"
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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
def get_messages_from_sender():
    try:
        # Use the Gmail API to search for messages from the specified sender
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', q=f'from:{sender_email}').execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
        else:
            print('Messages from {}:'.format(sender_email))
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                print(json.dumps(msg, indent=2))
                print(f"Subject: {msg.get('subject')}")
                print(f"Snippet: {msg.get('snippet')}")
                print('---')

    except Exception as e:
        print(f"An error occurred: {e}")

