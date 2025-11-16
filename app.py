from fastapi import FastAPI, Query
from fetch_nhl import fetch_all_players, save_players_json, load_players_json
from compute_projections import compute_all_projections
from trade_analyzer import evaluate_trade
from pathlib import Path
import time
import json

app = FastAPI(title="Fantasy Hockey Players Backend")

# Config
PLAYERS_FILE = Path("players.json")
UPDATE_INTERVAL = 24 * 3600  # 24 hours in seconds
last_update = 0  # timestamp of last fetch


def load_players():
    """Load players from JSON, fetch from NHL API if needed."""
    global last_update
    now = time.time()

    if not PLAYERS_FILE.exists() or (now - last_update) > UPDATE_INTERVAL:
        print("Fetching NHL data...")
        players = fetch_all_players()
        if players:
            save_players_json(players)
        else:
            print("Warning: Fetch failed, using cached JSON if available")
            players = load_players_json()
        last_update = now
    else:
        players = load_players_json()

    return players


@app.get("/")
def read_root():
    return {"message": "Fantasy Hockey Players Backend is running!"}


@app.get("/players")
def get_players():
    players = load_players()
    return {"players": players, "count": len(players)}


@app.get("/projections")
def get_projections():
    players = load_players()
    projections = compute_all_projections(players)
    return {"projections": projections, "count": len(projections)}


@app.get("/trade-analyzer")
def analyze_trade(
    playerA: str = Query(..., description="Name of first player"),
    playerB: str = Query(..., description="Name of second player")
):
    result = evaluate_trade(playerA, playerB)
    return result
