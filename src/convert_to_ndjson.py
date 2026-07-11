import os
import re
import glob
import json

OUTPUT_DIR = os.path.join("..", "output")
NDJSON_DIR = os.path.join("..", "output_ndjson")


FIELDS_TO_STRINGIFY = {
    "auditlogs.json": ["requestBody", "responseBody"],
    "customerprofiles.json": ["customFields"],
}


def get_base_name(filename):
   
    return re.sub(r'_part\d+\.json$', '.json', filename)


def stringify_fields(record, fields):
    for field in fields:
        if field in record and record[field] is not None:
            record[field] = json.dumps(record[field], ensure_ascii=False)
    return record


def convert_file(filepath):
    filename = os.path.basename(filepath)
    base_name = get_base_name(filename)
    fields_to_fix = FIELDS_TO_STRINGIFY.get(base_name, [])

    out_path = os.path.join(NDJSON_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(out_path, "w", encoding="utf-8") as out:
        for record in data:
            if fields_to_fix:
                record = stringify_fields(record, fields_to_fix)
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"  Converted: {filename} ({len(data)} records)" +
          (f" [stringified: {fields_to_fix}]" if fields_to_fix else ""))


def main():
    os.makedirs(NDJSON_DIR, exist_ok=True)
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))

    print(f"Converting {len(json_files)} files to NDJSON format...\n")
    for filepath in json_files:
        try:
            convert_file(filepath)
        except Exception as e:
            print(f"  Failed to convert {os.path.basename(filepath)}: {e}")

    print("\nConversion complete. Files saved in output_ndjson/")


if __name__ == "__main__":
    main()