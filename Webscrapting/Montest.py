import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
from bs4 import BeautifulSoup
import json

# créer une url pour toutes les saisons

base_url = 'https://understat.com/league'
leagues = ['La_liga', 'EPL', 'Bundesliga', 'Serie_A', 'Ligue_1', 'RFPL']
seasons = ['2014', '2015', '2016', '2017', '2018']


class Application:

    def __init__(self):
        self.url = base_url + '/' + leagues[2] + '/' + seasons[0]
        self.res = requests.get(self.url)
        self.soup = BeautifulSoup(self.res.content, "lxml")
        self.scripts = self.soup.find_all('script')
        self.string_with_json_obj = ''
        for el in self.scripts:
            if 'teamsData' in str(el):
                self.string_with_json_obj = str(el).strip()
        self.ind_start = self.string_with_json_obj.index("('") + 2
        self.ind_end = self.string_with_json_obj.index("')")
        self.json_data = self.string_with_json_obj[self.ind_start:self.ind_end]
        self.json_data = self.json_data.encode('utf8').decode('unicode_escape')
        self.data = json.loads(self.json_data)
        self.teams = {}
        for id in self.data.keys():
            self.teams[id] = self.data[id]['title']
        self.columns = []
        self.values = []
        for id in self.data.keys():
            self.columns = list(self.data[id]['history'][0].keys())
            self.values = list(self.data[id]['history'][0].values())
            break
        self.dataframes = {}
        for id, team in self.teams.items():
            self.teams_data = []
            for row in self.data[id]['history']:
                self.teams_data.append(list(row.values()))
            self.df = pd.DataFrame(self.teams_data, columns=self.columns)
            self.dataframes[team] = self.df

        for team, df in self.dataframes.items():
            self.dataframes[team]['ppda_coef'] = self.dataframes[team]['ppda'].apply(
                lambda x: x['att'] / x['def'] if x['def'] != 0 else 0)
            self.dataframes[team]['oppda_coef'] = self.dataframes[team]['ppda_allowed'].apply(
                lambda x: x['att'] / x['def'] if x['def'] != 0 else 0)

        self.cols_to_sum = ['xG', 'xGA', 'npxG', 'npxGA', 'deep', 'deep_allowed', 'scored', 'missed', 'xpts', 'wins',
                            'draws', 'loses', 'pts', 'npxGD']
        self.cols_to_mean = ['ppda_coef', 'oppda_coef']
        self.frames = []
        for team, df in self.dataframes.items():
            self.sum_data = pd.DataFrame(df[self.cols_to_sum].sum()).transpose()
            self.mean_data = pd.DataFrame(df[self.cols_to_mean].mean()).transpose()
            self.final_df = self.sum_data.join(self.mean_data)
            self.final_df['team'] = team
            self.final_df['matches'] = len(df)
            self.frames.append(self.final_df)

        self.full_stat = pd.concat(self.frames)

        self.full_stat = self.full_stat[
            ['team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG', 'npxG', 'xGA', 'npxGA',
             'npxGD', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed', 'xpts']]

        self.full_stat.sort_values('pts', ascending=False, inplace=True)
        self.full_stat.reset_index(inplace=True, drop=True)
        self.full_stat['position'] = range(1, len(self.full_stat) + 1)

        self.full_stat['xG_diff'] = self.full_stat['xG'] - self.full_stat['scored']
        self.full_stat['xGA_diff'] = self.full_stat['xGA'] - self.full_stat['missed']
        self.full_stat['xpts_diff'] = self.full_stat['xpts'] - self.full_stat['pts']

        self.cols_to_int = ['wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'deep', 'deep_allowed']
        self.full_stat[self.cols_to_int] = self.full_stat[self.cols_to_int].astype(int)

        self.col_order = ['position', 'team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG',
                          'xG_diff', 'npxG', 'xGA', 'xGA_diff', 'npxGA', 'npxGD', 'ppda_coef', 'oppda_coef', 'deep',
                          'deep_allowed', 'xpts', 'xpts_diff']
        self.full_stat = self.full_stat[self.col_order]
        self.full_stat = self.full_stat.set_index('position')
        print(self.full_stat.head(20))


Application()

#
# # Sur la base de la structure de la page Web, j'ai trouvé que les données se trouvent dans la variable JSON,
# # sous les balises <script>
#
#
#
# # Trouver des données pour les équipes
#
# string_with_json_obj = ''
# for el in scripts:
#     if 'teamsData' in str(el):
#         string_with_json_obj = str(el).strip()
#
# # Nettoyer mon fichier json
#
# ind_start = string_with_json_obj.index("('") + 2
# ind_end = string_with_json_obj.index("')")
# json_data = string_with_json_obj[ind_start:ind_end]
# json_data = json_data.encode('utf8').decode('unicode_escape')
#
# # convertir les données json en dictionnaire
#
# data = json.loads(json_data)
#
# # obtenir des équipes et leurs identifiants pertinents et les placés dans un dictionnaire séparé
#
# teams = {}
# for id in data.keys():
#     teams[id] = data[id]['title']
#     columns = []
#     values = []
#
# for id in data.keys():
#     columns = list(data[id]['history'][0].keys())
#     values = list(data[id]['history'][0].values())
#     break
#
# # récupérer les données de toutes les équipes
#
# dataframes = {}
# for id, team in teams.items():
#     teams_data = []
#     for row in data[id]['history']:
#         teams_data.append(list(row.values()))
#
#     df = pd.DataFrame(teams_data, columns=columns)
#     dataframes[team] = df
#
# for team, df in dataframes.items():
#     dataframes[team]['ppda_coef'] = dataframes[team]['ppda'].apply(
#         lambda x: x['att'] / x['def'] if x['def'] != 0 else 0)
#     dataframes[team]['oppda_coef'] = dataframes[team]['ppda_allowed'].apply(
#         lambda x: x['att'] / x['def'] if x['def'] != 0 else 0)
#
# # Faisons la somme et les moyennes des résultats de nos colonnes
#
# cols_to_sum = ['xG', 'xGA', 'npxG', 'npxGA', 'deep', 'deep_allowed', 'scored', 'missed', 'xpts', 'wins', 'draws', 'loses', 'pts', 'npxGD']
# cols_to_mean = ['ppda_coef', 'oppda_coef']
#
# frames = []
# for team, df in dataframes.items():
#     sum_data = pd.DataFrame(df[cols_to_sum].sum()).transpose()
#     mean_data = pd.DataFrame(df[cols_to_mean].mean()).transpose()
#     final_df = sum_data.join(mean_data)
#     final_df['team'] = team
#     final_df['matches'] = len(df)
#     frames.append(final_df)
# full_stat = pd.concat(frames)
#
# # Ensuite, nous réorganisons les colonnes pour une meilleure lisibilité
#
# full_stat = full_stat[['team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG', 'npxG', 'xGA', 'npxGA', 'npxGD', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed', 'xpts']]
# full_stat.sort_values('pts', ascending=False, inplace=True)
# full_stat.reset_index(inplace=True, drop=True)
# full_stat['position'] = range(1,len(full_stat)+1)
#
# # Calculons la différence entre nos prédictions et les résultats réels
#
# full_stat['xG_diff'] = full_stat['xG'] - full_stat['scored']
# full_stat['xGA_diff'] = full_stat['xGA'] - full_stat['missed']
# full_stat['xpts_diff'] = full_stat['xpts'] - full_stat['pts']
#
# # arrondissons là où c'est necessaire
#
# cols_to_int = ['wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'deep', 'deep_allowed']
# full_stat[cols_to_int] = full_stat[cols_to_int].astype(int)
#
# # Vue finale de la dataframe
#
# col_order = ['position','team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG', 'xG_diff', 'npxG', 'xGA', 'xGA_diff', 'npxGA', 'npxGD', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed', 'xpts', 'xpts_diff']
# full_stat = full_stat[col_order]
# pd.options.display.float_format = '{:,.2f}'.format
# # full_stat.head(10)
#
# # #Obtenir les données pour toutes les équipes de tous les championnats
#
# season_data = dict()
# season_data[seasons[0]] = full_stat
# print(season_data)
#
