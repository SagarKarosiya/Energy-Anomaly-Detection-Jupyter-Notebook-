import pandas as pd

def evaluate_model(df):

    print("📊 Evaluation...")

    anomaly_rate = df["final_anomaly"].mean() * 100

    stats = {
        "Total Samples": len(df),
        "Anomaly Rate (%)": round(anomaly_rate,2),
        "Total Anomalies": df["final_anomaly"].sum()
    }

    print(stats)
    print("📊 Evaluation Summary")
    print("-----------------------")
    for k, v in stats.items():
        print(f"{k}: {v}")
    return stats