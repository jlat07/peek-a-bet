import streamlit as st
from utils.api_client import APIClient
from utils.ticket import Ticket
from utils.auth import authenticate, logout
import utils.data_and_config as config  # Import the entire module

# Set page configuration for dark theme
st.set_page_config(page_title="🏈 Parlay Check", page_icon="🏈", layout="wide")

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
    THEME_COLOR = config.THEME_COLOR
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: #1e1e1e;
        color: #ffffff;
    }}
    .stButton>button {{
        background-color: {THEME_COLOR};
        color: #ffffff;
    }}
    .bet-card {{
        border: 1px solid #444;
        padding: 10px;
        margin-bottom: 5px;
        background-color: #2e2e2e;
    }}
    .bet-card > span {{
        font-size: 20px;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Initialize API Client
    api_client = APIClient()

    # Function to Initialize Session State
    def initialize_session_state():
        if 'tickets' not in st.session_state:
            st.session_state.tickets = []
        if 'draft_ticket' not in st.session_state:
            st.session_state.draft_ticket = {'matchups': [], 'bets': []}
        if 'ticket_counter' not in st.session_state:
            st.session_state.ticket_counter = 1

    # Call the initialization function
    initialize_session_state()

    # Function to determine bet status and display accordingly
    def get_bet_status_color(bet_status):
        if bet_status in ["Currently Winning", "Won"]:
            return "green", "✅"
        elif bet_status in ["Currently Losing", "Lost"]:
            return "red", "❌"
        elif bet_status == "Currently Tied":
            return "yellow", "⚖️"
        else:
            return "gray", "⏳"

    # Display Finalized Tickets
    st.subheader("Your Tickets")
    if st.session_state.tickets:
        for idx, ticket in enumerate(st.session_state.tickets):
            st.markdown(f"## 🎟️ PARLAY CARD #{ticket.ticket_id}")
            for i, (matchup, bet) in enumerate(zip(ticket.matchups, ticket.bets)):
                bet_type = bet['type']
                selected_team = bet.get('team')
                bet_value = bet['value']

                # Fetch game score
                game_score = api_client.get_scores().get(matchup, {})
                home_team = game_score.get('home_team')
                away_team = game_score.get('away_team')
                home_score = game_score.get('home_score')
                away_score = game_score.get('away_score')
                bet_status = bet.get('status', 'Game Not Started')

                # Set colors based on status
                color, icon = get_bet_status_color(bet_status)

                if bet_type == "Spread":
                    # Spread bet logic
                    delta = (home_score + float(bet_value)) - away_score if selected_team == home_team else (away_score + float(bet_value)) - home_score
                    opponent_team = away_team if selected_team == home_team else home_team
                    st.markdown(f"""
                    <div class="bet-card" style="color:{color}">
                        {icon} {selected_team} {bet_value}  |  Score: ({home_score} + {bet_value}) vs {away_score} {opponent_team}  |  Delta: {delta:+.1f}  |  Status: {bet_status}
                    </div>
                    """, unsafe_allow_html=True)

                elif bet_type == "Total":
                    # Over/Under bet logic
                    total_score = home_score + away_score if home_score is not None and away_score is not None else 0
                    delta = total_score - float(bet_value)
                    st.markdown(f"""
                    <div class="bet-card" style="color:{color}">
                        {icon} {selected_team} {bet_value}  |  Total: ({home_score} + {away_score})  |  Delta: {delta:+.1f}  |  Status: {bet_status}
                    </div>
                    """, unsafe_allow_html=True)

            if st.button("Remove Ticket", key=f"remove_ticket_{ticket.ticket_id}"):
                st.session_state.tickets.pop(idx)
                st.success(f"Ticket {ticket.ticket_id} removed.")
                st.experimental_rerun()
    else:
        st.write("No finalized tickets.")

    # Manual Refresh Button
    st.subheader("Update Ticket Statuses")
    if st.button("Refresh"):
        with st.spinner("Updating scores and bet statuses..."):
            # Fetch scores and update bets
            game_scores = api_client.get_scores()
            for ticket in st.session_state.tickets:
                ticket.compute_outcome(game_scores)
        st.success("Scores and statuses updated!")