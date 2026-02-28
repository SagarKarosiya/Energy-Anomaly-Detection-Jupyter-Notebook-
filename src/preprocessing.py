import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def detect_energy_columns(df):

    possible_energy_keywords = [
        "electricity",
        "energy",
        "power",
        "consumption",
        "kwh"
    ]

    energy_cols = []

    for col in df.columns:
        for keyword in possible_energy_keywords:
            if keyword.lower() in col.lower():
                energy_cols.append(col)

    return energy_cols
def standardize_columns(df):

    df.columns = df.columns.str.strip().str.lower()

    rename_map = {}

    for col in df.columns:
        if "temp" in col:
            rename_map[col] = "temperature"
        if "humid" in col:
            rename_map[col] = "humidity"
        if "time" in col:
            rename_map[col] = "timestamp"

    df = df.rename(columns=rename_map)

    return df


def preprocess_data(df):

    print("🧹 Preprocessing...")

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # Fill missing
    df = df.ffill().bfill()

    # Cap outliers at 99 percentile
    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        upper = df[col].quantile(0.99)
        df[col] = np.clip(df[col], None, upper)

    # Scale to 0-1
    scaler = MinMaxScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    print("✅ Preprocessing Completed")
    # Validation checks
    print("🔎 Missing Values:", df.isna().sum().sum())

    print("🔎 Timestamp Sorted:",
      df["timestamp"].is_monotonic_increasing)

    numeric_cols = df.select_dtypes(include='number').columns

    print("🔎 Min Value After Scaling:",
      df[numeric_cols].min().min())

    print("🔎 Max Value After Scaling:",
      df[numeric_cols].max().max())
    return df