import unittest
from commands import details_command
from test_base import captured_output,captured_io
from io import StringIO
import os
import datetime

events = [{
  'summary': 'Code Clinic by test1.',
  'id':'available slots should appear',
  'description': 'Volunteer available',
  'start': {"dateTime": '2022-02-18T16:30:00+02:00'},
  'end':{"dateTime": '2022-02-18T16:30:00+02:00'},
  'attendees': [
      {
          "email": f"test1@student.wethinkcode.co.za"
      }
  ]
},
{
  'summary': 'Code Clinic by test2.',
  'id':"fully booked by others shouldn't appear",
  'description': 'Help with life',
  'start': {"dateTime": '2022-02-18T16:30:00+02:00'},
  'end':{"dateTime": '2022-02-18T16:30:00+02:00'},
  'attendees': [
      {
          "email": "test2@student.wethinkcode.co.za"
      },
      {
          "email": 'test1@student.wethinkcode.co.za'
      }
  ]
},
{
  'summary': 'Code Clinic by test1.',
  'id':"booked by user should appear",
  'description': 'help with docker',
  'start': {"dateTime": '2022-02-18T16:30:00+02:00'},
  'end':{"dateTime": '2022-02-18T16:30:00+02:00'},
  'attendees': [
      {
          "email": f"test1@student.wethinkcode.co.za"
      },
      {
          "email": "user@student.wethinkcode.co.za"
      },
  ]
},
{
  'summary': 'Code Clinic by user.',
  'id':"volunteer by user should appear",
  'description': 'Help with toy 5',
  'start': {"dateTime": '2022-02-18T16:30:00+02:00'},
  'end':{"dateTime": '2022-02-18T16:30:00+02:00'},
  'attendees': [
      {
          "email": f"test1@student.wethinkcode.co.za"
      },
      {
          "email": "user@student.wethinkcode.co.za"
      },
  ]
}]


class MyTestCase(unittest.TestCase):

    def test_details_info_only_provides_events_it_should(self):

        output = details_command.details_info(events, 'user')
        self.assertEqual(
'''You can access details for the following events (run the command to view details):

\tcode_clinic details available slots should appear
\tcode_clinic details booked by user should appear
\tcode_clinic details volunteer by user should appear\n''', output)


    def test_details_event_shows_info_for_available_slot(self):

        output = details_command.details_event(events, 'user', event_id='available slots should appear').strip()
        self.assertEqual(
"""Summary: Code Clinic by test1.
Start: 2022-02-18 16:30:00
End: 2022-02-18 16:30:00
Doctor: test1
Patient: ________
Status: Volunteer available""", output)

    def test_details_event_shows_info_for_user_volunteer_slots(self):

        output = details_command.details_event(events, 'user', event_id='volunteer by user should appear').strip()
        self.assertEqual(
"""Summary: Code Clinic by user.
Start: 2022-02-18 16:30:00
End: 2022-02-18 16:30:00
Doctor: user
Patient: test1
Reason for visit: Help with toy 5""", output)

    def test_details_event_shows_info_for_user_booked_slots(self):

        output = details_command.details_event(events, 'user', event_id='booked by user should appear').strip()
        self.assertEqual(
"""Summary: Code Clinic by test1.
Start: 2022-02-18 16:30:00
End: 2022-02-18 16:30:00
Doctor: test1
Patient: user
Reason for visit: help with docker""", output)

    def test_details_event_shows_no_info_for_others_booked_slots(self):

        output = details_command.details_event(events, 'user', event_id="fully booked by others shouldn't appear").strip()
        self.assertEqual("You do not have permission to view this event", output)