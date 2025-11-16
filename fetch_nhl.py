import requests

SEASON = "20242025"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_all_players():
    all_players = []

    # Step 1: Get all teams
    teams_url = "https://statsapi.web.nhl.com/api/v1/teams"
    try:
        teams_data = requests.get(teams_url, headers=HEADERS, timeout=10).json()
        teams = teams_data.get("teams", [])
    except Exception as e:
        print(f"Error fetching teams: {e}")
        return all_players

    # Step 2: Loop through each team
    for team in teams:
        team_id = team.get("id")
        team_abbrev = team.get("abbreviation", "")
        roster_url = f"https://statsapi.web.nhl.com/api/v1/teams/{team_id}/roster"

        try:
            roster_data = requests.get(roster_url, headers=HEADERS, timeout=10).json()
            roster = roster_data.get("roster", [])
        except Exception as e:
            print(f"Error fetching roster for team {team_abbrev}: {e}")
            continue

        # Step 3: Loop through each player on the roster
        for player in roster:
            person = player.get("person", {})
            player_id = person.get("id")
            full_name = person.get("fullName", "")
            position = player.get("position", {}).get("abbreviation", "")

            # Step 4: Fetch player stats
            stats_url = (
                f"https://statsapi.web.nhl.com/api/v1/people/"
                f"{player_id}/stats?stats=statsSingleSeason&season={SEASON}"
            )

            try:
                stats_data = requests.get(stats_url, headers=HEADERS, timeout=10).json()
                stats_list = stats_data.get("stats", [])
                splits = stats_list[0].get("splits", []) if stats_list else []
                stat = splits[0].get("stat", {}) if splits else {}
            except Exception as e:
                print(f"Error fetching stats for player {full_name}: {e}")
                stat = {}

            # Step 5: Separate skaters and goalies
            if position == "G":
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
                    "position": position,
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

    return all_players


if __name__ == "__main__":
    players = fetch_all_players()
    print(f"Fetched {len(players)} players")
    for p in players[:5]:
        print(p)
