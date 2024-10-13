import os
import streamlit as st

# Settings
USE_MOCK_DATA = True  # Set to True to use mock data; False to use live API data

# Fetch API credentials from Streamlit secrets or environment variables
API_KEY = st.secrets.get("API_KEY") or os.getenv('API_KEY')
BASE_URL = 'https://api.the-odds-api.com/v4'  # Updated base URL

# API Configuration
REGIONS = 'us'  # Regions to get odds from
MARKETS = 'h2h,spreads,totals'  # Types of bets
ODDS_FORMAT = 'american'  # 'decimal' or 'american'
DATE_FORMAT = 'iso'  # 'iso' or 'unix'

# Bet Configurations
bet_types = ['Spread', 'Over/Under']
spread_values = [float(x) for x in range(-20, 21)]  # Including zero
over_under_values = [float(x) for x in range(30, 71)]  # Over/Under values from 30 to 70

# Theme Configuration
THEME_COLOR = "#39FF14"  # Neon green color for the theme

# Mock Data for testing (useful when USE_MOCK_DATA is True)
mock_matchups = {
    'Buffalo Bills vs Miami Dolphins': {
        'event_id': '1',
        'home_team': 'Buffalo Bills',
        'away_team': 'Miami Dolphins',
        'commence_time': "2023-10-12T17:00:00Z",
        'home_score': 28,
        'away_score': 24,
        'completed': True,
        'sport_key': 'americanfootball_nfl'
    },
    'Kansas City Chiefs vs Denver Broncos': {
        'event_id': '2',
        'home_team': 'Kansas City Chiefs',
        'away_team': 'Denver Broncos',
        'commence_time': "2023-10-12T20:00:00Z",
        'home_score': 35,
        'away_score': 14,
        'completed': True,
        'sport_key': 'americanfootball_nfl'
    },
    'Green Bay Packers vs Chicago Bears': {
        'event_id': '3',
        'home_team': 'Green Bay Packers',
        'away_team': 'Chicago Bears',
        'commence_time': "2023-10-13T17:00:00Z",
        'home_score': None,
        'away_score': None,
        'completed': False,
        'sport_key': 'americanfootball_nfl'
    }
}

mock_scores = {
    'Buffalo Bills vs Miami Dolphins': {
        'home_score': 28,
        'away_score': 24,
        'completed': True
    },
    'Kansas City Chiefs vs Denver Broncos': {
        'home_score': 35,
        'away_score': 14,
        'completed': True
    },
    'Green Bay Packers vs Chicago Bears': {
        'home_score': None,
        'away_score': None,
        'completed': False
    }
}