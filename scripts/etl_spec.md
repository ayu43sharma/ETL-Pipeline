# ETL Specification – Retail Sales Data

This document defines the transformation rules for cleaning raw retail sales data (`sample_sales_dirty.csv`) and preparing it for analytics in Snowflake.

---

## Input: Raw Data (from S3 `/raw/`)

Source file: **`sample_sales_dirty.csv`**
Columns:

* `order_id` (may contain duplicates)
* `product` (may be missing/empty)
* `category`
* `quantity`
* `price`
* `order_date` (inconsistent formats: sometimes `YYYY-MM-DD`, sometimes `DD-MM-YYYY`)
* `region` (mixed casing: "singapore", "MALAYSIA", etc.)

---

## Transform Rules (applied in AWS Lambda)

1. **Remove Duplicates**

   * Keep only the first occurrence of each `order_id`.

2. **Handle Missing Values**

   * Drop rows where `product` is missing/empty.
   * Drop rows where `order_date` is missing/invalid.

3. **Standardize Dates**

   * Convert `order_date` to `YYYY-MM-DD` format.

4. **Normalize Regions**

   * Convert all region names to **Title Case** (e.g., `singapore` → `Singapore`).

5. **Add Derived Column**

   * Create `line_total = quantity * price`.

---

## Output: Cleaned Data (to S3 `/cleaned/` → Snowflake `SALES_CLEANED`)

Target columns in **Snowflake `etl_db.etl_schema.sales_cleaned`**:

* `order_id` (STRING)
* `product` (STRING)
* `category` (STRING)
* `quantity` (NUMBER)
* `price` (FLOAT)
* `order_date` (DATE, ISO format)
* `region` (STRING, Title Case)
* `line_total` (FLOAT, derived)

---

## Validation & Logging

* Row count before vs after cleaning (log differences).
* Save rejected rows (bad data) into a separate S3 folder `/rejected/` (optional enhancement).
* Log transformation steps in CloudWatch (Lambda logs).