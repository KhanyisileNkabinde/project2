from API import connection


def volunteer_info(events: list):
    """Checks all events and finds all slots that can be created

    Args:
        events (list): list of all events

    Returns:
        str: a message of all the available volunteer slots"""

    slots = connection.get_open_times(connection.get_event_times(events))
    if slots:
        msg = 'There are some available slots that can be created.\n'
    else:
        msg = 'Unfortunately there are no available slots at the moment.\n'
    for num,slot in enumerate(slots):
        msg += slot.isoformat().replace('T', ' ') + (
            '\n' if not (num+1)%5 or num+1 ==len(slots) else '\t')
    msg += 'To book a slot please run the following command:\ncode_clinic volunteer [YYYY/MM/DD hh:mm:ss]'
    return msg


def volunteer(calendar: object,events: list,user: str,args: list) -> str:
    """Attempts to create a slot at the given date & time

    Args:
        calendar(object): the google calendar API service
        events(list): a list of all events
        user(str): the current active user
        args(list): a list of the date and time to book
    
    Returns:
        str: a message on the outcome of the attempt to create a slot"""

    try:
        year,month,day = (int(x) for x in args[0].split('-'))
        hour,mins,secs = (int (x) for x in args[1].split(':'))
        if connection.can_add_event(events,day,month,year,hour,mins,secs):
            succ, msg=connection.insert_events(calendar, user, day, month, year, hour, mins, secs)
            if succ:
                msg +=("\nSlot successfully created.")
            else:
                msg = "Something went wrong on the server\n"+msg
            return msg
        else:
            return("Sorry that slot cannot be created.")
    except ValueError as err:
        print(err)
        return ("Please ensure that you enter all values correctly "
            "(all dates and times should be digits without any surrounding brackets)")

