import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = "techtrax_raw"
WATERMARK_TABLE = "_ingestion_watermarks"


def _table_ref():
    return f"{PROJECT_ID}.{DATASET_ID}.{WATERMARK_TABLE}"


def ensure_watermark_table(client: bigquery.Client):
    client.query(f"""
        CREATE TABLE IF NOT EXISTS `{_table_ref()}` (
            collection STRING NOT NULL,
            last_watermark TIMESTAMP,
            updated_at TIMESTAMP
        )
    """).result()


def get_watermark(client: bigquery.Client, collection: str):
    """بترجع آخر توقيت اتسحب لحد ما، أو None لو أول مرة (يبقى full load)"""
    rows = client.query(
        f"SELECT last_watermark FROM `{_table_ref()}` WHERE collection = @collection",
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("collection", "STRING", collection)
            ]
        ),
    ).result()
    row = next(iter(rows), None)
    return row.last_watermark if row else None


def set_watermark(client: bigquery.Client, collection: str, last_watermark: datetime):
    client.query(f"""
        MERGE `{_table_ref()}` T
        USING (SELECT @collection AS collection, @ts AS last_watermark) S
        ON T.collection = S.collection
        WHEN MATCHED THEN
            UPDATE SET last_watermark = S.last_watermark, updated_at = CURRENT_TIMESTAMP()
        WHEN NOT MATCHED THEN
            INSERT (collection, last_watermark, updated_at)
            VALUES (S.collection, S.last_watermark, CURRENT_TIMESTAMP())
    """, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("collection", "STRING", collection),
            bigquery.ScalarQueryParameter("ts", "TIMESTAMP", last_watermark),
        ]
    )).result()