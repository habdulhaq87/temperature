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
local_file = "Hourly_Temperature_Readings_Dataset.csv"  # Local copy for updates

@st.cache_data
def load_data(url):
    """Fetch the dataset from GitHub."""
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

# Function to add a row
def add_row_to_data(data, timestamp, temperature, ac_status, fan_status):
    """Adds a new row to the dataset."""
    new_row = {
        "Timestamp": pd.to_datetime(timestamp),
        "Temperature": float(temperature),
        "AC_Status": int(ac_status),
        "Fan_Status": int(fan_status)
    }
    return data.append(new_row, ignore_index=True)

# Load the data
data = load_data(github_repo)

# Main application with multiple pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Analysis", "Input Data"])

if page == "Analysis":
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

        # Notify about updates
        st.info("Note: If you add new rows using the input page, refresh the app to see the updated dataset.")
    else:
        st.error("Unable to load the dataset. Please check the GitHub repository URL.")

elif page == "Input Data":
    st.title("Input Data")
    st.markdown("""
    Use this page to manually add new rows to the dataset. The changes will be applied to the local dataset.
    """)

    if data is not None:
        # Timestamp selection using date and time input
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Select Date")
        with col2:
            time = st.time_input("Select Time")
        timestamp = pd.Timestamp.combine(date, time)

        # Temperature control using slider
        temperature = st.slider(
            "Temperature (°C)", 
            min_value=-50.0, 
            max_value=50.0, 
            value=25.0, 
            step=0.1
        )

        # AC and Fan status using toggle buttons
        col3, col4 = st.columns(2)
        with col3:
            ac_status = st.radio("AC Status", options=[1, 0], format_func=lambda x: "ON" if x == 1 else "OFF")
        with col4:
            fan_status = st.radio("Fan Status", options=[1, 0], format_func=lambda x: "ON" if x == 1 else "OFF")

        # Add row to the dataset
        if st.button("Add Row"):
            try:
                data = add_row_to_data(data, timestamp, temperature, ac_status, fan_status)
                data.to_csv(local_file, index=False)
                st.success("Row added successfully!")
            except Exception as e:
                st.error(f"Failed to add row: {e}")

        # Show the updated dataset
        st.subheader("Updated Dataset Preview")
        st.dataframe(data.tail(10))  # Show last 10 rows
    else:
        st.error("Unable to load the dataset. Please check the GitHub repository URL.")
