import unittest
from commands import book_command
from API import connection


class Testclass(unittest.TestCase):



   # (cannot book the slot you created)
    def test_cannot_book_event_you_created(self):
        book_command.input = lambda a: 'Testing'



        event = {

            'id': 'test1',
            'Summary': "Code clinic by pzik021.",

            'Description': "Help",
            'Start': {
                'DateTime': "2022-02-10 08:00:00",

            },
            'End': {
                'DateTime': "2022-02-10 08:30:00",

            },

            'attendees': [
                {'email': 'pzik021@student.wethinkcode.co.za'},

            ],
        }

    
        calendar = connection.build_calendar()
        events = [event]
        event_id = 'test1'
        user = 'pzik021'
        self.assertEqual('You cannot book that session', book_command.book_event(calendar, events, event_id, user))


    #(if the even ID is not there different)
    def test_book_event_wrong_id(self):
        book_command.input = lambda a: 'Testing'



        event = {

            'id': 'test1',
            'Summary': "Code clinic by pzik.",

            'Description': "Help",
            'Start': {
                'DateTime': "2022-02-10 07:00:00",

            },
            'End': {
                'DateTime': "2022-02-10 07:30:00",

            },

            'attendees': [
               
                {'email': 'ken021@student.wethinkcode.co.za'},
                {'email': 'pzik021@student.wethinkcode.co.za'},

            ],
        }

        calendar = connection.build_calendar()
        events = [event]
        event_id = 'test'
        user = 'ken021'
        self.assertEqual('Could not find the specified event, please ensure you entered the right ID', book_command.book_event(calendar, events, event_id, user))

    
    #(successful booking, still having issues)
    def test_book_event_successful_book(self):
        book_command.input = lambda a: 'Testing'



        event = {

            'id': 'test1',
            'Summary': "Code clinic by pzik021.",

            'Description': "Help",
            'Start': {
                'DateTime': "2022-02-10 08:00:00",

            },
            'End': {
                'DateTime': "2022-02-10 08:30:00",

            },

            'attendees': [
                {'email': 'pzik021@student.wethinkcode.co.za'}
                

            ],
        }

    
        calendar = connection.build_calendar()
        events = [event]
        event_id = 'test1'
        user = 'yamato021'
        self.assertEqual('Something went wrong on the server.', book_command.book_event(calendar, events, event_id, user))


   
    def test_book_event_already_booked_event_fails(self):
        book_command.input = lambda a: 'Testing'



        event = {

            'id': 'test1',
            'Summary': "Code clinic by pzik.",

            'Description': "Help",
            'Start': {
                'DateTime': "2022-02-10 07:00:00",

            },
            'End': {
                'DateTime': "2022-02-10 07:30:00",

            },

            'attendees': [
               
                {'email': 'ken021@student.wethinkcode.co.za'},
                {'email': 'pzik021@student.wethinkcode.co.za'},

            ],
        }

        calendar = connection.build_calendar()
        events = [event]
        event_id = 'test1'
        user = 'lquick021'
        self.assertEqual('You cannot book that session', book_command.book_event(calendar, events, event_id, user))
    


if __name__ == '__main__':
    unittest.main()
