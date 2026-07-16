import ijson
import json
import os
import re
from decimal import Decimal

OUTPUT_DIR = os.path.join("..", "output")
RECORDS_PER_PART = 20000

FILES_TO_SPLIT = ["auditlogs.json", "googlesheetssynclogs.json"]


def clean_nan_in_file(filepath):
    cleaned_path = filepath + ".cleaned"
    with open(filepath, "r", encoding="utf-8") as f_in, \
         open(cleaned_path, "w", encoding="utf-8") as f_out:
        for line in f_in:
            cleaned_line = re.sub(r':\s*NaN\b', ': null', line)
            f_out.write(cleaned_line)
    return cleaned_path


def json_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return str(obj)


def split_json_array(filepath, records_per_file=RECORDS_PER_PART):
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    part_num = 1
    buffer = []

    print(f"  Cleaning invalid JSON values (NaN)...")
    cleaned_path = clean_nan_in_file(filepath)

    with open(cleaned_path, "rb") as f:
        for item in ijson.items(f, "item"):
            buffer.append(item)
            if len(buffer) >= records_per_file:
                out_path = os.path.join(OUTPUT_DIR, f"{base_name}_part{part_num}.json")
                with open(out_path, "w", encoding="utf-8") as out:
                    json.dump(buffer, out, ensure_ascii=False, default=json_default)
                print(f"  Wrote {out_path} ({len(buffer)} records)")
                buffer = []
                part_num += 1

        if buffer:
            out_path = os.path.join(OUTPUT_DIR, f"{base_name}_part{part_num}.json")
            with open(out_path, "w", encoding="utf-8") as out:
                json.dump(buffer, out, ensure_ascii=False, default=json_default)
            print(f"  Wrote {out_path} ({len(buffer)} records)")

    os.remove(cleaned_path)


def main():
    for filename in FILES_TO_SPLIT:
        filepath = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename}: not found")
            continue
        print(f"\nSplitting: {filename}")
        split_json_array(filepath)


if __name__ == "__main__":
    main()