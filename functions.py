import pandas as pd
import resources
import os
from collections import OrderedDict
import unicodecsv


def make_standings_req(gameid, leagueid):
    base = "http://fantasysports.yahooapis.com/fantasy/v2/league/"
    sub_resource = "/standings"
    final = base + str(gameid) + '.l.' + str(leagueid) + sub_resource
    return final


def make_daily_team_stats_req(team, date):
    base = "http://fantasysports.yahooapis.com/fantasy/v2/team/"
    sub_resource = "/stats;type=date;date="
    final = base + team + sub_resource + str(date)
    return final


def make_daily_roster_request(team, date):
    base = "http://fantasysports.yahooapis.com/fantasy/v2/team/"
    sub_resource = "/roster;date="
    final = base + team + sub_resource + str(date)
    return final


def make_daily_player_stats_request(player_key, date):
    base = "http://fantasysports.yahooapis.com/fantasy/v2/player/"
    sub_resource = "/stats;type=date;date="
    final = base + player_key + sub_resource + str(date)
    return final


def make_owner_details_req(team_key):
    base = "http://fantasysports.yahooapis.com/fantasy/v2/team/"
    final = base + team_key
    return final


def make_league_players_req(gameid, leagueid, start):
    base = 'http://fantasysports.yahooapis.com/fantasy/v2/league/'
    game_league = str(gameid) + '.l.' + str(leagueid)
    sub_resource = '/players;start=' + str(start)
    final = base + game_league + sub_resource
    return final


def process_owner_details(raw):
    owner = raw['fantasy_content']['team']
    #dont need these
    owner.pop("team_logos", None)
    owner.pop("roster_adds", None)
    owner['managers'] = process_managers(owner['managers']['manager'])
    df = pd.DataFrame.from_dict(owner)
    return df


def process_managers(managers):
    #if dict
    if isinstance(managers, dict):
        manager = managers['nickname']
        return manager
    #if list
    manager = []
    for i in managers:
        manager.append(i['nickname'])
    manager = ', '.join(manager)
    return manager


def process_team_stats(raw):
    #grab the stat part of the dict
    stats = raw['fantasy_content']['team']['team_stats']['stats']['stat']
    #convert to df
    df = pd.DataFrame.from_dict(stats)
    df['date'] = raw['fantasy_content']['team']['team_stats']['date']
    df['team_key'] = raw['fantasy_content']['team']['team_key']

    #managers can sometimes have co-managers.  collapse.
    managers = process_managers(raw['fantasy_content']['team']['managers']['manager'])
    df['manager'] = managers
    df['team_name'] = raw['fantasy_content']['team']['name']
    #convert the stat id to stat name
    df = pd.concat([df, resources.stat_names], axis=1, join='inner')
    return df


def process_team_rosters(raw):
    #grab the player part of the dict
    players = raw['fantasy_content']['team']['roster']['players']
    #on days with no games (eg first day of season) there wont be any players
    if players is None:
        return pd.DataFrame()

    players = players['player']
    #convert to df
    df = pd.DataFrame.from_dict(players)

    #lots o processing here
    df.drop(['editorial_player_key',
           'editorial_team_full_name', 'editorial_team_key',
           'has_player_notes', 'has_recent_player_notes', 'headshot',
           'uniform_number'], axis=1, inplace=True)

    if 'batting_order' in df.keys():
        df.drop(['batting_order'], axis=1, inplace=True)
    if 'starting_status' in df.keys():
        df.drop(['starting_status'], axis=1, inplace=True)

    df['team_key'] = raw['fantasy_content']['team']['team_key']
    df['team_name'] = raw['fantasy_content']['team']['name']

    df['date'] = [d.get('date') for d in df.selected_position]
    df['eligible'] = [d.get('position') for d in df.eligible_positions]
    df['played'] = [d.get('position') for d in df.selected_position]

    df['fullname'] = [d.get('full') for d in df.name]
    df['firstname'] = [d.get('first') for d in df.name]
    df['lastname'] = [d.get('last') for d in df.name]

    df.drop(['selected_position', 'eligible_positions', 'name'], axis=1, inplace=True)

    return df


def process_league_players(raw):
    player_list = raw['fantasy_content']['league']['players']
    #if we've gone too high player_list will be None
    if player_list is None:
        print('empty')
        return []

    #seeing some weird errors.  print the content if it's not a dict
    if not isinstance(player_list, dict):
        print('LOOK HERE')
        print(player_list)

    player_list = player_list['player']
    out = [d.get('player_key') for d in player_list]

    return out


def process_player_stats(raw):
    #grab the player stats of the dict
    player_stats = raw['fantasy_content']['player']['player_stats']
    if player_stats is None:
        return

    player_stats = player_stats['stats']['stat']
    df = pd.DataFrame(player_stats)
    df['player_key'] = raw['fantasy_content']['player']['player_key']
    df['date'] = raw['fantasy_content']['player']['player_stats']['date']

    return df


def process_standings(raw):
    stats = raw['fantasy_content']['league']['standings']['teams']['team']
    return stats


def process_one_standing_team(team):
    stat_dict = team['team_stats']['stats']['stat']
    df = pd.DataFrame.from_dict(stat_dict)
    #convert the stat id to stat name
    df = pd.concat([df, resources.stat_names], axis=1, join='inner')
    df['team_key'] = team['team_key']
    df['manager'] = process_managers(team['managers']['manager'])
    df['team_name'] = team['name']
    return df


def data_to_csv(target_dir, data_to_write, desired_name):
    """Convenience function to write a dict to CSV with appropriate parameters."""
    #generate directory if doesn't exist
    global d
    if len(data_to_write) == 0:
        return None
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if type(data_to_write) == dict:
        #order dict by keys
        d = OrderedDict(sorted(data_to_write.items()))
        keys = d.keys()
    if type(data_to_write) == list:
        d = data_to_write
        keys = data_to_write[0].keys()
    with open("%s/%s.csv" % (target_dir, desired_name), 'wb') as f:
        dw = unicodecsv.DictWriter(f, keys, dialect='ALM')
        dw.writeheader()
        if type(data_to_write) == dict:
            dw.writerow(d)
        if type(data_to_write) == list:
            dw.writerows(d)
    f.close()
