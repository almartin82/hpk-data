#local stuff
import yahoo_api, functions, resources

#standard
from getpass import getuser
from datetime import date, timedelta
from time import gmtime, strftime
import os

#external (remember to update requirements.txt for heroku)
import yaml
import pandas
import tinys3
import mandrill

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

d = resources.yr_2015
dd = [d[0] + timedelta(days=x) for x in range((d[1]-d[0]).days + 1)]
#dd = [d[0] + timedelta(days=x) for x in range((d[1]-d[0]).days - 90)]

stat_df = pandas.DataFrame()

for day in dd:
    print day
    for team in resources.hpk_teams_cur:
        r = functions.make_daily_stats_req(team, day)
        raw = y.api_query(r)
        df = functions.process_team_stats(raw)
        stat_df = stat_df.append(df)

#up to s3
stat_df.to_csv('hpk_2015.csv', index=False)
conn = tinys3.Connection(aws_access_key, aws_secret_access_key, tls=True)
f = open('hpk_2015.csv','rb')
conn.upload('hpk_2015.csv', f, 'hpk')

#send receipt email to ALM
mandrill_client = mandrill.Mandrill(mandrill_key)
message = {
    'from_email': 'datarobot@hpkdiaspora.com',
    'from_name': 'hpk data robot',
    'subject': 'grabbed 2015 standings successfully',
    'text': 'heroku process ran at ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()),
    'to': [
        {'email': 'almartin@gmail.com',
         'name': 'Andrew Martin',
         'type': 'to'}]
}
result = mandrill_client.messages.send(message=message)