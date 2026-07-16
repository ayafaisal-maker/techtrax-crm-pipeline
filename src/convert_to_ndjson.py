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

# حقول لازم تتحول لـ نص دايمًا (بغض النظر عن نوعها الأصلي)
# عشان تتجنب تعارض النوع في BigQuery (زي phone بترجع string أحيانًا و int أحيانًا)
FIELDS_TO_FORCE_STRING = {
    "googlesheetssynclogs.json": ["phone"],
}


def get_base_name(filename):
    return re.sub(r'_part\d+\.json$', '.json', filename)


def stringify_fields(record, fields):
    """بتحول قيمة الحقل كامل (object/array) لنص JSON واحد"""
    for field in fields:
        if field in record and record[field] is not None:
            record[field] = json.dumps(record[field], ensure_ascii=False)
    return record


def force_string_fields(record, fields):
    """بتحول قيمة الحقل (رقم، bool، إلخ) لنص عادي بسيط، مش JSON مغلف"""
    for field in fields:
        if field in record and record[field] is not None:
            record[field] = str(record[field])
    return record


def convert_file(filepath):
    filename = os.path.basename(filepath)
    base_name = get_base_name(filename)
    fields_to_fix = FIELDS_TO_STRINGIFY.get(base_name, [])
    fields_to_force_string = FIELDS_TO_FORCE_STRING.get(base_name, [])

    out_path = os.path.join(NDJSON_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(out_path, "w", encoding="utf-8") as out:
        for record in data:
            if fields_to_fix:
                record = stringify_fields(record, fields_to_fix)
            if fields_to_force_string:
                record = force_string_fields(record, fields_to_force_string)
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    notes = []
    if fields_to_fix:
        notes.append(f"stringified: {fields_to_fix}")
    if fields_to_force_string:
        notes.append(f"forced string: {fields_to_force_string}")
    note_str = f" [{', '.join(notes)}]" if notes else ""

    print(f"  Converted: {filename} ({len(data)} records){note_str}")


def main():
    os.makedirs(NDJSON_DIR, exist_ok=True)
    json_files = [
        f for f in glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
        if not os.path.basename(f).startswith("_")
    ]

    print(f"Converting {len(json_files)} files to NDJSON format...\n")
    for filepath in json_files:
        try:
            convert_file(filepath)
        except Exception as e:
            print(f"  Failed to convert {os.path.basename(filepath)}: {e}")

    print("\nConversion complete. Files saved in output_ndjson/")


if __name__ == "__main__":
    main()