from Summoner import Summoner
from fastapi import FastAPI, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError


app = FastAPI()


@app.get("/")
async def get_elo(region: str = "euw", name: str = None):
    try:
        summoner = Summoner(region=region, summoner_name=name)
    except ValidationError:
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


@app.get("/json")
async def get_elo_json(region: str = "euw", name: str = None):
    try:
        summoner = Summoner(region=region, summoner_name=name)
    except ValidationError:
        return Response(content="Region not Found", status_code=501)

    if summoner.id == None:
        return Response(content=f"Summoner: {summoner.summoner_name} on {summoner.region} not found.", status_code=404)

    if summoner.unranked:
        json_data = jsonable_encoder(summoner, include={"region", "summoner_name", "unranked"})
        return JSONResponse(content=json_data)
    elif summoner.promo:
        json_data = jsonable_encoder(summoner, exclude={"id", "accountId", "puuid", "unranked"})
        return JSONResponse(content=json_data)
    else:
        json_data = jsonable_encoder(summoner, exclude={"id", "accountId", "puuid", "unranked", "promo", "promoWins", "promoLosses"})
        return JSONResponse(content=json_data)

