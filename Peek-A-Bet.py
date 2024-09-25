import streamlit as st
from utils.api_client import APIClient
from utils.data_and_config import bet_types, spread_values, over_under_values, THEME_COLOR
from utils.ticket import Ticket

# Set page configuration for dark theme
st.set_page_config(page_title="Peek-A-Bet", page_icon="🎲", layout="wide", initial_sidebar_state="expanded")

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
    </style>
""", unsafe_allow_html=True)

# Initialize API Client
api_client = APIClient()

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
    else:
        # Validate editing_bet_index
        idx = st.session_state.editing_bet_index
        if idx is not None and idx >= len(st.session_state.draft_ticket['bets']):
            st.session_state.editing_bet_index = None

# Call the initialization function
initialize_session_state()

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
        ticket_id = st.session_state.ticket_counter
        st.session_state.ticket_counter += 1
        new_ticket = Ticket(ticket_id, st.session_state.draft_ticket['matchups'], st.session_state.draft_ticket['bets'])
        new_ticket.validate()
        st.session_state.tickets.append(new_ticket)
        st.session_state.draft_ticket = {
            'matchups': [],
            'bets': []
        }
        st.session_state.editing_bet_index = None  # Reset editing index
        st.success(f"Ticket #{ticket_id} finalized!")
    else:
        st.warning("A ticket requires between 3 to 10 bets.")

# Function to Edit Bet in Draft Ticket
def edit_bet_in_draft(idx):
    if idx is None or idx >= len(st.session_state.draft_ticket['matchups']):
        st.error("Invalid bet index. Unable to edit bet.")
        st.session_state.editing_bet_index = None
        return

    st.write(f"Editing Bet #{idx + 1}")
    selected_matchup = st.session_state.draft_ticket['matchups'][idx]
    bet_details = st.session_state.draft_ticket['bets'][idx]

    # Fetch matchups data
    matchups_data = api_client.get_matchups()

    # Matchup Selection (display only)
    st.markdown(f"**Matchup:** {selected_matchup}")

    # Bet Type Selection
    selected_bet_type = st.selectbox('Bet Type', bet_types, index=bet_types.index(bet_details['type']))

    updated_bet_details = {'type': selected_bet_type}

    if selected_bet_type == 'Spread':
        selected_team = st.selectbox('Select Team', [
            matchups_data[selected_matchup]['home_team'],
            matchups_data[selected_matchup]['away_team']
        ], index=[
            matchups_data[selected_matchup]['home_team'],
            matchups_data[selected_matchup]['away_team']
        ].index(bet_details['team']))
        selected_value = st.selectbox('Select Spread', spread_values, index=spread_values.index(float(bet_details['value'])))
        updated_bet_details['value'] = selected_value
        updated_bet_details['team'] = selected_team
    else:
        over_under_choice = st.selectbox('Over or Under', ['Over', 'Under'], index=['Over', 'Under'].index(bet_details['over_under']))
        selected_value = st.selectbox('Select Over/Under Value', over_under_values, index=over_under_values.index(float(bet_details['value'])))
        updated_bet_details['value'] = selected_value
        updated_bet_details['over_under'] = over_under_choice

    if st.button("Update Bet"):
        st.session_state.draft_ticket['bets'][idx] = updated_bet_details
        st.success("Bet updated!")
        st.session_state.editing_bet_index = None
        st.rerun()

    if st.button("Cancel Edit"):
        st.session_state.editing_bet_index = None
        st.rerun()

# UI Elements and Logic
st.title("🎲 Peek-A-Bet")

if st.session_state.editing_bet_index is not None:
    idx = st.session_state.editing_bet_index
    if idx < len(st.session_state.draft_ticket['bets']):
        edit_bet_in_draft(idx)
    else:
        st.session_state.editing_bet_index = None
        st.warning("The bet you're trying to edit no longer exists.")
else:
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
                # Adjust editing_bet_index if necessary
                if st.session_state.editing_bet_index is not None:
                    if st.session_state.editing_bet_index == idx:
                        st.session_state.editing_bet_index = None
                    elif st.session_state.editing_bet_index > idx:
                        st.session_state.editing_bet_index -= 1
                st.rerun()
else:
    st.write("No bets in draft ticket.")

# Finalize Ticket Button
if st.button("Finalize Ticket"):
    finalize_ticket()

st.info("Note: Finalized tickets cannot be edited. If you need to make changes, please remove the ticket and create a new one.")

# Display Finalized Tickets
st.subheader("Your Tickets")
if st.session_state.tickets:
    for idx, ticket in enumerate(st.session_state.tickets):
        st.markdown(f"## 🎟️ Ticket ID: {ticket.ticket_id}")
        for i, (matchup, bet) in enumerate(zip(ticket.matchups, ticket.bets)):
            bet_info = f"**Bet #{i + 1}:** {matchup} - {bet['type']} {bet['value']}"

            # Get bet status and delta
            bet_status = bet.get('status', 'Game Not Started')
            delta = bet.get('delta', None)

            # Get current scores
            game_score = api_client.get_scores().get(matchup, {})
            home_score = game_score.get('home_score')
            away_score = game_score.get('away_score')

            # Prepare score display
            if home_score is not None and away_score is not None:
                score_display = f"{game_score['home_team']} {home_score} - {away_score} {game_score['away_team']}"
            else:
                score_display = "Scores not available"

            # Prepare delta display
            if delta is not None:
                delta_display = f"Delta: {delta:+.1f}"
            else:
                delta_display = ""

            # Prepare status icon and color
            if bet_status in ["Currently Winning", "Won"]:
                status_icon = "✅"
                status_color = THEME_COLOR
            elif bet_status in ["Currently Losing", "Lost"]:
                status_icon = "❌"
                status_color = "#ff4d4d"
            elif bet_status == "Currently Tied":
                status_icon = "⚖️"
                status_color = "#ffd700"
            else:
                status_icon = "⏳"
                status_color = "#888888"

            # Combine all info
            bet_info_full = f"""
            <div style='border: 1px solid #444; padding: 10px; margin-bottom: 5px; background-color: #2e2e2e;'>
                <span style='color: {status_color}; font-size: 20px;'>{status_icon}</span>
                {bet_info}<br>
                <strong>Status:</strong> {bet_status}<br>
                <strong>Score:</strong> {score_display}<br>
                <strong>{delta_display}</strong>
            </div>
            """
            st.markdown(bet_info_full, unsafe_allow_html=True)
        if st.button("Remove Ticket", key=f"remove_ticket_{ticket.ticket_id}"):
            st.session_state.tickets.pop(idx)
            st.success(f"Ticket #{ticket.ticket_id} removed.")
            st.rerun()
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