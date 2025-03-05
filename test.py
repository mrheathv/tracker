import streamlit as st
import sqlite3
import os

# Function to connect to the database
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "job_tracker.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

# Ensure the table exists
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        status TEXT
    )
""")
conn.commit()
conn.close()

# Streamlit app layout
st.title("Job Tracker - Data Entry")

title = st.text_input("Job Title")
company = st.text_input("Company")
location = st.text_input("Location")
status = st.selectbox("Application Status", ["Applied", "Interviewing", "Offered", "Rejected"])

if st.button("Submit"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, company, location, status) VALUES (?, ?, ?, ?)",
                   (title, company, location, status))
    conn.commit()
    conn.close()
    st.success("Job entry added successfully!")

# Display current data
st.subheader("Current Job Entries")
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM jobs")
rows = cursor.fetchall()
conn.close()

for row in rows:
    st.write(row)
