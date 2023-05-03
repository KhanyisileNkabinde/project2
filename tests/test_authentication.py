import unittest
from user import authentication
from test_base import captured_output,captured_io
from io import StringIO
import os
import pickle
import datetime


class MyTestCase(unittest.TestCase):

    def test_user_creation_and_validation_process(self):
        if os.path.exists('.data/test.pickle'):
            os.remove('.data/test.pickle')

        authentication.getpass.getpass = lambda a: 'right_pass'
        self.assertFalse(authentication.auth_login('test',[])[0],'Login of nonexisting user should return False')
        self.assertFalse(authentication.verify_token('test'),'Verification of token that does not exist should return False')


        authentication.getpass.getpass = lambda a: 'right_pass'
        self.assertTrue(authentication.create_user('test',[]),'Successful creation of a user should return True')
        self.assertTrue(authentication.verify_token('test'),'Verification of a newly created token should return True')
        self.assertTrue(authentication.auth_login('test',[])[0],'Successful login of a user should return True')

        authentication.getpass.getpass = lambda a: 'wrong_pass'
        self.assertFalse(authentication.auth_login('test',[])[0],'Unsuccessful login of a user because of wrong password should return False')
        self.assertFalse(authentication.create_user('test',[]),'Attempting to create an already existing user should return False')

        if os.path.exists('.data/test.pickle'):
            os.remove('.data/test.pickle')


    def test_token_expire_after_4_hours(self):
        if os.path.exists('.data/test.pickle'):
            os.remove('.data/test.pickle')

        authentication.getpass.getpass = lambda a: 'right_pass'
        with captured_io(StringIO('right_pass')) as (out, err):
            authentication.create_user('test',[])
        with open('.data/test.pickle','rb') as f:
            name,salt,pass_key,token,own_events=pickle.load(f)
            token = datetime.datetime.now() - datetime.timedelta(hours=4)
        with open('.data/test.pickle','wb') as f:
            pickle.dump([name,salt,pass_key,token,own_events], f)
        self.assertFalse(authentication.verify_token('test'),"Token should expire after 4 hours")
        if os.path.exists('.data/test.pickle'):
            os.remove('.data/test.pickle')



if __name__ == '__main__':
    unittest.main()
