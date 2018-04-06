from json.decoder import JSONDecodeError
from time import sleep

import requests


class Pocket:
    URLS = {
        'request_token': 'https://getpocket.com/v3/oauth/request',
        'convert_token': 'https://getpocket.com/v3/oauth/authorize',
        'add_single': 'https://getpocket.com/v3/add',
        'modify': 'https://getpocket.com/v3/send',
    }
    HEADERS = {'X-Accept': 'application/json'}
    REDIRECT = 'https://gist.github.com/jarhill0/19bf65f4b455c0c6e70a8ff64c741216'

    def __init__(self, consumer_key, *, redirect_uri=None):
        self.consumer_key = consumer_key
        self.redirect_uri = redirect_uri or Pocket.REDIRECT

    def authenticate_user(self):
        """Authenticate and initialize a user with Pocket."""
        code = self.start_authentication()
        input('Press enter to continue when instructed.')
        access_token = self.resume_authentication(code)
        return Pocket.AuthenticatedUser(self, access_token)

    def get_auth_url(self, code):
        """Format a URL for web-based authentication."""
        return ('https://getpocket.com/auth/authorize?request_token'
                '={code}&redirect_uri={redirect_uri}').format(
            code=code,
            redirect_uri=self.redirect_uri)

    def post(self, url_name, data=None):
        """Make a request to Pocket."""
        url = Pocket.URLS[url_name]
        if data is None:
            data = {'consumer_key': self.consumer_key}
        else:
            data['consumer_key'] = self.consumer_key

        def _try_five_times():
            for _ in range(5):
                try:
                    resp = requests.post(url, data=data, headers=Pocket.HEADERS)
                except requests.RequestException:
                    sleep(0.1)
                else:
                    break

            resp.raise_for_status()
            return resp

        response = _try_five_times()
        try:
            return response.json()
        except JSONDecodeError:
            return response.content

    def resume_authentication(self, code):
        """Finish the authentication process."""
        response = self.post('convert_token', data={'code': code})
        return response['access_token']

    def start_authentication(self):
        """Initialize the authentication process."""
        code = self.post('request_token',
                         data={'redirect_uri': self.redirect_uri})['code']

        print('Please authenticate online at the following url:')
        print(self.get_auth_url(code))
        return code

    def user(self, access_token):
        """Make a user from a known access token."""
        return Pocket.AuthenticatedUser(self, access_token)

    class AuthenticatedUser:
        def __init__(self, pocket, access_token):
            self.access_token = access_token
            self.pocket = pocket
            self.consumer_key = self.pocket.consumer_key

        def add(self, url, *, title=None, tags=None, tweet_id=None):
            """Add a single URL to this user's Pocket."""
            data = {'url': url}
            if title:
                data['title'] = title
            if tags:
                data['tags'] = tags
            if tweet_id:
                data['tweet_id'] = tweet_id

            return self.post('add_single', data=data)

        def post(self, url_name, data=None):
            if data is None:
                data = {'access_token': self.access_token}
            else:
                data['access_token'] = self.access_token
            return self.pocket.post(url_name, data=data)
