import streamlit as st
from utils.auth import authenticate, logout
from utils.database import fetch_matchups, fetch_scores, save_finalized_ticket  # Replace API calls with DB functions
import utils.data_and_config as config
from utils.ticket import Ticket

# Set page configuration for dark theme
st.set_page_config(page_title="Parlay Check", page_icon="🏈", layout="wide")

# Initialize authentication
session = authenticate()

# If not logged in, show login form
if not session:
    st.warning("Please log in to access the app.")
else:
    st.success(f"Welcome, {session['user']['email']}!")

    # Logout button in the sidebar
    logout()

    # Theme configuration
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
        </style>
    """, unsafe_allow_html=True)

    # Initialize Session State for tickets
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

    # Fetch matchups from the database
    matchups_data = fetch_matchups()  # Replace API call with DB function
    
    # User selects matchup and bet details
    selected_week = st.selectbox('Select Week', ['Week 1', 'Week 2', 'Week 3'])
    selected_matchup = st.selectbox('Select Matchup', list(matchups_data.keys()))
    selected_bet_type = st.radio('Select Bet Type', ['Spread', 'Total'])

    bet_details = {'type': selected_bet_type}
    
    # Bet type logic (Spread or Total)
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

    # Add bet to draft
    if st.button("Add Bet"):
        st.session_state.draft_ticket['matchups'].append(selected_matchup)
        st.session_state.draft_ticket['bets'].append(bet_details)
        st.success("Bet added to draft ticket!")

    # Finalize the ticket
    def finalize_ticket():
        num_bets = len(st.session_state.draft_ticket['bets'])
        if 3 <= num_bets <= 10:
            ticket_id = st.session_state.ticket_counter
            st.session_state.ticket_counter += 1
            new_ticket = Ticket(ticket_id, st.session_state.draft_ticket['matchups'], st.session_state.draft_ticket['bets'])
            new_ticket.validate()

            # Save the finalized ticket to the database
            save_finalized_ticket(session['user']['id'], new_ticket)
            
            # Clear draft
            st.session_state.draft_ticket = {'matchups': [], 'bets': []}
            st.success(f"Ticket {ticket_id} finalized and saved!")
        else:
            st.error("A ticket must have between 3 and 10 bets.")

    if st.button("Finalize Ticket"):
        finalize_ticket()

    # Display finalized tickets
    st.subheader("Your Tickets")
    tickets = st.session_state.tickets
    if tickets:
        for idx, ticket in enumerate(tickets):
            st.markdown(f"## 🎟️ Ticket {ticket.ticket_id}")
            for i, (matchup, bet) in enumerate(zip(ticket.matchups, ticket.bets)):
                st.write(f"**Bet #{i + 1}:** {matchup} - {bet['type']} {bet['value']}")
    
    # Manual refresh for updating scores and ticket evaluation
    if st.button("Refresh"):
        with st.spinner("Updating scores and evaluating bets..."):
            scores = fetch_scores()  # Fetch the latest scores from the database
            for ticket in tickets:
                ticket.compute_outcome(scores)
            st.experimental_rerun()