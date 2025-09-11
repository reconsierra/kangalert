import streamlit as st
import folium
from streamlit_folium import folium_static
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import json

# Check if Firebase is already initialized
if not firebase_admin._apps:
    # Load Firebase credentials from Streamlit secrets
    firebase_credentials = st.secrets["firebase"]["json"]
    cred = credentials.Certificate(json.loads(firebase_credentials))
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.set_page_config(layout="wide")

st.title("Kangalert Rescue Admin Dashboard 🐾")
st.write("View all reported wildlife strikes and manage their status.")

# --- Fetch Data from Firestore ---
@st.cache_data(ttl=60) # Cache the data for 60 seconds
def get_reports():
    reports_ref = db.collection('reports').stream()
    reports = []
    for doc in reports_ref:
        report_data = doc.to_dict()
        report_data['id'] = doc.id
        reports.append(report_data)
    return reports

reports = get_reports()

# --- Map Visualization ---
st.header("Report Map")
if reports:
    # Convert reports to a pandas DataFrame for easier handling
    reports_df = pd.DataFrame(reports)

    # Create a map centered on the average location of reports
    avg_lat = reports_df['geoPoint'].apply(lambda x: x.latitude).mean()
    avg_lon = reports_df['geoPoint'].apply(lambda x: x.longitude).mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

    # Add a marker for each report
    for index, row in reports_df.iterrows():
        folium.Marker(
            location=[row['geoPoint'].latitude, row['geoPoint'].longitude],
            popup=f"Animal: {row['animalType']}<br>Status: {row['status']}<br>Condition: {row['condition']}",
            tooltip=row['animalType']
        ).add_to(m)

    folium_static(m)
else:
    st.info("No reports have been submitted yet.")

# --- Data Table and Analytics ---
st.header("Report Details")
if reports:
    # Prepare data for the table, converting GeoPoint to a readable format
    reports_df['latitude'] = reports_df['geoPoint'].apply(lambda x: x.latitude)
    reports_df['longitude'] = reports_df['geoPoint'].apply(lambda x: x.longitude)

    # Drop the geopoint column as it is not needed in the table
    reports_df = reports_df.drop(columns=['geoPoint'])

    # Display the data table
    st.dataframe(reports_df)

    # Add basic analytics
    st.header("Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Reports by Animal Type")
        animal_counts = reports_df['animalType'].value_counts()
        st.bar_chart(animal_counts)
    with col2:
        st.subheader("Reports by Condition")
        condition_counts = reports_df['condition'].value_counts()
        st.bar_chart(condition_counts)
