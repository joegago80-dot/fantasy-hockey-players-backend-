import requests

def fetch_all_players():
    skaters_url = "https://api-web.nhle.com/v1/skater-stats-leaders/20242025/2?categories=goals&limit=-1"
    goalies_url = "https://api-web.nhle.com/v1/goalie-stats-leaders/20242025/2?limit=-1"
    
    all_players = []
    
    try:
        skaters_response = requests.get(skaters_url, timeout=10)
        skaters_response.raise_for_status()
        skaters_data = skaters_response.json()
        
        players_list = skaters_data.get("players", [])
        for player in players_list:
            all_players.append({
                "name": player.get("firstName", {}).get("default", "") + " " + player.get("lastName", {}).get("default", ""),
                "position": player.get("position", ""),
                "team": player.get("teamAbbrev", ""),
                "gamesPlayed": player.get("gamesPlayed", 0),
                "goals": player.get("goals", 0),
                "assists": player.get("assists", 0),
                "points": player.get("points", 0),
                "ppPoints": player.get("powerPlayPoints", 0),
                "shPoints": player.get("shorthandedPoints", 0),
                "gameWinningGoals": player.get("gameWinningGoals", 0),
                "shots": player.get("shots", 0),
                "hits": player.get("hits", 0),
                "blocks": player.get("blockedShots", 0),
                "playerType": "skater"
            })
    except Exception as e:
        print(f"Error fetching skaters: {e}")
    
    try:
        goalies_response = requests.get(goalies_url, timeout=10)
        goalies_response.raise_for_status()
        goalies_data = goalies_response.json()
        
        goalies_list = goalies_data.get("goalies", [])
        for player in goalies_list:
            all_players.append({
                "name": player.get("firstName", {}).get("default", "") + " " + player.get("lastName", {}).get("default", ""),
                "position": "G",
                "team": player.get("teamAbbrev", ""),
                "gamesPlayed": player.get("gamesPlayed", 0),
                "goalieWins": player.get("wins", 0),
                "savePercentage": player.get("savePercentage", 0.0),
                "goalsAgainstAverage": player.get("goalsAgainstAverage", 0.0),
                "shutouts": player.get("shutouts", 0),
                "playerType": "goalie"
            })
    except Exception as e:
        print(f"Error fetching goalies: {e}")
    
    return all_players
