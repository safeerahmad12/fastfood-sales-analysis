import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# =============== SETTINGS ===============
NUM_ROWS = 250_000
OUTPUT_PATH = "data/raw/fast_food_dataset_raw_expanded.csv"

# Items including Kids Menu
items = [
    ("Cheeseburger", "Burgers", 3.99),
    ("Double Cheeseburger", "Burgers", 4.99),
    ("Chicken Burger", "Burgers", 4.49),
    ("Veggie Burger", "Burgers", 4.29),
    ("BBQ Burger", "Burgers", 5.49),

    ("Chicken Nuggets 6pc", "Chicken", 3.99),
    ("Chicken Nuggets 9pc", "Chicken", 4.99),
    ("Chicken Wings 6pc", "Chicken", 5.49),

    ("Large Fries", "Sides", 2.49),
    ("Medium Fries", "Sides", 1.99),
    ("Onion Rings", "Sides", 2.79),

    ("Coca Cola", "Drinks", 1.99),
    ("Fanta", "Drinks", 1.99),
    ("Sprite", "Drinks", 1.99),
    ("Chocolate Shake", "Drinks", 3.49),

    ("Kids Chicken Nuggets", "Kids", 2.99),
    ("Kids Cheeseburger", "Kids", 2.49),
    ("Kids Fries", "Kids", 1.29),
    ("Kids Juice Box", "Kids", 1.49),
    ("Kids Ice Cream Cup", "Kids", 1.99),
    ("Kids Toy Pack", "Kids", 0.99),
]

order_types = ["Dine-In", "Drive-Thru", "Delivery", "Takeaway"]
payment_methods = ["Cash", "Card", "Apple Pay", "Google Pay", "Voucher"]
weather_conditions = ["Sunny", "Cloudy", "Rain", "Snow"]

employees = [
    ("E001", "Anna"), ("E002", "John"), ("E003", "Maria"),
    ("E004", "Leo"), ("E005", "Sophie"), ("E006", "Markus")
]

# =============== DATA GENERATION ===============
rows = []

start_date = datetime(2024, 1, 1)

for i in range(NUM_ROWS):
    order_id = random.randint(100000, 999999)
    item_name, category, price = random.choice(items)
    quantity = np.random.choice([1, 1, 1, 2, 2, 3, 5, 20], p=[0.5,0.2,0.1,0.1,0.05,0.03,0.019,0.001])

    # Introduce random price errors (realistic)
    if random.random() < 0.01:
        price = None

    # Promotion & discount
    promo = np.random.choice(["Yes", "No"], p=[0.15, 0.85])
    discount = round(price * 0.1, 2) if promo == "Yes" and price else 0

    # Timestamp
    dt = start_date + timedelta(minutes=random.randint(0, 525600))
    date = dt.date()
    time = dt.time().strftime("%H:%M:%S")

    year = date.year
    month = date.month
    day = date.day
    dow = dt.strftime("%A")
    hour = dt.hour

    order_type = random.choice(order_types)
    payment_method = random.choice(payment_methods)

    temp = round(random.uniform(-5, 35), 1)
    weather = random.choice(weather_conditions)

    employee_id, employee_name = random.choice(employees)

    # Possible typos
    if random.random() < 0.005:
        item_name = item_name.replace("e", "ee")

    rows.append([
        order_id, item_name, category, quantity, price,
        quantity * price if price else None,
        date, time, year, month, day, dow, hour,
        order_type, payment_method, promo, discount,
        employee_id, employee_name,
        temp, weather
    ])

columns = [
    "order_id", "item_name", "category", "quantity", "unit_price", "total_price",
    "date", "time", "year", "month", "day", "day_of_week", "hour",
    "order_type", "payment_method", "promotion_applied", "discount_amount",
    "employee_id", "employee_name",
    "temperature_c", "weather"
]

df = pd.DataFrame(rows, columns=columns)

# Ensure folders exist
os.makedirs("data/raw", exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print(f"Dataset generated with {len(df)} rows → {OUTPUT_PATH}")