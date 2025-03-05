import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

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

# Allow user to filter number of companies displayed
num_companies = st.slider("Select number of companies to display", min_value=5, max_value=len(df["Company_Name"].unique()), value=10)

def plot_stacked_bar_chart(df, num_companies):
    grouped = df.groupby(["Company_Name", "Status"]).size().reset_index(name="Count")
    top_companies = grouped.groupby("Company_Name")["Count"].sum().nlargest(num_companies).index
    filtered_df = grouped[grouped["Company_Name"].isin(top_companies)]
    
    fig = px.bar(
        filtered_df,
        x="Count",
        y="Company_Name",
        color="Status",
        orientation="h",
        title="Job Applications by Company and Status",
        labels={"Count": "Number of Applications", "Company_Name": "Company"},
        text="Count"
    )
    fig.update_layout(barmode="stack")
    st.plotly_chart(fig)

# Show the stacked bar chart with dynamic company selection
plot_stacked_bar_chart(df, num_companies)
