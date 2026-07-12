import os
import time
import json
import yaml
from datetime import datetime
from pymongo.errors import AutoReconnect, OperationFailure
from db_connection import get_client

print("Script started")

CONFIG_PATH = os.path.join("..", "config", "collections.yaml")
OUTPUT_DIR = os.path.join("..", "output")

EXCLUDED_COLLECTIONS = ["auditlogs"]


def load_config():
    print("Loading config...")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    print(f"Config loaded, found {len(data['collections'])} collections")
    return data["collections"]


def build_query(collection_config):
    # مفيش فلتر خالص - نجيب كل الصفوف بما فيهم soft-deleted
    return {}


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


def extract_collection(db, name, config, batch_size=5000, max_retries=3):
    query = build_query(config)
    collection = db[name]

    print(f"\n--- Extracting: {name} ---")
    print(f"  Load type: {config['load_type']}")
    print(f"  Query filter: {query}")

    for attempt in range(1, max_retries + 1):
        try:
            docs = []
            cursor = collection.find(query, batch_size=batch_size)
            for i, doc in enumerate(cursor, start=1):
                doc["_id"] = str(doc["_id"])
                docs.append(doc)
                if i % batch_size == 0:
                    print(f"  ...fetched {i} documents so far")

            print(f"  Documents fetched (total): {len(docs)}")
            return docs

        except Exception as e:
            print(f"  Connection error on attempt {attempt}/{max_retries}: {e}")
            if attempt < max_retries:
                wait_time = 5 * attempt
                print(f"  Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"  Failed after {max_retries} attempts. Skipping {name}.")
                return []


def main():
    print("Entering main()...")
    config = load_config()

    print("Connecting to MongoDB...")
    client = get_client()
    db = client["techtrax"]
    print("Connected.")

    results = {}
    for name, cfg in config.items():
        if name in EXCLUDED_COLLECTIONS:
            print(f"\nSkipping excluded collection: {name}")
            continue
        docs = extract_collection(db, name, cfg)
        save_to_json(name, docs)
        results[name] = docs

    print("\n" + "=" * 60)
    print("Extraction summary:")
    for name, docs in results.items():
        print(f"  {name}: {len(docs)} documents")

    return results


if __name__ == "__main__":
    main() 