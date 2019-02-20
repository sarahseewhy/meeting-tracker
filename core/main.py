from __future__ import print_function
import pickle
import os.path
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

    today = datetime.today()
    week_ago = today - relativedelta(weeks=1)
    time_max = today.isoformat('T') + "Z"
    time_min = week_ago.isoformat('T') + "Z"

    # Call the Calendar API
    events_result = service.events().list(calendarId='primary', timeMin=time_min, timeMax=time_max,
                                          maxResults=50, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:

        # retrieve the summary, currently the only thing I'm interested in
        summary = event["summary"]

        # extract the event from the summary
        event_type = extract_event_type_from(summary)

        # output event types from the given time period
        print(event_type)


def extract_event_type_from(summary):
    pattern = "^.*(?=(\())"
    re.compile(pattern)
    event_type = re.match(pattern, summary).group(0)
    return event_type


if __name__ == '__main__':
    main()
