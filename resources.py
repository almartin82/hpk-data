from datetime import date
import pandas as pd

### STATS and IDs
stat_names = pd.DataFrame(
    {'stat_id': [60, 7, 13, 16, 23, 4, 50, 28, 32, 42, 26, 27],
     'stat_name': ['AVG', 'R', 'RBI', 'SB', 'TB', 'OBP', 'IP', 'W', 'SV', 'K', 'ERA', 'WHIP']}
)

#### YAHOO TEAMS ####
#current yahoo codes
hpk_teams_cur = []

hpk_teams_2015 = [
    '346.l.49099.t.1', '346.l.49099.t.2', '346.l.49099.t.3',
    '346.l.49099.t.4', '346.l.49099.t.5', '346.l.49099.t.6',
    '346.l.49099.t.7', '346.l.49099.t.8', '346.l.49099.t.9',
    '346.l.49099.t.10', '346.l.49099.t.11', '346.l.49099.t.12']

#added eric
hpk_teams_2014 = [
    '328.l.69518.t.1', '328.l.69518.t.2', '328.l.69518.t.3',
    '328.l.69518.t.4', '328.l.69518.t.5', '328.l.69518.t.6',
    '328.l.69518.t.7', '328.l.69518.t.8', '328.l.69518.t.9',
    '328.l.69518.t.10', '328.l.69518.t.11', '328.l.69518.t.12']

hpk_teams_2013 = [
    '308.l.54481.t.1', '308.l.54481.t.2', '308.l.54481.t.3',
    '308.l.54481.t.4', '308.l.54481.t.5', '308.l.54481.t.6',
    '308.l.54481.t.7', '308.l.54481.t.8', '308.l.54481.t.9',
    '308.l.54481.t.10', '308.l.54481.t.11']

hpk_teams_2012 = [
    '268.l.14615.t.1', '268.l.14615.t.2', '268.l.14615.t.3',
    '268.l.14615.t.4', '268.l.14615.t.5', '268.l.14615.t.6',
    '268.l.14615.t.7', '268.l.14615.t.8', '268.l.14615.t.9',
    '268.l.14615.t.10', '268.l.14615.t.11']

#added mintz
hpk_teams_2011 = [
    '253.l.27468.t.1', '253.l.27468.t.2', '253.l.27468.t.3',
    '253.l.27468.t.4', '253.l.27468.t.5', '253.l.27468.t.6',
    '253.l.27468.t.7', '253.l.27468.t.8', '253.l.27468.t.9',
    '253.l.27468.t.10', '253.l.27468.t.11']

hpk_teams_2010 = [
    '238.l.432962.t.1', '238.l.432962.t.2', '238.l.432962.t.3',
    '238.l.432962.t.4', '238.l.432962.t.5', '238.l.432962.t.6',
    '238.l.432962.t.7', '238.l.432962.t.8', '238.l.432962.t.9',
    '238.l.432962.t.10']

hpk_teams_2009 = [
    '215.l.67870.t.1', '215.l.67870.t.2', '215.l.67870.t.3',
    '215.l.67870.t.4', '215.l.67870.t.5', '215.l.67870.t.6',
    '215.l.67870.t.7', '215.l.67870.t.8', '215.l.67870.t.9',
    '215.l.67870.t.10']

hpk_teams_2008 = [
    '195.l.168490.t.1', '195.l.168490.t.2', '195.l.168490.t.3',
    '195.l.168490.t.4', '195.l.168490.t.5', '195.l.168490.t.6',
    '195.l.168490.t.7', '195.l.168490.t.8', '195.l.168490.t.9',
    '195.l.168490.t.10']

hpk_teams_2007 = [
    '172.l.5643.t.1', '172.l.5643.t.2', '172.l.5643.t.3',
    '172.l.5643.t.4', '172.l.5643.t.5', '172.l.5643.t.6',
    '172.l.5643.t.7', '172.l.5643.t.8', '172.l.5643.t.9',
    '172.l.5643.t.10']

#added saud
hpk_teams_2006 = [
    '147.l.72277.t.1', '147.l.72277.t.2', '147.l.72277.t.3',
    '147.l.72277.t.4', '147.l.72277.t.5', '147.l.72277.t.6',
    '147.l.72277.t.7', '147.l.72277.t.8', '147.l.72277.t.9',
    '147.l.72277.t.10']

hpk_teams_2005 = [
    '113.l.58563.t.1', '113.l.58563.t.2', '113.l.58563.t.3',
    '113.l.58563.t.4', '113.l.58563.t.5', '113.l.58563.t.6',
    '113.l.58563.t.7', '113.l.58563.t.8', '113.l.58563.t.9']

all_hpk_teams = hpk_teams_cur + hpk_teams_2014 + hpk_teams_2013 + hpk_teams_2012 + hpk_teams_2011 + hpk_teams_2010 + hpk_teams_2009 + hpk_teams_2008 + hpk_teams_2007 + hpk_teams_2006 + hpk_teams_2005

#### START/END YEARS ####
yr_2015 = [date(2015, 4, 05), date.today()]
yr_2014 = [date(2014, 3, 22), date(2014, 9, 28)]
yr_2013 = [date(2013, 4, 01), date(2013, 9, 29)]
yr_2012 = [date(2012, 3, 28), date(2012, 10, 3)]

#### LEAGUE INFO ####
all_leagues = [
    # #2016 (no league yet)
    # {'gameid': 357, 'leagueid': 00000},
    #2015
    {'gameid': 346, 'leagueid': 49099},
    #2014
    {'gameid': 328, 'leagueid': 69518},
    #2013
    {'gameid': 308, 'leagueid': 54481},
    #2012
    {'gameid': 268, 'leagueid': 14615},
    #2011
    {'gameid': 253, 'leagueid': 27468},
    #2010
    {'gameid': 238, 'leagueid': 432962},
    #2009
    {'gameid': 215, 'leagueid': 67870},
    #2008
    {'gameid': 195, 'leagueid': 168490},
    #2007 (we were 'pro' this year
    {'gameid': 172, 'leagueid': 5643},
    #2006
    {'gameid': 147, 'leagueid': 72277},
    #2005
    {'gameid': 113, 'leagueid': 58563}
]