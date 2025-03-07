import streamlit as st
import sqlite3
import pandas as pd
import altair as alt


db_path = "job_tracker.db"

def get_application_data():
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
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

import altair as alt

# Create the bar chart
chart = alt.Chart(status_data).mark_bar().encode(
    x="Total_Applications:Q",
    y=alt.Y("Status:N", sort="-x"),  # Sorting bars by value
).properties(
    width=600,  # Increase width
    height=400  # Increase height
)

# Add labels on the bars
text = chart.mark_text(
    align="left",
    baseline="middle",
    dx=5  # Adjust distance from bar
).encode(
    text="Total_Applications:Q"
)

# Combine bar chart and text labels
final_chart = chart + text

st.altair_chart(final_chart, use_container_width=True)


# Fetch application data
df = get_application_data()

# Display DataFrame in Streamlit
st.write(df)

def plot_stacked_bar_chart(df):
    grouped = df.groupby(["Company_Name", "Status"]).size().unstack(fill_value=0)
    
    st.write("### Job Applications by Company and Status")
    st.bar_chart(grouped, horizontal=True)

# Show the stacked bar chart with all companies
plot_stacked_bar_chart(df)
