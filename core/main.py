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
    number_of_weeks = 1

    calendar = build('calendar', 'v3', credentials=authorized_credentials())
    calendar_items = retrieve_calendar_items_from(calendar, for_time_range_in(number_of_weeks))
    event_types = extract_types_from(calendar_items.get('items', []))

    display(collated_event_types_and_frequency_from(event_types), number_of_weeks)


def display(output, number_of_weeks):
    date = datetime.today() - relativedelta(weeks=number_of_weeks)
    print('Team events since %s' % date.strftime("%B %d, %Y"))
    print(output)


def collated_event_types_and_frequency_from(event_types):
    types = Counter(event_types).keys()
    frequency = Counter(event_types).values()
    return dict(zip(types, frequency))


def extract_types_from(events):
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


def extract_event_type_from(summary):
    pattern = "^.*(?=(\())"
    return re.match(re.compile(pattern), summary).group(0)


def retrieve_calendar_items_from(service, time_frame):
    return service.events().list(calendarId='primary', timeMin=time_frame.get("min"), timeMax=time_frame.get("max"),
                                 maxResults=50, singleEvents=True, orderBy='startTime').execute()


def for_time_range_in(number_of_weeks):
    weeks_ago = datetime.today() - relativedelta(weeks=number_of_weeks)
    time_frame = {
        "min": weeks_ago.isoformat('T') + "Z",
        "max": datetime.today().isoformat('T') + "Z"
    }
    return time_frame


def authorized_credentials():
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
    return InstalledAppFlow.from_client_secrets_file('env/credentials.json', SCOPES).run_console()


def load_token():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    return credentials


if __name__ == '__main__':
    main()
