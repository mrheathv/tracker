import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px  # Import Plotly

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

# 📈 **Applications Over Time (Plotly)**
st.subheader("📈 Applications Over Time")

# Aggregate data by month
applications_over_time = df.groupby(df["date_applied"].dt.to_period("M")).size().reset_index(name="count")
applications_over_time["date_applied"] = applications_over_time["date_applied"].astype(str)  # Convert Period to String

# Create Plotly Bar Chart
fig = px.bar(applications_over_time, x="date_applied", y="count",
             labels={"date_applied": "Month", "count": "Number of Applications"},
             title="📈 Applications Submitted Over Time")

# Show the chart in Streamlit
st.plotly_chart(fig)

