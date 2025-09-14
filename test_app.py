import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Load Firebase credentials from Streamlit secrets
try:
    if not firebase_admin._apps:
        firebase_credentials = st.secrets.firebase.json
        cred = credentials.Certificate(json.loads(firebase_credentials))
        firebase_admin.initialize_app(cred)
        st.success("Firebase credentials loaded successfully!")
except Exception as e:
    st.error(f"Error loading Firebase credentials: {e}")
    st.stop()
