import streamlit as st
import pandas as pd
import requests
from io import StringIO
from ux import render_filters, render_statistics, render_temperature_chart, render_filtered_dataset
from input import update_database, DATABASE_PATH

# Set page configuration
st.set_page_config(
    page_title="Hourly Temperature Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GitHub raw URL for the CSV file (used as backup)
github_repo = "https://raw.githubusercontent.com/habdulhaq87/temperature/main/Hourly_Temperature_Readings_Dataset.csv"

@st.cache_data
def load_data():
    """Loads data from the local database or GitHub repository."""
    try:
        data = pd.read_csv(DATABASE_PATH)
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        return data
    except FileNotFoundError:
        # Fallback to GitHub if local file is missing
        response = requests.get(github_repo)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        data = pd.read_csv(csv_data)
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        return data

# Load the data
data = load_data()

if data is not None:
    # Sidebar controls and filters
    start_date, end_date, view_ac_status, view_fan_status, temp_min, temp_max = render_filters(data)

    # Apply filters
    filtered_data = data[(data['Timestamp'].dt.date >= start_date) & (data['Timestamp'].dt.date <= end_date)]
    if view_ac_status:
        filtered_data = filtered_data[filtered_data['AC_Status'] == 1]
    if view_fan_status:
        filtered_data = filtered_data[filtered_data['Fan_Status'] == 1]
    filtered_data = filtered_data[(filtered_data['Temperature'] >= temp_min) & (filtered_data['Temperature'] <= temp_max)]

    # Main content
    st.title("Hourly Temperature Analysis")
    st.markdown("""
    This application provides an in-depth analysis of hourly temperature readings, including interactive visualizations, statistics, and dataset exploration.
    """)

    # Render components
    render_statistics(filtered_data)
    render_temperature_chart(filtered_data)
    render_filtered_dataset(filtered_data)

    # Download option
    st.download_button(
        label="Download Filtered Dataset",
        data=filtered_data.to_csv(index=False),
        file_name="filtered_temperature_data.csv",
        mime="text/csv"
    )

    # Update database functionality
    st.sidebar.header("Update Database")
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)
        update_database(new_data)
        st.sidebar.success("Database updated successfully! Please refresh the page to view changes.")
else:
    st.error("Unable to load the dataset. Please check the GitHub repository URL.")
