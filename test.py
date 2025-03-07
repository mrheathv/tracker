import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
import plotly.express as px


db_path = "job_tracker.db"

def get_application_data():
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        dim_company.name AS Company_Name,
        dim_role.role AS Role
    FROM fact_application
    JOIN dim_company ON fact_application.company_id = dim_company.id
    JOIN dim_role ON fact_application.role_id = dim_role.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


st.title("Applications Tracker")

def get_application_summary():
    conn = sqlite3.connect(db_path)
    query = """
    SELECT COUNT(app_id) AS total_apps FROM fact_application
    """
    total_apps = pd.read_sql(query, conn).iloc[0, 0]
    conn.close()
    return total_apps

# Display the total applications
st.header("Total Applications")
st.write(get_application_summary())

# Load application data
data = get_application_data()
st.dataframe(data)
