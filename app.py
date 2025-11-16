from fastapi import FastAPI, Query
from fetch_nhl import fetch_all_players, save_players_json
import json
from pathlib import Path
import time

app = FastAPI(title="Fantasy Hockey Players Backend")

# Config
PLAYERS_FILE = Path("players.json")
UPDATE_INTERVAL = 24 * 3600  # 24 hours in seconds
last_update = 0  # timestamp of last fetch

# Helper function to load or update players
def load_players():
    global last_update
    now = time.time()

    # Check if players.json exists or last update was >24h ago
    if not PLAYERS_FILE.exists() or (now - last_update) > UPDATE_INTERVAL:
        players = fetch_all_players()
        save_players_json(players)
        last_update = now
        return players
    else:
        with PLAYERS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)

# Endpoint: root
@app.get("/")
def read_root():
    return {"message": "Fantasy Hockey Players Backend is running!"}

# Endpoint: all players
@app.get("/players")
def get_players():
    players = load_players()
    return {"players": players, "count": len(players)}

# Endpoint: projections
@app.get("/projections")
def get_projections():
    from compute_projections import compute_all_projections
    players = load_players()
    projections = compute_all_projections(players)
    return {"projections": projections, "count": len(projections)}

# Endpoint: trade analyzer
@app.get("/trade-analyzer")
def analyze_trade(
    playerA: str = Query(..., description="Name of first player"),
    playerB: str = Query(..., description="Name of second player")
):
    from trade_analyzer import evaluate_trade
    result = evaluate_trade(playerA, playerB)
    return result
