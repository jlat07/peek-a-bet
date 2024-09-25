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
        # Add other validation rules if necessary

    def compute_outcome(self, game_scores):
        for i, bet in enumerate(self.bets):
            bet_type = bet["type"].lower()
            bet_value = float(bet["value"])
            matchup = self.matchups[i]

            # Extract the corresponding game score
            game_score = game_scores.get(matchup)
            if not game_score:
                bet["status"] = "pending"
                continue

            # Check if the game is completed
            if not game_score['completed']:
                bet["status"] = "pending"
                continue

            # Get scores
            home_team = game_score['home_team']
            away_team = game_score['away_team']
            home_score = game_score['home_score']
            away_score = game_score['away_score']

            # Compute outcome
            if bet_type == "spread":
                selected_team = bet['team']
                if selected_team == home_team:
                    adjusted_score = home_score + bet_value
                    opponent_score = away_score
                elif selected_team == away_team:
                    adjusted_score = away_score + bet_value
                    opponent_score = home_score
                else:
                    bet["status"] = "invalid team"
                    continue

                bet["status"] = "win" if adjusted_score > opponent_score else "lose"

            elif bet_type == "over/under":
                total_score = home_score + away_score
                over_under_choice = bet['over_under']
                if over_under_choice == 'Over':
                    bet["status"] = "win" if total_score > bet_value else "lose"
                else:
                    bet["status"] = "win" if total_score < bet_value else "lose"
            else:
                bet["status"] = "pending"