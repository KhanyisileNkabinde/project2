
def details_info(events: list,user: list) -> str:
    """Checks all events and returns all events that the user can interact with

    Args:
        events (list): list of all events
        user (str): the currently logged in user

    Returns:
        str: a message of all the interactable event IDs"""

    msg = 'You can access details for the following events (run the command to view details):\n'
    events = [event for event in events if user in event['summary'] or 
        f'{user}@student.wethinkcode.co.za' in (x['email'] for x in event['attendees'])
        or len(event['attendees']) ==1]
    for event in events:
        msg += f'\n\tcode_clinic details {event["id"]}'
    if events:
        return msg+'\n'
    return 'There are no events that you can access details for.'



def details_event(events: list,user: str,event_id: str):
    """Attempts to find details for the specified event

    Args:
        events(list): a list of all events
        event_id(str): the id of the event to find details for
        user(str): the current active user
    
    Returns:
        str: a message on the details of the event"""

    event = [event for event in events if event['id'] == event_id]
    try:
        event = event[0]
    except:
        return f'Could not find event with id: {event_id}'
    access_allowed = False
    attendees = [x['email'][:-26] for x in event['attendees']]
    ev_det = {
        "Summary": event["summary"],
        "Start": event["start"]["dateTime"][:-6].replace('T',' '),
        "End": event["end"]["dateTime"][:-6].replace('T',' '),
        "Doctor": event["summary"][15:-1],
        "Patient": '________',}
    if len(attendees) == 1:
        ev_det['Status'] = event["description"]
        access_allowed = True
    elif user in attendees:
        ev_det["Patient"] = [x for x in attendees if x not in event['summary']][0]
        ev_det["Reason for visit"] = event["description"]
        access_allowed = True
    if access_allowed:
        to_ret = '\n'
        for key,value in ev_det.items():
            to_ret += f"{key}: {value}\n"
    else:
        to_ret = '\nYou do not have permission to view this event'
    return to_ret


