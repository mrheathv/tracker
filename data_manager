import streamlit as st
import pandas as pd
import sqlite3

# Connect to database
db_path = "job_tracker.db"

def get_connection():
    return sqlite3.connect(db_path)

# Load dropdown data
def load_dropdown_data():
    conn = get_connection()
    df_company = pd.read_sql("SELECT company_id, name FROM dim_company", conn)
    df_status = pd.read_sql("SELECT status_id, status FROM dim_status", conn)
    df_role = pd.read_sql("SELECT role_id, role FROM dim_role", conn)
    conn.close()
    return df_company, df_status, df_role

# Load applications
def load_applications():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM fact_application", conn)
    conn.close()
    return df

# Insert new application
def insert_application(company_id, role_id, date_applied, status_id, referral, screening, interview_1, interview_2, interview_3, offer):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fact_application (company_id, role_id, date_applied, status_id, referral, screening, interview_1, interview_2, interview_3, offer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (company_id, role_id, date_applied, status_id, referral, screening, interview_1, interview_2, interview_3, offer))
    conn.commit()
    conn.close()

# Update existing application
def update_application(app_id, status_id, referral, screening, interview_1, interview_2, interview_3, offer):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE fact_application 
        SET status_id=?, referral=?, screening=?, interview_1=?, interview_2=?, interview_3=?, offer=?
        WHERE app_id=?
    """, (status_id, referral, screening, interview_1, interview_2, interview_3, offer, app_id))
    conn.commit()
    conn.close()

# Delete application
def delete_application(app_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fact_application WHERE app_id=?", (app_id,))
    conn.commit()
    conn.close()

# Streamlit UI
st.title("📝 Job Application Data Manager")
df_company, df_status, df_role = load_dropdown_data()
df = load_applications()

# Add New Application
st.subheader("➕ Add a New Application")
with st.form("add_form"):
    company = st.selectbox("Company", df_company["name"].tolist())
    role = st.selectbox("Job Role", df_role["role"].tolist())
    date_applied = st.date_input("Date Applied")
    status = st.selectbox("Application Status", df_status["status"].tolist())
    referral = st.text_input("Referral (Leave blank if none)")
    screening = st.checkbox("Completed Screening?")
    interview_1 = st.checkbox("Completed Interview 1?")
    interview_2 = st.checkbox("Completed Interview 2?")
    interview_3 = st.checkbox("Completed Interview 3?")
    offer = st.checkbox("Received Offer?")
    submit = st.form_submit_button("Submit Application")

if submit:
    company_id = df_company[df_company["name"] == company]["company_id"].values[0]
    role_id = df_role[df_role["role"] == role]["role_id"].values[0]
    status_id = df_status[df_status["status"] == status]["status_id"].values[0]
    insert_application(company_id, role_id, date_applied, status_id, referral, screening, interview_1, interview_2, interview_3, offer)
    st.success("✅ Application added successfully!")
    st.experimental_rerun()

# Modify Existing Applications
st.subheader("✏️ Modify Existing Applications")
app_id = st.selectbox("Select Application to Edit", df["app_id"].tolist())
if app_id:
    selected_app = df[df["app_id"] == app_id].iloc[0]
    new_status = st.selectbox("Update Status", df_status["status"].tolist(), index=df_status[df_status["status_id"] == selected_app["status_id"]].index[0])
    new_referral = st.text_input("Update Referral", selected_app["referral"])
    new_screening = st.checkbox("Completed Screening?", selected_app["screening"])
    new_interview_1 = st.checkbox("Completed Interview 1?", selected_app["interview_1"])
    new_interview_2 = st.checkbox("Completed Interview 2?", selected_app["interview_2"])
    new_interview_3 = st.checkbox("Completed Interview 3?", selected_app["interview_3"])
    new_offer = st.checkbox("Received Offer?", selected_app["offer"])
    update = st.button("Update Application")
    delete = st.button("❌ Delete Application")

    if update:
        status_id = df_status[df_status["status"] == new_status]["status_id"].values[0]
        update_application(app_id, status_id, new_referral, new_screening, new_interview_1, new_interview_2, new_interview_3, new_offer)
        st.success("✅ Application updated successfully!")
        st.experimental_rerun()

    if delete:
        delete_application(app_id)
        st.success("🗑️ Application deleted successfully!")
        st.experimental_rerun()

# Display Current Applications
df_display = df.merge(df_company, left_on="company_id", right_on="company_id", how="left").merge(df_status, left_on="status_id", right_on="status_id", how="left").merge(df_role, left_on="role_id", right_on="role_id", how="left")
st.subheader("📊 Current Applications")
st.dataframe(df_display)
