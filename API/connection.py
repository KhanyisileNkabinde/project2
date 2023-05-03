import datetime as dt

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def build_calendar():
    """Attempts to connect to connect to the code clinic calendar via google api

    Returns:
        calendar: the calendar service on success (Returns False on failure)
    """

    try:
        creds = Credentials.from_authorized_user_file('.data/token.json', SCOPES)
        if not creds.valid and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        with open('.data/token.json', 'w') as token:
            token.write(creds.to_json())


        calendar = build('calendar', 'v3', credentials=creds)
        return calendar
    except RefreshError as err:
        print(err)
        return False

def login_calendar():

    flow = InstalledAppFlow.from_client_secrets_file(
                '.data/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('.data/token.json', 'w') as token:
            token.write(creds.to_json())




def insert_events (calendar: object, user: str, day: int, month: int, year: int,
                    hour: int, mins: int, secs: int) -> bool:
    """Attempts to insert a 30 minute code clinic session at the supplied date & time

    Args:
        calendar (object): the google calendar service
        user (str): the volunteer creating the session
        day (int): the day of the code clinic
        month (int): the month of the code clinic (January = 1)
        year (int): the year of the code clinic
        hour (int): the hour of the code clinic

    Returns:
        bool: whether the session was created succsessfully
    """

    start = dt.datetime(year, month, day, hour, mins, secs)
    end = (start + dt.timedelta(minutes=30)).isoformat()
    start = start.isoformat()
    event = {
      'summary': f'Code Clinic by {user}.',
      
      'description': 'Volunteer available',
      'start': {
        'dateTime': start,
        'timeZone': 'Africa/Johannesburg',
      },
      'end': {
        'dateTime': end,
        'timeZone': 'Africa/Johannesburg',
      },
      'attendees': [
          {
              "email": f"{user}@student.wethinkcode.co.za",
              "responseStatus": "accepted"
          }
      ]
    }
    try:
        event = calendar.events().insert(calendarId='primary',body=event).execute()
        return True,('Event created.')
    except:
        return False,('The event creation failed.')
        


def del_events (calendar: object,event_id: str) -> bool:
    """Attempts to delete the specified event from the calendar

    Args:
        calendar(object): the google calendar service object
        event_id(str): the google event id

    Returns:
        bool: whether the deletion was succsessful
    """

    try:
        calendar.events().delete(
            calendarId='primary',
            eventId = event_id,
        ).execute()
        return True
    except:
        print('Somethings wrong, I can feel it.')
        return False



def get_events(calendar: object, days = 7) -> list:
    """Requests all the events from the google calendar for the next specified days

    Args:
        calendar(object): The google calendar service object
        days(int): how many days of events to look for
            (default is 7)
    
    Returns:
        list: all the events for the specified time (empty if no events)
    """

    now = dt.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    a_week = (dt.datetime.utcnow() +dt.timedelta(days=days)).isoformat() + 'Z'
    print(f'Getting the next {days} days of code clinics.')
    events_result = calendar.events().list(
        calendarId='primary', timeMin=now, timeMax=a_week,
        singleEvents=True, orderBy='startTime'
        ).execute()
    events = events_result.get('items', [])
    return events


def get_event_times(events: list) -> list:
    """Converts a list of events into a list of their date & times

    Args:
        events(list): the events to find dates & times for

    Returns:
        list: a list of dates & times
    """

    event_times = []
    for event in events:
        start = event['start']['dateTime']
        event_times.append(start[:19]) # Removes timezone info
    return event_times


def get_open_times(event_times: list, days=7,allowed_hours=range(7,18)) -> list:
    """Finds all times within the specified parameters that aren't in event_times

    Args:
        event_times(list): a list of booked times
        days(int): how many days ahead that are allowed to be open
            (default is 7)
        allowed_hours(iterable): hours that are allowed
            (default is 7-18)

    Returns:
        list: a list of open dates & times
    """

    d = dt.datetime.now().date()
    tomorrow = dt.datetime(d.year, d.month, d.day, 0) + dt.timedelta(days=1)
    open_slots = []
    for days in range(days):
        for hours in allowed_hours:
            if (tomorrow+dt.timedelta(days=days)+
                    dt.timedelta(hours=hours)).isoformat() not in event_times:
                open_slots.append(
                    (tomorrow+dt.timedelta(days=days)+
                    dt.timedelta(hours=hours)))

            if (tomorrow+dt.timedelta(days=days)+
                    dt.timedelta(hours=hours,minutes=30)).isoformat() not in event_times:
                open_slots.append(
                    (tomorrow+dt.timedelta(days=days)+
                        dt.timedelta(hours=hours,minutes=30)))

    return open_slots


def can_add_event(events: list, day: int, month: int, year: int,
                    hour:int, mins: int, secs: int, days=7):
    d = dt.datetime(year, month, day, hour, mins, secs)
    if d not in get_open_times(get_event_times(events),days=days):
        return False
    return True






if __name__ == '__main__':
    pass