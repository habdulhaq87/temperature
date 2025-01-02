import streamlit as st
import pandas as pd
import requests
from io import StringIO

# GitHub raw URL for the CSV file
github_repo = "https://raw.githubusercontent.com/habdulhaq87/temperature/main/Hourly_Temperature_Readings_Dataset.csv"
local_file = "Hourly_Temperature_Readings_Dataset.csv"  # Local copy

def load_existing_data(url):
    """Loads the existing dataset from GitHub."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        data = pd.read_csv(csv_data)
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Ensure Timestamp is datetime
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load data from GitHub: {e}")
        return pd.DataFrame()

def add_row(data, timestamp, temperature, ac_status, fan_status):
    """Adds a new row to the dataset."""
    new_row = {
        "Timestamp": pd.to_datetime(timestamp),
        "Temperature": float(temperature),
        "AC_Status": int(ac_status),
        "Fan_Status": int(fan_status)
    }
    return data.append(new_row, ignore_index=True)

def save_updated_data(data, file_path):
    """Saves the updated dataset locally."""
    data.to_csv(file_path, index=False)
    st.success(f"Updated dataset saved to {file_path}")

# Load existing data
st.title("Update Dataset")
st.markdown("Use this tool to manually add rows to the dataset.")

data = load_existing_data(github_repo)

if not data.empty:
    st.success("Dataset loaded successfully!")

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
            data = add_row(data, timestamp, temperature, ac_status, fan_status)
            save_updated_data(data, local_file)
        except Exception as e:
            st.error(f"Failed to add row: {e}")

    # Display the updated dataset
    st.subheader("Updated Dataset Preview")
    st.dataframe(data.tail(10))  # Show last 10 rows
else:
    st.error("Failed to load the dataset. Please check the GitHub repository URL.")
