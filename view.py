import streamlit as st
import sqlite3
import pandas as pd

db_path = "job_tracker.db"

def get_application_data():
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        fact_application.app_id AS Application_ID,
        dim_company.name AS Company_Name,
        dim_role.role AS Role,
        dim_status.status AS Status
    FROM fact_application
    JOIN dim_company ON fact_application.company_id = dim_company.id
    JOIN dim_role ON fact_application.role_id = dim_role.id
    JOIN dim_status ON fact_application.status_id = dim_status.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("Applications List")

# Display Total Applications and Status Counts
def get_application_summary():
    conn = sqlite3.connect(db_path)
    query = """
    SELECT COUNT(app_id) AS total_apps FROM fact_application
    """
    total_apps = pd.read_sql(query, conn).iloc[0, 0]
    
    query = """
    SELECT dim_status.status AS Status, COUNT(fact_application.app_id) AS Total_Applications
    FROM fact_application
    JOIN dim_status ON fact_application.status_id = dim_status.id
    GROUP BY dim_status.status
    """
    status_counts = pd.read_sql(query, conn)
    conn.close()
    return total_apps, status_counts

total_apps, status_counts = get_application_summary()
st.write(f"### Total Applications: {total_apps}")
for index, row in status_counts.iterrows():
    st.write(f"- {row['Status']}: {row['Total_Applications']}")

# Chart: Total Applications by Status
def get_status_counts():
    conn = sqlite3.connect(db_path)
    query = """
    SELECT dim_status.status AS Status, COUNT(fact_application.app_id) AS Total_Applications
    FROM fact_application
    JOIN dim_status ON fact_application.status_id = dim_status.id
    GROUP BY dim_status.status
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

status_data = get_status_counts()
st.bar_chart(status_data.set_index("Status"))

# Filters
company_filter = st.selectbox("Filter by Company", ["All"] + sorted(data["Company_Name"].unique().tolist()))
status_filter = st.selectbox("Filter by Status", ["All"] + sorted(data["Status"].unique().tolist()))

filtered_data = data
if company_filter != "All":
    filtered_data = filtered_data[filtered_data["Company_Name"] == company_filter]
if status_filter != "All":
    filtered_data = filtered_data[filtered_data["Status"] == status_filter]

st.dataframe(filtered_data, hide_index=True)
st.dataframe(data, hide_index=True)
