import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO

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
    # Sidebar filters
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start Date", value=data['Timestamp'].min().date())
    end_date = st.sidebar.date_input("End Date", value=data['Timestamp'].max().date())
    view_ac_status = st.sidebar.checkbox("View Only AC Status ON", value=False)
    view_fan_status = st.sidebar.checkbox("View Only Fan Status ON", value=False)

    # Apply filters
    filtered_data = data[(data['Timestamp'].dt.date >= start_date) & (data['Timestamp'].dt.date <= end_date)]
    if view_ac_status:
        filtered_data = filtered_data[filtered_data['AC_Status'] == 1]
    if view_fan_status:
        filtered_data = filtered_data[filtered_data['Fan_Status'] == 1]

    # Main content
    st.title("Hourly Temperature Analysis")
    st.markdown("""
    This application provides an in-depth analysis of hourly temperature readings, including interactive visualizations, statistics, and dataset exploration.
    """)

    # Statistics
    st.subheader("Statistics")
    st.markdown("### General Stats")
    st.write(filtered_data.describe())

    # Line chart for temperature over time
    st.subheader("Temperature Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_data['Timestamp'], filtered_data['Temperature'], label='Temperature', color='blue')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Hourly Temperature Readings")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Dynamic parameters for temperature thresholds
    st.sidebar.header("Temperature Thresholds")
    temp_min = st.sidebar.slider("Minimum Temperature", float(filtered_data['Temperature'].min()), float(filtered_data['Temperature'].max()), float(filtered_data['Temperature'].min()))
    temp_max = st.sidebar.slider("Maximum Temperature", float(filtered_data['Temperature'].min()), float(filtered_data['Temperature'].max()), float(filtered_data['Temperature'].max()))

    filtered_by_temp = filtered_data[(filtered_data['Temperature'] >= temp_min) & (filtered_data['Temperature'] <= temp_max)]

    st.subheader("Filtered by Temperature Threshold")
    st.write(filtered_by_temp)

    # Dataset exploration
    st.subheader("Dataset Explorer")
    st.markdown("Use the table below to explore the full dataset.")
    st.dataframe(filtered_data, use_container_width=True)

    # Download option
    st.download_button(
        label="Download Filtered Dataset",
        data=filtered_data.to_csv(index=False),
        file_name="filtered_temperature_data.csv",
        mime="text/csv"
    )
else:
    st.error("Unable to load the dataset. Please check the GitHub repository URL.")
