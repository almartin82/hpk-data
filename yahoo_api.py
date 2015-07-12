import rauth
from rauth.utils import parse_utf8_qsl
import time
import xmltodict

#adapted from https://github.com/dkempiners/python-yahooapi/blob/master/yahooapi.py
#thank you darren!
class YahooAPI:
    # access token lifetime in seconds
    access_token_lifetime = 3600

    # one request every X seconds to try to prevent 999 error codes
    request_period = 2

    def __init__(self, consumer_key, consumer_secret, access_token=None,
                 access_token_secret=None, session_handle=None):

        self.saved_token = None

        if all(x is not None for x in (access_token, access_token_secret, session_handle)):
            self.saved_token = {
                "access_token": access_token,
                "access_token_secret": access_token_secret,
                "session_handle": session_handle
            }

        self.oauth = rauth.OAuth1Service(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            name="yahoo",
            request_token_url="https://api.login.yahoo.com/oauth/v2/get_request_token",
            access_token_url="https://api.login.yahoo.com/oauth/v2/get_token",
            authorize_url="https://api.login.yahoo.com/oauth/v2/request_auth",
            base_url="http://fantasysports.yahooapis.com/")

        self.last_request = time.time()

        if (self.saved_token is not None and
                self.saved_token["access_token"] and
                self.saved_token["access_token_secret"] and
                self.saved_token["session_handle"]):
            # refresh access token, it may not have expired yet but refresh anyway
            self.refresh_access_token()

        else:
            request_token, request_token_secret = \
                self.oauth.get_request_token(params={"oauth_callback": "oob"})

            authorize_url = self.oauth.get_authorize_url(request_token)

            print "Sign in here: " + str(authorize_url)
            verification_code = raw_input("Enter code: ")

            self.access_token_time = time.time()

            raw_access = self.oauth.get_raw_access_token(
                request_token, request_token_secret,
                params={"oauth_verifier": verification_code})

            parsed_access_token = parse_utf8_qsl(raw_access.content)

            self.saved_token = {
                "access_token": parsed_access_token["oauth_token"],
                "access_token_secret": parsed_access_token["oauth_token_secret"],
                "session_handle": parsed_access_token["oauth_session_handle"]
            }

            print self.saved_token

            self.session = self.oauth.get_session(
                (self.saved_token["access_token"],
                 self.saved_token["access_token_secret"])
            )

    def refresh_access_token(self):
        self.access_token_time = time.time()

        (access_token, access_token_secret) = self.oauth.get_access_token(
            self.saved_token["access_token"],
            self.saved_token["access_token_secret"],
            params={"oauth_session_handle": self.saved_token["session_handle"]}
        )

        self.session = self.oauth.get_session(
            (access_token, access_token_secret))

    def request(self, request_str):
        now = time.time()
        tdiff = max(0, now - self.last_request)
        if 0 <= tdiff < self.request_period:
            time.sleep(self.request_period - tdiff)

        now = time.time()
        self.last_request = now

        # check if our access token has expired
        tdiff = max(0, now - self.access_token_time)

        # refresh 60 seconds before it expires
        if tdiff > self.access_token_lifetime - 60:
            self.refresh_access_token()

        return self.session.get(request_str)

    def api_query(self, request_str):
        resp = self.request(request_str)
        if resp.status_code == 999:
            raise Exception("got a 999 response; exceeded yahoo's rate limit.")
        return xmltodict.parse(resp.content)

