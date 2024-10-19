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
        """
        Evaluates and updates the status of each bet based on current game scores.
        This function modifies the bet dictionaries within the ticket.
        """
        for i, bet in enumerate(self.bets):
            bet_type = bet["type"].lower()
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

            # Check if scores are available
            if home_score is None or away_score is None:
                bet["status"] = "Game Not Started"
                continue

            # Compute outcome based on current scores
            if bet_type == "spread":
                selected_team = bet['team']
                if selected_team == home_team:
                    adjusted_score = home_score + bet_value
                    opponent_score = away_score
                elif selected_team == away_team:
                    adjusted_score = away_score + bet_value
                    opponent_score = home_score
                else:
                    bet["status"] = "Invalid Team"
                    continue

                bet["delta"] = adjusted_score - opponent_score

                if adjusted_score > opponent_score:
                    bet["status"] = "Currently Winning"
                elif adjusted_score < opponent_score:
                    bet["status"] = "Currently Losing"
                else:
                    bet["status"] = "Currently Tied"

                # If the game is completed, set final status
                if game_score.get('completed', False):
                    bet["status"] = "Won" if adjusted_score > opponent_score else "Lost"

            elif bet_type == "total":
                total_score = home_score + away_score
                over_under_choice = bet['over_under'].lower()
                bet["delta"] = total_score - bet_value

                if over_under_choice == 'over':
                    if total_score > bet_value:
                        bet["status"] = "Currently Winning"
                    elif total_score < bet_value:
                        bet["status"] = "Currently Losing"
                    else:
                        bet["status"] = "Currently Tied"
                else:
                    if total_score < bet_value:
                        bet["status"] = "Currently Winning"
                    elif total_score > bet_value:
                        bet["status"] = "Currently Losing"
                    else:
                        bet["status"] = "Currently Tied"

                # If the game is completed, set final status
                if game_score.get('completed', False):
                    if over_under_choice == 'over':
                        bet["status"] = "Won" if total_score > bet_value else "Lost"
                    else:
                        bet["status"] = "Won" if total_score < bet_value else "Lost"
            else:
                bet["status"] = "Invalid Bet Type"