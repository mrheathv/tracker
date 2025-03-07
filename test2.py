import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Connect to SQLite database
DB_PATH = "job_tracker.db"  # Adjust if needed
conn = sqlite3.connect(DB_PATH)

# Fetch interview progression data
query = "SELECT screening, interview_1, interview_2, interview_3, offer FROM fact_application;"
applications_df = pd.read_sql(query, conn)
conn.close()

# Count occurrences at each stage
stages = ["Applied", "Screening", "Interview 1", "Interview 2", "Interview 3", "Offer"]
counts = [
    len(applications_df),
    applications_df["screening"].notnull().sum(),
    applications_df["interview_1"].notnull().sum(),
    applications_df["interview_2"].notnull().sum(),
    applications_df["interview_3"].notnull().sum(),
    applications_df["offer"].notnull().sum()
]

# Calculate funnel metrics
metrics = {
    "Applications per Screening": counts[0] / counts[1] if counts[1] > 0 else 0,
    "Screenings per Interview 1": counts[1] / counts[2] if counts[2] > 0 else 0,
    "Interview 1 per Interview 2": counts[2] / counts[3] if counts[3] > 0 else 0,
    "Interview 2 per Interview 3": counts[3] / counts[4] if counts[4] > 0 else 0,
    "Interview 3 per Offer": counts[4] / counts[5] if counts[5] > 0 else 0
}

# Convert to DataFrame
metrics_df = pd.DataFrame(list(metrics.items()), columns=["Metric", "Value"])

# Create a Plotly bar chart
fig = px.bar(
    metrics_df,
    x="Metric",
    y="Value",
    title="Funnel Metrics Breakdown",
    text_auto=".2f",
    labels={"Value": "Ratio"},
    color="Metric"
)

# Use Markdown with custom styling for a smaller title with reduced spacing
st.markdown("<h3 style='text-align: center; margin-bottom: -20px;'>Interview Progression Funnel</h3>", unsafe_allow_html=True)
st.plotly_chart(fig)

# Display the raw funnel metrics data
st.dataframe(metrics_df)
