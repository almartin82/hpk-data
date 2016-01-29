from __future__ import print_function

#local stuff
import yahoo_api, functions, resources

#standard
from getpass import getuser
from datetime import date, timedelta
from time import gmtime, strftime
from getpass import getuser
import os

#external (remember to update requirements.txt for heroku)
import yaml
import pandas
import tinys3
import mandrill

#heroku or local
if getuser() == 'almartin':
    #local == yaml
    with open("credentials.yml", 'r') as ymlfile:
        creds = yaml.load(ymlfile)
    key = creds['consumer_key']
    secret = creds['consumer_secret']
    access_token = creds['access_token']
    access_token_secret = creds['access_token_secret']
    session_handle = creds['session_handle']
    aws_access_key = creds['aws_access_key']
    aws_secret_access_key = creds['aws_secret_access_key']
    mandrill_key = creds['mandrill_key']
else:
    #remote == os.environ
    key = os.environ['consumer_key']
    secret = os.environ['consumer_secret']
    access_token = os.environ['access_token']
    access_token_secret = os.environ['access_token_secret']
    session_handle = os.environ['session_handle']
    aws_access_key = os.environ['aws_access_key']
    aws_secret_access_key = os.environ['aws_secret_access_key']
    mandrill_key = os.environ['mandrill_key']

#initialize a yahoo session
y = yahoo_api.YahooAPI(
    consumer_key=key,
    consumer_secret=secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    session_handle=session_handle
)

for i in resources.all_leagues:
    print(i)
    r = functions.make_standings_req(i['gameid'], i['leagueid'])
    print(r)
    raw = y.api_query(r)