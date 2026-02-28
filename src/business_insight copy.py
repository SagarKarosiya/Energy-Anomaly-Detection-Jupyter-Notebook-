def generate_business_insights(df, cost_per_unit=0.12):

    total_energy = df["electricity"].sum()
    anomaly_energy = df[df["final_anomaly"]==1]["electricity"].sum()

    cost_loss = anomaly_energy * cost_per_unit

    peak_hours = df[df["final_anomaly"]==1]["hour"].value_counts().to_dict()
    peak_months = df[df["final_anomaly"]==1]["month"].value_counts().to_dict()

    recommendations = []

    if cost_loss > 1000:
        recommendations.append("Immediate HVAC system inspection recommended.")
    if len(peak_hours) > 0:
        recommendations.append("Peak anomaly hours require operational adjustment.")
    if len(peak_months) > 0:
        recommendations.append("Seasonal recalibration of energy systems advised.")

    insights = {
        "total_samples": len(df),
        "anomaly_rate_percent": round(df["final_anomaly"].mean()*100,2),
        "estimated_cost_loss_$": round(cost_loss,2),
        "peak_anomaly_hours": peak_hours,
        "peak_anomaly_months": peak_months,
        "recommendations": recommendations
    }

    return insights, df