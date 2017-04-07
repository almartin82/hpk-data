#local stuff
import yahoo_api, functions, resources

#standard
from getpass import getuser
from datetime import date, timedelta
from time import gmtime, strftime, sleep
from getpass import getuser
import os

#external (remember to update requirements.txt for heroku)
import yaml
import pandas
import tinys3
import mandrill
import requests

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

d = resources.yr_2017
dd = [d[0] + timedelta(days=x) for x in range((d[1]-d[0]).days + 1)]
#dd = [d[0] + timedelta(days=x) for x in range((d[1]-d[0]).days - 90)]

stat_df = pandas.DataFrame()
roster_df = pandas.DataFrame()

def request_and_process_team_totals(r, times = 0):
    raw = y.api_query(r)
    if times > 0:
        print('request and process called after failure.')
        print(raw)
    try:
        df = functions.process_team_stats(raw)
        return df
    except TypeError:
        print('processing team stats failed')
        print(Exception)
        sleep(5)
        request_and_process_team_totals(r, times = times + 1)


def request_and_process_team_rosters(r, times = 0):
    raw = y.api_query(r)

    if times > 0:
        print('request and process called after failure.')
        print(raw)
    try:
        df = functions.process_team_rosters(raw)
        return df
    except TypeError:
        print('processing team stats failed')
        print(Exception)
        sleep(5)
        request_and_process_team_rosters(r, times = times + 1)


for day in dd:
    print(day)

    for team in resources.hpk_teams_cur[0]:
        print(team)

        # rr = functions.make_daily_roster_request(team, day)
        # dfr = request_and_process_team_rosters(rr)
        # roster_df = roster_df.append(dfr)

        rt = functions.make_daily_stats_req(team, day)
        dft = request_and_process_team_totals(rt)
        stat_df = stat_df.append(dft)

#up to s3
# conn = tinys3.Connection(aws_access_key, aws_secret_access_key, tls=True)
# stat_df.to_csv('hpk_2017.csv', index=False, encoding='utf-8')
# f = open('hpk_2017.csv','rb')
# conn.upload('hpk_2017.csv', f, 'hpk')
#
# roster_df.to_csv('hpk_2017_rosters.csv', index=False, encoding='utf-8')
# fr = open('hpk_2017_rosters.csv','rb')
# conn.upload('hpk_2017_rosters.csv', fr, 'hpk')
#
# print(conn)

#send receipt email to ALM
# mandrill_client = mandrill.Mandrill(mandrill_key)
# message = {
#     'from_email': 'datarobot@hpkdiaspora.com',
#     'from_name': 'hpk data robot',
#     'subject': 'grabbed 2015 standings successfully',
#     'text': 'heroku process ran at ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()),
#     'to': [
#         {'email': 'almartin@gmail.com',
#          'name': 'Andrew Martin',
#          'type': 'to'}]
# }
# result = mandrill_client.messages.send(message=message)

#dead man's snitch
requests.get('https://nosnch.in/414bc5d315')

#beginning of year
#f = open('/Users/almartin/Downloads/all_owners.csv','rb')
#conn.upload('all_owners.csv', f, 'hpk')