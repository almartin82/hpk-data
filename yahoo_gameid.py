#local stuff
import yahoo_api, functions

import yaml

with open("credentials.yml", 'r') as ymlfile:
    creds = yaml.load(ymlfile)
key = creds['consumer_key']
secret = creds['consumer_secret']
access_token = creds['access_token']
access_token_secret = creds['access_token_secret']
session_handle = creds['session_handle']

y = yahoo_api.YahooAPI(
    consumer_key=key,
    consumer_secret=secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    session_handle=session_handle
)

mlb_url = 'http://fantasysports.yahooapis.com/fantasy/v2/game/mlb'
raw = y.api_query(mlb_url)
print raw