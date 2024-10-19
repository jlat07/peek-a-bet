import streamlit as st
from utils.api_client import APIClient
from utils.ticket import Ticket
from utils.auth import authenticate, logout
import utils.data_and_config as config  # Import the entire module
from utils.db import fetch_tickets, insert_ticket  # Import database functions

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

    # Main app logic after login goes here...
    THEME_COLOR = config.THEME_COLOR  # Use the theme color from config

    # Apply custom CSS for dark theme and neon colors
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
    .stButton.remove-bet>button {{
        background-color: #ff4b4b;  /* Red for Remove Bet */
        color: #ffffff;
    }}
    .stButton.edit-bet>button {{
        background-color: #1e90ff;  /* Blue for Edit Bet */
        color: #ffffff;
    }}
    .stButton.finalize-bet>button {{
        background-color: #32cd32;  /* Green for Finalize Bet */
        color: #ffffff;
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

    # Simulated Weeks and Teams for Mock Data
    mock_weeks = {
        "Week 5": {
            "Buccaneers vs Dolphins": {"home_team": "Buccaneers", "away_team": "Dolphins"},
            "Panthers vs Falcons": {"home_team": "Panthers", "away_team": "Falcons"},
        },
        "Week 6": {
            "Packers vs Bears": {"home_team": "Packers", "away_team": "Bears"},
            "Raiders vs Broncos": {"home_team": "Raiders", "away_team": "Broncos"},
        }
    }

    # Function to Simulate Matchups by Week
    def get_matchups_by_week(selected_week):
        return mock_weeks.get(selected_week, {})

    # User Input Function
    def get_user_input():
        # Select Week
        selected_week = st.selectbox("Select Week", list(mock_weeks.keys()))

        # Fetch matchups dynamically based on selected week
        matchups_data = get_matchups_by_week(selected_week)
        matchup_options = list(matchups_data.keys())

        if not matchup_options:
            st.error("No matchups available at the moment.")
            return None, None

        selected_matchup = st.selectbox('Select Team', matchup_options)

        # Bet Type Selection (Spread or Total)
        bet_type = st.radio('Select Bet Type', ['Spread', 'Total'], horizontal=True)

        bet_details = {'type': bet_type}

        # Input Bet Value
        if bet_type == 'Spread':
            selected_team = st.selectbox('Select Team', [
                matchups_data[selected_matchup]['home_team'],
                matchups_data[selected_matchup]['away_team']
            ])
            selected_value = st.number_input('Enter Spread Value', min_value=-100.0, max_value=100.0, step=0.5)
            bet_details['value'] = selected_value
            bet_details['team'] = selected_team
        else:
            selected_value = st.number_input('Enter Total Value (Over/Under)', min_value=0.0, max_value=100.0, step=0.5)
            over_under_choice = st.selectbox('Over or Under', ['Over', 'Under'])
            bet_details['value'] = selected_value
            bet_details['over_under'] = over_under_choice

        return selected_matchup, bet_details

    # Function to Add Bet to Draft
    def add_bet_to_draft(selected_matchup, bet_details):
        st.session_state.draft_ticket['matchups'].append(selected_matchup)
        st.session_state.draft_ticket['bets'].append(bet_details)

    # Function to Finalize a Ticket
    def finalize_ticket():
        num_bets = len(st.session_state.draft_ticket['bets'])
        if 3 <= num_bets <= 10:
            ticket_id = st.session_state.ticket_counter
            st.session_state.ticket_counter += 1
            new_ticket = Ticket(ticket_id, st.session_state.draft_ticket['matchups'], st.session_state.draft_ticket['bets'])
            new_ticket.validate()
            st.session_state.tickets.append(new_ticket)
            st.session_state.draft_ticket = {'matchups': [], 'bets': []}
            st.success(f"Ticket {ticket_id} finalized!")
        else:
            st.error("A ticket must have between 3 and 10 bets.")

    # UI Elements and Logic
    st.title("🏈 Parlay Check")

    selected_matchup, bet_details = get_user_input()

    # Add Bet Button
    if st.button("Add Bet"):
        if selected_matchup and bet_details:
            add_bet_to_draft(selected_matchup, bet_details)
            st.success("Bet added to draft ticket!")

    # Display Draft Ticket
    st.subheader("Draft Ticket")
    if st.session_state.draft_ticket['bets']:
        for idx, (matchup, bet) in enumerate(zip(st.session_state.draft_ticket['matchups'], st.session_state.draft_ticket['bets'])):
            st.write(f"**Bet #{idx + 1}:** {matchup} - {bet['type']} {bet['value']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Edit Bet", key=f"edit_{idx}"):
                    st.session_state.editing_bet_index = idx
                    st.rerun()
            with col2:
                if st.button("Remove Bet", key=f"remove_{idx}"):
                    st.session_state.draft_ticket['matchups'].pop(idx)
                    st.session_state.draft_ticket['bets'].pop(idx)
                    st.rerun()
    else:
        st.write("No bets in draft ticket.")

    # Finalize Ticket Button
    if st.button("Finalize Ticket"):
        finalize_ticket()

    # Display Finalized Tickets
    st.subheader("Your Tickets")
    if st.session_state.tickets:
        for idx, ticket in enumerate(st.session_state.tickets):
            st.markdown(f"## 🎟️ Ticket {ticket.ticket_id}")
            for i, (matchup, bet) in enumerate(zip(ticket.matchups, ticket.bets)):
                bet_info = f"**Bet #{i + 1}:** {matchup} - {bet['type']} {bet['value']}"

                # Prepare status, score, and delta for bet
                st.write(bet_info)
    else:
        st.write("No finalized tickets.")