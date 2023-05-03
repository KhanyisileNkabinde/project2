from API import connection


def cancel_info(events: list,user: str) -> str:
    """Checks all events and returns all cancellable events of the user

    Args:
        events (list): list of all events
        user (str): the currently logged in user

    Returns:
        str: a message of all the cancellable events"""

    msg = ''
    for event in events:
        if len(event['attendees']) == 1 and event['attendees'][0]['email'][:-26] == user:
            msg+=(f"\n{event['start']['dateTime'][:-6].replace('T',' ')}: {event['summary']}\n\t")
            msg+=(f"code_clinic cancel {event['id']}\n\t")
            msg+=(f"code_clinic details {event['id']}\n")
        elif len(event['attendees']) > 1 and user not in event['summary'] and (
                user in [att['email'][:-26] for att in event['attendees']]):
            msg+=(f"\n{event['start']['dateTime'][:-6].replace('T',' ')}: {event['summary']}\n\t")
            msg+=(f"code_clinic cancel {event['id']}\n\t")
            msg+=(f"code_clinic details {event['id']}\n")
    if not msg:
        return('There is nothing for you to cancel (You can only cancel your own booking/volunteer slots)')
    return(msg)


def cancel_event(calendar: object,events: list,event_id: str,user: str) -> str:
    """Attempts to cancel the given event

    Args:
        calendar(object): the google calendar API service
        events(list): a list of all events
        event_id(str): the id of the event to cancel
        user(str): the current active user
    
    Returns:
        str: a message on the outcome of the attempt to cancel"""

    event = [event for event in events if event['id'] == event_id]
    try:
        event = event[0]
    except IndexError as err:
        return (f"Could not find the event with ID: {event_id}")
    if len(event['attendees']) == 1 and event['attendees'][0]['email'][:-26] == user:
        connection.del_events(calendar, event['id'])
        return('You have successfully cancelled your code clinic.')
    elif len(event['attendees']) > 1 and user not in event['summary'] and (
            user in [att['email'][:-26] for att in event['attendees']]):
        attendees = [att for att in event['attendees'] if att['email'][:-26] != user]
        event['description'] = 'Volunteer available'
        event['attendees'] = attendees
        try:
            calendar.events().update(calendarId='primary',eventId=event['id'],body=event).execute()
            return('You have successfully cancelled your booking')
        except Exception as err:
            return(f"Something went wrong on the server: {err}")
    else:
        return("You can't cancel that booking.")
