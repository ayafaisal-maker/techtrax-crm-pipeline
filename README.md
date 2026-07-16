# TechTrax CRM — MongoDB to BigQuery ETL Pipeline

Extraction pipeline that pulls TechTrax CRM data from MongoDB (production)
and loads it into BigQuery as raw tables, ready for dbt transformation.

## Pipeline Steps (run in this order)

1. `src/extract.py` — Connects to MongoDB, pulls each collection listed in
   `config/collections.yaml`, saves results as JSON files in `output/`.
2. `src/convert_to_ndjson.py` — Converts JSON array files to NDJSON format
   (required by BigQuery), and stringifies fields with mixed/variable types
   (`customerprofiles.customFields`, `auditlogs.requestBody`,
   `auditlogs.responseBody`). Output goes to `output_ndjson/`.
3. `src/upload_to_gcs.py` — Uploads all files from `output_ndjson/` to
   `gs://techtrax-crm-pipeline/raw_ndjson/`.
4. `src/load_to_bigquery.py` — Loads files from GCS into BigQuery tables
   in the `techtrax_raw` dataset (project `data-analysis-450711`).

## Setup

1. Install dependencies:
pip install -r requirements.txt
2. Create a `.env` file in the project root (not committed to git) with:
MONGO_PROD_URI=<mongodb connection string>
GOOGLE_APPLICATION_CREDENTIALS=../gcp-keys/service-account-key.json
GCP_PROJECT_ID=data-analysis-450711

3. Place the GCP service account key at `gcp-keys/service-account-key.json`
   (not committed to git).

## Scope

**24 collections** are extracted (core CRM only). CMS/Clinical collections
(patients, appointments, payments, etc.) are explicitly out of scope — see
`config/collections.yaml` for the full list of what's included and how each
collection is filtered.

## Important Notes for Anyone Building on This Data

- **No tenant filtering** is applied during extraction — all tenants are
  mixed together in each table. Tenant-level filtering should happen at
  the dbt/staging layer.
- **Soft-delete filter is currently disabled** — all rows are extracted,
  including soft-deleted ones (`isSoftDeleted = true`). The column itself
  is preserved in every table so it can still be filtered downstream if
  needed.
- **`auditlogs` is excluded** from extraction (see `EXCLUDED_COLLECTIONS`
  in `extract.py`). The last snapshot in BigQuery (190,160 rows) is a
  stale copy and will NOT update on future runs unless this exclusion is
  removed.
- **These 3 tables are currently empty** in BigQuery (zero records in the
  source itself, not a pipeline error): `crmleaves`,
  `crmrequestshiftchanges`, `crmuserleavebalances`. They'll populate
  automatically next time the pipeline runs, once real data exists for
  them.
- **JSON string fields**: `customerprofiles.customFields`,
  `auditlogs.requestBody`, and `auditlogs.responseBody` are stored as
  JSON strings (not native objects/arrays) because their structure varies
  row to row. Use `PARSE_JSON()` / `JSON_EXTRACT()` in BigQuery/dbt to
  work with them.

## Current Status

This pipeline currently runs **manually** — it is NOT scheduled or live.
Data in BigQuery reflects a snapshot from the last manual run. To make
this live, the next step is to wrap these four scripts in an **Airflow
DAG** with an appropriate schedule (see handoff notes / team
communication for details).

## Data Location

- **GCS bucket**: `gs://techtrax-crm-pipeline/raw_ndjson/`
- **BigQuery dataset**: `data-analysis-450711.techtrax_raw`
- **Service account used**: `natix-etl@data-analysis-450711.iam.gserviceaccount.com`

