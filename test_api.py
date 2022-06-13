import requests
import json
from flask import Flask

app = Flask(__name__)

url = "https://jikan1.p.rapidapi.com/anime/16498/episodes"
# url_video = "https://jikan1.p.rapidapi.com/anime/{idAnime}/videos"


@app.route("/anime", methods=["GET", "POST"])
def get_anime():
    headers = {
        'x-rapidapi-host': "jikan1.p.rapidapi.com",
        'x-rapidapi-key': "c64b9c2637mshffc88dfe24a165ap138a94jsn22beceb2dbdf",
    }

    response = requests.request("GET", url, headers=headers)
    monJson = json.loads(response.text)
    unEpisode = monJson["request_cache_expiry"]
    # Le partitionnement de Json.loads est mieux
    # myDump = json.dumps(response.text, indent=8)

    print(unEpisode)
    # print(monJson)


get_anime()

# @app.route('/', methods=['GET'])
# def hello():
#     return "hello world"


# @app.route('/getteamprofil/<get_teams_team_id>', methods=['GET'])
# def getteamprofil(get_teams_team_id):
#   url = "https://football-api.com/documentation3/#!/Teams/{get_teams_team_id}"
#  response = requests.get("https://football-api.com/documentation3/#!/Players/{0}".format(get_teams_team_id))
# return response.text

# @app.route('/getmatchlist/<comp_id>/<team_id>/<match_date>/<from_date>/<to_date>', methods=['GET'])
# def getmatchlist(comp_id, team_id, match_date, from_date, to_date):
#   url = "https://football-api.com/documentation3/#!/Matches/get_matches"
#  response = requests.get("https://football-api.com/documentation3/#!/Players/{0}/{1}/{2}/{3}/{4}".format(comp_id, team_id, match_date, from_date, to_date))
# return response.text


# @app.route('/getresultgp/<year>/<round>', methods=['GET'])
# def getresult2(year, round) :
#   response = requests.get("http://ergast.com/api/f1/{0}/{1}/driverStandings".format(year, round))
#  return response.text

# @app.route('/getresultgp/<year>/<round>', methods=['GET'])
# def getresult3(year, round) :
#   response = requests.get("http://ergast.com/api/f1/{0}/{1}/driverStandings".format(year, round))
#  return response.text
