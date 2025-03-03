import streamlit as st
import sqlite3
import pandas as pd

db_path = "job_tracker.db"

def get_data(table):
    conn = sqlite3.connect(db_path)
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("Job Tracker")

st.header("View Data")
table_option = st.selectbox("Select a table to view", ["fact_application", "dim_company", "dim_role", "dim_status"])
data = get_data(table_option)
st.dataframe(data)

def insert_entry(company_id, role_id, referral, date_applie, status_id, screening, interview_1, interview_2, interview_3, offer):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fact_application (company_id, role_id, referral, date_applie, status_id, screening, interview_1, interview_2, interview_3, offer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (company_id, role_id, referral, date_applie, status_id, screening, interview_1, interview_2, interview_3, offer))
    conn.commit()
    conn.close()
    st.rerun()

def update_entry(app_id, column, new_value):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE fact_application SET {column} = ? WHERE app_id = ?", (new_value, app_id))
    conn.commit()
    conn.close()
    st.rerun()

def delete_entry(app_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fact_application WHERE app_id = ?", (app_id,))
    conn.commit()
    conn.close()
    st.rerun()

st.header("Add New Application")
company_names = get_data("dim_company")["name"].tolist()
company_name = st.selectbox("Company Name", company_names)
company_id = get_data("dim_company").set_index("name").loc[company_name, "id"]
role_id = st.number_input("Role ID", min_value=1, step=1)
referral = st.text_input("Referral (X or blank)")
date_applie = st.date_input("Date Applied")
status_id = st.number_input("Status ID", min_value=1, step=1)
screening = st.text_input("Screening (X or blank)")
interview_1 = st.text_input("Interview 1 (X or blank)")
interview_2 = st.text_input("Interview 2 (X or blank)")
interview_3 = st.text_input("Interview 3 (X or blank)")
offer = st.text_input("Offer (X or blank)")
if st.button("Add Application"):
    insert_entry(company_id, role_id, referral, date_applie, status_id, screening, interview_1, interview_2, interview_3, offer)

st.header("Update Application")
app_id = st.number_input("Application ID", min_value=1, step=1)
column = st.selectbox("Column to Update", ["company_id", "role_id", "referral", "date_applie", "status_id", "screening", "interview_1", "interview_2", "interview_3", "offer"])
new_value = st.text_input("New Value")
if st.button("Update Application"):
    update_entry(app_id, column, new_value)

st.header("Delete Application")
del_app_id = st.number_input("Application ID to Delete", min_value=1, step=1)
if st.button("Delete Application"):
    delete_entry(del_app_id)
