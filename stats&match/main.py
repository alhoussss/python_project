import json
# from math import *
# from random import *
# import matplotlib.pyplot as plt
# import numpy as np
from scipy.stats import poisson
# from statistics import mean


def team_one_stats(team_one):
    with open('data/data.json',  encoding='UTF8') as json_file:
        data = json.load(json_file)
        print(team_one)

# La force d'attaque de la team_one

        moyen_home_goal_one = data[team_one]["home_goal"] / data[team_one]["home_match"]
        moyen_home_goal_match = data["goal"]["home_goal"] / data["match"]["all_match"]
        attack_strength_one = moyen_home_goal_one / moyen_home_goal_match

# la force de défense de la team_one

        moyen_away_cash_goal = data[team_one]["goal_conced_away"] / data[team_one]["away_match"]
        moyen_home_goal_match = data["goal"]["away_goal"] / data["match"]["all_match"]
        defense_strength_one = moyen_away_cash_goal / moyen_home_goal_match

# le nombre de but susceptible d'être marqué par team_one

        team_one_goal = poisson.cdf(k=2, mu=attack_strength_one * defense_strength_one * moyen_home_goal_match,)*100

        print(team_one_goal)


def team_two_stats(team_two):

    with open('data/data.json', encoding='UTF8') as json_file:
        data = json.load(json_file)
        victory_two = data[team_two]["Victoire"]
        match_two = data[team_two]["matchs"]
        print(team_two)

        moyen_away_cash_goal = data[team_two]["goal_conced_away"] / data[team_two]["away_match"]

# La force d'attaque de la team_two

        moyen_away_goal_two = data[team_two]["away_goal"] / data[team_two]["away_match"]
        moyen_home_goal_match = data["goal"]["away_goal"] / data["match"]["all_match"]
        attack_strength_two = moyen_away_goal_two / moyen_home_goal_match
# la force de défense de la team_two

        moyen_home_cash_goal = data[team_two]["goal_conced_home"] / data[team_two]["home_match"]
        moyen_home_goal_match = data["goal"]["home_goal"] / data["match"]["all_match"]
        defense_strength_two = moyen_away_cash_goal / moyen_home_goal_match

# le nombre de but susceptible d'être marqué par team_two

        team_two_goal = poisson.cdf(k=3, mu=attack_strength_two * defense_strength_two * moyen_home_goal_match,)*100

        print(team_two_goal)


def compare(team_one, team_two):
    pourc_team_one = team_one_stats(team_one)
    print(pourc_team_one)
    pourc_team_two = team_two_stats(team_two)
    print(pourc_team_two)
    if pourc_team_one > pourc_team_two:
        print("l'equipe du "+" " + team_one + " " + "gagne")
    elif pourc_team_one == pourc_team_two:
        print("ce sera un match nulle")
    else:
        print("l'equipe du "+" " + team_two + " " + "gagne")


if __name__ == '__main__':
    # team_one()
    # team_two()
    team_one_stats("Man_city")
    team_two_stats("Arsenal")
    #compare("Real madrid", "Man_city")
