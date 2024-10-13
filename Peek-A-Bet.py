import streamlit as st
from utils.api_client import APIClient
from utils.ticket import Ticket
from utils.auth import authenticate, logout
import utils.data_and_config as config  # Import the entire module

# Set page configuration for dark theme
st.set_page_config(page_title="Peek-A-Bet", page_icon="🎟️", layout="wide")

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
        </style>
    """)

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

    # User Input Function
    def get_user_input():
        # Fetch available matchups dynamically
        with st.spinner("Fetching matchups..."):
            matchups_data = api_client.get_matchups() if not config.USE_MOCK_DATA else config.mock_matchups
        matchup_options = list(matchups_data.keys())

        if not matchup_options:
            st.error("No matchups available at the moment.")
            return None, None

        selected_matchup = st.selectbox('Select Matchup', matchup_options)
        selected_bet_type = st.selectbox('Bet Type', config.bet_types)

        bet_details = {'type': selected_bet_type}

        if selected_bet_type == 'Spread':
            selected_team = st.selectbox('Select Team', [
                matchups_data[selected_matchup]['home_team'],
                matchups_data[selected_matchup]['away_team']
            ])
            selected_value = st.selectbox('Select Spread', config.spread_values)
            bet_details['value'] = selected_value
            bet_details['team'] = selected_team
        else:
            over_under_choice = st.selectbox('Over or Under', ['Over', 'Under'])
            selected_value = st.selectbox('Select Over/Under Value', config.over_under_values)
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

    # Display finalized tickets
    st.subheader("Your Tickets")
    if st.session_state.tickets:
        for idx, ticket in enumerate(st.session_state.tickets):
            st.markdown(f"## 🎟️ Ticket {ticket.ticket_id}")
            for i, (matchup, bet) in enumerate(zip(ticket.matchups, ticket.bets)):
                bet_info = f"**Bet #{i + 1}:** {matchup} - {bet['type']} {bet['value']}"

                # Get bet status and delta
                bet_status = bet.get('status', 'Game Not Started')
                delta = bet.get('delta', None)

                # Get current scores
                game_score = api_client.get_scores().get(matchup, {}) if not config.USE_MOCK_DATA else config.mock_scores.get(matchup, {})
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

                # Additional info for bets
                if home_score is not None and away_score is not None:
                    if bet['type'] == 'Over/Under':
                        total_score = home_score + away_score
                        extra_info = f"Total Score: {total_score}, Over/Under: {bet['value']}"
                    elif bet['type'] == 'Spread':
                        selected_team = bet.get('team')
                        extra_info = f"Selected Team: {selected_team}, Spread: {bet['value']}"
                    else:
                        extra_info = ""
                else:
                    extra_info = ""

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

                # Combine all info in the desired order
                bet_info_full = f"""
                <div style='border: 1px solid #444; padding: 10px; margin-bottom: 5px; background-color: #2e2e2e;'>
                    <span style='color: {status_color}; font-size: 20px;'>{status_icon}</span>
                    {bet_info}<br>
                    <strong>Score:</strong> {score_display}<br>
                    <strong>{extra_info}</strong><br>
                    <strong>{delta_display}</strong><br>
                    <strong>Status:</strong> {bet_status}
                </div>
                """
                st.markdown(bet_info_full, unsafe_allow_html=True)
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
            game_scores = api_client.get_scores() if not config.USE_MOCK_DATA else config.mock_scores
            for ticket in st.session_state.tickets:
                ticket.compute_outcome(game_scores)
        st.success("Scores and statuses updated!")