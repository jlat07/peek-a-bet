from utils.ticket import Ticket

class TicketManager:
    def __init__(self):
        self.tickets = {}
        self.ticket_order = []

    def add_ticket(self, matchups, bets):
        ticket_id = len(self.tickets) + 1
        new_ticket = Ticket(ticket_id, matchups, bets)
        new_ticket.validate()
        self.tickets[ticket_id] = new_ticket
        self.ticket_order.append(ticket_id)

    def get_ticket(self, ticket_id):
        return self.tickets.get(ticket_id)

    def ordered_tickets(self):
        return [self.tickets[ticket_id] for ticket_id in self.ticket_order]