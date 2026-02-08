# ETL Automation Plan

This document describes the complete automated ETL pipeline from raw data ingestion to analytics-ready data in Snowflake.

---

## Architecture Overview

```
Raw Data → S3 (raw/) → Lambda Trigger → Data Transformation → S3 (cleaned/) → Snowflake (COPY INTO)
```

---

## Step-by-Step Flow

### 1. Data Ingestion
- **Trigger**: File uploaded to `s3://etl-retail-data-rounit/raw/`
- **Input**: Dirty CSV files with data quality issues
- **Example**: `sample_sales_dirty.csv` with duplicates, missing values, wrong date formats

### 2. Lambda Processing
- **Function**: `lambda_function.py` (see `scripts/lambda/`)
- **Trigger**: S3 PUT event on `/raw/` folder
- **Environment Variables**:
  - `BUCKET_NAME`: `etl-retail-data-rounit`
  - `CLEANED_PREFIX`: `cleaned/`

#### Transformation Logic:
1. **Deduplication**: Remove duplicate `order_id`s (keep first occurrence)
2. **Missing Data Handling**: Replace empty products with "Unknown"
3. **Date Standardization**: Convert DD-MM-YYYY → YYYY-MM-DD format
4. **Region Normalization**: Convert to Title Case (e.g., "singapore" → "Singapore")
5. **Derived Columns**: Calculate `line_total = quantity * price`

### 3. Cleaned Data Storage
- **Output Location**: `s3://etl-retail-data-rounit/cleaned/`
- **Format**: CSV with standardized schema
- **Schema**: `order_id, product, category, quantity, price, order_date, region, line_total`

### 4. Snowflake Loading
- **External Stage**: `cleaned_stage` pointing to S3 `/cleaned/` folder
- **Target Table**: `etl_db.etl_schema.sales_cleaned`
- **Load Command**:
  ```sql
  COPY INTO sales_cleaned
  FROM @cleaned_stage
  FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1)
  ON_ERROR = 'CONTINUE';
  ```

---

## Deployment Steps

### AWS Console Setup:
1. **Create Lambda Function**:
   - Runtime: Python 3.9
   - Role: `lambda-etl-role` (with S3 + CloudWatch permissions)
   - Environment Variables: `BUCKET_NAME`, `CLEANED_PREFIX`

2. **Configure S3 Trigger**:
   - Event Type: PUT
   - Prefix: `raw/`
   - Suffix: `.csv`

3. **Deploy Code**:
   - Copy-paste `lambda_function.py` into Lambda console editor
   - Save and Deploy

### Snowflake Setup:
1. **Create Storage Integration**: `s3_int` (with IAM trust relationship)
2. **Create External Stage**: `cleaned_stage`
3. **Test COPY INTO**: Load sample cleaned data

---

## Testing Workflow

1. **Upload Test File**: 
   ```bash
   aws s3 cp data/sample_sales_dirty.csv s3://etl-retail-data-rounit/raw/
   ```

2. **Verify Lambda Execution**:
   - Check CloudWatch logs for processing confirmation
   - Verify cleaned file appears in `/cleaned/` folder

3. **Load into Snowflake**:
   ```sql
   COPY INTO sales_cleaned FROM @cleaned_stage
   FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1);
   ```

4. **Validate Results**:
   ```sql
   SELECT COUNT(*) FROM sales_cleaned;
   SELECT * FROM sales_cleaned LIMIT 10;
   ```

---

## Monitoring & Logging

- **Lambda Logs**: CloudWatch `/aws/lambda/[function-name]`
- **S3 Events**: CloudTrail for file operations
- **Snowflake Logs**: Query history and COPY INTO results
- **Error Handling**: Lambda continues processing on individual row errors

---

## Future Enhancements

- **Error Quarantine**: Save rejected rows to `/rejected/` S3 folder
- **Data Validation**: Add schema validation and data quality checks
- **Notifications**: SNS alerts for processing failures
- **Scheduling**: CloudWatch Events for batch processing
- **Monitoring**: Custom CloudWatch metrics for data volume tracking