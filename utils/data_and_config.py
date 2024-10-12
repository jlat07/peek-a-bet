import os
import streamlit as st
from data_and_config import auth

# Authenticate user
user = auth.authenticate()

if user:
    st.write(f"Welcome {user['email']}!")
    # Settings
    USE_MOCK_DATA = True  # Set to True to use mock data; False to use live API data

    # Fetch API credentials from Streamlit secrets or environment variables
    API_KEY = st.secrets.get("API_KEY") or os.getenv('API_KEY')
    BASE_URL = st.secrets.get("BASE_URL")

    # Supabase credentials
    SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv('SUPABASE_URL')
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv('SUPABASE_KEY')

    # Initialize Supabase Auth
    auth = Auth(SUPABASE_URL, SUPABASE_KEY)

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
else:
    st.write("Please log in to access the app.")