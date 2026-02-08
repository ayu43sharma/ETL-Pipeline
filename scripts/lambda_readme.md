# AWS Lambda ETL Design

This document defines how AWS Lambda will transform raw sales data into clean, analytics-ready data.

---

## Function Overview

- **Trigger**: S3 event → when a new file is uploaded into `s3://etl-retail-data-rounit/raw/`
- **Input**: Raw CSV file with dirty sales data
- **Transformations**: (see `etl_spec.md`)
  1. Remove duplicate `order_id`s
  2. Drop rows with missing `product` or invalid `order_date`
  3. Standardize `order_date` → `YYYY-MM-DD`
  4. Normalize region names → Title Case
  5. Add derived column `line_total = quantity * price`
- **Output**: Cleaned CSV file saved to `s3://etl-retail-data-rounit/cleaned/`

---

## IAM Role & Permissions

Lambda will need an execution role with the following permissions:

### S3 Access
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::etl-retail-data-rounit",
        "arn:aws:s3:::etl-retail-data-rounit/*"
      ]
    }
  ]
}
```

### CloudWatch Logs
```json
{
  "Effect": "Allow",
  "Action": [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents"
  ],
  "Resource": "arn:aws:logs:*:*:*"
}
```

---

## Runtime & Dependencies

- **Runtime**: Python 3.9
- **Libraries**: boto3, csv, datetime, io
- **Deployment**: packaged and uploaded from VS Code (Phase 6)

---

## Notes

- Lambda only handles cleaning & writing back to S3
- Loading into Snowflake will be done via COPY INTO later
- Optional: rejected rows may be written into /rejected/ S3 folder