#my stuff
import yahoo_api, functions, resources

#standard
from getpass import getuser
from datetime import date, timedelta
import os

#external (remember to update requirements.txt for heroku)
import yaml
import pandas

#heroku or local
if getuser() == 'amartin':
    #local == yaml
    with open("credentials.yml", 'r') as ymlfile:
        creds = yaml.load(ymlfile)
    key = creds['consumer_key']
    secret = creds['consumer_secret']
    access_token = creds['access_token']
    access_token_secret = creds['access_token_secret']
    session_handle = creds['session_handle']
else:
    #remote == os.environ
    key = os.environ['consumer_key']
    secret = os.environ['consumer_secret']
    access_token = os.environ['access_token']
    access_token_secret = os.environ['access_token_secret']
    session_handle = os.environ['session_handle']

#initialize a yahoo session
y = yahoo_api.YahooAPI(
    consumer_key=key,
    consumer_secret=secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    session_handle=session_handle
)

d = resources.yr_2015
#dd = [d[0] + timedelta(days=x) for x in range((d[1]-d[0]).days + 1)]
dd = [d[0] + timedelta(days=x) for x in range((d[1]-d[0]).days - 75)]

stat_df = pandas.DataFrame()

for day in dd:
    print day
    for team in resources.hpk_teams_cur:
        r = functions.make_daily_stats_req(team, day)
        raw = y.api_query(r)
        df = functions.process_team_stats(raw)
        stat_df = stat_df.append(df)

print stat_df
