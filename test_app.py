import streamlit as st
import json

try:
    firebase_credentials = st.secrets.firebase.json
    json.loads(firebase_credentials)
    st.success("Firebase credentials loaded successfully!")
except Exception as e:
    st.error(f"Error loading Firebase credentials: {e}")
    st.stop()
