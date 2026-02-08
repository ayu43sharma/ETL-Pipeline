import csv
import random
from datetime import datetime, timedelta

# Output file
OUTPUT_FILE = "../data/sample_sales.csv"

# Sample values
products = [
    ("Blue T-Shirt", "Apparel", 15.00),
    ("Red Mug", "Home", 7.50),
    ("Water Bottle", "Outdoors", 12.00),
    ("Sneakers", "Footwear", 55.00),
    ("Backpack", "Outdoors", 35.00),
    ("Laptop Stand", "Electronics", 40.00),
    ("Desk Chair", "Furniture", 120.00),
    ("Headphones", "Electronics", 65.00),
    ("Notebook", "Stationery", 5.00),
    ("Pen Set", "Stationery", 3.00),
]

regions = ["Singapore", "Malaysia", "Thailand", "Vietnam", "Philippines", "Indonesia"]

# Generate random dates (last 90 days)
def random_date():
    start_date = datetime.now() - timedelta(days=90)
    rand_days = random.randint(0, 90)
    return (start_date + timedelta(days=rand_days)).strftime("%Y-%m-%d")

# Generate data
def generate_sales_data(num_rows=100):
    rows = []
    for i in range(1001, 1001 + num_rows):
        product, category, price = random.choice(products)
        quantity = random.randint(1, 5)
        total_price = round(quantity * price, 2)
        order_date = random_date()
        region = random.choice(regions)

        rows.append([
            i, product, category, quantity, total_price, order_date, region
        ])
    return rows

# Write CSV
def save_to_csv(rows):
    header = ["order_id", "product", "category", "quantity", "price", "order_date", "region"]
    with open(OUTPUT_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == "__main__":
    sales_data = generate_sales_data(150)  # generate 150 rows
    save_to_csv(sales_data)
    print(f"✅ Generated {len(sales_data)} rows of sales data in {OUTPUT_FILE}")