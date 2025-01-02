import streamlit as st
import pandas as pd
import requests
from io import StringIO
from ux import render_filters, render_statistics, render_temperature_chart, render_filtered_dataset

# Set page configuration
st.set_page_config(
    page_title="Hourly Temperature Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GitHub raw URL for the CSV file
github_repo = "https://raw.githubusercontent.com/habdulhaq87/temperature/main/Hourly_Temperature_Readings_Dataset.csv"

@st.cache_data
def load_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        data = pd.read_csv(csv_data)
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Ensure Timestamp is datetime
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load data from GitHub: {e}")
        return None

# Load the data
data = load_data(github_repo)

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
else:
    st.error("Unable to load the dataset. Please check the GitHub repository URL.")
