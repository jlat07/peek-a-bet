import requests
from utils.data_and_config import (
    USE_MOCK_DATA, API_KEY, BASE_URL, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT
)

class APIClient:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL

    def get_sports(self):
        # Existing code remains the same...
        pass

    def get_odds(self, sport_key='americanfootball_nfl'):
        # Existing code remains the same...
        pass

    def get_matchups(self):
        if USE_MOCK_DATA:
            # Return mock data for matchups
            mock_matchups = {
                'Team A vs Team B': {
                    'event_id': '1',
                    'home_team': 'Team B',
                    'away_team': 'Team A',
                    'commence_time': '2023-10-01T18:00:00Z',
                    'sport_key': 'americanfootball_nfl'
                },
                'Team C vs Team D': {
                    'event_id': '2',
                    'home_team': 'Team D',
                    'away_team': 'Team C',
                    'commence_time': '2023-10-01T21:00:00Z',
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
            # Return mock data for scores
            mock_scores = {
                'Team A vs Team B': {
                    'event_id': '1',
                    'home_team': 'Team B',
                    'away_team': 'Team A',
                    'home_score': 21,
                    'away_score': 28,
                    'completed': True,
                    'commence_time': '2023-10-01T18:00:00Z'
                },
                'Team C vs Team D': {
                    'event_id': '2',
                    'home_team': 'Team D',
                    'away_team': 'Team C',
                    'home_score': 14,
                    'away_score': 14,
                    'completed': False,
                    'commence_time': '2023-10-01T21:00:00Z'
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