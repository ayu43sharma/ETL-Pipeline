# Snowflake Load Design

This document defines how Snowflake ingests cleaned data from AWS S3 into the target table.

---

## External Stage

- **Stage name**: `cleaned_stage`
- **S3 location**: `s3://etl-retail-data-rounit/cleaned/`
- **Integration**: `s3_int`
- Purpose: provides a secure link between Snowflake and AWS S3

```sql
CREATE OR REPLACE STAGE cleaned_stage
  STORAGE_INTEGRATION = s3_int
  URL = 's3://etl-retail-data-rounit/cleaned/';
```

## COPY INTO Command

The following loads data from the stage into sales_cleaned:

```sql
COPY INTO sales_cleaned
FROM @cleaned_stage
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1)
ON_ERROR = 'CONTINUE';
```

- **SKIP_HEADER=1**: skips CSV header row
- **ON_ERROR=CONTINUE**: ignores bad rows (optional)

## Workflow

1. Lambda writes cleaned files to `s3://.../cleaned/`
2. Stage (`cleaned_stage`) points to that folder
3. COPY INTO ingests files into `sales_cleaned` table
4. (Optional) files are moved/archived after loading