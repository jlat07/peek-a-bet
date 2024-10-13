# utils/auth.py

import os
import streamlit as st
from streamlit_supabase_auth import login_form, logout_button

# Supabase credentials
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv('SUPABASE_URL')
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv('SUPABASE_KEY')

def authenticate():
    session = login_form(
        url=SUPABASE_URL,
        apiKey=SUPABASE_KEY,
        providers=["apple", "facebook", "github", "google"],
    )
    if not session:
        return None

    # Update query param to reset URL fragments
    st.experimental_set_query_params(page=["success"])
    return session

def logout():
    with st.sidebar:
        logout_button()