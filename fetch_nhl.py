# fetch_nhl.py
from edgework import Edgework
import json
from pathlib import Path
import time

OUTPUT_FILE = Path("players.json")
SEASON = "2024-2025"  # Edgework season format
CACHE_EXPIRY = 24 * 3600  # 24 hours

def fetch_all_players():
    """
    Fetch all skaters and goalies via Edgework.
    Uses local cache (players.json) if data is fresh.
    """
    # Check cache
    if OUTPUT_FILE.exists():
        mtime = OUTPUT_FILE.stat().st_mtime
        if time.time() - mtime < CACHE_EXPIRY:
            with OUTPUT_FILE.open("r", encoding="utf-8") as f:
                print("Loading players from cache")
                return json.load(f)

    print("Fetching players from Edgework NHL API...")
    client = Edgework(user_agent="FantasyHockeyBackend/1.0")
    players = []

    # Fetch skaters
    try:
        skaters = client.skater_stats(season=SEASON, sort="points", limit=1000)
        for s in skaters:
            players.append({
                "name": s.name,
                "position": s.position,
                "team": s.team,
                "gamesPlayed": s.games_played,
                "goals": s.goals,
                "assists": s.assists,
                "points": s.points,
                "ppPoints": getattr(s, "power_play_points", 0),
                "shPoints": getattr(s, "short_handed_points", 0),
                "gameWinningGoals": getattr(s, "game_winning_goals", 0),
                "shots": getattr(s, "shots", 0),
                "hits": getattr(s, "hits", 0),
                "blocks": getattr(s, "blocked_shots", 0),
                "playerType": "skater"
            })
    except Exception as e:
        print(f"Error fetching skaters: {e}")

    # Fetch goalies
    try:
        goalies = client.goalie_stats(season=SEASON, sort="wins", limit=500)
        for g in goalies:
            players.append({
                "name": g.name,
                "position": "G",
                "team": g.team,
                "gamesPlayed": g.games_played,
                "goalieWins": g.wins,
                "savePercentage": getattr(g, "save_pct", 0.0),
                "playerType": "goalie"
            })
    except Exception as e:
        print(f"Error fetching goalies: {e}")

    # Save cache
    try:
        with OUTPUT_FILE.open("w", encoding="utf-8") as f:
            json.dump(players, f, indent=2)
        print(f"Saved {len(players)} players to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving players.json: {e}")

    return players


# Quick test
if __name__ == "__main__":
    players = fetch_all_players()
    print(f"Fetched {len(players)} players")
    for p in players[:5]:
        print(p)
