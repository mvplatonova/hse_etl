import csv
import random
from datetime import datetime, timedelta

# Constants
NUM_TRANSACTIONS = 1_000_000
OUTPUT_FILE = "transactions_dataset.csv"

# Product categories and names
PRODUCT_CATEGORIES = {
    "Smartphones": ["iPhone 14", "Samsung Galaxy S23", "Google Pixel 7"],
    "Laptops": ["MacBook Pro", "Dell XPS 13", "Lenovo ThinkPad X1"],
    "Tablets": ["iPad Pro", "Samsung Galaxy Tab", "Microsoft Surface"],
    "TVs": ["LG OLED", "Samsung QLED", "Sony Bravia"],
    "Accessories": ["Wireless Headphones", "Smartwatch", "Bluetooth Speaker"]
}

def generate_random_date():
    """Generate a random date within the last 5 years."""
    start_date = datetime.now() - timedelta(days=5 * 365)
    random_days = random.randint(0, 5 * 365)
    return start_date + timedelta(days=random_days)

def generate_transaction_data():
    """Generate a single transaction record."""
    user_id = random.randint(1, 100_000)  # Simulate 100,000 unique users
    category = random.choice(list(PRODUCT_CATEGORIES.keys()))
    product = random.choice(PRODUCT_CATEGORIES[category])
    quantity = random.randint(1, 5)
    price_per_unit = round(random.uniform(50, 5000), 2)
    total_price = round(quantity * price_per_unit, 2)
    transaction_date = generate_random_date().strftime("%Y-%m-%d %H:%M:%S")
    return [user_id, transaction_date, category, product, quantity, price_per_unit, total_price]

def main():
    # Write the dataset to a CSV file
    with open(OUTPUT_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["UserID", "TransactionDate", "Category", "Product", "Quantity", "PricePerUnit", "TotalPrice"])
        # Write transaction data
        for _ in range(NUM_TRANSACTIONS):
            writer.writerow(generate_transaction_data())

if __name__ == "__main__":
    main()