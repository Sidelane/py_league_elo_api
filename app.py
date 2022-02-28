from Summoner import Summoner
from fastapi import FastAPI, Response


app = FastAPI()


@app.get("/")
async def get_elo(region: str = "euw", name: str = None):
    summoner = Summoner(region, name)

    if summoner == None:
        return Response(content="Region not Found", status_code=501)

    if summoner.id == None:
        return Response(content=f"Summoner: {summoner.summoner_name} on {summoner.region} not found.", status_code=404)

    if summoner.unranked == True:
        res = f"Summoner: {summoner.summoner_name} || Elo: Unranked"
    elif summoner.promo == True:
        res = f"Summoner: {summoner.summoner_name} || Elo: {summoner.tier} {summoner.rank} {summoner.leaguePoints}LP Promo: {summoner.promoWins}-{summoner.promoLosses} -- {summoner.wins}W {summoner.losses}L - {summoner.winrate}%"
    else:
        res = f"Summoner: {summoner.summoner_name} || Elo: {summoner.tier} {summoner.rank} {summoner.leaguePoints}LP -- {summoner.wins}W {summoner.losses}L - {summoner.winrate}%"

    return Response(content=res, status_code=200)
