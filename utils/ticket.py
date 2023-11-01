from utils.api_client import APIClient

class Bet:
    def __init__(self, team, bet_type, value):
        self.team = team
        self.bet_type = bet_type  # 'OV', 'UN', '+', '-'
        self.value = value

class Ticket:
    def __init__(self, uuid, ticket_number, week, bets):
        self.uuid = uuid
        self.ticket_number = ticket_number
        self.week = week
        self.bets = bets  # A list of Bet objects
        self.status = "In Progress"
        self.deltas = []


    def update_status(self, game_data):
    # Assuming game_data is a dictionary containing data about each team's game.
    
        for i, team in enumerate(self.teams):
            current_score = game_data[team]['score']
            opponent_score = game_data[team]['opponent_score']
            
            adjusted_score = current_score + self.points[i]
            
            if adjusted_score > opponent_score:
                self.status = "Winning"
            else:
                self.status = "Losing"
            
            if game_data[team]['final']:
                self.status = "Final"
        
            # Calculate deltas for the team
            team_delta = adjusted_score - opponent_score
            self.deltas.append({'team': team, 'delta': team_delta})
            
            # Calculate deltas for over/under
            total_score = current_score + opponent_score
            total_delta = total_score - self.totals[i]
            self.deltas.append({'team': team, 'over_under_delta': total_delta})


    def display(self):
        # This method would typically return a formatted string or data structure for Streamlit display.
        display_data = {
            'ticket_id': self.ticket_id,
            'teams': self.teams,
            'points': self.points,
            'totals': self.totals,
            'status': self.status,
            'deltas': self.deltas
        }
        return display_data


    def check_status(self):
        api_client = APIClient()

        # Get live game data for teams on the ticket
        game_data = api_client.get_live_game_data(self.team_name)
        
        # Based on the game_data, determine the status of the ticket
        # For example:
        if game_data["current_score"] + self.bet_points > game_data["opponent_score"]:
            # The team is currently winning when considering the bet points
            self.status = "Winning"
        else:
            self.status = "Losing"
        #... Other logic based on the game data and ticket data
