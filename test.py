import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

db_path = "job_tracker.db"

def get_data(table):
    conn = sqlite3.connect(db_path)
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_application_data():
    conn = sqlite3.connect(db_path)
    query = """
        SELECT fa.company_id, fa.status_id, dc.name AS company_name, ds.status AS status_name
        FROM fact_application fa
        JOIN dim_company dc ON fa.company_id = dc.id
        JOIN dim_status ds ON fa.status_id = ds.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("Job Tracker")

st.header("View Data")
table_option = st.selectbox("Select a table to view", ["fact_application", "dim_company", "dim_role", "dim_status"])
data = get_data(table_option)
st.dataframe(data)

st.header("Job Applications by Company and Status")
application_data = get_application_data()

# Aggregate data for visualization
df_grouped = application_data.groupby(["company_name", "status_name"]).size().unstack(fill_value=0)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
df_grouped.plot(kind='barh', stacked=True, ax=ax)
ax.set_xlabel("Number of Applications")
ax.set_ylabel("Company")
ax.set_title("Job Applications by Company and Status")
ax.legend(title="Application Status", bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig)

def insert_entry(company_id, role_id, referral, date_applie, status_id, screening, interview_1, interview_2, interview_3, offer):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fact_application (company_id, role_id, referral, date_applie, status_id, screening, interview_1, interview_2, interview_3, offer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (company_id, role_id, referral, date_applie, status_id, screening, interview_1, interview_2, interview_3, offer))
    conn.commit()
    conn.close()
