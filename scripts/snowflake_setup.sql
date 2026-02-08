-- Create warehouse (compute resource)
CREATE OR REPLACE WAREHOUSE etl_wh
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

-- Create database
CREATE OR REPLACE DATABASE etl_db;

-- Create schema
CREATE OR REPLACE SCHEMA etl_schema;

-- Use the new objects
USE WAREHOUSE etl_wh;
USE DATABASE etl_db;
USE SCHEMA etl_schema;

-- Create table for sales data
CREATE OR REPLACE TABLE sales (
    order_id INT,
    product STRING,
    category STRING,
    quantity INT,
    price FLOAT,
    order_date DATE,
    region STRING
);

-- Optional: create a staging table (raw load)
CREATE OR REPLACE TABLE sales_staging LIKE sales;