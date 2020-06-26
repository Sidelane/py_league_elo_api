from modules.elo import Elo
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get_elo/<region>/<username>')
def get_elo(region, username):

    elo = Elo(region, username)
    rank = elo.get_elo()

    if rank[0] == "Unranked or Flex":
        return "Unranked"
    else:
        return f"Summoner: {rank[1]} || Elo: {rank[2]} {rank[3]}"

@app.route('/get_wr/<region>/<username>')
def get_wr(region, username):
    
    elo = Elo(region, username)
    wr =  elo.get_wr()

    if wr[0] == "Unranked or Flex":
        return "Unranked"
    else:
        return f"Summoner: {wr[1]} || {wr[2]} {wr[3]} - {wr[4]}"

@app.route('/get_full/<region>/<summoner>')
def get_full(region, summoner):
    elo = Elo(region, summoner)
    rank = elo.get_elo()
    wr = elo.get_wr()

    if wr[0] == "Unranked of Flex":
        return "Unranked"
    else:
        return f"Summoner: {rank[1]} || Elo: {rank[2]} {rank[3]} -- {wr[2]} {wr[3]} - {wr[4]}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
