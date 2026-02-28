def generate_business_insights(
    df,
    cost_per_unit=0.12,
    selected_month=None,
    selected_date=None
):

    df_filtered = df.copy()
    
    
    # -------------------------------------------------
    # MONTH FILTER
    # -------------------------------------------------
    if selected_month is not None:
        df_filtered = df_filtered[df_filtered["month"] == selected_month]

    # -------------------------------------------------
    # DATE FILTER
    # -------------------------------------------------
    if selected_date is not None:
        df_filtered = df_filtered[
            df_filtered["timestamp"].dt.date == selected_date
        ]

    # -------------------------------------------------
    # PEAK HOUR CALCULATION
    # -------------------------------------------------
    peak_hours = (
        df_filtered[df_filtered["final_anomaly"] == 1]
        ["hour"]
        .value_counts()
        .sort_index()
    )
    # -------------------------------------------------
    # PEAK months CALCULATION
    # -------------------------------------------------
    peak_months = df[df["final_anomaly"]==1]["month"].value_counts().to_dict()
    # -------------------------------------------------
    # COST IMPACT
    # -------------------------------------------------
    energy_col = df.select_dtypes(include="number").columns[0]

    anomaly_energy = df_filtered[
        df_filtered["final_anomaly"] == 1
    ][energy_col].sum()

    estimated_cost = round(anomaly_energy * cost_per_unit, 2)

    anomaly_rate = round(
        df_filtered["final_anomaly"].mean() * 100, 2
    )

    total_anomalies = int(df_filtered["final_anomaly"].sum())

    # -------------------------------------------------
    # SEVERITY CLASSIFICATION
    # -------------------------------------------------
    if anomaly_rate > 15:
        severity = "High"
    elif anomaly_rate > 7:
        severity = "Medium"
    else:
        severity = "Low"

    # -------------------------------------------------
    # RECOMMENDATION ENGINE
    # -------------------------------------------------
    recommendations = []

    if severity == "High":
        recommendations.append(
            " Immediate equipment inspection required. High anomaly rate detected."
        )
        recommendations.append(
            " Conduct HVAC ( Heat,Vantilation,Air,Conditining ) and electrical load diagnostics."
        )
        recommendations.append(
            " Implement real-time monitoring alerts to prevent recurring spikes."
        )

    elif severity == "Medium":
        recommendations.append(
            "⚠ Schedule preventive maintenance within this month."
        )
        recommendations.append(
            " Analyze operational schedules for inefficiencies."
        )

    else:
        recommendations.append(
            " System operating within acceptable anomaly range."
        )
        recommendations.append(
            " Continue monitoring for early detection of faults."
        )

    # Cost-based suggestion
    if estimated_cost > 10000:
        recommendations.append(
            " High financial impact detected. Prioritize anomaly reduction strategy."
        )
    elif estimated_cost > 2000:
        recommendations.append(
            " Moderate cost impact. Optimize peak-hour operations."
        )

    # Peak-hour-based suggestion
    if len(peak_hours) > 0:
        peak_hour = peak_hours.idxmax()
        recommendations.append(
            f" Peak anomalies frequently occur around {int(peak_hour):02d}:00. "
            "Inspect load conditions during this time window."
        )

    # -------------------------------------------------
    # INSIGHTS DICTIONARY
    # -------------------------------------------------
    insights = {
        "estimated_cost_loss_$": estimated_cost,
        "anomaly_rate_percent": anomaly_rate,
        "total_anomalies": total_anomalies,
        "severity_level": severity,
        "peak_anomaly_months": peak_months,
        "peak_hours": peak_hours,
        "recommendations": recommendations
    }

    return insights, df_filtered