import csv
import random
from datetime import datetime, timedelta

# Output file (dirty dataset)
OUTPUT_FILE = "../data/sample_sales_dirty.csv"

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

regions = ["singapore", "MALAYSIA", "thailand", "Vietnam", "Philippines", "indonesia"]  # intentionally mixed casing

# Generate random dates (last 90 days)
def random_date():
    start_date = datetime.now() - timedelta(days=90)
    rand_days = random.randint(0, 90)
    return (start_date + timedelta(days=rand_days)).strftime("%Y-%m-%d")

# Introduce dirty data
def generate_dirty_sales_data(num_rows=100):
    rows = []
    used_ids = set()

    for i in range(1001, 1001 + num_rows):
        product, category, price = random.choice(products)
        quantity = random.randint(1, 5)
        total_price = round(quantity * price, 2)

        # 10% chance to duplicate order_id
        if random.random() < 0.1 and used_ids:
            order_id = random.choice(list(used_ids))
        else:
            order_id = i
            used_ids.add(order_id)

        # 10% chance to insert a bad/missing product
        if random.random() < 0.1:
            product = ""  # missing product

        # 10% chance to mess up the date format
        if random.random() < 0.1:
            order_date = datetime.now().strftime("%d-%m-%Y")  # wrong format
        else:
            order_date = random_date()

        # Region is sometimes lowercase/uppercase (already in list)
        region = random.choice(regions)

        rows.append([
            order_id, product, category, quantity, total_price, order_date, region
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
    sales_data = generate_dirty_sales_data(150)  # generate 150 rows with dirty data
    save_to_csv(sales_data)
    print(f"⚠️ Generated {len(sales_data)} rows of DIRTY sales data in {OUTPUT_FILE}")