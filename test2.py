import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Connect to SQLite database
DB_PATH = "job_tracker.db"  # Adjust if needed
conn = sqlite3.connect(DB_PATH)

# Fetch role, company, and application data
query = """
SELECT dr.role_category, dr.location, dc.number_of_employees AS company_size, 
       dc.industry AS company_industry, fa.referral, COUNT(fa.app_id) as application_count
FROM fact_application fa
JOIN dim_role dr ON fa.role_id = dr.id
JOIN dim_company dc ON fa.company_id = dc.id
GROUP BY dr.role_category, dr.location, dc.number_of_employees, dc.industry, fa.referral
ORDER BY application_count DESC;
"""
role_location_df = pd.read_sql(query, conn)
conn.close()

# Sidebar filters
st.sidebar.header("Filter Applications")

# Filter by Referral
referral_options = ["All"] + sorted(role_location_df["referral"].dropna().unique().tolist())
selected_referral = st.sidebar.selectbox("Application Referral", referral_options)

# Filter by Role Category
role_options = ["All"] + sorted(role_location_df["role_category"].dropna().unique().tolist())
selected_role = st.sidebar.selectbox("Role Category", role_options)

# Filter by Role Location
location_options = ["All"] + sorted(role_location_df["location"].dropna().unique().tolist())
selected_location = st.sidebar.selectbox("Role Location", location_options)

# Filter by Company Size
company_size_options = ["All"] + sorted(role_location_df["company_size"].dropna().unique().tolist())
selected_company_size = st.sidebar.selectbox("Company Size", company_size_options)

# Filter by Company Industry
industry_options = ["All"] + sorted(role_location_df["company_industry"].dropna().unique().tolist())
selected_industry = st.sidebar.selectbox("Company Industry", industry_options)

# Apply filters
filtered_df = role_location_df.copy()
if selected_referral != "All":
    filtered_df = filtered_df[filtered_df["referral"] == selected_referral]
if selected_role != "All":
    filtered_df = filtered_df[filtered_df["role_category"] == selected_role]
if selected_location != "All":
    filtered_df = filtered_df[filtered_df["location"] == selected_location]
if selected_company_size != "All":
    filtered_df = filtered_df[filtered_df["company_size"] == selected_company_size]
if selected_industry != "All":
    filtered_df = filtered_df[filtered_df["company_industry"] == selected_industry]

# Create a grouped bar chart using Plotly
fig = px.bar(
    filtered_df,
    x="role_category",
    y="application_count",
    color="location",
    barmode="group",
    title="Applications by Role Category and Location",
    labels={"application_count": "Number of Applications", "role_category": "Role Category", "location": "Location"}
)

# Use Markdown with custom styling for a smaller title with reduced spacing
st.markdown("<h3 style='text-align: center; margin-bottom: -20px;'>Applications by Role and Location</h3>", unsafe_allow_html=True)
st.plotly_chart(fig)

# Display the raw filtered data
st.dataframe(filtered_df)
