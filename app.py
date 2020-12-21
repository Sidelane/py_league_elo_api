from Summoner import Summoner
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get_elo/<region>/<username>')
def get_elo(region, username):

    summoner = Summoner(region, username)

    if summoner.unranked == True:
        return f"Summoner: {summoner.summoner_name} || Elo: Unranked"
    elif summoner.promo == True:
        return f"Summoner: {summoner.summoner_name} || Elo: {summoner.tier} {summoner.rank} {summoner.leaguePoints}LP Promo: {summoner.promoWins}-{summoner.promoLosses}"
    else:
        return f"Summoner: {summoner.summoner_name} || Elo: {summoner.tier} {summoner.rank} {summoner.leaguePoints}LP"

@app.route('/get_wr/<region>/<username>')
def get_wr(region, username):

    summoner = Summoner(region, username)

    if summoner.unranked == True:
        return f"Summoner: {summoner.summoner_name} || Elo: Unranked"
    else:
        return f"Summoner: {summoner.summoner_name} || {summoner.wins}W {summoner.losses}L - {summoner.winrate}%"

@app.route('/get_full/<region>/<username>')
def get_full(region, username):

    summoner = Summoner(region, username)

    if summoner.unranked == True:
        return f"Summoner: {summoner.summoner_name} || Elo: Unranked"
    elif summoner.promo == True:
        return f"Summoner: {summoner.summoner_name} || Elo: {summoner.tier} {summoner.rank} {summoner.leaguePoints}LP Promo: {summoner.promoWins}-{summoner.promoLosses} -- {summoner.wins}W {summoner.losses}L - {summoner.winrate}%"
    else:
        return f"Summoner: {summoner.summoner_name} || Elo: {summoner.tier} {summoner.rank} {summoner.leaguePoints}LP -- {summoner.wins}W {summoner.losses}L - {summoner.winrate}%"

@app.route('/json/get_full/<region>/<username>')
def json_get_full(region, username):
    
    summoner = Summoner(region, username)

    if summoner.unranked == True:
        return jsonify(
            summoner = summoner.summoner_name,
            unranked = summoner.unranked
        )
    elif summoner.promo == True:
        return jsonify(
            summoner = summoner.summoner_name,
            region = summoner.region,
            tier = summoner.tier,
            rank = summoner.rank,
            leaguePoints = summoner.leaguePoints,
            wins = summoner.wins,
            losses = summoner.losses,
            winratio = summoner.winrate,
            miniSeries = summoner.promo,
            miniSeriesWins = summoner.promoWins,
            miniSeriesLosses = summoner.promoLosses
        )
    else:
        return jsonify(
            summoner = summoner.summoner_name,
            region = summoner.region,
            tier = summoner.tier,
            rank = summoner.rank,
            leaguePoints = summoner.leaguePoints,
            wins = summoner.wins,
            losses = summoner.losses,
            winratio = summoner.winrate
        )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
