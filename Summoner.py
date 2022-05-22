import requests
import json

from sys import exit
from pydantic import BaseModel, root_validator


class Summoner(BaseModel):
    _headers = {"X-Riot-Token": "Your API Token"}
    _regions = {"euw": "euw1", "na": "na1", "eune": "eun1", "br": "br1", "jp": "jp1", "kr": "kr", "oce": "oc1", "ru": "ru", "tr": "tr1"}
    _id_api = "lol/summoner/v4/summoners/by-name"
    _sum_api = "lol/league/v4/entries/by-summoner"

    region: str
    summoner_name: str

    id: int = None
    accountId: int = None
    puuid: int = None
    unranked: bool = False
    tier: str = None
    rank: str = None
    leaguePoints: int = None
    wins: int = None
    losses: int = None
    winrate: int = None
    promo: bool = False
    promoWins: int = None
    promoLosses: int = None

    @root_validator(pre=True)
    def validate(cls, values):
        assert values.get("region") in cls._regions
        return values

    def __init__(self, **data):
        super().__init__(**data)
        self.fetch_ids()
        self.fetch_rank()

    def fetch_ids(self):
        try:
            res = requests.get(f"https://{Summoner._regions[self.region]}.api.riotgames.com/{Summoner._id_api}/{self.summoner_name}", headers=Summoner._headers)
            res_json = json.loads(res.text)
            self.id = res_json["id"]
            self.accountId = res_json["accountId"]
            self.puuid = res_json["puuid"]
        except:
            return print("Error while fetching ids from the riot api")

    def fetch_rank(self):
        try:
            res = requests.get(f"https://{Summoner._regions[self.region]}.api.riotgames.com/{Summoner._sum_api}/{self.id}", headers=Summoner._headers)
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
