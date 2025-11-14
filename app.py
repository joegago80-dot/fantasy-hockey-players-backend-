from fastapi import FastAPI, Query
from fetch_nhl import fetch_all_players
from compute_projections import compute_all_projections
from trade_analyzer import evaluate_trade

app = FastAPI(title="Fantasy Hockey Players Backend")

@app.get("/")
def read_root():
    return {"message": "Fantasy Hockey Players Backend is running!"}

@app.get("/players")
def get_players():
    players = fetch_all_players()
    return {"players": players, "count": len(players)}

@app.get("/projections")
def get_projections():
    players = fetch_all_players()
    projections = compute_all_projections(players)
    return {"projections": projections, "count": len(projections)}

@app.get("/trade-analyzer")
def analyze_trade(
    playerA: str = Query(..., description="Name of first player"),
    playerB: str = Query(..., description="Name of second player")
):
    result = evaluate_trade(playerA, playerB)
    return result
