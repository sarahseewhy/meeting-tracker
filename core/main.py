from __future__ import print_function
import pickle
import os.path
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import Counter
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():

    credentials = configure_app_authorization()
    calendar = build('calendar', 'v3', credentials=credentials)
    time_max, time_min, week_ago = calculate_timeframe()
    calendar_items = retrieve_calendar_items_from(calendar, time_max, time_min)
    events = calendar_items.get('items', [])
    event_types = extract_type_from(events)

    output = generate_output(event_types)

    display_output(output, week_ago)


def display_output(output, week_ago):
    print('Team events since %s' % week_ago.date())
    print(output)


def generate_output(event_types):
    types = Counter(event_types).keys()
    frequency = Counter(event_types).values()
    return dict(zip(types, frequency))


def extract_type_from(events):
    event_types = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        # retrieve the summary, currently the only thing I'm interested in
        summary = event["summary"]
        # extract the event from the summary
        event_type = extract_event_type_from(summary)
        # add types to array of types
        event_types.append(event_type)
        # output event types from the given time period
    return event_types


def retrieve_calendar_items_from(service, time_max, time_min):
    events_result = service.events().list(calendarId='primary', timeMin=time_min, timeMax=time_max,
                                          maxResults=50, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result


def calculate_timeframe():
    today = datetime.today()
    week_ago = today - relativedelta(weeks=1)
    time_max = today.isoformat('T') + "Z"
    time_min = week_ago.isoformat('T') + "Z"
    return time_max, time_min, week_ago


def configure_app_authorization():
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    credentials = load_token()
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            credentials = authorize_credentials()
        with open('token.pickle', 'wb') as token:
            save_credentials(credentials, token)
    return credentials


def save_credentials(credentials, token):
    pickle.dump(credentials, token)


def authorize_credentials():
    flow = InstalledAppFlow.from_client_secrets_file('env/credentials.json', SCOPES)
    credentials = flow.run_console()
    return credentials


def load_token():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    return credentials


def extract_event_type_from(summary):
    pattern = "^.*(?=(\())"
    re.compile(pattern)
    event_type = re.match(pattern, summary).group(0)
    return event_type


if __name__ == '__main__':
    main()
