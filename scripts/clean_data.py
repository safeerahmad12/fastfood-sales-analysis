import pandas as pd
import os

RAW_PATH = "data/raw/fast_food_dataset_raw_expanded.csv"
CLEAN_PATH = "data/cleaned/fast_food_dataset_cleaned.csv"

def clean_dataset():
    print("Loading dataset...")
    df = pd.read_csv(RAW_PATH)

    print(f"Initial rows: {len(df)}")

    # 1. Remove duplicates
    df = df.drop_duplicates()
    print(f"After removing duplicates: {len(df)}")

    # 2. Fix column names
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

    # 3. Combine date + time into a single datetime column
    df["order_time"] = pd.to_datetime(df["date"] + " " + df["time"], errors="coerce")
    df = df.dropna(subset=["order_time"])

    # 4. Fix impossible values
    df["quantity"] = df["quantity"].apply(lambda x: max(x, 1))
    df["unit_price"] = df["unit_price"].apply(lambda x: max(x, 0))

    # 5. Recalculate total price
    df["total_price"] = df["quantity"] * df["unit_price"]

    # 6. Rename columns for analysis
    df = df.rename(columns={
        "item_name": "menu_item",
        "category": "menu_category",
        "unit_price": "price"
    })

    # 7. Extract extra features
    df["weekday"] = df["order_time"].dt.day_name()
    df["hour"] = df["order_time"].dt.hour

    # 8. Reorder clean structure
    df = df[
        [
            "order_id",
            "order_time",
            "year",
            "month",
            "day",
            "weekday",
            "hour",
            "order_type",
            "payment_method",
            "menu_category",
            "menu_item",
            "quantity",
            "price",
            "total_price",
            "promotion_applied",
            "discount_amount",
            "employee_id",
            "employee_name",
            "temperature_c",
            "weather"
        ]
    ]

    print(f"Final cleaned rows: {len(df)}")

    os.makedirs("data/cleaned", exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)

    print("Dataset cleaned and saved to:", CLEAN_PATH)


if __name__ == "__main__":
    clean_dataset()