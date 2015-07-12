import yahoo_api
import yaml
import mandrill
from time import gmtime, strftime
import json
import functions
import daily_stats
import pandas as pd
from datetime import date
import resources

#read in credentials
with open("credentials.yml", 'r') as ymlfile:
    creds = yaml.load(ymlfile)

#read the consumer key and secret from yaml
key = creds['consumer_key']
secret = creds['consumer_secret']

y = yahoo_api.YahooAPI(
    consumer_key=creds['consumer_key'],
    consumer_secret=creds['consumer_secret'],
    access_token=creds['access_token'],
    access_token_secret=creds['access_token_secret'],
    session_handle=creds['session_handle']
)

stat_df = pd.DataFrame()

for i in resources.hpk_teams_cur:
    yesterday = date.fromordinal(date.today().toordinal()-1)
    r = functions.make_daily_stats_req(i, yesterday)
    raw = y.api_query(r)
    df = functions.process_team_stats(raw)
    stat_df = stat_df.append(df)


foo = y.request('http://fantasysports.yahooapis.com/fantasy/v2/league/346.l.49099/standings')
print foo.content
foo = y.request('http://fantasysports.yahooapis.com/fantasy/v2/league/346.l.49099/standings;date=2015-05-01')
print foo.content

foo = y.api_query('http://fantasysports.yahooapis.com/fantasy/v2/league/346.l.49099/settings')
print json.dumps(
    foo['fantasy_content']['league']['settings']['stat_categories']['stats'],
    sort_keys=True, indent=2
)


#send receipt email to ALM
mandrill_client = mandrill.Mandrill(creds['mandrill_key'])
message = {
    'from_email': 'standings-bot@hpkdiaspora.com',
    'from_name': 'hpk standings bot',
    'subject': 'stats update',
    'text': 'testing, testing, time is: ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()),
    'to': [
        {'email': 'almartin@gmail.com',
         'name': 'Andrew Martin',
         'type': 'to'}]
}
result = mandrill_client.messages.send(message=message)