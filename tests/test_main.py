import unittest
from test_base import captured_output
from io import StringIO
from tests import test_authentication,test_booking,test_details,test_volunteer
from test_base import run_unittests


class MyTestCase(unittest.TestCase):


    def test_details_succeeds(self):
        import tests.test_details
        test_result = run_unittests("tests.test_details")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_booking_succeeds(self):
        import tests.test_booking
        test_result = run_unittests("tests.test_booking")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_volunteer_succeeds(self):
        import tests.test_volunteer
        test_result = run_unittests("tests.test_volunteer")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_authentication_succeeds(self):
        import tests.test_authentication
        test_result = run_unittests("tests.test_authentication")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_cancellation_succeeds(self):
        import tests.test_cancelling
        test_result = run_unittests("tests.test_cancelling")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")



        

if __name__ == '__main__':
    unittest.main()

