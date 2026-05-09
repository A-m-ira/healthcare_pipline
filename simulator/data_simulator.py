import pandas as pd
import time
import os
from datetime import datetime
import random

SOURCE_CSV = r"C:\Users\hanan\Downloads\healthcare-data-pipeline\data\healthcare_dataset.csv"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BASE_DIR)

STREAMING_LANDING_ZONE = os.path.join(
    BASE_DIR,
    "data",
    "raw_healthcare_pings"
)

os.makedirs(STREAMING_LANDING_ZONE, exist_ok=True)

print("BASE_DIR:", BASE_DIR)
print("OUTPUT:", STREAMING_LANDING_ZONE)

HEALTH_COLS = [
    'Age',
    'Gender',
    'Medical Condition',
    'Admission Type',
    'Billing Amount',
    'Hospital',
    'Test Results'
]

def run_simulator():
    try:
        df = pd.read_csv(SOURCE_CSV)
        df.columns = df.columns.str.strip()

        missing = [c for c in HEALTH_COLS if c not in df.columns]
        if missing:
            print(f"Missing columns in dataset: {missing}")
            return

        print("Data Loaded Successfully")
        print("Simulating Healthcare Streaming Data")

    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    batch_size = 5

    for i in range(0, len(df), batch_size):

        chunk = df.iloc[i:i + batch_size][HEALTH_COLS].copy()

        chunk['patient_id'] = f"HC-{random.randint(1, 1000)}"
        chunk['event_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # type cleaning
        chunk['Age'] = pd.to_numeric(chunk['Age'], errors='coerce').fillna(0)
        chunk['Billing Amount'] = pd.to_numeric(chunk['Billing Amount'], errors='coerce').fillna(0)

        # save JSON batch
        file_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        file_path = os.path.join(
            STREAMING_LANDING_ZONE,
            f"healthcare_ping_{file_id}.json"
        )

        chunk.to_json(file_path, orient='records', lines=True)

        print(f"Batch {i // batch_size + 1} | Records: {len(chunk)} | Time: {chunk['event_time'].iloc[0]}")

        time.sleep(2)

if __name__ == "__main__":
    try:
        run_simulator()
    except KeyboardInterrupt:
        print("Simulator Stopped")