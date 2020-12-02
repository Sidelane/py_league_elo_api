from modules.summoner import Summoner
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get_elo/<region>/<username>')
def get_elo(region, username):

    summoner = Summoner(username, region)

    if summoner.unranked == True:
        return "Unranked"
    else:
        return f"Summoner: {summoner.name} || Elo: {summoner.tier} {summoner.leaguepoints}"

@app.route('/get_wr/<region>/<username>')
def get_wr(region, username):

    summoner = Summoner(username, region)

    if summoner.unranked == True:
        return "Unranked"
    else:
        return f"Summoner: {summoner.name} || {summoner.wins} {summoner.losses} - {summoner.winratio}"

@app.route('/get_full/<region>/<username>')
def get_full(region, username):

    summoner = Summoner(username, region)

    if summoner.unranked == True:
        return f"Unranked"
    else:
        return f"Summoner: {summoner.name} || Elo: {summoner.tier} {summoner.leaguepoints} -- {summoner.wins} {summoner.losses} - {summoner.winratio}"

@app.route('/json/get_full/<region>/<username>')
def json_get_full(region, username):
    
    summoner = Summoner(username, region)

    if summoner.unranked == True:
        return jsonify(
            summoner = summoner.name,
            unranked = summoner.unranked
        )
    else:
        return jsonify(
            summoner = summoner.name,
            region = summoner.region,
            tier = summoner.tier,
            lp = summoner.leaguepoints[:-3],
            wins = summoner.wins[:-1],
            losses = summoner.losses[:-1],
            winratio = summoner.winratio[10:][:-1]
        )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
