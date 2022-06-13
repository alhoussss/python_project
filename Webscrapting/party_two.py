import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
from bs4 import BeautifulSoup
import json
import django
from Webscrapting.party_one import seasons, leagues, base_url


full_data = dict()
for league in leagues:

    season_data = dict()
    for season in seasons:
        url = base_url + '/' + league + '/' + season
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "lxml")

        # Based on the structure of the webpage, I found that data is in the JSON variable, under <script> tags
        scripts = soup.find_all('script')

        string_with_json_obj = ''

        # Find data for teams
        for el in scripts:
            if 'teamsData' in str(el):
                string_with_json_obj = str(el).strip()

        # print(string_with_json_obj)

        # strip unnecessary symbols and get only JSON data
        ind_start = string_with_json_obj.index("('") + 2
        ind_end = string_with_json_obj.index("')")
        json_data = string_with_json_obj[ind_start:ind_end]
        json_data = json_data.encode('utf8').decode('unicode_escape')

        # convert JSON data into Python dictionary
        data = json.loads(json_data)

        # Get teams and their relevant ids and put them into separate dictionary
        teams = {}
        for id in data.keys():
            teams[id] = data[id]['title']

        # EDA to get a feeling of how the JSON is structured
        # Column names are all the same, so we just use first element
        columns = []
        # Check the sample of values per each column
        values = []
        for id in data.keys():
            columns = list(data[id]['history'][0].keys())
            values = list(data[id]['history'][0].values())
            break

        # Getting data for all teams
        dataframes = {}
        for id, team in teams.items():
            teams_data = []
            for row in data[id]['history']:
                teams_data.append(list(row.values()))

            df = pd.DataFrame(teams_data, columns=columns)
            dataframes[team] = df
            # print('Added data for {}.'.format(team))
        dataframes['Barcelona'].head(2)

        cols_to_sum = ['xG', 'xGA', 'npxG', 'npxGA', 'deep', 'deep_allowed', 'scored', 'missed', 'xpts', 'wins',
                       'draws', 'loses', 'pts', 'npxGD']
        cols_to_mean = ['ppda_coef', 'oppda_coef']

        frames = []
        for team, df in dataframes.items():
            sum_data = pd.DataFrame(df[cols_to_sum].sum()).transpose()
            mean_data = pd.DataFrame(df[cols_to_mean].mean()).transpose()
            final_df = sum_data.join(mean_data)
            final_df['team'] = team
            final_df['matches'] = len(df)
            frames.append(final_df)

        full_stat = pd.concat(frames)

        full_stat = full_stat[
            ['team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG', 'npxG', 'xGA', 'npxGA',
             'npxGD', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed', 'xpts']]
        full_stat.sort_values('pts', ascending=False, inplace=True)
        full_stat.reset_index(inplace=True, drop=True)
        full_stat['position'] = range(1, len(full_stat) + 1)

        full_stat['xG_diff'] = full_stat['xG'] - full_stat['scored']
        full_stat['xGA_diff'] = full_stat['xGA'] - full_stat['missed']
        full_stat['xpts_diff'] = full_stat['xpts'] - full_stat['pts']

        cols_to_int = ['wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'deep', 'deep_allowed']
        full_stat[cols_to_int] = full_stat[cols_to_int].astype(int)

        col_order = ['position', 'team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG',
                     'xG_diff', 'npxG', 'xGA', 'xGA_diff', 'npxGA', 'npxGD', 'ppda_coef', 'oppda_coef', 'deep',
                     'deep_allowed', 'xpts', 'xpts_diff']
        full_stat = full_stat[col_order]
        full_stat = full_stat.set_index('position')
        # print(full_stat.head(20))

        season_data[season] = full_stat

    df_season = pd.concat(season_data)
    full_data[league] = df_season

data = pd.concat(full_data)
data.head()
print(data.head(20))