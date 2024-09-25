from datetime import datetime, timedelta, timezone
import requests
from utils.data_and_config import (
    USE_MOCK_DATA, API_KEY, BASE_URL, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT
)

class APIClient:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL

    def get_sports(self):
        try:
            response = requests.get(
                f"{self.base_url}/sports",
                params={'apiKey': self.api_key}
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            raise Exception(f"Error fetching sports: {e}")

    def get_odds(self, sport_key='americanfootball_nfl'):
        try:
            params = {
                'apiKey': self.api_key,
                'regions': REGIONS,
                'markets': MARKETS,
                'oddsFormat': ODDS_FORMAT,
                'dateFormat': DATE_FORMAT,
            }
            response = requests.get(
                f"{self.base_url}/sports/{sport_key}/odds",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            raise Exception(f"Error fetching odds: {e}")

    def get_matchups(self):
        if USE_MOCK_DATA:
            mock_matchups = {
                'Buffalo Bills vs Miami Dolphins': {
                    'event_id': '1',
                    'home_team': 'Buffalo Bills',
                    'away_team': 'Miami Dolphins',
                    'commence_time': (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat().replace('+00:00', 'Z'),
                    'sport_key': 'americanfootball_nfl'
                },
                'Kansas City Chiefs vs Denver Broncos': {
                    'event_id': '2',
                    'home_team': 'Kansas City Chiefs',
                    'away_team': 'Denver Broncos',
                    'commence_time': (datetime.now(timezone.utc) - timedelta(hours=4)).isoformat().replace('+00:00', 'Z'),
                    'sport_key': 'americanfootball_nfl'
                },
                'Green Bay Packers vs Chicago Bears': {
                    'event_id': '3',
                    'home_team': 'Green Bay Packers',
                    'away_team': 'Chicago Bears',
                    'commence_time': (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat().replace('+00:00', 'Z'),
                    'sport_key': 'americanfootball_nfl'
                }
            }
            return mock_matchups
        else:
            # Fetch matchups from the API
            odds_data = self.get_odds()
            matchups = {}
            for event in odds_data:
                event_id = event['id']
                home_team = event['home_team']
                away_team = event['away_team']
                commence_time = event['commence_time']
                matchup_key = f"{away_team} vs {home_team}"
                matchups[matchup_key] = {
                    'event_id': event_id,
                    'home_team': home_team,
                    'away_team': away_team,
                    'commence_time': commence_time,
                    'sport_key': event['sport_key']
                }
            return matchups

    def get_matchups(self):
        if USE_MOCK_DATA:
            # Updated mock data for matchups with realistic NFL teams
            mock_matchups = {
                'Buffalo Bills vs Miami Dolphins': {
                    'event_id': '1',
                    'home_team': 'Buffalo Bills',
                    'away_team': 'Miami Dolphins',
                    'commence_time': (datetime.utcnow() - datetime.timedelta(hours=1)).isoformat() + 'Z',  # Game started 1 hour ago
                    'sport_key': 'americanfootball_nfl'
                },
                'Kansas City Chiefs vs Denver Broncos': {
                    'event_id': '2',
                    'home_team': 'Kansas City Chiefs',
                    'away_team': 'Denver Broncos',
                    'commence_time': (datetime.utcnow() - datetime.timedelta(hours=4)).isoformat() + 'Z',  # Game started 4 hours ago
                    'sport_key': 'americanfootball_nfl'
                },
                'Green Bay Packers vs Chicago Bears': {
                    'event_id': '3',
                    'home_team': 'Green Bay Packers',
                    'away_team': 'Chicago Bears',
                    'commence_time': (datetime.utcnow() + datetime.timedelta(hours=2)).isoformat() + 'Z',  # Game starts in 2 hours
                    'sport_key': 'americanfootball_nfl'
                }
            }
            return mock_matchups
        else:
            # Fetch matchups from the API
            odds_data = self.get_odds()
            matchups = {}
            for event in odds_data:
                event_id = event['id']
                home_team = event['home_team']
                away_team = event['away_team']
                commence_time = event['commence_time']
                matchup_key = f"{away_team} vs {home_team}"
                matchups[matchup_key] = {
                    'event_id': event_id,
                    'home_team': home_team,
                    'away_team': away_team,
                    'commence_time': commence_time,
                    'sport_key': event['sport_key']
                }
            return matchups

    def get_scores(self, sport_key='americanfootball_nfl', days_from=3):
        if USE_MOCK_DATA:
            mock_scores = {
                'Buffalo Bills vs Miami Dolphins': {
                    'event_id': '1',
                    'home_team': 'Buffalo Bills',
                    'away_team': 'Miami Dolphins',
                    'home_score': 28,
                    'away_score': 24,
                    'completed': False,
                    'commence_time': (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat().replace('+00:00', 'Z')
                },
                'Kansas City Chiefs vs Denver Broncos': {
                    'event_id': '2',
                    'home_team': 'Kansas City Chiefs',
                    'away_team': 'Denver Broncos',
                    'home_score': 35,
                    'away_score': 14,
                    'completed': True,
                    'commence_time': (datetime.now(timezone.utc) - timedelta(hours=4)).isoformat().replace('+00:00', 'Z')
                },
                'Green Bay Packers vs Chicago Bears': {
                    'event_id': '3',
                    'home_team': 'Green Bay Packers',
                    'away_team': 'Chicago Bears',
                    'home_score': None,
                    'away_score': None,
                    'completed': False,
                    'commence_time': (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat().replace('+00:00', 'Z')
                }
            }
            return mock_scores
        else:
            # Fetch scores from the API
            try:
                params = {
                    'apiKey': self.api_key,
                    'daysFrom': days_from,
                    'dateFormat': DATE_FORMAT,
                }
                response = requests.get(
                    f"{self.base_url}/sports/{sport_key}/scores",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                # Process data to extract scores
                scores = {}
                for game in data:
                    event_id = game['id']
                    home_team = game['home_team']
                    away_team = game['away_team']
                    completed = game['completed']
                    commence_time = game['commence_time']
                    scores_list = game.get('scores', [])
                    home_score = None
                    away_score = None
                    if scores_list:
                        for score_entry in scores_list:
                            if score_entry['name'] == home_team:
                                home_score = int(score_entry['score'])
                            elif score_entry['name'] == away_team:
                                away_score = int(score_entry['score'])

                    matchup_key = f"{away_team} vs {home_team}"
                    scores[matchup_key] = {
                        'event_id': event_id,
                        'home_team': home_team,
                        'away_team': away_team,
                        'home_score': home_score,
                        'away_score': away_score,
                        'completed': completed,
                        'commence_time': commence_time
                    }
                return scores
            except requests.RequestException as e:
                raise Exception(f"Error fetching scores: {e}")