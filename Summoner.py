import requests
import json
from sys import exit


class Summoner:

    headers = {"X-Riot-Token": "Your API Token"}

    regions = {"euw": "euw1", "na": "na1", "eune": "eun1", "br": "br1", "jp": "jp1", "kr": "kr", "oce": "oc1", "ru": "ru", "tr": "tr1"}

    id_api = "lol/summoner/v4/summoners/by-name"
    sum_api = "lol/league/v4/entries/by-summoner"

    def __init__(self, region, summoner_name):

        if region not in self.regions.keys():
            return None

        self.region = region
        self.summoner_name = summoner_name

        self.id = None
        self.accountId = None
        self.puuid = None

        self.unranked = False

        self.tier = None
        self.rank = None
        self.leaguePoints = None
        self.wins = None
        self.losses = None
        self.winrate = None

        self.promo = False
        self.promoWins = None
        self.promoLosses = None

        self.fetch_ids()
        self.fetch_rank()

    def fetch_ids(self):
        try:
            res = requests.get(f"https://{self.regions[self.region]}.api.riotgames.com/{self.id_api}/{self.summoner_name}", headers=self.headers)
            res_json = json.loads(res.text)
            self.id = res_json["id"]
            self.accountId = res_json["accountId"]
            self.puuid = res_json["puuid"]
        except:
            return print("Error while fetching ids from the riot api")

    def fetch_rank(self):
        try:
            res = requests.get(f"https://{self.regions[self.region]}.api.riotgames.com/{self.sum_api}/{self.id}", headers=self.headers)
            res_json = json.loads(res.text)

            if res_json == []:
                self.unranked = True
                return 0

            if res_json[0]["queueType"] == 'RANKED_SOLO_5x5':
                r_json = res_json[0]
            else:
                r_json = res_json[1]

            self.tier = r_json["tier"].lower().capitalize()
            self.rank = r_json["rank"]
            self.leaguePoints = r_json["leaguePoints"]
            self.wins = r_json["wins"]
            self.losses = r_json["losses"]
            self.winrate = int(self.wins / (self.wins + self.losses) * 100)

            if "miniSeries" in r_json:
                self.promo = True
                self.promoWins = r_json["miniSeries"]["wins"]
                self.promoLosses = r_json["miniSeries"]["losses"]
        except:
            return print("Error while fetching ranks from the riot api")
