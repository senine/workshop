from time import sleep
from datetime import datetime

import requests

import numpy as np
import pandas as pd

from functools import reduce


USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' +
    'AppleWebKit/537.36 (KHTML, like Gecko) ' +
    'Chrome/61.0.3163.100 Safari/537.36'
)

REQUEST_HEADERS = {
    'user-agent': USER_AGENT,
}

NBA_URL = 'https://stats.nba.com/stats/teamgamelogs'

def scrape_teamgamelogs(period, season = '2017-18', season_type = 'Regular Season', sleep_for=None):
    """Process JSON from stats.nba.com teamgamelogs endpoint and return unformatted DataFrame."""
    if sleep_for:
        sleep(sleep_for) # be nice to server by sleeping if we are scraping inside a loop
    nba_params = {
        'Period': period,
        'Season': season,
        'SeasonType': season_type,
    }
    r = requests.get(
        NBA_URL,
        params=nba_params,
        headers=REQUEST_HEADERS,
        allow_redirects=False,
        timeout=15,
    )
    r.raise_for_status()
    results = r.json()['resultSets'][0]
    rows = results['rowSet']
    if len(rows) == 0:
        return 0
    else:
        headers = results['headers']
        return pd.DataFrame(rows, columns=headers)

def check_maxperiod(max = 10, season = '2017-18', season_type = 'Regular Season', sleep_for=None):
    """check max period available for given nba param."""
    for period in range(5, max+1):
        if type(scrape_teamgamelogs(period, season = '2017-18',
            season_type = 'Regular Season', sleep_for=None)) == int:
            return period - 1

## create dict reference for period
periodname = {
    1:'QTR1',
    2:'QTR2',
    3:'QTR3',
    4:'QTR4',
    0:'FUL'
}
maxperiod = check_maxperiod()
if maxperiod >= 5:
    for ot in range(5,maxperiod+1):
        periodname[ot] = 'OT'+str(ot-4)


def rename_period(period):
    '''return period name given period number.'''
    return periodname[period]


def clean_teamgamelogs(teamlog, period):
    '''return necessary cols for scores for each period'''
    periodscore = teamlog[['SEASON_YEAR','TEAM_ID','TEAM_ABBREVIATION','TEAM_NAME',
        'GAME_ID','GAME_DATE','MATCHUP','PTS']]
    periodscore['PTS'] = periodscore['PTS'].astype(int)
    periodscore.rename(columns = {'PTS':rename_period(period)}, inplace = True)
    return periodscore


def join_periodscore(periodscores = []):
    '''create game score per team, including period scores and total score. NaN indicates there's not such an OT.'''
    return reduce(lambda left,right: pd.merge(left,
            right.drop(['SEASON_YEAR','TEAM_ABBREVIATION','TEAM_NAME','GAME_DATE','MATCHUP'],axis = 1),
            on=['TEAM_ID','GAME_ID'],how='left'), periodscores)



periodscores = []
for period in range(maxperiod+1):
    periodscores.append(clean_teamgamelogs(
                        scrape_teamgamelogs(period),period))

data = join_periodscore(periodscores)

# results sanity check
assert data.shape[0] == 82* 30
assert np.array_equal((data['FUL'] * 2).values, data[list(periodname.values())].sum(axis = 1).values)


# output results to csv
data.to_csv('data/gamescores_2017_18.csv',index = False)

OT = [i for i in periodname.values() if 'OT' in i]

# due to nan ot and 2nd scores are float

data['1ST'] = data.QTR1 + data.QTR2
data['2ND'] = (data.QTR3 + data.QTR4 + data[OT].sum(axis = 1)).astype('int32')
data['REG'] = data.QTR1 + data.QTR2 + data.QTR3 + data.QTR4

data.to_csv('data/gamescores_2017_18_full.csv', index = False)

# generate avg score across nba per period.
period_avg = data[list(periodname.values()) + ['1ST','2ND','REG']].mean()
period_team = data.groupby(['TEAM_ID','TEAM_ABBREVIATION'])[list(periodname.values()) + ['1ST','2ND','REG']].mean()
factor = (period_team - period_avg).reset_index()
factor.to_csv('data/factor_2017_18.csv', index = False)