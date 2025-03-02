import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connect to database
db_path = "job_tracker.db"
conn = sqlite3.connect(db_path)

# Load data
df = pd.read_sql("SELECT * FROM fact_application", conn)
df_company = pd.read_sql("SELECT ID, Name FROM dim_company", conn)
df_status = pd.read_sql("SELECT ID, Status FROM dim_status", conn)

# Close connection
conn.close()

# Normalize column names
df.columns = df.columns.str.lower().str.replace(" ", "_")
df_company.columns = df_company.columns.str.lower().str.replace(" ", "_")
df_status.columns = df_status.columns.str.lower().str.replace(" ", "_")

# Merge company names and status names
df = df.merge(df_company, left_on="company_id", right_on="id", how="left").drop(columns=["company_id", "id"])
df = df.rename(columns={"name": "company_name"})
df = df.merge(df_status, left_on="status_id", right_on="id", how="left").drop(columns=["status_id", "id"])
df = df.rename(columns={"status": "application_status"})

# Convert date column to datetime format
df["date_applied"] = pd.to_datetime(df["date_applied"])

# Streamlit App Title
st.title("📊 Job Application Tracker")

# Sidebar Filters
company_filter = st.sidebar.multiselect("Filter by Company", df["company_name"].unique())
status_filter = st.sidebar.multiselect("Filter by Status", df["application_status"].unique())

# Apply filters
if company_filter:
    df = df[df["company_name"].isin(company_filter)]
if status_filter:
    df = df[df["application_status"].isin(status_filter)]

# Display Data Table
st.dataframe(df)

# 📊 **Interview Progression Funnel**
st.subheader("📝 Interview Progression Funnel")

# Calculate Interview Stages
interview_stages = ["screening", "interview_1", "interview_2", "interview_3", "offer"]
interview_counts = {stage: df[stage].notna().sum() for stage in interview_stages}
interview_counts["total_applications"] = len(df)

# Order categories for visualization
ordered_keys = ["total_applications", "screening", "interview_1", "interview_2", "interview_3", "offer"]
ordered_values = [interview_counts[key] for key in ordered_keys]

# Generate Horizontal Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(ordered_keys, ordered_values, align="center")
ax.set_xlabel("Number of Applications")
ax.set_ylabel("Interview Stages")
ax.set_title("📝 Interview Progression Funnel (Total Applications First)")
ax.invert_yaxis()  # Invert for better visual alignment

# Display in Streamlit
st.pyplot(fig)
