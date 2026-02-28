import matplotlib.pyplot as plt

def save_plots(df):

    print("📈 Saving Visualizations...")

    plt.figure()
    plt.plot(df["timestamp"], df["electricity"])
    plt.scatter(
        df[df["final_anomaly"]==1]["timestamp"],
        df[df["final_anomaly"]==1]["electricity"]
    )
    plt.title("Energy with Anomalies")
    plt.savefig("energy_anomalies.png")
    plt.close()

    print("✅ Plots Saved")