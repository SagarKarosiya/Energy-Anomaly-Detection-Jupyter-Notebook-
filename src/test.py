def generate_business_insights(df, cost_per_unit=0.12,
                               selected_month=None,
                               selected_date=None):

    df_filtered = df.copy()

    # -----------------------------
    # Month Filter
    # -----------------------------
    if selected_month is not None:
        df_filtered = df_filtered[df_filtered["month"] == selected_month]

    # -----------------------------
    # Date Filter
    # -----------------------------
    if selected_date is not None:
        df_filtered = df_filtered[
            df_filtered["timestamp"].dt.date == selected_date
        ]

    # -----------------------------
    # Peak Hour Calculation
    # -----------------------------
    peak_hours = (
        df_filtered[df_filtered["final_anomaly"] == 1]
        ["hour"]
        .value_counts()
        .sort_index()
    )
    # -----------------------------
    #Recommendation
    # ----------------------------
    recommendations = []

    if cost_loss > 1000:
        recommendations.append("Immediate HVAC system inspection recommended.")
    if len(peak_hours) > 0:
        recommendations.append("Peak anomaly hours require operational adjustment.")
    if len(peak_months) > 0:
        recommendations.append("Seasonal recalibration of energy systems advised.")

    # -----------------------------
    # Cost Impact
    # -----------------------------
    energy_col = df.select_dtypes(include="number").columns[0]

    anomaly_energy = df_filtered[df_filtered["final_anomaly"] == 1][energy_col].sum()

    estimated_cost = round(anomaly_energy * cost_per_unit, 2)

    insights = {
        "estimated_cost_loss_$": estimated_cost,
        "anomaly_rate_percent": round(
            df_filtered["final_anomaly"].mean() * 100, 2
        ),
        "peak_hours": peak_hours
        "recommendations": recommendations
    }

    return insights, df_filtered