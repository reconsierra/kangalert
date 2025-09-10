
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="Kangalert", layout="wide")
st.title("🦘 Kangalert – Wildlife Strike Reporting")

# Get user's current location
user_location = streamlit_js_eval(
    js_expressions="navigator.geolocation.getCurrentPosition((pos) => [pos.coords.latitude, pos.coords.longitude])",
    key="get_user_location"
)

# Sidebar
st.sidebar.header("Profile / Settings")
rescue_service = st.sidebar.selectbox("Preferred rescue service", ["Wildlife Rescue NSW", "WIRES", "Local Rescue Team"])
screen_name = st.sidebar.text_input("Screen name (optional)")
anonymous = st.sidebar.checkbox("Report anonymously", value=False)

# Report Form
st.subheader("📍 Report a Wildlife Strike")
with st.form("strike_form"):
    animal_type = st.selectbox("Animal type", ["Kangaroo", "Possum", "Wombat", "Bird", "Other"])
    location_type = st.radio("Location", ["On road", "Off road"])
    condition = st.radio("Condition", ["Alive", "Deceased"])
    size = st.radio("Size", ["Large", "Medium", "Small"])
    joey_present = st.selectbox("Joey Present", ["Yes", "No", "Unknown"])
    can_remain = st.radio("Can you remain with the animal?", ["Yes", "No"])
    notes = st.text_area("Optional notes")
    photo = st.file_uploader("Optional photo upload", type=["jpg", "jpeg", "png"])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    submitted = st.form_submit_button("Submit Report")

    if submitted:
        st.success("Report submitted successfully.")
        st.write("Alert sent to:", rescue_service)
        st.write("Timestamp:", timestamp)
        if photo:
            st.image(photo, caption="Uploaded photo", use_column_width=True)

# Map
st.subheader("🗺️ Map of Reported Strikes")
default_location = [-33.86, 151.20]  # Sydney fallback
if user_location and isinstance(user_location, list) and len(user_location) == 2:
    default_location = user_location

m = folium.Map(location=default_location, zoom_start=10)
folium.Marker(location=default_location, popup="Your location", tooltip="Current position").add_to(m)
st_folium(m, width=700)

# Privacy
st.subheader("🔒 Privacy & Data Handling")
st.write("Minimal personal data collected. Location used only for mapping. Anonymous reporting supported.")
