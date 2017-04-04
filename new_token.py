import yahoo_api
import yaml

with open("credentials.yml", 'r') as ymlfile:
    creds = yaml.load(ymlfile)
key = creds['consumer_key']
secret = creds['consumer_secret']
access_token = creds['access_token']
access_token_secret = creds['access_token_secret']
session_handle = creds['session_handle']

#initialize a yahoo session
y = yahoo_api.YahooAPI(
    consumer_key=key,
    consumer_secret=secret
)

#follow the prompts and enter the auth code as a string
#eg 'randomcodexyz'