import icalendar as ical
import datetime


def export_ical(events: list):
    """Converts a list of events into a usable .ical file

    Args:
        events(list): a list of events to convert"""

    cal = ical.Calendar()
    for event in events:
        iEvent = ical.Event()
        summary = event['summary']
        description = event['description']
        start = event['start']['dateTime']
        date,time = start.split('T')
        y,mo,d = (int(x) for x in date.split('-'))
        time,zone = time.split('+')
        h,mi,s = (int(x) for x in time.split(':'))
        start = datetime.datetime(y,mo,d,h,mi,s)
        end = event['end']['dateTime']
        date,time = end.split('T')
        y,mo,d = (int(x) for x in date.split('-'))
        time,zone = time.split('+')
        h,mi,s = (int(x) for x in time.split(':'))
        end = datetime.datetime(y,mo,d,h,mi,s)

        organizer = summary[15:-1]
        attendee = [x['email'] for x in event['attendees'] if 
                    x['email'] !=f'{organizer}@student.wethinkcode.co.za']
        attendee = attendee[0] if attendee else ''
        iEvent.add('summary', summary)
        iEvent.add('dtstart',start)
        iEvent.add('dtend',end)
        organizer = ical.vCalAddress(f'MAILTO:{organizer}@student.wethinkcode.co.za')
        organizer.params['ROLE'] = ical.vText('DOCTOR')
        iEvent['organizer']=organizer
        iEvent['uid']=event['id']
        if attendee:
            attendee = ical.vCalAddress(f'MAILTO:{attendee}')
            attendee.params['ROLE'] = ical.vText('PATIENT')
            iEvent.add('attendee',attendee,encode=0)
        cal.add_component(iEvent)
    with open('.data/code_clinics.ical','wb') as f:
        f.write(cal.to_ical())


