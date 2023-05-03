from user import authentication
import shutil

def login(events: object) -> str:
    """Asks the user for username and password in order to log them in as the current user
    creating a user data file if it cannot be found

    Returns:
        str: the username on successful login or an empty string otherwise
    """

    user_creds = None
    name = input("Enter your username (e.g. jdoe021): ")    
    user_creds, msg = authentication.auth_login(name,events)
    if not user_creds:
        user_creds = authentication.create_user(name,events)
        if user_creds:
            msg = "User creation successful"
    if user_creds:
        shutil.copyfile(f'.data/{name}.pickle', '.data/user.pickle')
    return  msg
