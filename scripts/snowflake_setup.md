# Snowflake Setup

## Warehouse, Database, Schema
```sql
CREATE WAREHOUSE IF NOT EXISTS etl_wh;
CREATE DATABASE IF NOT EXISTS etl_db;
CREATE SCHEMA IF NOT EXISTS etl_db.etl_schema;
```

## Tables

### Raw/staging table (sales_staging)

### Base sales table (sales)

### Final cleaned table (sales_cleaned)

```sql
CREATE OR REPLACE TABLE sales_cleaned (
    order_id STRING,
    product STRING,
    category STRING,
    quantity INT,
    price FLOAT,
    order_date DATE,
    region STRING,
    line_total FLOAT
);
```

## Next

Later we will:

- Create stage pointing to S3 bucket.
- Use COPY INTO to load data from /cleaned/ into sales_cleaned.