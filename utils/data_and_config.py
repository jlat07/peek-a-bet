import os
import streamlit as st

# Settings
USE_MOCK_DATA = False  # Set to False to use live API data

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