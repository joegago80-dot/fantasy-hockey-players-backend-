import json
from pathlib import Path
from compute_projections import compute_all_projections

PLAYERS_FILE = Path("players.json")

def load_players_json():
    if PLAYERS_FILE.exists():
        with PLAYERS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def evaluate_trade(playerA, playerB):
    players = load_players_json()
    projections = compute_all_projections(players)

    player_a_data = None
    player_b_data = None

    for proj in projections:
        if proj.get("name", "").lower() == playerA.lower():
            player_a_data = proj
        if proj.get("name", "").lower() == playerB.lower():
            player_b_data = proj

    if not player_a_data:
        return {"error": f"Player '{playerA}' not found"}
    if not player_b_data:
        return {"error": f"Player '{playerB}' not found"}
    if player_a_data.get("playerType") != player_b_data.get("playerType"):
        return {"error": "Cannot compare skater and goalie"}

    value_scores = {}
    if player_a_data.get("playerType") == "skater":
        categories = ["projectedGoals", "projectedAssists", "projectedPPP", "projectedSHP",
                      "projectedGWG", "projectedSOG", "projectedHits", "projectedBlocks"]
        for cat in categories:
            value_scores[cat] = round(player_a_data.get(cat, 0) - player_b_data.get(cat, 0), 2)
    else:
        categories = ["projectedWins", "projectedSavePercentage"]
        for cat in categories:
            value_scores[cat] = round(player_a_data.get(cat, 0) - player_b_data.get(cat, 0), 4)

    total_advantage = sum(1 for v in value_scores.values() if v > 0)
    total_disadvantage = sum(1 for v in value_scores.values() if v < 0)

    return {
        "playerA": playerA,
        "playerB": playerB,
        "playerA_data": player_a_data,
        "playerB_data": player_b_data,
        "value_scores": value_scores,
        "summary": {
            "categories_advantage_A": total_advantage,
            "categories_advantage_B": total_disadvantage,
            "recommendation": "Player A" if total_advantage > total_disadvantage
            else "Player B" if total_disadvantage > total_advantage
            else "Even trade"
        }
    }
