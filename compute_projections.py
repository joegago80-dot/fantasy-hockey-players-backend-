def compute_all_projections(players):
    projections = []
    
    for player in players:
        games_played = player.get("gamesPlayed", 0)
        
        if games_played == 0:
            continue
        
        if player.get("playerType") == "skater":
            goals = player.get("goals", 0)
            assists = player.get("assists", 0)
            points = player.get("points", 0)
            pp_points = player.get("ppPoints", 0)
            sh_points = player.get("shPoints", 0)
            gwg = player.get("gameWinningGoals", 0)
            shots = player.get("shots", 0)
            hits = player.get("hits", 0)
            blocks = player.get("blocks", 0)
            
            pace_goals = (goals / games_played) * 82
            pace_assists = (assists / games_played) * 82
            pace_points = (points / games_played) * 82
            pace_pp_points = (pp_points / games_played) * 82
            pace_sh_points = (sh_points / games_played) * 82
            pace_gwg = (gwg / games_played) * 82
            pace_shots = (shots / games_played) * 82
            pace_hits = (hits / games_played) * 82
            pace_blocks = (blocks / games_played) * 82
            
            projected_goals = 0.6 * pace_goals + 0.4 * goals
            projected_assists = 0.6 * pace_assists + 0.4 * assists
            projected_points = 0.6 * pace_points + 0.4 * points
            projected_pp_points = 0.6 * pace_pp_points + 0.4 * pp_points
            projected_sh_points = 0.6 * pace_sh_points + 0.4 * sh_points
            projected_gwg = 0.6 * pace_gwg + 0.4 * gwg
            projected_shots = 0.6 * pace_shots + 0.4 * shots
            projected_hits = 0.6 * pace_hits + 0.4 * hits
            projected_blocks = 0.6 * pace_blocks + 0.4 * blocks
            
            projections.append({
                "name": player.get("name"),
                "position": player.get("position"),
                "team": player.get("team"),
                "gamesPlayed": games_played,
                "projectedGoals": round(projected_goals, 2),
                "projectedAssists": round(projected_assists, 2),
                "projectedPoints": round(projected_points, 2),
                "projectedPPP": round(projected_pp_points, 2),
                "projectedSHP": round(projected_sh_points, 2),
                "projectedGWG": round(projected_gwg, 2),
                "projectedSOG": round(projected_shots, 2),
                "projectedHits": round(projected_hits, 2),
                "projectedBlocks": round(projected_blocks, 2),
                "playerType": "skater"
            })
        
        elif player.get("playerType") == "goalie":
            wins = player.get("goalieWins", 0)
            save_pct = player.get("savePercentage", 0.0)
            
            pace_wins = (wins / games_played) * 82
            
            projected_wins = 0.6 * pace_wins + 0.4 * wins
            projected_save_pct = save_pct
            
            projections.append({
                "name": player.get("name"),
                "position": player.get("position"),
                "team": player.get("team"),
                "gamesPlayed": games_played,
                "projectedWins": round(projected_wins, 2),
                "projectedSavePercentage": round(projected_save_pct, 4),
                "playerType": "goalie"
            })
    
    return projections
