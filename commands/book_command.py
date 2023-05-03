
def book_info(events: list,user: str) -> str:
    """Checks all events and returns all available slots with a doctor

    Args:
        events (list): list of all events
        user (str): the currently logged in user

    Returns:
        str: a message of all the open code clinics"""

    msg = ''
    for event in events:
        if len(event['attendees']) == 1 and event['attendees'][0]['email'][:-26] != user:
            msg+=(f"\n{event['start']['dateTime'][:-6].replace('T',' ')}: {event['summary']}\n\t")
            msg+=(f"code_clinic book {event['id']}\n\t")
            msg+=(f"code_clinic details {event['id']}\n")
    if not msg:
        return 'There are no available code clinics at the moment'
    return (msg)


def book_event(calendar: object,events: list,event_id: str,user: str) -> str:
    """Attempts to book a code clinic session as the user

    Args:
        calendar(object): the google calendar API service
        events(list): a list of all events
        event_id(str): the id of the event to book
        user(str): the current active user
    
    Returns:
        str: a message on the outcome of the attempt to book"""
        
    event = [event for event in events if event['id'] == event_id]
    try:
        event = event[0]
        if len(event['attendees']) == 1 and event['attendees'][0]['email'][:-26] != user:
            event['attendees'].append({'email':f"{user}@student.wethinkcode.co.za",'responseStatus':'accepted'})
            description = input('What would you like to get help with?: ')
            event['description'] = description
            try:
                calendar.events().update(calendarId='primary',eventId=event['id'],body=event).execute()
                return "Booking successfully created"
            except Exception as err:
                return "Something went wrong on the server."
        else:
            return("You cannot book that session")
    except IndexError as err:
        return("Could not find the specified event, please ensure you entered the right ID")
