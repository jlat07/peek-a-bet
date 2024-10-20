from supabase import create_client, Client
import os

# Fetching environment variables from your config or .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to fetch matchups from Supabase
def fetch_matchups():
    response = supabase.table('matchups').select("*").execute()
    data = response.data

    if data:
        matchups_dict = {}
        for row in data:
            matchup_key = f"{row['away_team']} vs {row['home_team']}"
            matchups_dict[matchup_key] = {
                'event_id': row['event_id'],
                'home_team': row['home_team'],
                'away_team': row['away_team'],
                'commence_time': row['commence_time'],
                'sport_key': row['sport_key']
            }
        return matchups_dict
    else:
        return {}

# Function to fetch scores from Supabase
def fetch_scores():
    response = supabase.table('scores').select("*").execute()
    data = response.data

    if data:
        scores_dict = {}
        for row in data:
            matchup_key = f"{row['away_team']} vs {row['home_team']}"
            scores_dict[matchup_key] = {
                'event_id': row['event_id'],
                'home_team': row['home_team'],
                'away_team': row['away_team'],
                'home_score': row['home_score'],
                'away_score': row['away_score'],
                'completed': row['completed'],
                'commence_time': row['commence_time']
            }
        return scores_dict
    else:
        return {}

# Function to save finalized tickets into Supabase
def save_finalized_ticket(user_id, ticket):
    ticket_data = {
        'user_id': user_id,
        'ticket_id': ticket.ticket_id,
        'matchups': str(ticket.matchups),
        'bets': str(ticket.bets)
    }
    response = supabase.table('tickets').insert(ticket_data).execute()
    return response.data