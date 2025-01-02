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
        print(f"Failed to load data from GitHub: {e}")
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
    print(f"Updated dataset saved to {file_path}")

# Load existing data
data = load_existing_data(github_repo)

# Input new data row
if not data.empty:
    print("Existing dataset loaded. Add a new row.")
    timestamp = input("Enter Timestamp (YYYY-MM-DD HH:MM:SS): ")
    temperature = input("Enter Temperature (°C): ")
    ac_status = input("Enter AC Status (1 for ON, 0 for OFF): ")
    fan_status = input("Enter Fan Status (1 for ON, 0 for OFF): ")

    # Add new row
    data = add_row(data, timestamp, temperature, ac_status, fan_status)

    # Save updated data locally
    save_updated_data(data, local_file)
else:
    print("Failed to load existing dataset. No changes made.")
