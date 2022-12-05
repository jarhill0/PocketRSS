from .config import consumer_key
from .feeds import get_new_items
from .pocket import Pocket
from .util import get_access_token, set_access_token


def main():
    """Perform the RSS-saving actions."""
    pocket = Pocket(consumer_key)

    token = get_access_token()
    if token:
        user = pocket.user(token)
    else:
        print("User token not saved. Authentication necessary.")
        user = pocket.authenticate_user()
        print("Successfully authenticated, thank you.")

        set_access_token(user.access_token)

    print("Adding posts... ", end="", flush=True)
    for item in get_new_items():
        user.add(**item)
    print("Done.")
