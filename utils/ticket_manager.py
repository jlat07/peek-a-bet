# from utils.ticket import Ticket
# import streamlit as st

# class TicketManager:
#     def __init__(self):
#         self.tickets = {}
#         self.ticket_order = []

#     def add_ticket(self, matchups, bets):
#         if 'ticket_counter' not in st.session_state:
#             st.session_state.ticket_counter = 1
#         ticket_id = st.session_state.ticket_counter
#         st.session_state.ticket_counter += 1
#         new_ticket = Ticket(ticket_id, matchups, bets)
#         new_ticket.validate()
#         self.tickets[ticket_id] = new_ticket
#         self.ticket_order.append(ticket_id)

#     def get_ticket(self, ticket_id):
#         return self.tickets.get(ticket_id)

#     def ordered_tickets(self):
#         return [self.tickets[ticket_id] for ticket_id in self.ticket_order]

#     def remove_ticket(self, ticket_id):
#         if ticket_id in self.tickets:
#             del self.tickets[ticket_id]
#             self.ticket_order.remove(ticket_id)