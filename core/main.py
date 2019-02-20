from __future__ import print_function
import datetime
import pickle
import os.path
import json
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    # Shows basic usage of the Google Calendar API.
    # Prints the start and name of the next 10 events on the user's calendar.
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/Users/sarah.young/code/play/meeting-tracker/env/credentials.json', SCOPES)

            # Tutorial says to use flow.run_local_server() but this also works.
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        event_summary = event["summary"]
        print(event_summary)

        event_type = extract_event_type(event_summary)

        data = {}
        data['summary'] = {
            "type": event_type,
        }
        json_data = json.dumps(data)
        print(json_data)


def extract_event_type(event_summary):
    type_pattern = "^.*(?=(\())"
    re.compile(type_pattern)
    event_type = re.match(type_pattern, event_summary).group(0)
    return event_type


if __name__ == '__main__':
    main()
