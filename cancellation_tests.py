import unittest
from API import quickstart
from test_base import captured_output,captured_io
from io import StringIO
import sys
from test_base import run_unittests




class MyTestCase(unittest.TestCase):

    def test_cancel_info_no_events(self):
        with captured_output() as (out, err): # for testing print outputs
            events = []
            user = 'test'
            quickstart.cancel_info(events,user)

        output = out.getvalue().strip()
        expected_output = "There is nothing for you to cancel (You can only cancel your own booking/volunteer slots)"
        self.assertEqual(output, expected_output)

    def test_cancel_event_test_cancel_volunteer_unsuccessful(self):
        with captured_output() as (out, err): # for testing print outputs
            events= [{'id':'test_id','description':'code clinic with test','attendees':[{'email':'test@student.wethinkcode.co.za'}]}]
            calendar = quickstart.build_calendar()
            event_id='test_id'
            user='test'
            quickstart.cancel_event(calendar,events,event_id,user)
        output = out.getvalue().strip()
        expected_output = 'unfortunatly something went wrong on the sever, You cannot cancelled your code clinic.'
        self.assertEqual(output,expected_output)



    def test_cancel_event_test_cancel_user_success(self):
        with captured_output() as (out, err): # for testing print outputs
            events= [{'id':'test_id','description':'code clinic with test','attendees':[{'email':'test@student.wethinkcode.co.za'}]}]
            calendar = quickstart.build_calendar()
            event_id='test_id'
            user='test'
            quickstart.cancel_event(calendar,events,event_id,user)
        output = out.getvalue().strip()
        expected_output = 'You have successfully cancelled your booking'
        self.assertEqual(output,expected_output)


    def test_cancel_event_test_cancell_user_sucess(self):
        with captured_output() as (out, err): # for testing print outputs
            events= [{'id':'test_id','description':'code clinic with test','attendees':[{'email':'test@student.wethinkcode.co.za'}]}]
            calendar = quickstart.build_calendar()
            event_id='test_id'
            user='test'
            quickstart.cancel_event(calendar,events,event_id,user)
        output = out.getvalue().strip()
        expected_output = "unfortunatly something went wrrong on sever,You can't cancel that booking."
        self.assertEqual(output,expected_output)

    def test_cancel_event_test_with_two_attendees_cancel_user_success(self):
        with captured_output() as (out, err): # for testing print outputs
            events= [{'id':'test_id','description':'code clinic with test','attendees':[{'email':'test1@student.wethinkcode.co.za'},{'email':'test2@student.wethinkcode.co.za'}]}]
            calendar = quickstart.build_calendar()
            event_id='test_id'
            user = 'test1'
            quickstart.cancel_event(calendar,events,event_id,user)
        output = out.getvalue().strip()
        expected_output = 'You have successfully cancelled your booking'
        self.assertEqual(output,expected_output)


    def test_cancel_info_no_events(self):
        with captured_output() as (out, err): # for testing print outputs
            events= [{'id':'test_id','description':'code clinic with test','attendees':[{'email':'test1@student.wethinkcode.co.za'},{'email':'test2@student.wethinkcode.co.za'},{'email':'test3@student.wethinkcode.co.za'}]}]
            calendar = quickstart.build_calendar()
            event_id='test_id'
            user = 'test3'
            quickstart.cancel_event(calendar,events,event_id,user)

        output = out.getvalue().strip()
        expected_output = "There is nothing for you to cancel (You can only cancel your own booking/volunteer slots)"
        self.assertEqual(output, expected_output)
     

if __name__ == '__main__':
    unittest.main()
