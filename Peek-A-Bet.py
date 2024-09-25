import streamlit as st
from streamlit_autorefresh import st_autorefresh
from utils.ticket_manager import TicketManager
from utils.api_client import APIClient
from utils.data_and_config import bet_types, spread_values, over_under_values

# Initialize Ticket Manager and API Client
ticket_manager = TicketManager()
api_client = APIClient()

# Setup Session State
if 'draft_ticket' not in st.session_state:
    st.session_state.draft_ticket = {
        'matchups': [],
        'bets': []
    }

if 'tickets' not in st.session_state:
    st.session_state.tickets = []

# User Input Function
def get_user_input():
    # Fetch available matchups dynamically
    with st.spinner("Fetching matchups..."):
        matchups_data = api_client.get_matchups()
    matchup_options = list(matchups_data.keys())

    if not matchup_options:
        st.error("No matchups available at the moment.")
        return None, None

    selected_matchup = st.selectbox('Select Matchup', matchup_options)
    selected_bet_type = st.selectbox('Bet Type', bet_types)

    bet_details = {'type': selected_bet_type}

    if selected_bet_type == 'Spread':
        selected_team = st.selectbox('Select Team', [
            matchups_data[selected_matchup]['home_team'],
            matchups_data[selected_matchup]['away_team']
        ])
        selected_value = st.selectbox('Select Spread', spread_values)
        bet_details['value'] = selected_value
        bet_details['team'] = selected_team
    else:
        over_under_choice = st.selectbox('Over or Under', ['Over', 'Under'])
        selected_value = st.selectbox('Select Over/Under Value', over_under_values)
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
        ticket_manager.add_ticket(st.session_state.draft_ticket['matchups'], st.session_state.draft_ticket['bets'])
        st.session_state.tickets = ticket_manager.ordered_tickets()
        st.session_state.draft_ticket = {
            'matchups': [],
            'bets': []
        }
        st.success("Ticket finalized!")
    else:
        st.warning("A ticket requires between 3 to 10 bets.")

# UI Elements and Logic
st.title("Peek-A-Bet")

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
        st.write(f"{matchup} - {bet['type']} {bet['value']}")
        if st.button("Remove Bet", key=f"remove_{idx}"):
            st.session_state.draft_ticket['matchups'].pop(idx)
            st.session_state.draft_ticket['bets'].pop(idx)
            st.experimental_rerun()
else:
    st.write("No bets in draft ticket.")

# Finalize Ticket Button
if st.button("Finalize Ticket"):
    finalize_ticket()

# Display Finalized Tickets
st.subheader("Your Tickets")
if st.session_state.tickets:
    for ticket in st.session_state.tickets:
        st.markdown(f"### Ticket ID: {ticket.ticket_id}")
        for matchup, bet in zip(ticket.matchups, ticket.bets):
            st.write(f"{matchup} - {bet['type']} {bet['value']}")
else:
    st.write("No finalized tickets.")

# Check Scores and Update Bet Statuses
st.subheader("Update Ticket Statuses")
if st.button("Check Scores"):
    with st.spinner("Fetching game scores..."):
        game_scores = api_client.get_scores()  # Fetch scores using the new method
        for ticket in st.session_state.tickets:
            ticket.compute_outcome(game_scores)
    st.success("Scores updated!")

    # Display tickets with updated bet statuses
    for ticket in st.session_state.tickets:
        st.markdown(f"### Ticket ID: {ticket.ticket_id}")
        for matchup, bet in zip(ticket.matchups, ticket.bets):
            bet_status = bet.get('status', 'pending')
            status_color = 'green' if bet_status == 'win' else 'red' if bet_status == 'lose' else 'gray'
            st.markdown(
                f"<div style='background-color: {status_color}; padding: 10px;'>{matchup} - {bet['type']} {bet['value']} - {bet_status.capitalize()}</div>",
                unsafe_allow_html=True
            )