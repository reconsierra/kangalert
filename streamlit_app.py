import streamlit as st

st.title("Secret Test App")

try:
    test_value = st.secrets["test"]
    st.success(f"Successfully read secret: {test_value}")
except KeyError:
    st.error("Failed to read secret 'test'.")
