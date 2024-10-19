from supabase import create_client
import streamlit as st

def get_supabase_client():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def fetch_tickets():
    supabase = get_supabase_client()
    response = supabase.table("tickets").select("*").execute()
    return response.data

def insert_ticket(ticket_data):
    supabase = get_supabase_client()
    response = supabase.table("tickets").insert(ticket_data).execute()
    return response.data