import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
from bs4 import BeautifulSoup
import json

# créer une url pour toutes les saisons

base_url = 'https://understat.com/league'
leagues = ['La_liga', 'EPL', 'Bundesliga', 'Serie_A', 'Ligue_1', 'RFPL']
seasons = ['2014', '2015', '2016', '2017', '2018']

# choisir le championnat et la saison à afficher

url = base_url+'/'+leagues[2]+'/'+seasons[0]
res = requests.get(url)
soup = BeautifulSoup(res.content, "lxml")

# Sur la base de la structure de la page Web, j'ai trouvé que les données se trouvent dans la variable JSON,
# sous les balises <script>

scripts = soup.find_all('script')

# Trouver des données pour les équipes

string_with_json_obj = ''
for el in scripts:
    if 'teamsData' in str(el):
        string_with_json_obj = str(el).strip()

# Nettoyer mon fichier json

ind_start = string_with_json_obj.index("('") + 2
ind_end = string_with_json_obj.index("')")
json_data = string_with_json_obj[ind_start:ind_end]
json_data = json_data.encode('utf8').decode('unicode_escape')

# convertir les données json en dictionnaire

data = json.loads(json_data)

# obtenir des équipes et leurs identifiants pertinents et les placés dans un dictionnaire séparé

teams = {}
for id in data.keys():
    teams[id] = data[id]['title']
    columns = []
    values = []

for id in data.keys():
    columns = list(data[id]['history'][0].keys())
    values = list(data[id]['history'][0].values())
    break

# récupérer les données de toutes les équipes

dataframes = {}
for id, team in teams.items():
    teams_data = []
    for row in data[id]['history']:
        teams_data.append(list(row.values()))

    df = pd.DataFrame(teams_data, columns=columns)
    dataframes[team] = df

for team, df in dataframes.items():
    dataframes[team]['ppda_coef'] = dataframes[team]['ppda'].apply(
        lambda x: x['att'] / x['def'] if x['def'] != 0 else 0)
    dataframes[team]['oppda_coef'] = dataframes[team]['ppda_allowed'].apply(
        lambda x: x['att'] / x['def'] if x['def'] != 0 else 0)

# Faisons la somme et les moyennes des résultats de nos colonnes

cols_to_sum = ['xG', 'xGA', 'npxG', 'npxGA', 'deep', 'deep_allowed', 'scored', 'missed', 'xpts', 'wins', 'draws', 'loses', 'pts', 'npxGD']
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

# Ensuite, nous réorganisons les colonnes pour une meilleure lisibilité

full_stat = full_stat[['team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG', 'npxG', 'xGA', 'npxGA', 'npxGD', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed', 'xpts']]
full_stat.sort_values('pts', ascending=False, inplace=True)
full_stat.reset_index(inplace=True, drop=True)
full_stat['position'] = range(1,len(full_stat)+1)

# Calculons la différence entre nos prédictions et les résultats réels

full_stat['xG_diff'] = full_stat['xG'] - full_stat['scored']
full_stat['xGA_diff'] = full_stat['xGA'] - full_stat['missed']
full_stat['xpts_diff'] = full_stat['xpts'] - full_stat['pts']

# arrondissons là où c'est necessaire

cols_to_int = ['wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'deep', 'deep_allowed']
full_stat[cols_to_int] = full_stat[cols_to_int].astype(int)

# Vue finale de la dataframe

col_order = ['position','team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG', 'xG_diff', 'npxG', 'xGA', 'xGA_diff', 'npxGA', 'npxGD', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed', 'xpts', 'xpts_diff']
full_stat = full_stat[col_order]
pd.options.display.float_format = '{:,.2f}'.format
# full_stat.head(10)

# #Obtenir les données pour toutes les équipes de tous les championnats

season_data = dict()
season_data[seasons[0]] = full_stat
print(season_data)

