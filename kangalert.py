
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="Kangalert", layout="wide")
st.title("🦘 Kangalert – Wildlife Strike Reporting & Rescue")

# --- Access Control ---
st.sidebar.header("User Mode")
user_mode = st.sidebar.radio("Select mode", ["Public User", "Rescuer"])

# --- Geolocation ---
user_location = streamlit_js_eval(
    js_expressions="navigator.geolocation.getCurrentPosition((pos) => [pos.coords.latitude, pos.coords.longitude])",
    key="get_user_location"
)
default_location = [-33.86, 151.20]  # Fallback to Sydney
if user_location and isinstance(user_location, list) and len(user_location) == 2:
    default_location = user_location

# --- Shared Map ---
st.subheader("🗺️ Wildlife Strike Map")
m = folium.Map(location=default_location, zoom_start=12)
folium.Marker(location=default_location, popup="Your location", tooltip="Current position").add_to(m)
st_folium(m, width=700)

# --- Public User Mode ---
if user_mode == "Public User":
    st.subheader("📍 Report a Wildlife Strike")
    with st.form("public_form"):
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
            st.write("Timestamp:", timestamp)
            if photo:
                st.image(photo, caption="Uploaded photo", use_column_width=True)

    st.subheader("🔒 Privacy & Data Handling")
    st.write("Minimal personal data collected. Location used only for mapping. Anonymous reporting supported.")

# --- Rescuer Mode ---
if user_mode == "Rescuer":
    st.sidebar.header("Rescuer Access")
    access_code = st.sidebar.text_input("Enter admin access code", type="password")
    if access_code == "kangarescue":  # Replace with secure method in production
        st.success("Access granted.")
        st.subheader("📂 Report Management")
        st.write("View and manage incoming reports.")
        st.button("View New Reports")
        st.button("View Current Reports")

        status_update = st.selectbox("Send status update", ["Rescue dispatched", "Animal deceased", "Joey recovered"])
        broadcast = st.checkbox("Broadcast signal to local volunteers")
        if st.button("Send Update"):
            st.success(f"Status update sent: {status_update}")
            if broadcast:
                st.info("Volunteer signal broadcasted.")

        st.subheader("➕ Submit a New Report")
        with st.form("rescue_form"):
            animal_type = st.selectbox("Animal type", ["Kangaroo", "Possum", "Wombat", "Bird", "Other"], key="rescue_animal")
            location_type = st.radio("Location", ["On road", "Off road"], key="rescue_location")
            condition = st.radio("Condition", ["Alive", "Deceased"], key="rescue_condition")
            size = st.radio("Size", ["Large", "Medium", "Small"], key="rescue_size")
            joey_present = st.selectbox("Joey Present", ["Yes", "No", "Unknown"], key="rescue_joey")
            can_remain = st.radio("Can you remain with the animal?", ["Yes", "No"], key="rescue_remain")
            notes = st.text_area("Optional notes", key="rescue_notes")
            photo = st.file_uploader("Optional photo upload", type=["jpg", "jpeg", "png"], key="rescue_photo")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            submitted = st.form_submit_button("Submit Report")

            if submitted:
                st.success("Report submitted successfully.")
                st.write("Timestamp:", timestamp)
                if photo:
                    st.image(photo, caption="Uploaded photo", use_column_width=True)

        st.subheader("📊 Hotspot Reporting & Analytics")
        data = pd.DataFrame({
            "Location": ["Highway A", "Road B", "Track C"],
            "Strikes": [12, 7, 4],
            "Rescued": [5, 2, 1]
        })
        st.dataframe(data)
        if st.button("Export CSV"):
            data.to_csv("kangalert_hotspots.csv", index=False)
            st.success("CSV report exported.")
    else:
        st.warning("Enter a valid access code to unlock rescuer tools.")
