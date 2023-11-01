import streamlit as st
from utils.image_processor import ImageProcessor
from utils.ticket_manager import TicketManager
from utils.api_client import APIClient

# Initialize classes
image_processor = ImageProcessor()
ticket_manager = TicketManager()
api_client = APIClient()

# Main app interface
st.title("Peek-A-Bet: Parlay Ticket Checker")

uploaded_file = st.file_uploader("Upload an image")

if uploaded_file:
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    st.write("Extracted Text:")
    extracted_text = process_image_and_extract_text(uploaded_file)
    st.text(extracted_text)

# # Section for uploading or capturing a ticket
# with st.expander("Add a Parlay Ticket"):
#     uploaded_image = st.file_uploader("Upload your parlay ticket", type=["jpg", "jpeg", "png"])
#     if uploaded_image:
#         ticket_data = image_processor.process_image(uploaded_image)
#         if ticket_data:  # Ensure there's valid data before adding
#             ticket_manager.add_ticket(ticket_data)
#             st.success("Ticket added successfully!")
#         else:
#             st.warning("Unable to process ticket. Please try another image.")

# # Section for displaying all tickets and their status
# with st.expander("Your Tickets", expanded=True):
#     tickets = ticket_manager.get_all_tickets()
#     if not tickets:
#         st.info("You have not added any tickets.")
#     for ticket in tickets:
#         ticket.display()
#         if st.button(f"Delete Ticket {ticket.id}"):
#             ticket_manager.remove_ticket(ticket.id)
#             st.experimental_rerun()  # Refresh the page

# # Section for refreshing the game data and calculating results
# with st.expander("Actions"):
#     if st.button("Refresh Game Data"):
#         # Ideally, loop through each ticket and update its game data
#         for ticket in tickets:
#             ticket.refresh_data(api_client)  # This assumes Ticket has a method to update its data
#         st.success("Game data refreshed!")
#     if st.button("Clear All Tickets"):
#         if st.confirm("Are you sure you want to clear all tickets?"):
#             ticket_manager.clear_all_tickets()
#             st.experimental_rerun()

# Display a counter for winning tickets
winning_tickets = sum(1 for ticket in tickets if ticket.is_winning())  # Assumes Ticket has an `is_winning` method
st.sidebar.title("Statistics")
st.sidebar.markdown(f"**Winning Tickets:** {winning_tickets}")
st.sidebar.markdown(f"**Total Tickets:** {len(tickets)}")

# Additional UI/UX features can be added as per requirements.

# Running the app will display the UI and allow users to interact with their tickets.
