from typing import List, Dict

# Primary client
try:
    from nhl_stats_api_client import NHLAPIClient
    has_nhl_client = True
except ImportError:
    has_nhl_client = False

# Fallback client
try:
    from sportsreference.nhl.roster import Player as SRPlayer
    has_sportsref = True
except ImportError:
    has_sportsref = False

SEASON = "2024-25"

def fetch_all_players() -> List[Dict]:
    players = []

    # ===== Primary: nhl-stats-api-client =====
    if has_nhl_client:
        try:
            client = NHLAPIClient()
            teams = client.get_teams().get("data", [])
            for team in teams:
                team_id = team.get("id")
                roster = client.get_roster(team_id, SEASON).get("data", [])
                for p in roster:
                    pid = p.get("id")
                    stats = client.get_player_season_stats(pid, SEASON)

                    # Determine player type
                    player_type = "goalie" if stats.get("primaryPosition") == "G" else "skater"

                    if player_type == "goalie":
                        players.append({
                            "name": p.get("fullName", "N/A"),
                            "position": "G",
                            "team": p.get("currentTeamAbbrevs", "N/A"),
                            "gamesPlayed": stats.get("gamesPlayed", 0),
                            "goalieWins": stats.get("wins", 0),
                            "savePercentage": stats.get("savePct", 0.0),
                            "playerType": "goalie"
                        })
                    else:
                        players.append({
                            "name": p.get("fullName", "N/A"),
                            "position": stats.get("primaryPosition", "N/A"),
                            "team": p.get("currentTeamAbbrevs", "N/A"),
                            "gamesPlayed": stats.get("gamesPlayed", 0),
                            "goals": stats.get("goals", 0),
                            "assists": stats.get("assists", 0),
                            "points": stats.get("points", 0),
                            "ppPoints": stats.get("powerPlayPoints", 0),
                            "shPoints": stats.get("shortHandedPoints", 0),
                            "gameWinningGoals": stats.get("gameWinningGoals", 0),
                            "shots": stats.get("shots", 0),
                            "hits": stats.get("hits", 0),
                            "blocks": stats.get("blocked", 0),
                            "playerType": "skater"
                        })
            return players
        except Exception as e:
            print("Error in NHLAPIClient:", e)

    # ===== Fallback: sportsreference =====
    if has_sportsref:
        try:
            # Example: small list of player IDs; expand as needed
            example_ids = ["matthewsau01", "mcdavcon01"]  # Replace with full roster IDs
            for pid in example_ids:
                sr = SRPlayer(pid)
                # Season stats
                try:
                    sr_season = sr(SEASON)
                except Exception:
                    sr_season = sr  # fallback to career

                # Determine if goalie (SportsReference may not include goalies fully)
                player_type = "skater"  # assume skater
                players.append({
                    "name": getattr(sr_season, "name", "N/A"),
                    "position": getattr(sr_season, "position", "N/A"),
                    "team": getattr(sr_season, "team_abbreviation", "N/A"),
                    "gamesPlayed": getattr(sr_season, "games_played", 0),
                    "goals": getattr(sr_season, "goals", 0),
                    "assists": getattr(sr_season, "assists", 0),
                    "points": getattr(sr_season, "points", 0),
                    "ppPoints": getattr(sr_season, "power_play_points", 0),
                    "shPoints": getattr(sr_season, "short_handed_points", 0),
                    "gameWinningGoals": getattr(sr_season, "game_winning_goals", 0),
                    "shots": getattr(sr_season, "shots", 0),
                    "hits": getattr(sr_season, "hits", 0),
                    "blocks": getattr(sr_season, "blocked", 0),
                    "playerType": player_type
                })
            return players
        except Exception as e:
            print("Error in sportsreference fallback:", e)

    print("No data source available or all failed")
    return players

# ===== Quick test =====
if __name__ == "__main__":
    all_players = fetch_all_players()
    print(f"Fetched {len(all_players)} players")
    for p in all_players[:5]:
        print(p)
