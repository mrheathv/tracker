import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

db_path = "job_tracker.db"

def get_application_data():
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        dim_company.name AS Company_Name,
        dim_status.status AS Status
    FROM fact_application
    JOIN dim_company ON fact_application.company_id = dim_company.id
    JOIN dim_status ON fact_application.status_id = dim_status.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("Applications List")

# Fetch application data
df = get_application_data()

# Display DataFrame in Streamlit
st.write(df)

# Create a stacked bar chart
def plot_stacked_bar_chart(df):
    grouped = df.groupby(["Company_Name", "Status"]).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped.plot(kind="barh", stacked=True, ax=ax)
    ax.set_xlabel("Number of Applications")
    ax.set_ylabel("Company")
    ax.set_title("Job Applications by Company and Status")
    st.pyplot(fig)

# Show the stacked bar chart
plot_stacked_bar_chart(df)
