from os import path
from time import time


def get_feeds():
    """Get the list of subscribed feeds."""
    try:
        with open(get_file('data', 'feeds.txt')) as feeds:
            return [item.strip() for item in feeds.read().split('\n') if item]
    except FileNotFoundError:
        return []


def get_file(*args):
    """Get a file within this project."""
    return path.join(get_folder_path(), *args)


def get_folder_path():
    """Return the path of this project."""
    return path.dirname(path.abspath(__file__))


def get_time():
    """Get the time saved to a text file.

    Defaults to a week ago if nothing is found
    """
    try:
        with open(get_file('data', 'time.txt')) as time_file:
            try:
                return int(time_file.read().strip())
            except ValueError:
                return time() - 60 * 60 * 24 * 7
    except FileNotFoundError:
        return time() - 60 * 60 * 24 * 7


def get_access_token():
    """Get the saved access token."""
    try:
        with open(get_file('data', 'access_token.txt')) as token:
            return token.read().strip()
    except FileNotFoundError:
        return ''


def save_time():
    """Save the current time to a text file."""
    with open(get_file('data', 'time.txt'), 'w') as time_file:
        time_file.write(str(int(time())))


def set_access_token(token):
    """Set the access token."""
    with open(get_file('data', 'access_token.txt'), 'w') as token_f:
        token_f.write(token)
