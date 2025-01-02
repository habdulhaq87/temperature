import streamlit as st
import matplotlib.pyplot as plt

def render_filters(data):
    """Renders the sidebar filters."""
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start Date", value=data['Timestamp'].min().date())
    end_date = st.sidebar.date_input("End Date", value=data['Timestamp'].max().date())
    view_ac_status = st.sidebar.checkbox("View Only AC Status ON", value=False)
    view_fan_status = st.sidebar.checkbox("View Only Fan Status ON", value=False)
    temp_min = st.sidebar.slider(
        "Minimum Temperature", 
        float(data['Temperature'].min()), 
        float(data['Temperature'].max()), 
        float(data['Temperature'].min())
    )
    temp_max = st.sidebar.slider(
        "Maximum Temperature", 
        float(data['Temperature'].min()), 
        float(data['Temperature'].max()), 
        float(data['Temperature'].max())
    )
    return start_date, end_date, view_ac_status, view_fan_status, temp_min, temp_max

def render_statistics(filtered_data):
    """Displays the statistics of the dataset."""
    st.subheader("Statistics")
    st.markdown("### General Stats")
    st.write(filtered_data.describe())

def render_temperature_chart(filtered_data):
    """Displays a line chart for temperature over time."""
    st.subheader("Temperature Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_data['Timestamp'], filtered_data['Temperature'], label='Temperature', color='blue')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Hourly Temperature Readings")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

def render_filtered_dataset(filtered_data):
    """Displays the filtered dataset."""
    st.subheader("Dataset Explorer")
    st.markdown("Use the table below to explore the dataset.")
    st.dataframe(filtered_data, use_container_width=True)
