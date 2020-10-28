import requests
import pandas as pd
from datetime import datetime


def get_summoner_info(summoner_name, apikey):
    # This function takes the summoner name and the API Key
    # and retrieves its account id
    url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    html = requests.get(url,
                        params={'api_key': apikey})
    json = html.json()
    df = pd.DataFrame(json, index=[0])

    return df


def get_matchlist(accountid, api, champions, queues):
    url = f'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{accountid}'
    html = requests.get(url,
                        params={'api_key': api})
    json = html.json()
    df = pd.DataFrame(json['matches'])
    df['Date'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(x/1000).strftime("%d/%m/%Y %A, %H:%M:%S"))
    df['Date2'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(x / 1000).strftime("%Y/%m/%d"))
    df = df.merge(champions, left_on='champion', right_on='champion', how='left')
    df = df.merge(queues, left_on='queue', right_on='queue', how='left')

    df.drop(['champion', 'queue'], axis=1, inplace=True)
    df.rename(columns={'name': 'champion', 'queue_type': 'queue'}, inplace=True)

    return df


def get_match_info(matchid, api):
    url = f'https://euw1.api.riotgames.com/lol/match/v4/matches/{matchid}'
    html = requests.get(url,
                        params={'api_key': api})
    json = html.json()

    return json


def get_players_info(json):
    players = pd.DataFrame()

    for participant in range(10):
        df = pd.DataFrame.from_dict(json['participants'][participant]['stats'], orient='index').T
        df.insert(loc=0, column='championId', value=json['participants'][participant]['championId'])
        df.insert(loc=1, column='teamId', value=json['participants'][participant]['teamId'])

        dff = pd.DataFrame.from_dict(json['participantIdentities'][participant]['player'], orient='index').T
        dff.insert(loc=0, column='participantId', value=json['participantIdentities'][participant]['participantId'])
        df_final = pd.merge(df, dff, on='participantId')

        players = players.append(df_final)

    players.insert(loc=0, column='gameid', value=[json['gameId'] for value in range(len(players))])

    return players


def get_match_timeline(matchid, api):
    url = f'https://euw1.api.riotgames.com/lol/match/v4/timelines/by-match/{matchid}'
    html = requests.get(url,
                        params={'api_key': api})
    json = html.json()

    return json


def participant_frames(json, playersinfo):
    ## Extracting frames from json

    all_frames = pd.DataFrame()

    for frame in list(range(len(json['frames']))):
        iterable = json['frames'][frame]['participantFrames']
        for elem in iterable:
            dic = {}
            for sub_elem in iterable[elem]:
                if type(iterable[elem][sub_elem]) == dict:
                    dic.update(iterable[elem][sub_elem])
                else:
                    dic[sub_elem] = iterable[elem][sub_elem]
            df = pd.DataFrame(dic, index=[0])
            df.insert(loc=0, column='timestamp', value=json['frames'][frame]['timestamp'])
            all_frames = all_frames.append(df, ignore_index=True)

    cols = ['timestamp', 'participantId', 'x', 'y', 'currentGold', 'totalGold', 'level',
            'xp', 'minionsKilled', 'jungleMinionsKilled',
            # 'dominionScore','teamScore',
            ]
    all_frames = all_frames[cols]

    teams = playersinfo[['participantId', 'teamId']]
    frames = pd.merge(all_frames, teams, on='participantId')
    frames = pd.merge(frames, playersinfo[['participantId', 'summonerName', 'championId']], on='participantId')
    frames['timestamp'] = (frames['timestamp'] / 60000).astype('int')

    return frames


def get_events(json, players_info):
    events = pd.DataFrame()

    frames = json['frames']
    for elem in range(len(frames)):
        events = events.append(pd.DataFrame(frames[elem]['events']))

    events['position_x'] = [elem.get('x') if type(elem) == dict else 'none' for elem in events['position']]
    events['position_y'] = [elem.get('y') if type(elem) == dict else 'none' for elem in events['position']]
    events.drop(columns='position', inplace=True)
    events['timestamp'] = (events['timestamp'] / 60000).astype('int')
    events.drop(columns=['teamId'], axis=1, inplace=True)
    events = events.merge(players_info[['participantId', 'teamId']], on='participantId', how='left')
    events = events.merge(players_info[['participantId', 'teamId']], left_on='killerId', right_on='participantId',
                          how='outer')

    return events


def gold_diff(frames):
    data = frames.groupby(['timestamp', 'teamId']).sum().reset_index()[['timestamp', 'teamId', 'totalGold']]

    team100gold = data[data['teamId'] == 100]
    team100gold.rename(columns={"totalGold": "team100gold"}, inplace=True)
    team200gold = data[data['teamId'] == 200][['timestamp', 'teamId', 'totalGold']]
    team200gold.rename(columns={"totalGold": "team200gold"}, inplace=True)

    golddiff = pd.merge(team100gold, team200gold, on='timestamp')
    golddiff['golddiff'] = golddiff['team100gold'] - golddiff['team200gold']

    golddiff['team100golddiff'] = [a if a > 0 else 0 for a in golddiff['golddiff']]
    golddiff['team200golddiff'] = [a if a < 0 else 0 for a in golddiff['golddiff']]

    return golddiff


def championsid(api):
    url = 'http://ddragon.leagueoflegends.com/cdn/10.21.1/data/en_US/champion.json'

    html = requests.get(url,
                        params={'api_key': api})
    json = html.json()

    champions = pd.DataFrame()
    for champ in json['data'].keys():
        df = pd.DataFrame({'name': json['data'][f'{champ}']['id'], 'champion': json['data'][f'{champ}']['key']},
                          index=[0])
        champions = champions.append(df, ignore_index=True)
    champions['champion'] = champions['champion'].astype('int')

    return champions


def get_queuesid(api):
    url = 'http://static.developer.riotgames.com/docs/lol/queues.json'
    html = requests.get(url,
                        params={'api_key': api})
    json = html.json()

    queuesid = pd.DataFrame()
    for queue in json:
        df = pd.DataFrame({'queue': queue['queueId'], 'queue_type': queue['description']},
                          index=[0])
        queuesid = queuesid.append(df, ignore_index=True)

    return queuesid


def player_stats_table(frames_df, champs):
    df = frames_df.copy()
    df.rename(columns={'championId': 'champion'}, inplace=True)
    df = df.merge(champs, on='champion')
    df.drop(['champion'], axis=1, inplace=True)
    df.rename(columns={'name': 'champion'}, inplace=True)
    df = df[['timestamp', 'summonerName', 'champion', 'level', 'minionsKilled', 'totalGold']]

    return df
