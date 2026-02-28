import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.preprocessing import preprocess_data
from src.feature_engineering import feature_engineering
from src.model import train_model
from src.evaluation import evaluate_model
from src.business_insight import generate_business_insights
from src.pdf_report import generate_pdf_report


# =====================================================
# PAGE CONFIG Main File 
# =====================================================
st.set_page_config(
    page_title="Energy AI Dashboard",
    layout="wide",
    page_icon="⚡"
)

st.title("⚡ Energy Anomaly Detection System")
st.markdown("AI-Powered Commercial Energy Intelligence Platform")
st.markdown("**Developed by Sagar Karosiya**")


# =====================================================
# SESSION STATE INIT
# =====================================================
if "df_final" not in st.session_state:
    st.session_state.df_final = None

if "insights" not in st.session_state:
    st.session_state.insights = None

if "evaluation_stats" not in st.session_state:
    st.session_state.evaluation_stats = None


# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.header("⚙ Configuration")

uploaded_file = st.sidebar.file_uploader(
    "Upload Energy CSV File",
    type=["csv"]
)

cost_per_unit = st.sidebar.number_input(
    "Cost per Energy Unit ($)",
    value=0.52
)

model_choice = st.sidebar.selectbox(
    "Select Anomaly Detection Model",
    [
        "Isolation Forest",
        "Local Outlier Factor (LOF)",
        "One-Class SVM",
        "Robust Covariance"
    ]
)

run_button = st.sidebar.button(" Run Analysis")


# =====================================================
# RUN PIPELINE
# =====================================================
if uploaded_file is not None and run_button:

    with st.spinner("Running ML pipeline... Please wait."):

        df = pd.read_csv(uploaded_file)

        # Auto detect timestamp column
        timestamp_found = False
        for col in df.columns:
            if "time" in col.lower():
                df.rename(columns={col: "timestamp"}, inplace=True)
                timestamp_found = True
                break

        if not timestamp_found:
            st.error(" No timestamp column detected.")
            st.stop()
        # -----------------------------
        # LOAD DATA
        # -----------------------------
        st.spinner("Data Reading..")

        
       # -------------------------------------------------
       # Preprocessing
       # -------------------------------------------------
        df = preprocess_data(df)
        

        st.header(" Preprocessing Results")
        st.spinner("Preprocessing Data..")
        col1, col2 = st.columns(2)

        col1.metric("Missing Values", df.isna().sum().sum())
        col1.metric("Timestamp Sorted",
                    df["timestamp"].is_monotonic_increasing)

        numeric_cols = df.select_dtypes(include=np.number).columns
        col2.metric("Min Scaled Value",
                    round(df[numeric_cols].min().min(), 4))
        col2.metric("Max Scaled Value",
                    round(df[numeric_cols].max().max(), 4))

        st.divider()

       # -------------------------------------------------
       # FEATURE ENGINEERING
       # -------------------------------------------------
        df = feature_engineering(df)
        st.header("⚙ Feature Engineering Results")
        st.success(f"Total Features After Engineering: {df.shape[1]}")
        st.success(f"Total Features After Engineering: {df.columns}")
        st.success("✔ Rolling deviation metrics added")
        st.success("✔ Temporal seasonality features added")
        st.success("✔ Lag & momentum features added")

        st.divider()


        # Model Training
        df, switched, model = train_model(df, model_choice)

        if switched:
            st.warning("Large dataset detected. Switched to Isolation Forest for performance.")
        st.header(" Model Results")

        anomaly_rate = round(df["final_anomaly"].mean() * 100, 2)
        total_anomalies = int(df["final_anomaly"].sum())

        col1, col2 = st.columns(2)
        col1.metric("Anomaly Rate (%)", anomaly_rate)
        col2.metric("Total Anomalies", total_anomalies)

        st.metric("Model Used", model_choice)
        st.metric("Anomaly Rate (%)", anomaly_rate)
        st.success("✔ Anomaly labels generated")
        st.success("✔ Anomaly predictions generated")
        st.success("✔ Anomaly scores computed")
        st.success("✔ Model Competitable with  Isolation Forest")
        st.success("✔ Model Competitable with  Local Outlier Factor (LOF)")
        st.success("✔ Model Competitable with  One-Class SVM")
        st.success("✔ Model Competitable with  Robust Covariance")

        st.divider()
         # -----------------------------
        # DATA OVERVIEW
        # -----------------------------
        st.header(" Data Overview")

        col_df = pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes.values
        })

        st.dataframe(col_df, width="stretch")

        st.divider()
        
        # Evaluation
        evaluation_stats = evaluate_model(df)
        
        st.header(" Evaluation Results")

        col1, col2 = st.columns(2)

        col1.metric("Total Samples",
                    evaluation_stats["Total Samples"])
        col1.metric("Total Anomalies",
                    evaluation_stats["Total Anomalies"])

        col2.metric("Anomaly Rate (%)",
                    evaluation_stats["Anomaly Rate (%)"])

        st.success("✔ Anomaly distribution statistics calculated")
        st.success("✔ Top anomalous samples identified")

        st.divider()
        # -----------------------------
        # TOP ANOMALIES
        # -----------------------------
        st.subheader(" Top 10 Most Anomalous Samples")

        if "anomaly_score" in df.columns:
            top_anomalies = df.sort_values("anomaly_score").head(10)
        else:
            top_anomalies = df[df["final_anomaly"] == 1].head(10)

        st.dataframe(top_anomalies, width="stretch")

        st.divider()
        # ----------


    # -------------------------------------------------
    # BUSINESS INSIGHTS
    # -------------------------------------------------
        st.header(" Business Insight & Impact")
        insights, df = generate_business_insights(df, cost_per_unit)

        # Save in session
        st.session_state.df_final = df
        st.session_state.insights = insights
        st.session_state.evaluation_stats = evaluation_stats
        col1, col2 = st.columns(2)
        col1.metric("Estimated Cost Impact ($)", insights["estimated_cost_loss_$"])
        col2.metric("Anomaly Rate (%)", insights["anomaly_rate_percent"])
         

