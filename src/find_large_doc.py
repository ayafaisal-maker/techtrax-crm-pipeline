import os
import json
import glob

NDJSON_DIR = os.path.join("..", "output_ndjson")

files = glob.glob(os.path.join(NDJSON_DIR, "auditlogs_part*.json"))

for filepath in files:
    filename = os.path.basename(filepath)
    max_size = 0
    max_line_num = 0

    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            size_mb = len(line.encode("utf-8")) / (1024 * 1024)
            if size_mb > max_size:
                max_size = size_mb
                max_line_num = i

    print(f"{filename}: max line size = {max_size:.2f} MB (line {max_line_num})")