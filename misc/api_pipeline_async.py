import asyncio
import logging
from typing import List

import httpx
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector

# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("async_snowflake_ingestion")

# -------------------------------------------------
# Config
# -------------------------------------------------
API_URL = "https://api.example.com/data"
API_KEY = "your_api_key"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

REQUIRED_FIELDS = ["id", "name", "value", "created_at"]
CONCURRENT_REQUESTS = 5
PAGE_SIZE = 100

SNOWFLAKE_TABLE = "API_DATA"

# -------------------------------------------------
# Custom Exceptions
# -------------------------------------------------
class RateLimitError(Exception):
    pass

# -------------------------------------------------
# Async API Fetch
# -------------------------------------------------
@retry(
    retry=retry_if_exception_type(RateLimitError),
    stop=stop_after_attempt(5),
    wait=wait_exponential(min=2, max=30),
)
async def fetch_page(client: httpx.AsyncClient, page: int) -> List[dict]:
    logger.info("Fetching page %s", page)

    resp = await client.get(
        API_URL,
        headers=HEADERS,
        params={"page": page, "limit": PAGE_SIZE},
        timeout=30
    )

    if resp.status_code == 429:
        logger.warning("Rate limit hit on page %s", page)
        raise RateLimitError()

    resp.raise_for_status()
    return resp.json().get("results", [])

# -------------------------------------------------
# Data Cleaning
# -------------------------------------------------
def clean_records(records: List[dict]) -> pd.DataFrame:
    logger.info("Cleaning %d records", len(records))

    df = pd.json_normalize(records)

    for col in REQUIRED_FIELDS:
        if col not in df.columns:
            df[col] = None

    df = df[REQUIRED_FIELDS]

    df["id"] = df["id"].astype("string")
    df["name"] = df["name"].fillna("unknown")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    df = df.dropna(subset=["id"])
    return df

# -------------------------------------------------
# Snowflake Load
# -------------------------------------------------
def load_to_snowflake(df: pd.DataFrame):
    if df.empty:
        logger.warning("No data to load into Snowflake")
        return

    logger.info("Loading %d rows into Snowflake", len(df))

    ctx = snowflake.connector.connect(**SNOWFLAKE_CONN)
    success, nchunks, nrows, _ = write_pandas(
        conn=ctx,
        df=df,
        table_name=SNOWFLAKE_TABLE,
        auto_create_table=True
    )

    ctx.close()

    logger.info(
        "Snowflake load success=%s chunks=%s rows=%s",
        success, nchunks, nrows
    )

# -------------------------------------------------
# Orchestration
# -------------------------------------------------
async def run_pipeline():
    all_records = []
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async with httpx.AsyncClient() as client:

        async def bounded_fetch(page: int):
            async with semaphore:
                return await fetch_page(client, page)

        page = 1
        while True:
            batch = await bounded_fetch(page)
            if not batch:
                break

            all_records.extend(batch)
            page += 1

    logger.info("Fetched total %d records", len(all_records))

    df = clean_records(all_records)

    # Snowflake connector is blocking → run in thread
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, load_to_snowflake, df)

    logger.info("Pipeline completed successfully")

# -------------------------------------------------
# Entry Point
# -------------------------------------------------
if __name__ == "__main__":
    asyncio.run(run_pipeline())
