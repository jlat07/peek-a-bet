# utils/auth.py

import streamlit as st
from streamlit_supabase_auth import Auth

# Supabase credentials
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")

# Initialize Supabase Auth
auth = Auth(SUPABASE_URL, SUPABASE_KEY)