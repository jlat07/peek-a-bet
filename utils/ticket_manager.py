import streamlit as st
from ticket import Ticket

class TicketManager:
    def __init__(self):
        # Retrieve the tickets from the session state or initialize an empty list
        if 'tickets' not in st.session_state:
            st.session_state.tickets = []

    def add_ticket(self, ticket_data):
        """Add a new ticket to the session."""
        ticket = Ticket(ticket_data)
        st.session_state.tickets.append(ticket)

    def remove_ticket(self, ticket_id):
        """Remove a ticket from the session based on its ID."""
        st.session_state.tickets = [ticket for ticket in st.session_state.tickets if ticket.id != ticket_id]

    def get_all_tickets(self):
        """Return all tickets in the current session."""
        return st.session_state.tickets

    def clear_all_tickets(self):
        """Clear all tickets from the session."""
        st.session_state.tickets = []

    def display_tickets(self):
        """Display all tickets and their current status."""
        for ticket in st.session_state.tickets:
            ticket.display()
