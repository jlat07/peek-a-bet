class Ticket:
    def __init__(self, ticket_id, matchups, bets):
        self.ticket_id = ticket_id
        self.matchups = matchups  # List of matchup strings
        self.bets = bets          # List of bet dictionaries

    def display(self):
        bet_str = ', '.join([f"{bet['type']} {bet['value']}" for bet in self.bets])
        return f"Ticket ID: {self.ticket_id}\nMatchups: {', '.join(self.matchups)}\nBets: {bet_str}"

    def validate(self):
        if not self.matchups:
            raise ValueError("Matchups should not be empty!")
        if not self.bets:
            raise ValueError("Bets should not be empty!")
        # Additional validation rules can be added here

    def compute_outcome(self, game_scores):
        for i, bet in enumerate(self.bets):
            bet_type = bet["type"]
            bet_value = float(bet["value"])
            matchup = self.matchups[i]

            # Extract the corresponding game score
            game_score = game_scores.get(matchup)
            if not game_score:
                bet["status"] = "Game Not Started"
                continue

            # Get scores
            home_team = game_score['home_team']
            away_team = game_score['away_team']
            home_score = game_score['home_score']
            away_score = game_score['away_score']
            game_completed = game_score['completed']

            # Save scores in the bet dictionary
            bet['home_team'] = home_team
            bet['away_team'] = away_team
            bet['home_score'] = home_score
            bet['away_score'] = away_score

            # Check if scores are available
            if home_score is None or away_score is None:
                bet["status"] = "Game Not Started"
                continue

            # Compute outcome based on current scores
            if bet_type == 'Spread':
                selected_team = bet['team']
                if selected_team == home_team:
                    adjusted_home_score = home_score + bet_value
                    adjusted_away_score = away_score
                else:
                    adjusted_home_score = home_score
                    adjusted_away_score = away_score + bet_value

                delta = adjusted_home_score - adjusted_away_score
                bet['delta'] = delta

                if adjusted_home_score > adjusted_away_score:
                    bet["status"] = "Won" if game_completed else "Currently Winning"
                elif adjusted_home_score < adjusted_away_score:
                    bet["status"] = "Lost" if game_completed else "Currently Losing"
                else:
                    bet["status"] = "Tied" if game_completed else "Currently Tied"

            elif bet_type == 'Over/Under':
                total_score = home_score + away_score
                delta = total_score - bet_value
                bet['delta'] = delta

                if bet['over_under'] == 'Over':
                    if total_score > bet_value:
                        bet["status"] = "Won" if game_completed else "Currently Winning"
                    elif total_score < bet_value:
                        bet["status"] = "Lost" if game_completed else "Currently Losing"
                    else:
                        bet["status"] = "Tied" if game_completed else "Currently Tied"
                elif bet['over_under'] == 'Under':
                    if total_score < bet_value:
                        bet["status"] = "Won" if game_completed else "Currently Winning"
                    elif total_score > bet_value:
                        bet["status"] = "Lost" if game_completed else "Currently Losing"
                    else:
                        bet["status"] = "Tied" if game_completed else "Currently Tied"

            else:
                bet["status"] = "Unknown Bet Type"