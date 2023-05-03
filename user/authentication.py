import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass
import datetime
import pickle


def auth_login(name: str, events: list) -> bool:
    """Attempts to find user data for supplied and if successful will ask for a
    password to sign in with, returns false on a failed sign in for any reason

    Args:
        name (str): The username to log in as.

    Returns:
        bool: whether the login was successful
    """

    try:
        with open(f'.data/{name}.pickle','rb') as fn:
            name,salt,pass_key,token,own_events=pickle.load(fn)
    except FileNotFoundError as err:
        return False, (f"Could not find user data for {name}")
    password = bytes(getpass.getpass('Password: '),'utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length= 32,
        salt= salt, 
        iterations=390000)
    try:
        kdf.verify(password, pass_key)
        token = datetime.datetime.now() + datetime.timedelta(hours=4)
        own_events = user_events(name, events)

        with open(f'.data/{name}.pickle','wb') as fn:
            pickle.dump([name,salt,pass_key,token,own_events], fn)
        return True, "Login Successful."
    except:
        return False, "Could not verify password"


def user_events(user, events):
    own_events = []
    for event in events:
        for attendee in event['attendees']:
            if user in attendee:
                own_events.append(event)
                break
    return own_events



def verify_token(user: str) -> str:
    """Attempts to find the specified user data file and verify the token within

    Args:
        user(str): The file name of the user.pickle file

    Returns:
        str: The name of the associated token on success or an empty string if unable to validate
    """

    try:
        with open(f'.data/{user}.pickle','rb') as fn:
            name,salt,pass_key,token,events = pickle.load(fn)
        if datetime.datetime.now() > token:
            return ''
        return name
    except FileNotFoundError as err:
        return ''
        



def create_user(name: str, events) -> bool:
    """Attempts to create a user data file with the supplied username

    Args:
        name (str): the username to create a data file for

    Returns
        bool: Whether the user creation was successful
    """

    if os.path.exists(f'.data/{name}.pickle'):
        return False
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length= 32,
            salt= salt,
            iterations=390000)
    password = bytes(getpass.getpass('Password: '),'utf-8')
    pass_key = kdf.derive(password)
    token = datetime.datetime.now() + datetime.timedelta(hours=4)
    own_events = user_events(name, events)
    with open(f'.data/{name}.pickle','wb') as fn:
        pickle.dump([name,salt,pass_key,token,own_events], fn)
    return True


if __name__ == '__main__':
    #TODO
    pass