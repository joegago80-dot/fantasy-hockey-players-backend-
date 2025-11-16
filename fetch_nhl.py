from typing import List, Dict
import requests

# Try NHL API client first
try:
    from nhl_stats_api_client import NHLAPIClient
    has_nhl_client = True
except ImportError:
    has_nhl_client = False

# Fallback: sportsreference for NHL
try:
    from sportsreference.nhl.roster import Player as SRPlayer
    has_sportsref = True
except ImportError:
    has_sportsref = False

SEASON = "2024-25"  # format used by NHLAPIClient / sportsreference may differ

def fetch_all_players() -> List[Dict]:
    players = []

    # First: try using nhl_stats_api_client
    if has_nhl_client:
        try:
            client = NHLAPIClient()
            # Get list of teams
            teams = client.get_teams()["data"]
            for team in teams:
                team_id = team["id"]
                # Get roster / season players
                roster = client.get_roster(team_id, SEASON)["data"]
                for p in roster:
                    pid = p["id"]
                    stats = client.get_player_season_stats(pid, SEASON)
                    # Depending on stats structure; assume skater / goalie
                    if stats.get("primaryPosition") == "G":
                        players.append({
                            "name": p["fullName"],
                            "position": "G",
                            "team": p.get("currentTeamAbbrevs", ""),
                            "gamesPlayed": stats.get("gamesPlayed", 0),
                            "goalieWins": stats.get("wins", 0),
                            "savePercentage": stats.get("savePct", 0.0),
                            "playerType": "goalie"
                        })
                    else:
                        players.append({
                            "name": p["fullName"],
                            "position": stats.get("primaryPosition", ""),
                            "team": p.get("currentTeamAbbrevs", ""),
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

    # Fallback: sportsreference
    if has_sportsref:
        try:
            # sportsreference does not have *all* players easily; you may need to maintain a list of IDs
            # Here is a simple example using a few known player IDs or team rosters:
            # For simplicity, scraping a small set or a fixed list is shown; adapt as needed.
            example_ids = ["matthewsau01", "mcdavcon01"]  # proper ids should be looked up
            for pid in example_ids:
                sr = SRPlayer(pid)
                career_games = sr.games_played
                # If you want only this season:
                try:
                    sr_season = sr(SEASON)
                except Exception:
                    sr_season = sr  # fallback to career
                players.append({
                    "name": sr_season.name,
                    "position": sr_season.position,
                    "team": sr_season.team_abbreviation,
                    "gamesPlayed": sr_season.games_played,
                    "goals": sr_season.goals or 0,
                    "assists": sr_season.assists or 0,
                    "points": sr_season.points or 0,
                    "ppPoints": getattr(sr_season, "power_play_points", 0),
                    "shPoints": getattr(sr_season, "short_handed_points", 0),
                    "gameWinningGoals": getattr(sr_season, "game_winning_goals", 0),
                    "shots": getattr(sr_season, "shots", 0),
                    "hits": getattr(sr_season, "hits", 0),
                    "blocks": getattr(sr_season, "blocked", 0),
                    "playerType": "skater"
                })
            return players
        except Exception as e:
            print("Error in sportsreference fallback:", e)

    # If neither method works, return empty list
    print("No API client or fallback available")
    return players
