import unittest
import datetime
from API import connection
from commands import volunteer_command


class MyTestCase(unittest.TestCase):

    def test_book_volunteer_date_too_far_ahead(self):
        volunteer_command.connection.insert_events = lambda *a : (True, 'Event Created.')
        calendar = connection.build_calendar()
        events = []
        user = 'test'
        args = [(datetime.datetime.now() + datetime.timedelta(days=365)).isoformat()[:10],'10:00:00']
        self.assertEqual('Sorry that slot cannot be created.',volunteer_command.volunteer(calendar, events, user, args))


    def test_book_volunteer_date_in_past(self):
        volunteer_command.connection.insert_events = lambda *a : (True, 'Event Created.')
        calendar = connection.build_calendar()
        events = []
        user = 'test'
        args = [(datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()[:10],'10:00:00']
        self.assertEqual('Sorry that slot cannot be created.',volunteer_command.volunteer(calendar, events, user, args))


    def test_book_volunteer_date_already_booked(self):
        volunteer_command.connection.insert_events = lambda *a : (True, 'Event Created.')
        calendar = connection.build_calendar()
        event_time = (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()[:11]+'10:00:00'
        events = [
            {
                'start':{'dateTime': event_time}
            }
        ]
        user = 'test'
        args = [(datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()[:10],'10:00:00']
        self.assertEqual('Sorry that slot cannot be created.',volunteer_command.volunteer(calendar, events, user, args))

    def test_book_volunteer_success(self):
        volunteer_command.connection.insert_events = lambda *a : (True, 'Event Created.')
        calendar = connection.build_calendar()
        events = []
        user = 'test'
        args = [(datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()[:10],'10:00:00']
        self.assertEqual('Event Created.\nSlot successfully created.',volunteer_command.volunteer(calendar, events, user, args))


if __name__ == '__main__':
    unittest.main()