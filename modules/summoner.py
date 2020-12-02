from requests import get
from bs4 import BeautifulSoup

class Summoner:

    def __init__(self, name: str, region: str):
        self.name = name
        self.region = region

        self.unranked = False

        self.tier = None
        self.leaguepoints = None
        self.wins = None
        self.losses = None
        self.winratio = None

        self.update_data()

    def __repr__(self):
        if self.unranked == False:
            return f"{self.region} - {self.name} - {self.tier} {self.leaguepoints} - {self.winratio}"
        else:
            return f"Unranked"

    def update_data(self):
        if self.region == "kr":
            html = get(f"https://op.gg/summoner/userName={self.name}")
        else:
            html = get(f"https://{self.region}.op.gg/summoner/userName={self.name}")

        soup = BeautifulSoup(html.text, 'html.parser')

        if soup.find('span', {'class': 'wins'}) is None:
            self.unranked = True
            return 0

        self.tier = soup.find('div', {'class': 'TierRank'}).text.strip()
        self.leaguepoints = soup.find('span', {'class': 'LeaguePoints'}).text.strip()
        self.wins = soup.find('span', {'class': 'wins'}).text.strip()
        self.losses = soup.find('span', {'class': 'losses'}).text.strip()
        self.winratio = soup.find('span', {'class': 'winratio'}).text.strip()