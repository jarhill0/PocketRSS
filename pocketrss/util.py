from json import dump, load
from os import path


def get_feeds():
    """Get the list of subscribed feeds."""
    try:
        with open(get_file("data", "feeds.txt")) as feeds:
            return [item.strip() for item in feeds.read().split("\n") if item]
    except FileNotFoundError:
        return []


def get_file(*args):
    """Get a file within this project."""
    return path.join(get_folder_path(), *args)


def get_folder_path():
    """Return the path of this project."""
    return path.dirname(path.abspath(__file__))


def get_recent_posts():
    """Load the most recent post from each feed, as a dict."""
    try:
        with open(get_file("data", "posts.json")) as posts:
            return load(posts)
    except (IOError, ValueError):
        return dict()


def get_access_token():
    """Get the saved access token."""
    try:
        with open(get_file("data", "access_token.txt")) as token:
            return token.read().strip()
    except FileNotFoundError:
        return ""


def set_access_token(token):
    """Set the access token."""
    with open(get_file("data", "access_token.txt"), "w") as token_f:
        token_f.write(token)


def update_recent_posts(updated_items):
    """Update the dict of most recent posts from each feed."""
    saved_items = get_recent_posts()
    saved_items.update(updated_items)
    with open(get_file("data", "posts.json"), "w") as posts:
        dump(saved_items, posts)
