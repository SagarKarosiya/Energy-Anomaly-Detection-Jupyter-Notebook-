⚡ Energy Anomaly Detection System
An end-to-end Machine Learning project for detecting energy consumption anomalies in commercial buildings using Isolation Forest and deployed as an interactive Streamlit dashboard.

💻 Project Overview
Commercial buildings consume ~30% of global energy, generating billions in operational costs annually.

Unexpected energy spikes due to:

Equipment failures
Operational inefficiencies
Occupancy mismatches
System faults
This project builds a multivariate time-series anomaly detection system to automatically detect abnormal energy usage patterns.

Key Features

🔹 Advanced Data Preprocessing
Timestamp normalization

Missing value handling (forward/backward fill)

Outlier capping at 99th percentile

Min-Max scaling to [0,1]

Automatic energy column detection
🔹 50+ Engineered Features
Temporal Features

 Hour, Day, Month

 Day of Week

 Quarter

 Weekend indicator

 Cyclical Encoding

 Hour sine/cosine

 Month sine/cosine

 Rolling Statistics

 Rolling mean (6, 12, 24, 48, 168 hours)

 Rolling standard deviation

 Rolling min/max

 Lag Features

  Lag 1, 2, 3, 6, 12, 24, 48, 72, 168, 336

Deviation Metrics

 Z-score (24-hour & 168-hour window)
Machine Learning Models
Supported anomaly detection models:

✅ Isolation Forest

✅ Local Outlier Factor (LOF)

✅ One-Class SVM

✅ Robust Covariance (Elliptic Envelope)
🧠 Smart Model Switching
For large datasets (>300,000 rows), the system automatically switches to Isolation Forest for performance optimization.
Evaluation Metrics

Total Samples

Total Anomalies

Anomaly Detection Rate (~5%)

Feature importance ranking

Anomaly distribution statistics

Top anomalous samples identified
Business Insights & Impact

The system translates ML output into business value:

 💰 Estimated cost impact calculation

 📅 Seasonal anomaly analysis

 🕒 Peak anomaly hours identification

 🔎 Anomaly type classification

 📈 Executive recommendations
Momentum-based anomaly indicators

Interactive Dashboard
Built with Streamlit.
Features:

Upload custom CSV dataset

Select ML model

View anomaly detection metrics

Visualize anomalies on time-series plots

Download executive PDF report

View engineered feature list

Display column data types
Professional footer branding

🧠 ML Approach
Multivariate Time-Series Data
Feature Engineering (Rolling Statistics + Time Features)
Isolation Forest (Unsupervised Anomaly Detection)
Feature Scaling (StandardScaler)
📁 Project Structure
MajorProject_Evoastra/
│
├── Data
│
├──scr
    ├── data_loader.py
    │
    ├── preprocessing.py
    │
    ├── feature_engineering.py
    │
    ├── model.py
    │
    ├── evaluation.py
    │
    ├── business_insight.py
    │
    ├── pdf_report.py
│
├── requirements.txt
└── Streamlit Dashboard (app.py)
📁 Project Architecture
CSV Data
   ↓
data_loader.py
   ↓
preprocessing.py
   ↓
feature_engineering.py
   ↓
model.py
   ↓
evaluation.py
   ↓
business_insight.py
   ↓
pdf_report.py
   ↓
Streamlit Dashboard
How It Works 🤔
Load energy datasets (Electricity, Hot Water, Chilled Water)
Clean & preprocess time-series data
Generate statistical and temporal features
Train Isolation Forest model
Detect anomalies
Visualize anomalies in interactive dashboard
📊 Dashboard Features
Interactive energy type selection
Anomaly visualization (red markers)
KPI summary metrics
Download anomaly data
Real-time ML pipeline execution
How to run ML Model In my PC 😁✌️💻
Installation
1️⃣ Clone Repository
https://github.com/SagarKarosiya/Energy-Anomaly-Detection-.git

2️⃣ Create Virtual Environment
python -m venv venv venv\Scripts\activate

3️⃣ Install Requirements
pip install -r requirements.txt

4️⃣ Run Dashboard
Paste the command in your terminal of VS Code : streamlit run app.py

Open in browser: http://localhost:8501

Sample Dataset Format
Required columns:

  timestamp

  energy columns (electricity, water, gas, etc.)

  optional weather variables

  Timestamp must be in datetime-compatible format.
📱 Deployment
This project can be deployed on:

Streamlit
Link :https://nstnjn6q3kqdqwafkrbkg2.streamlit.app/
Dependencies
 Python 3.9+

 pandas

 numpy

 scikit-learn

  streamlit

  plotly

  reportlab
🏆 Key Highlights
✔ Industrial-scale time-series dataset
✔ Multivariate anomaly detection
✔ Modular ML pipeline architecture
✔ Interactive web dashboard
✔ Production-ready structure

📈 Future Improvements
Weather data integration
SHAP explainability
Model persistence
Real-time anomaly detection
Cloud deployment with CI/CD
License
This project is for academic and research purposes. All Rights Reserved © 2026 Sagar Karosiya

👨‍💻 Author
Sagar Karosiya
AI & ML Engineer | Game Developer | Data Scientist

https://sagarkarosiya-portfolio.onrender.com/
⭐ If You Like This Project
Give it a star ⭐ on GitHub!
