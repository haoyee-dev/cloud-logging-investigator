# Cloud Logging Investigator

## Description

Cloud Logging Investigator simplifies retrieving logs from Google Cloud Logging for further investigations.

Retrieving logs from Google Cloud requires logging into the Google Cloud Console and exporting and formatting it.

This script exports the relevant logs into a CSV file for quick investigations.

It currently supports only Google Cloud Run Functions.

## How to Run
1. Set up Google Cloud Application Default Credentials (ADC).
```bash
gcloud auth application-default login
```

2. Install dependencies
```bash
uv sync
```

3. Set environment variables in `.env` using `.env.example` as a template

4. Run `main.py`

```bash
python main.py
```

## Dependencies
- `uv` for package installation
- Google Cloud Application Default Credentials (ADC) for authentication
- Google Cloud Logging read access (Logs Viewer)

## Library Maintenance
This client library was created to support a personal project. No regular maintenance is done.

## Output Format
The output CSV will be of the form

| timestamp | severity | log_name     | insert_id   | text_payload | resource | labels | trace | span_id |
|-----------|----------|--------------|-------------|--------------|----------|--------|-------|---------|

Please refer to [Log Entry](https://docs.cloud.google.com/python/docs/reference/logging/latest/entries)
