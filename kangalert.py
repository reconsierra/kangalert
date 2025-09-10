
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="Kangalert", layout="wide")

st.title("🦘 Kangalert – Wildlife Strike Reporting App")

# Sidebar for user profile/settings
st.sidebar.header("Profile / Settings")
rescue_service = st.sidebar.selectbox("Select your preferred rescue service", ["Wildlife Rescue NSW", "WIRES", "Local Rescue Team"])
display_mode = st.sidebar.radio("Visual mode", ["Light", "Dark"])
screen_name = st.sidebar.text_input("Screen name (optional)")
anonymous = st.sidebar.checkbox("Report anonymously", value=False)

st.sidebar.markdown("---")
st.sidebar.header("Rescue Admin Settings")
admin_phone = st.sidebar.text_input("Contact phone number")
admin_name = st.sidebar.text_input("Rescue admin name")
admin_hours = st.sidebar.text_input("Available hours")
volunteer_list = st.sidebar.text_area("Add validated volunteer helpers (comma-separated)")

st.markdown("### 📍 Report a Wildlife Strike")

# Wildlife strike form
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
        st.write("Alert sent to rescue service:", rescue_service)
        st.write("Timestamp:", timestamp)
        if photo:
            st.image(photo, caption="Uploaded photo", use_column_width=True)

st.markdown("### 🗺️ Map of Reported Strikes")

# Sample map with folium
m = folium.Map(location=[-33.86, 151.20], zoom_start=6)
folium.Marker(location=[-33.86, 151.20], popup="Kangaroo strike reported", tooltip="Existing report").add_to(m)
st_data = st_folium(m, width=700)

st.markdown("### 🚨 Rescue Service Dashboard")
st.write("View new and current reports, send status updates, and call volunteers.")

status_update = st.selectbox("Send status update", ["Rescue dispatched", "Animal deceased", "Joey recovered"])
broadcast = st.checkbox("Broadcast signal to local volunteers")
if st.button("Send Update"):
    st.success(f"Status update sent: {status_update}")
    if broadcast:
        st.info("Volunteer signal broadcasted.")

st.markdown("### 🔥 Hotspot Reporting & Analytics")
st.write("Visualise strike frequency, outcomes, and patterns.")

# Sample data for export
data = pd.DataFrame({
    "Location": ["Highway A", "Road B", "Track C"],
    "Strikes": [12, 7, 4],
    "Rescued": [5, 2, 1]
})
st.dataframe(data)

if st.button("Export CSV"):
    data.to_csv("kangalert_hotspots.csv", index=False)
    st.success("CSV report exported.")

st.markdown("### 🔒 Privacy & Data Handling")
st.write("Minimal personal data collected. Location used only for mapping. Anonymous reporting supported.")
