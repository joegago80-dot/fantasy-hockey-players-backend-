import requests

SEASON = "20242025"

BASE_URL = "https://api.nhle.com/stats/rest"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_all_players():
    all_players = []

    # ---- Fetch skaters ----
    skater_url = (
        f"{BASE_URL}/skater/summary?isAggregate=false&isGame=false"
        f"&sort=[{{\"property\":\"points\",\"direction\":\"DESC\"}}]"
        f"&cayenneExp=seasonId={SEASON}"
    )

    try:
        resp = requests.get(skater_url, headers=HEADERS, timeout=10)
        skaters = resp.json().get("data", [])
        for p in skaters:
            all_players.append({
                "name": f"{p.get('playerFirstName','')} {p.get('playerLastName','')}",
                "position": p.get("playerPositionCode", ""),
                "team": p.get("playerTeamAbbrevs", ""),
                "gamesPlayed": p.get("gamesPlayed", 0),
                "goals": p.get("goals", 0),
                "assists": p.get("assists", 0),
                "points": p.get("points", 0),
                "ppPoints": p.get("ppPoints", 0),
                "shPoints": p.get("shPoints", 0),
                "gameWinningGoals": p.get("gameWinningGoals", 0),
                "shots": p.get("shots", 0),
                "hits": p.get("hits", 0),
                "blocks": p.get("blockedShots", 0),
                "playerType": "skater"
            })
    except Exception as e:
        print("Error fetching skaters:", e)

    # ---- Fetch goalies ----
    goalie_url = (
        f"{BASE_URL}/goalie/summary?isAggregate=false&isGame=false"
        f"&sort=[{{\"property\":\"wins\",\"direction\":\"DESC\"}}]"
        f"&cayenneExp=seasonId={SEASON}"
    )

    try:
        resp = requests.get(goalie_url, headers=HEADERS, timeout=10)
        goalies = resp.json().get("data", [])
        for p in goalies:
            all_players.append({
                "name": f"{p.get('playerFirstName','')} {p.get('playerLastName','')}",
                "position": "G",
                "team": p.get("playerTeamAbbrevs", ""),
                "gamesPlayed": p.get("gamesPlayed", 0),
                "goalieWins": p.get("wins", 0),
                "savePercentage": p.get("savePct", 0.0),
                "goalsAgainstAverage": p.get("gaa", 0.0),
                "shutouts": p.get("shutouts", 0),
                "playerType": "goalie"
            })
    except Exception as e:
        print("Error fetching goalies:", e)

    return all_players
