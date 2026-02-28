import numpy as np
from src.preprocessing import detect_energy_columns

def feature_engineering(df):

    print("⚙️ Feature Engineering...")

    # -----------------------------
    # Detect Energy Column Dynamically
    # -----------------------------
    energy_cols = detect_energy_columns(df)

    if len(energy_cols) == 0:
        raise ValueError("No energy column detected in dataset.")

    energy_col = energy_cols[0]
    print(f"Detected Energy Column: {energy_col}")

    # -----------------------------
    # Time Features
    # -----------------------------
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month
    df["dayofweek"] = df["timestamp"].dt.dayofweek
    df["week"] = df["timestamp"].dt.isocalendar().week.astype(int)
    df["quarter"] = df["timestamp"].dt.quarter
    df["is_weekend"] = df["dayofweek"].isin([5,6]).astype(int)

    # -----------------------------
    # Cyclical Encoding
    # -----------------------------
    df["hour_sin"] = np.sin(2*np.pi*df["hour"]/24)
    df["hour_cos"] = np.cos(2*np.pi*df["hour"]/24)
    df["month_sin"] = np.sin(2*np.pi*df["month"]/12)
    df["month_cos"] = np.cos(2*np.pi*df["month"]/12)

    # -----------------------------
    # Rolling Features
    # -----------------------------
    windows = [6, 12, 24, 48, 168]

    for w in windows:
        df[f"roll_mean_{w}"] = df[energy_col].rolling(w).mean()
        df[f"roll_std_{w}"] = df[energy_col].rolling(w).std()
        df[f"roll_min_{w}"] = df[energy_col].rolling(w).min()
        df[f"roll_max_{w}"] = df[energy_col].rolling(w).max()

    # -----------------------------
    # Lag Features
    # -----------------------------
    lags = [1,2,3,6,12,24,48,72,168,336]

    for lag in lags:
        df[f"lag_{lag}"] = df[energy_col].shift(lag)

    # -----------------------------
    # Deviation Features
    # -----------------------------
    df["zscore_24"] = (df[energy_col] - df["roll_mean_24"]) / (df["roll_std_24"] + 1e-5)
    df["zscore_168"] = (df[energy_col] - df["roll_mean_168"]) / (df["roll_std_168"] + 1e-5)

    # Drop NaN created by rolling/lag
    df = df.dropna()

    print("✅ Feature Engineering Completed")
    print("Total Features:", df.shape[1])
    print("🔎 Sample Columns:", df.columns[:50])

    return df