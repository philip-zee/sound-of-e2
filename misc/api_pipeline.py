import time
import requests
import pandas as pd
from typing import List
from sqlalchemy import create_engine
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# -----------------------------
# Configuration
# -----------------------------
API_URL = "https://api.example.com/data"
API_KEY = "your_api_key"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

DB_URL = "sqlite:///example.db"
TABLE_NAME = "api_data"

REQUIRED_FIELDS = ["id", "name", "value", "created_at"]

# -----------------------------
# Custom Exceptions
# -----------------------------
class RateLimitError(Exception):
    pass

# -----------------------------
# API Fetch with Rate Limit Handling
# -----------------------------
@retry(
    retry=retry_if_exception_type(RateLimitError),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
)
def fetch_api_data(page: int = 1) -> List[dict]:
    response = requests.get(
        API_URL,
        headers=HEADERS,
        params={"page": page},
        timeout=30
    )

    if response.status_code == 429:
        raise RateLimitError("Rate limit exceeded")

    response.raise_for_status()
    return response.json().get("results", [])

# -----------------------------
# Data Cleaning with Pandas
# -----------------------------
def clean_data(records: List[dict]) -> pd.DataFrame:
    df = pd.json_normalize(records)

    # Ensure required columns exist
    for field in REQUIRED_FIELDS:
        if field not in df.columns:
            df[field] = None

    # Select only expected fields
    df = df[REQUIRED_FIELDS]

    # Type conversions
    df["id"] = df["id"].astype("string")
    df["name"] = df["name"].fillna("unknown")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Drop rows missing critical identifiers
    df = df.dropna(subset=["id"])

    return df

# -----------------------------
# Store to Database
# -----------------------------
def store_to_db(df: pd.DataFrame):
    engine = create_engine(DB_URL)

    df.to_sql(
        TABLE_NAME,
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500
    )

# -----------------------------
# Main Pipeline
# -----------------------------
def run_pipeline():
    all_records = []
    page = 1

    while True:
        records = fetch_api_data(page)
        if not records:
            break

        all_records.extend(records)
        page += 1
        time.sleep(0.2)  # soft throttle

    if not all_records:
        print("No data fetched.")
        return

    df = clean_data(all_records)
    store_to_db(df)

    print(f"Ingested {len(df)} records successfully.")

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    run_pipeline()
