import os
import time
import json
import yaml
from datetime import datetime, timezone
from pymongo.errors import AutoReconnect, OperationFailure
from google.cloud import bigquery
from db_connection import get_client
from watermark import ensure_watermark_table, get_watermark, set_watermark

print("Script started")

CONFIG_PATH = os.path.join("..", "config", "collections.yaml")
OUTPUT_DIR = os.path.join("..", "output")
LOAD_MODES_PATH = os.path.join(OUTPUT_DIR, "_load_modes.json")

EXCLUDED_COLLECTIONS = ["auditlogs"]


def load_config():
    print("Loading config...")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    print(f"Config loaded, found {len(data['collections'])} collections")
    return data["collections"]


def build_query(watermark_field, since):
    if since is None:
        return {}
    return {watermark_field: {"$gt": since}}


def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


def save_to_json(name, docs):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(docs, f, default=json_default, ensure_ascii=False, indent=2)
    print(f"  Saved to: {filepath}")


def extract_collection(db, name, config, bq_client, batch_size=5000, max_retries=3):
    collection = db[name]

    watermark_field = config.get("watermark_field")
    is_incremental = config.get("load_type") == "incremental" and watermark_field is not None

    since = None
    if is_incremental:
        since = get_watermark(bq_client, name)
        if since is not None and since.tzinfo is not None:
            since = since.replace(tzinfo=None)

    query = build_query(watermark_field, since) if is_incremental else {}
    mode = "INCREMENTAL" if (is_incremental and since is not None) else "FULL"

    print(f"\n--- Extracting: {name} ---")
    print(f"  Mode: {mode}  (since={since})")
    print(f"  Query filter: {query}")

    for attempt in range(1, max_retries + 1):
        try:
            docs = []
            max_watermark = since
            cursor = collection.find(query, batch_size=batch_size)
            for i, doc in enumerate(cursor, start=1):
                doc["_id"] = str(doc["_id"])
                docs.append(doc)

                if is_incremental and watermark_field in doc:
                    val = doc[watermark_field]
                    if isinstance(val, datetime):
                        if max_watermark is None or val > max_watermark:
                            max_watermark = val

                if i % batch_size == 0:
                    print(f"  ...fetched {i} documents so far")

            print(f"  Documents fetched (total): {len(docs)}")
            return docs, mode, max_watermark

        except Exception as e:
            print(f"  Connection error on attempt {attempt}/{max_retries}: {e}")
            if attempt < max_retries:
                wait_time = 5 * attempt
                print(f"  Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"  Failed after {max_retries} attempts. Skipping {name}.")
                return [], mode, since


def main():
    print("Entering main()...")
    config = load_config()

    print("Connecting to MongoDB...")
    client = get_client()
    db = client["techtrax"]
    print("Connected.")

    print("Connecting to BigQuery for watermark tracking...")
    bq_client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))
    ensure_watermark_table(bq_client)
    print("Watermark table ready.")

    results = {}
    load_modes = {}

    for name, cfg in config.items():
        if name in EXCLUDED_COLLECTIONS:
            print(f"\nSkipping excluded collection: {name}")
            continue

        docs, mode, new_watermark = extract_collection(db, name, cfg, bq_client)
        save_to_json(name, docs)
        results[name] = docs
        load_modes[name] = mode

        if new_watermark is not None and len(docs) > 0:
            set_watermark(bq_client, name, new_watermark)
            print(f"  Watermark updated -> {new_watermark}")

    with open(LOAD_MODES_PATH, "w", encoding="utf-8") as f:
        json.dump(load_modes, f, indent=2)
    print(f"\nLoad modes saved to: {LOAD_MODES_PATH}")

    print("\n" + "=" * 60)
    print("Extraction summary:")
    for name, docs in results.items():
        print(f"  {name}: {len(docs)} documents ({load_modes[name]})")

    return results


if __name__ == "__main__":
    main()