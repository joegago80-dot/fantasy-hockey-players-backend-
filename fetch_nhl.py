import requests
import json
from pathlib import Path

SEASON = "20242025"
OUTPUT_FILE = Path("players.json")

def fetch_all_players():
    all_players = []

    try:
        teams_data = requests.get("https://statsapi.web.nhl.com/api/v1/teams", timeout=10).json()
        teams = teams_data.get("teams", [])
    except Exception as e:
        print(f"Error fetching teams: {e}")
        return []

    for team in teams:
        team_id = team.get("id")
        team_abbrev = team.get("abbreviation", "N/A")

        try:
            roster_data = requests.get(f"https://statsapi.web.nhl.com/api/v1/teams/{team_id}/roster", timeout=10).json()
            roster = roster_data.get("roster", [])
        except Exception as e:
            print(f"Error fetching roster for {team_abbrev}: {e}")
            continue

        for player in roster:
            person = player.get("person", {})
            player_id = person.get("id")
            full_name = person.get("fullName", "N/A")
            position_abbrev = player.get("position", {}).get("abbreviation", "N/A")

            try:
                stats_url = f"https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season={SEASON}"
                stats_data = requests.get(stats_url, timeout=10).json()
                splits = stats_data.get("stats", [{}])[0].get("splits", [])
                stat = splits[0].get("stat", {}) if splits else {}
            except Exception as e:
                print(f"Error fetching stats for {full_name}: {e}")
                stat = {}

            if position_abbrev == "G":
                all_players.append({
                    "name": full_name,
                    "position": "G",
                    "team": team_abbrev,
                    "gamesPlayed": stat.get("games", 0),
                    "goalieWins": stat.get("wins", 0),
                    "savePercentage": stat.get("savePercentage", 0.0),
                    "goalsAgainstAverage": stat.get("goalAgainstAverage", 0.0),
                    "shutouts": stat.get("shutouts", 0),
                    "playerType": "goalie"
                })
            else:
                all_players.append({
                    "name": full_name,
                    "position": position_abbrev,
                    "team": team_abbrev,
                    "gamesPlayed": stat.get("games", 0),
                    "goals": stat.get("goals", 0),
                    "assists": stat.get("assists", 0),
                    "points": stat.get("points", 0),
                    "ppPoints": stat.get("powerPlayPoints", 0),
                    "shPoints": stat.get("shortHandedPoints", 0),
                    "gameWinningGoals": stat.get("gameWinningGoals", 0),
                    "shots": stat.get("shots", 0),
                    "hits": stat.get("hits", 0),
                    "blocks": stat.get("blocked", 0),
                    "playerType": "skater"
                })

    print(f"Fetched {len(all_players)} players from NHL API")
    return all_players


def save_players_json(players):
    try:
        with OUTPUT_FILE.open("w", encoding="utf-8") as f:
            json.dump(players, f, indent=2)
        print(f"Saved {len(players)} players to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving JSON: {e}")


def load_players_json():
    if OUTPUT_FILE.exists():
        try:
            with OUTPUT_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return []
    return []

if __name__ == "__main__":
    players = fetch_all_players()
    save_players_json(players)
