import json
import boto3
import pandas as pd
import os
import snowflake.connector
from io import StringIO

s3 = boto3.client("s3")


def load_to_snowflake(df):

    print("Connecting to Snowflake...")

    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

    cur = conn.cursor()

    print("Creating table if not exists...")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales_cleaned (
            order_id INT,
            product STRING,
            quantity INT,
            price FLOAT,
            revenue FLOAT
        )
    """)

    print("Inserting data into Snowflake...")

    for _, row in df.iterrows():

        cur.execute("""
            INSERT INTO sales_cleaned VALUES (%s,%s,%s,%s,%s)
        """, (
            int(row["order_id"]),
            row["product"],
            int(row["quantity"]),
            float(row["price"]),
            float(row["revenue"])
        ))

    conn.commit()

    cur.close()
    conn.close()

    print("Data loaded into Snowflake successfully!")


def lambda_handler(event, context):

    print("Lambda triggered...")

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print(f"Bucket: {bucket}")
    print(f"File: {key}")

    obj = s3.get_object(Bucket=bucket, Key=key)

    data = obj["Body"].read().decode("utf-8")

    df = pd.read_csv(StringIO(data))

    print("Raw rows:", len(df))

    # Clean Data
    df = df.dropna()
    df = df.drop_duplicates()

    df["revenue"] = df["quantity"] * df["price"]

    print("Cleaned rows:", len(df))

    # Save cleaned file to S3
    cleaned_key = key.replace("raw/", "cleaned/")

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3.put_object(
        Bucket=bucket,
        Key=cleaned_key,
        Body=csv_buffer.getvalue()
    )

    print("Cleaned file saved to S3:", cleaned_key)

    # Load into Snowflake
    load_to_snowflake(df)

    return {
        "statusCode": 200,
        "body": json.dumps("ETL Completed Successfully")
    }
