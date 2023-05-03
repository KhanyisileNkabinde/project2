
def do_help():
    """
    Provides help information to the user
    
    Returns:
        str - A help message detailing use of the Code Clinic program"""
    return """Inflatus Team A Code Clinic
USAGE:
    code_clinic [COMMAND] [FLAGS]

FLAGS:
    (YYYY/MM/DD hh:mm:ss) - Date & Time
    (Event ID) - Event UUID (provided by the program)

COMMANDS:
    HELP - provide information about commands
    DETAILS - Allows you to get UUIDs for all events of the next 7 days
    BOOK - Allows patients to book a code clinic slot with a docto ron the calendar
    CANCEL - Allows user to cancel a booking/volunteer slot
    VOLUNTEER - Allows Doctors to create a slot for patients to book
"""