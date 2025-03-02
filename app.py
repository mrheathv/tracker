import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Connect to database (Use SQLite for now)
engine = create_engine("sqlite:///job_tracker.db")

st.title("📊 Job Application Tracker")

# Load application data
df = pd.read_sql("SELECT * FROM fact_application", engine)

# Sidebar Filters
company_filter = st.sidebar.multiselect("Filter by Company", df['company_id'].unique())
status_filter = st.sidebar.multiselect("Filter by Status", df['status_id'].unique())

# Apply filters
if company_filter:
    df = df[df['company_id'].isin(company_filter)]
if status_filter:
    df = df[df['status_id'].isin(status_filter)]

# Display data
st.dataframe(df)

# Show application status distribution
st.subheader("Application Status Distribution")
status_counts = df['status_id'].value_counts()
st.bar_chart(status_counts)

# Show applications by company
st.subheader("Applications by Company")
company_counts = df['company_id'].value_counts()
st.bar_chart(company_counts)
