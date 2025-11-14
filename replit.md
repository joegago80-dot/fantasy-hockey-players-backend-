# Fantasy Hockey Players Backend

## Overview
FastAPI backend service for fantasy hockey player statistics, projections, and trade analysis. Fetches real-time NHL data from the official NHL API and provides computed projections based on pace statistics.

## Project Structure
- `app.py` - FastAPI application with REST API endpoints
- `fetch_nhl.py` - NHL API integration for player statistics
- `compute_projections.py` - Statistical projection engine with blended formula
- `trade_analyzer.py` - Player comparison and trade evaluation logic
- `requirements.txt` - Python dependencies

## API Endpoints

### GET /
Health check endpoint returning service status

### GET /players
Returns all NHL player statistics (skaters and goalies) for the 2024-2025 season

### GET /projections
Returns projected statistics for all players using:
- 82-game pace calculation
- Blended projection: 60% pace + 40% current stats

### GET /trade-analyzer?playerA={name}&playerB={name}
Compares two players across all relevant categories and provides trade recommendation

## Deployment
Configured to run with:
```
uvicorn app:app --host=0.0.0.0 --port=5000
```

Render-compatible command:
```
uvicorn app:app --host=0.0.0.0 --port=$PORT
```

## Recent Changes
- 2025-11-14: Initial project setup with all core files and FastAPI endpoints
- 2025-11-14: Integrated NHL API endpoints for 2024-2025 season data
- 2025-11-14: Implemented projection algorithm and trade analyzer

## Dependencies
- FastAPI - Web framework
- Uvicorn - ASGI server
- Requests - HTTP client for NHL API
- Pydantic - Data validation
