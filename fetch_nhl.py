import requests

BASE_URL = "https://api-web.nhl.com/v1"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; FantasyApp/1.0)"
}

def fetch_json(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        print(f"URL: {url}, Status: {response.status_code}")
        print(f"RAW RESPONSE (first 200 chars): {response.text[:200]}")

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def fetch_skater_stats():
    url = f"{BASE_URL}/stats/leaders/skaters?categories=points,goals,assists"
    data = fetch_json(url)
    if not data or "points" not in data:
        return []
    return data["points"]  # NHL returns leaders lists by category


def fetch_goalie_stats():
    url = f"{BASE_URL}/stats/leaders/goalies?categories=wins,savePct"
    data = fetch_json(url)
    if not data or "wins" not in data:
        return []
    return data["wins"]


def fetch_all_players():
    skaters = fetch_skater_stats()
    goalies = fetch_goalie_stats()
    print(f"Skaters fetched: {len(skaters)}  |  Goalies fetched: {len(goalies)}")

    players = skaters + goalies
    return players
