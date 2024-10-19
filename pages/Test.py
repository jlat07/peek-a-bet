import streamlit as st
from utils.api_client import APIClient
from utils.ticket import Ticket
from utils.auth import authenticate, logout
import utils.data_and_config as config
#from utils.database import fetch_tickets, insert_ticket

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

    THEME_COLOR = config.THEME_COLOR  # Use theme color from config
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

    def get_user_input():
        # Fetch available matchups dynamically
        with st.spinner("Fetching matchups..."):
            matchups_data = api_client.get_matchups()
        matchup_options = list(matchups_data.keys())

        if not matchup_options:
            st.error("No matchups available at the moment.")
            return None, None

        selected_week = st.selectbox('Select Week', ['Week 1', 'Week 2', 'Week 3'])
        selected_matchup = st.selectbox('Select Team', matchup_options)
        selected_bet_type = st.radio('Select Bet Type', ['Spread', 'Total'])

        bet_details = {'type': selected_bet_type}

        if selected_bet_type == 'Spread':
            selected_team = st.selectbox('Select Team', [
                matchups_data[selected_matchup]['home_team'],
                matchups_data[selected_matchup]['away_team']
            ])
            selected_value = st.number_input('Enter Spread Value', min_value=-100.0, max_value=100.0, step=0.5)
            bet_details['value'] = selected_value
            bet_details['team'] = selected_team
        else:
            over_under_choice = st.radio('Over or Under', ['Over', 'Under'])
            selected_value = st.number_input('Enter Over/Under Value', min_value=0, step=0.5)
            bet_details['value'] = selected_value
            bet_details['over_under'] = over_under_choice

        return selected_matchup, bet_details

    # Function to Initialize Session State
    def initialize_session_state():
        if 'draft_ticket' not in st.session_state:
            st.session_state.draft_ticket = {
                'matchups': [],
                'bets': []
            }
        if 'tickets' not in st.session_state:
            st.session_state.tickets = []
        if 'ticket_counter' not in st.session_state:
            st.session_state.ticket_counter = 1
        if 'editing_bet_index' not in st.session_state:
            st.session_state.editing_bet_index = None

    # Initialize session state
    initialize_session_state()

    # Function to Add Bet to Draft
    def add_bet_to_draft(selected_matchup, bet_details):
        st.session_state.draft_ticket['matchups'].append(selected_matchup)
        st.session_state.draft_ticket['bets'].append(bet_details)

    # Add Bet Button
    selected_matchup, bet_details = get_user_input()
    if st.button("Add Bet"):
        if selected_matchup and bet_details:
            add_bet_to_draft(selected_matchup, bet_details)
            st.success("Bet added to draft ticket!")

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

    if st.button("Finalize Ticket"):
        finalize_ticket()

    st.info("Note: Finalized tickets cannot be edited. If you need to make changes, please remove the ticket and create a new one.")

    # Display Finalized Tickets
    st.subheader("Your Tickets")
    if st.session_state.tickets:
        for idx, ticket in enumerate(st.session_state.tickets):
            st.markdown(f"## 🎟️ Ticket {ticket.ticket_id}")
            
            # Use the computed outcome and display status from Ticket class
            for i, (matchup, bet) in enumerate(zip(ticket.matchups, ticket.bets)):
                bet_info = f"**Bet #{i + 1}:** {matchup} - {bet['type']} {bet['value']}"
                status_icon = "⏳" if bet['status'] == "Game Not Started" else ("✅" if bet['status'] == "Won" else "❌")
                st.markdown(f"{status_icon} {bet_info} - Status: {bet['status']}")

            if st.button("Remove Ticket", key=f"remove_ticket_{ticket.ticket_id}"):
                st.session_state.tickets.pop(idx)
                st.success(f"Ticket {ticket.ticket_id} removed.")
                st.experimental_rerun()
    else:
        st.write("No finalized tickets.")

    st.subheader("Update Ticket Statuses")
    if st.button("Refresh"):
        with st.spinner("Updating scores and bet statuses..."):
            # Fetch the latest scores from the API (mock data in this case)
            game_scores = api_client.get_scores()
            for ticket in st.session_state.tickets:
                ticket.compute_outcome(game_scores)  # Ticket now handles its own status updates
            st.experimental_rerun()