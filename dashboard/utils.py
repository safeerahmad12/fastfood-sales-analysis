import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/fast_food_dataset_cleaned.csv")
    df["timestamp"] = pd.to_datetime(df["order_time"])
    df["hour"] = df["timestamp"].dt.hour
    df["day_name"] = df["timestamp"].dt.day_name()
    df["weekday"] = df["timestamp"].dt.weekday
    df.rename(columns={"menu_category":"category","menu_item":"product_name"}, inplace=True)
    return df