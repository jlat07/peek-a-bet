import streamlit as st
from utils.api_client import APIClient
from utils.ticket import Ticket
from utils.auth import authenticate, logout
import utils.data_and_config as config  # Import the entire module

# Set page configuration for dark theme
st.set_page_config(page_title="Parlay Check", page_icon="🏈", layout="wide")

# Initialize authentication
session = authenticate()

# If not logged in, show login form
if not session:
    st.warning("Please log in to access the app.")
else:
    # User is logged in, display the main app content
    st.success(f"Welcome, {session['user']['email']}!")

    # Logout button in the sidebar
    logout()

    # Apply custom CSS for dark theme and neon colors
    THEME_COLOR = "#228B22"  # Forest Green color for the theme
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: #1e1e1e;
            color: #ffffff;
        }}
        .stButton>button {{
            background-color: {config.THEME_COLOR};
            color: #ffffff;
        }}
        </style>
    """)

    # Initialize API Client
    api_client = APIClient()

    # Fetch matchups from the database based on week
    def get_matchups_for_week(week):
        # Replace this with actual database fetching logic
        matchups = {
            "Week 5": [
                {"home_team": "Buccaneers", "away_team": "Panthers", "home_score": 23, "away_score": 20, "status": "In Progress"},
                {"home_team": "Raiders", "away_team": "Vikings", "home_score": 14, "away_score": 10, "status": "In Progress"},
            ]
        }
        return matchups.get(week, [])

    # Page title with football emoji
    st.title("🏈 Parlay Check")

    # Select Week Dropdown
    week_options = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"]  # Example values
    selected_week = st.selectbox('Select Week', week_options)

    # Fetch and show matchups for the selected week
    matchups = get_matchups_for_week(selected_week)
    
    if matchups:
        # Team selection
        team_options = [matchup['home_team'] for matchup in matchups] + [matchup['away_team'] for matchup in matchups]
        selected_team = st.selectbox('Select Team', team_options)

        # Automatically find the opponent based on the selected team
        opponent = None
        for matchup in matchups:
            if selected_team == matchup['home_team']:
                opponent = matchup['away_team']
                home_score = matchup['home_score']
                away_score = matchup['away_score']
                break
            elif selected_team == matchup['away_team']:
                opponent = matchup['home_team']
                home_score = matchup['home_score']
                away_score = matchup['away_score']
                break
        
        if opponent:
            st.write(f"Opponent: {opponent}")

            # Radio button to select bet type (Spread or Total)
            bet_type = st.radio(
                "Select Bet Type",
                ('Spread', 'Total'),
                horizontal=True  # Display radio buttons horizontally
            )

            # Input field for Bet Value
            bet_value = st.number_input(f"Bet Value ({bet_type})", min_value=0.0, step=0.5)

            # Example of adding a bet based on user inputs
            if st.button("Add Bet"):
                new_bet = {
                    "week": selected_week,
                    "team": selected_team,
                    "opponent": opponent,
                    "bet_type": bet_type,
                    "bet_value": bet_value
                }
                # You can add this bet to the draft ticket or process further.
                st.success(f"Bet added for {selected_team} vs {opponent} in {selected_week} with {bet_type} of {bet_value}")
                
            # Display live scores and evaluate conditions
            st.subheader("Live Scores and Bet Evaluation")
            total_score = home_score + away_score
            if bet_type == 'Total':
                delta = total_score - bet_value
                status = "Won" if delta <= 0 else "Lost"
                st.write(f"Total Score: {home_score} + {away_score} = {total_score}")
                st.write(f"Delta: {delta}")
                st.write(f"Status: {status}")
            elif bet_type == 'Spread':
                if selected_team == matchup['home_team']:
                    delta = home_score + bet_value - away_score
                else:
                    delta = away_score + bet_value - home_score
                status = "Won" if delta > 0 else "Lost"
                st.write(f"Score: {home_score} (Home) vs {away_score} (Away)")
                st.write(f"Delta: {delta}")
                st.write(f"Status: {status}")
        else:
            st.error("Invalid team selection. Please select a valid team.")
    else:
        st.write("No matchups available for the selected week.")