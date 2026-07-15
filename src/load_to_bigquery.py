import os
import json
import glob
import re
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = "techtrax_raw"
BUCKET_NAME = "techtrax-crm-pipeline"
OUTPUT_DIR = os.path.join("..", "output_ndjson")
LOAD_MODES_PATH = os.path.join("..", "output", "_load_modes.json")


def get_table_name(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r'_part\d+$', '', name)
    return name


def is_file_empty(filepath):
    return os.path.getsize(filepath) <= 1


def load_modes_map():
    """بيقرا نوع التحميل (FULL/INCREMENTAL) اللي extract.py سجله لكل collection"""
    if not os.path.exists(LOAD_MODES_PATH):
        print("  Warning: no _load_modes.json found, defaulting all to FULL (truncate)")
        return {}
    with open(LOAD_MODES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_to_bigquery():
    client = bigquery.Client(project=PROJECT_ID)
    modes = load_modes_map()

    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))

    skipped_empty = []
    filenames = []
    for f in json_files:
        basename = os.path.basename(f)
        if basename == "auditlogs.json" or basename.startswith("_"):
            continue
        if is_file_empty(f):
            skipped_empty.append(basename)
            continue
        filenames.append(basename)

    if skipped_empty:
        print(f"Skipping empty files (0 records): {skipped_empty}\n")

    tables = {}
    for filename in filenames:
        table_name = get_table_name(filename)
        tables.setdefault(table_name, []).append(filename)

    print(f"Found {len(tables)} tables to load into dataset '{DATASET_ID}'\n")

    for table_name, files in tables.items():
        table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        uris = [f"gs://{BUCKET_NAME}/raw_ndjson/{fname}" for fname in files]

        mode = modes.get(table_name, "FULL")
        write_disposition = (
            bigquery.WriteDisposition.WRITE_APPEND
            if mode == "INCREMENTAL"
            else bigquery.WriteDisposition.WRITE_TRUNCATE
        )

        print(f"Loading table: {table_name} ({len(files)} file(s)) — mode: {mode} ({write_disposition})")

        job_config_kwargs = dict(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=write_disposition,
            ignore_unknown_values=True,
            max_bad_records=1000,
        )

        # في حالة الـ INCREMENTAL، ناخد الـ schema من الجدول الموجود فعليًا
        # بدل ما نسيب autodetect يخمن من عينة صغيرة وممكن يختلف عن الجدول الأصلي
        if mode == "INCREMENTAL":
            try:
                existing_table = client.get_table(table_id)
                job_config_kwargs["schema"] = existing_table.schema
                job_config_kwargs["autodetect"] = False
                print(f"  Using existing table schema ({len(existing_table.schema)} fields)")
            except Exception:
                print(f"  Table doesn't exist yet, falling back to autodetect")
                job_config_kwargs["autodetect"] = True
        else:
            job_config_kwargs["autodetect"] = True

        job_config = bigquery.LoadJobConfig(**job_config_kwargs)

        try:
            load_job = client.load_table_from_uri(
                uris, table_id, job_config=job_config
            )
            load_job.result()

            table = client.get_table(table_id)
            print(f"  Loaded {table.num_rows} total rows now in {table_id}\n")
        except Exception as e:
            print(f"  Failed to load {table_name}: {e}\n")

    print("=" * 60)
    print("BigQuery load complete.")


if __name__ == "__main__":
    load_all_to_bigquery()