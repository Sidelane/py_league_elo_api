from requests import get
from bs4 import BeautifulSoup

class Elo:

    def __init__(self, region: str, username: str):
        self.region = region
        self.username = username

        self.html = self.get_html()

    def __repr__(self):
        return f"Elo({self.region}, {self.username})"

    def print_summoner(self):
        print(f"{self.region}, {self.username}")

    def get_html(self):
        if self.region == "kr":
            html = get(f"https://op.gg/summoner/userName={self.username}")
        else:
            html = get(f"https://{self.region}.op.gg/summoner/userName={self.username}")

        soup = BeautifulSoup(html.text, 'html.parser')
        return soup

    def get_elo(self):
        if self.html.find('span', {'class': 'wins'}) is not None:
            return [self.region, self.username, self.html.find('div', {'class': 'TierRank'}).text.strip(), self.html.find('span', {'class': 'LeaguePoints'}).text.strip()]
        else:
            return ['Unranked or Flex']

    def get_wr(self):
        if self.html.find('span', {'class': 'wins'}) is not None:
            return [self.region, self.username, self.html.find('span', {'class': 'wins'}).text.strip(), self.html.find('span', {'class': 'losses'}).text.strip(), self.html.find('span', {'class': 'winratio'}).text.strip()]
        else:
            return ['Unranked or Flex']
