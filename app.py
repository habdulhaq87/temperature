import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
from streamlit_lottie import st_lottie
import json

# Set page configuration
st.set_page_config(
    page_title="Hourly Temperature Visualization",
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

@st.cache_data
def load_lottie_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Load the data
data = load_data(github_repo)

# Load a Lottie animation for better UI
temperature_animation = load_lottie_file("assets/temperature.json")

if data is not None:
    # Sidebar filters
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start Date", value=data['Timestamp'].min().date())
    end_date = st.sidebar.date_input("End Date", value=data['Timestamp'].max().date())
    view_ac_status = st.sidebar.checkbox("View Only AC Status ON", value=False)

    # Apply filters
    filtered_data = data[(data['Timestamp'].dt.date >= start_date) & (data['Timestamp'].dt.date <= end_date)]
    if view_ac_status:
        filtered_data = filtered_data[filtered_data['AC_Status'] == 1]

    # Main content
    st.title("Hourly Temperature Visualization 🌡️")
    st.markdown(
        "This app visualizes hourly temperature readings along with AC and fan statuses."
    )

    # Add Lottie animation
    st_lottie(temperature_animation, height=200, key="temp")

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

    # Data table
    st.subheader("Filtered Data Table")
    st.dataframe(filtered_data, use_container_width=True)

    # Summary section
    st.subheader("Summary")
    avg_temp = filtered_data['Temperature'].mean()
    ac_on_count = filtered_data['AC_Status'].sum()
    st.write(f"Average Temperature: {avg_temp:.2f} °C")
    st.write(f"Number of Times AC was ON: {ac_on_count}")
else:
    st.error("Unable to load the dataset. Please check the GitHub repository URL.")
