import os
import time
import glob
from dotenv import load_dotenv
from google.cloud import storage
from google.api_core.exceptions import RetryError, GoogleAPICallError

load_dotenv()

BUCKET_NAME = "techtrax-crm-pipeline"
OUTPUT_DIR = os.path.join("..", "output_ndjson")

import glob as glob_module
ONLY_THESE_FILES = [
    os.path.basename(f) for f in glob_module.glob(os.path.join(OUTPUT_DIR, "auditlogs*.json"))
] + ["customerprofiles.json"]


def upload_file_with_retry(bucket, filepath, blob_path, max_retries=5):
    for attempt in range(1, max_retries + 1):
        try:
            blob = bucket.blob(blob_path)
            blob.chunk_size = 5 * 1024 * 1024
            blob.upload_from_filename(filepath, timeout=600)
            return True
        except Exception as e:
            print(f"  Attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                wait_time = 15 * attempt
                print(f"  Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"  Failed to upload after {max_retries} attempts.")
                return False


def upload_all_json_files():
    project_id = os.getenv("GCP_PROJECT_ID")
    client = storage.Client(project=project_id)
    bucket = client.bucket(BUCKET_NAME)

    all_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))

    if ONLY_THESE_FILES:
        json_files = [
            f for f in all_files
            if os.path.basename(f) in ONLY_THESE_FILES
        ]
    else:
        json_files = all_files

    if not json_files:
        print("No matching JSON files found in output_ndjson/.")
        return

    print(f"Found {len(json_files)} files to upload to bucket '{BUCKET_NAME}'\n")

    succeeded = []
    failed = []

    for filepath in json_files:
        filename = os.path.basename(filepath)
        blob_path = f"raw_ndjson/{filename}"
        size_kb = os.path.getsize(filepath) / 1024

        print(f"Uploading: {filename} ({size_kb:.1f} KB)...")

        success = upload_file_with_retry(bucket, filepath, blob_path)
        if success:
            print(f"  Uploaded -> gs://{BUCKET_NAME}/{blob_path}")
            succeeded.append(filename)
        else:
            failed.append(filename)

    print("\n" + "=" * 60)
    print(f"Upload summary: {len(succeeded)} succeeded, {len(failed)} failed")
    if failed:
        print(f"Failed files: {failed}")


if __name__ == "__main__":
    upload_all_json_files()