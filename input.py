import pandas as pd
from datetime import datetime
import os

DATABASE_PATH = "Hourly_Temperature_Readings_Dataset.csv"

def update_database(new_data):
    """
    Updates the existing database with new data.

    Args:
        new_data (pd.DataFrame): The new data to be added.
    """
    if os.path.exists(DATABASE_PATH):
        # Load existing data
        existing_data = pd.read_csv(DATABASE_PATH)
        existing_data['Timestamp'] = pd.to_datetime(existing_data['Timestamp'])
    else:
        # Initialize an empty DataFrame if database doesn't exist
        existing_data = pd.DataFrame(columns=["Timestamp", "Temperature", "AC_Status", "Fan_Status"])

    # Ensure timestamps are datetime objects in new data
    new_data['Timestamp'] = pd.to_datetime(new_data['Timestamp'])

    # Combine datasets and remove duplicates
    combined_data = pd.concat([existing_data, new_data]).drop_duplicates(subset="Timestamp").sort_values(by="Timestamp")

    # Save the updated database
    combined_data.to_csv(DATABASE_PATH, index=False)
    print(f"Database updated successfully! Total records: {len(combined_data)}")

def create_sample_data():
    """Creates sample new data for testing purposes."""
    new_data = pd.DataFrame({
        "Timestamp": [datetime(2025, 1, 3, hour) for hour in range(24)],
        "Temperature": [22 + i % 3 for i in range(24)],  # Simulated temperatures
        "AC_Status": [1 if i % 2 == 0 else 0 for i in range(24)],
        "Fan_Status": [0 if i % 2 == 0 else 1 for i in range(24)]
    })
    return new_data

if __name__ == "__main__":
    sample_data = create_sample_data()
    update_database(sample_data)
