
from datetime import date, datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class GoogleCalendar():
    def __init__(self):
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
        try:
            self.service = build('calendar', 'v3', credentials=creds)
        except HttpError as error:
            print('An error occurred: %s' % error)

    def get_ut_schedules(self):
        # Call the Calendar API
        today = date.today().isoformat() + 'T00:00:00+09:00'  
        tommorow = (date.today() + timedelta(days=1)).isoformat() + 'T23:59:59+09:00'  
        service_list = self.service.calendarList().list().execute()
        events = []
        try:
            for item in service_list['items']:
                events_result = self.service.events().list(calendarId=item['id'], 
                                                      timeMin=today,timeMax=tommorow,
                                                      singleEvents=True,orderBy='startTime').execute()
                events.extend(events_result.get('items', []))
        except HttpError as error:
            print('An error occurred: %s' % error)

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])



if __name__ == '__main__':
    sch = GoogleCalendar()
    sch.get_ut_schedules()