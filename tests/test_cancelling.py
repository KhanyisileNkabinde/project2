import unittest
import datetime
from API import connection
from commands import cancel_command


class MyTestCase(unittest.TestCase):

    def test_cancel_other_volunteer_slot(self):

        events = [{

            'id': 'test1',
            'summary': "Code clinic by pzik021.",

            'description': "Volunteer available",
            'start': {
                'dateTime': "2022-02-10 08:00:00",

            },
            'end': {
                'dateTime': "2022-02-10 08:30:00",

            },

            'attendees': [
                {'email': 'pzik021@student.wethinkcode.co.za'},

            ],
        }]
        user = 'lquick021'
        calendar = connection.build_calendar()
        event_id = 'test1'
        self.assertEqual("You can't cancel that booking.", cancel_command.cancel_event(calendar, events, event_id, user))


    def test_cancel_fully_booked_by_other(self):

        events = [{

            'id': 'test1',
            'summary': "Code clinic by pzik021.",

            'description': "Volunteer available",
            'start': {
                'dateTime': "2022-02-10 08:00:00",

            },
            'end': {
                'dateTime': "2022-02-10 08:30:00",

            },

            'attendees': [
                {'email': 'pzik021@student.wethinkcode.co.za'},
                {'email': 'smagwaxa021@student.wethinkcode.co.za'}

            ],
        }]
        user = 'lquick021'
        calendar = connection.build_calendar()
        event_id = 'test1'
        self.assertEqual("You can't cancel that booking.", cancel_command.cancel_event(calendar, events, event_id, user))


    def test_cancel_no_cancel_as_volunteer_when_booked(self):

        events = [{

            'id': 'test1',
            'summary': "Code clinic by pzik021.",

            'description': "Booked",
            'start': {
                'dateTime': "2022-02-10 08:00:00",

            },
            'end': {
                'dateTime': "2022-02-10 08:30:00",

            },

            'attendees': [
                {'email': 'pzik021@student.wethinkcode.co.za'},
                {'email': 'smagwaxa021@student.wethinkcode.co.za'}

            ],
        }]
        user = 'pzik021'
        calendar = connection.build_calendar()
        event_id = 'test1'
        self.assertEqual("You can't cancel that booking.", cancel_command.cancel_event(calendar, events, event_id, user))


    def test_cancel_as_patient(self):
        

        events = [{

            'id': 'test1',
            'summary': "Code clinic by pzik021.",

            'description': "Volunteer available",
            'start': {
                'dateTime': "2022-02-10 08:00:00",

            },
            'end': {
                'dateTime': "2022-02-10 08:30:00",

            },

            'attendees': [
                {'email': 'pzik021@student.wethinkcode.co.za'},
                {'email': 'smagwaxa021@student.wethinkcode.co.za'}

            ],
        }]
        user = 'smagwaxa021'
        calendar = connection.build_calendar()
        event_id = 'test1'
        self.assertIn("Something went wrong on the server:", cancel_command.cancel_event(calendar, events, event_id, user))

    def test_cancel_as_doctor(self):
        

        events = [{

            'id': 'test1',
            'summary': "Code clinic by pzik021.",

            'description': "Volunteer available",
            'start': {
                'dateTime': "2022-02-10 08:00:00",

            },
            'end': {
                'dateTime': "2022-02-10 08:30:00",

            },

            'attendees': [
                {'email': 'pzik021@student.wethinkcode.co.za'},

            ],
        }]
        user = 'pzik021'
        calendar = connection.build_calendar()
        event_id = 'test1'
        self.assertEqual("You have successfully cancelled your code clinic.", cancel_command.cancel_event(calendar, events, event_id, user))