# =====================================================
# DISPLAY RESULTS
# =====================================================
if st.session_state.df_final is not None:

    df = st.session_state.df_final
    insights = st.session_state.insights
    evaluation_stats = st.session_state.evaluation_stats

    # =====================================================
    # CUSTOM PEAK HOUR ANALYSIS
    # =====================================================
    st.header("Peak Hour Analysis")

    col1, col2 = st.columns(2)

    months = sorted(df["month"].unique())
    selected_month = col1.selectbox("Select Month", ["All"] + months)

    dates = sorted(df["timestamp"].dt.date.unique())
    selected_date = col2.selectbox("Select Specific Date", ["All"] + list(dates))

    df_filtered = df.copy()
    filter_label = "All Data"

    if selected_month != "All":
        df_filtered = df_filtered[df_filtered["month"] == selected_month]
        filter_label = f"Month: {selected_month}"

    if selected_date != "All":
        df_filtered = df_filtered[
            df_filtered["timestamp"].dt.date == selected_date
        ]
        filter_label = f"Date: {selected_date}"

    st.subheader(f" Peak Anomaly Hours ({filter_label})")

    peak_hours = (
        df_filtered[df_filtered["final_anomaly"] == 1]
        ["hour"]
        .value_counts()
        .sort_index()
    )

    if len(peak_hours) > 0:

        fig = px.bar(
            x=peak_hours.index,
            y=peak_hours.values,
            labels={"x": "Hour", "y": "Anomaly Count"},
            title=f"Peak Anomaly Hours - {filter_label}"
        )

        st.plotly_chart(fig, width="stretch")

        max_value = peak_hours.max()
        top_hours = peak_hours[peak_hours == max_value].index.tolist()
        hours_text = ", ".join([f"{int(h):02d}:00" for h in top_hours])

        st.markdown("### Peak Hour Summary")

        st.info(
            f"""
             Analysis Scope: **{filter_label}**

             Peak Anomaly Hour(s): **{hours_text}**

             Maximum Anomalies at that hour: **{int(max_value)}**
            """
        )

    else:
        st.warning("⚠ No anomalies found for selected filter.")

    st.divider()
    
    # -----------------------------
    # Seasonal Pattern
    # -----------------------------
    st.subheader(f" Seasonal Pattern ({filter_label})")

    monthly = df_filtered[df_filtered["final_anomaly"] == 1] \
            ["month"].value_counts().sort_index()

    if len(monthly) > 0:
         st.bar_chart(monthly)
    else:
         st.warning("No seasonal anomaly data available.")

    st.subheader(" Recommendations")
    for rec in insights["recommendations"]:
        st.success(rec)

    st.divider()

    # -------------------------------------------------
    # PDF DOWNLOAD
    # -------------------------------------------------
    st.subheader(" Download Executive Report")

    pdf_file = generate_pdf_report(df, insights, evaluation_stats)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label=" Download PDF Report",
            data=f,
            file_name="Energy_AI_Report.pdf",
            mime="application/pdf"
        )

else:
    st.info("Upload CSV file and click 'Run Analysis' to begin.")


# =====================================================
# FOOTER
# =====================================================
st.markdown(
    """
    <hr style="margin-top:50px;">
    <div style="text-align:center;font-size:14px;color:gray;">
        © 2026 Sagar Karosiya | Energy AI Dashboard <br>
        All Rights Reserved
    </div>
    """,
    unsafe_allow_html=True
)