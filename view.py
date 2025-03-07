import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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


st.title("Application Tracker")

def get_application_summary():
    conn = sqlite3.connect(db_path)
    query = """
    SELECT COUNT(app_id) AS total_apps FROM fact_application
    """
    total_apps = pd.read_sql(query, conn).iloc[0, 0]

    conn.close()
    return total_apps

total_apps = get_application_summary()
st.write(f"### Total Applications: {total_apps}")


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
#####

# Create a horizontal bar chart with Plotly
fig = px.bar(
    status_data,
    x="Total_Applications",
    y="Status",
    orientation="h",  # Horizontal bars
    text="Total_Applications",  # Labels directly on bars
)

# Customize the layout
fig.update_traces(textposition="outside")  # Position labels outside the bars
fig.update_layout(
    title="Applications by Status",
    xaxis_title="Total Applications",
    yaxis_title="Status",
    height=500,  # Adjust height
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

#####
# Fetch application data
df = get_application_data()

def plot_stacked_bar_chart(df):
    # Count applications per company and status
    grouped = df.groupby(["Company_Name", "Status"]).size().reset_index(name="Total_Applications")

    # Create a stacked bar chart
    fig = px.bar(
        grouped,
        x="Total_Applications",
        y="Company_Name",
        color="Status",  # Different colors for statuses
        orientation="h",  # Horizontal bars
        text="Total_Applications",  # Display counts on bars
        title="Job Applications by Company and Status",
    )

    # Customize layout
    fig.update_traces(textposition="inside")  # Place labels inside bars
    fig.update_layout(
        xaxis_title="Total Applications",
        yaxis_title="Company Name",
        barmode="stack",  # Ensure stacking
        height=600,  # Adjust height for readability
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Call the function in your Streamlit app
plot_stacked_bar_chart(df)

# Connect to SQLite database
DB_PATH = "job_tracker.db"  # Adjust if needed
conn = sqlite3.connect(DB_PATH)

# Fetch interview progression data
query = "SELECT screening, interview_1, interview_2, interview_3, offer FROM fact_application;"
applications_df = pd.read_sql(query, conn)
conn.close()

# Count occurrences at each stage
stages = ["Applied", "Screening", "Interview 1", "Interview 2", "Interview 3", "Offer"]
counts = [
    len(applications_df),
    applications_df["screening"].notnull().sum(),
    applications_df["interview_1"].notnull().sum(),
    applications_df["interview_2"].notnull().sum(),
    applications_df["interview_3"].notnull().sum(),
    applications_df["offer"].notnull().sum()
]

# Create a Plotly funnel chart inside a Figure
fig = go.Figure(go.Funnel(
    y=stages,
    x=counts,
    textinfo="value+percent initial",
    marker={"color": "royalblue"}
))

# Streamlit app layout
st.markdown("<h3 style='text-align: center; margin-bottom: -20px;'>Interview Progression Funnels</h3>", unsafe_allow_html=True)
st.plotly_chart(fig)

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Connect to SQLite database
DB_PATH = "job_tracker.db"  # Adjust if needed
conn = sqlite3.connect(DB_PATH)

# Fetch interview progression data
query = "SELECT screening, interview_1, interview_2, interview_3, offer FROM fact_application;"
applications_df = pd.read_sql(query, conn)
conn.close()

# Count occurrences at each stage
stages = ["Applied", "Screening", "Interview 1", "Interview 2", "Interview 3", "Offer"]
counts = [
    len(applications_df),
    applications_df["screening"].notnull().sum(),
    applications_df["interview_1"].notnull().sum(),
    applications_df["interview_2"].notnull().sum(),
    applications_df["interview_3"].notnull().sum(),
    applications_df["offer"].notnull().sum()
]

# Calculate funnel metrics
metrics = {
    "Applications per Screening": counts[0] / counts[1] if counts[1] > 0 else 0,
    "Screenings per Interview 1": counts[1] / counts[2] if counts[2] > 0 else 0,
    "Interview 1 per Interview 2": counts[2] / counts[3] if counts[3] > 0 else 0,
    "Interview 2 per Interview 3": counts[3] / counts[4] if counts[4] > 0 else 0,
    "Interview 3 per Offer": counts[4] / counts[5] if counts[5] > 0 else 0
}

# Convert to DataFrame
metrics_df = pd.DataFrame(list(metrics.items()), columns=["Metric", "Value"])

# Create a Plotly bar chart
fig = px.bar(
    metrics_df,
    x="Metric",
    y="Value",
    title="Funnel Metrics Breakdown",
    text_auto=".2f",
    labels={"Value": "Ratio"},
    color="Metric"
)

# Use Markdown with custom styling for a smaller title with reduced spacing
st.plotly_chart(fig)

# Display the raw funnel metrics data
st.dataframe(metrics_df, hide_index=True)


# Connect to SQLite database
DB_PATH = "job_tracker.db"  # Adjust if needed
conn = sqlite3.connect(DB_PATH)

# Fetch role category and location data along with application counts
query = """
SELECT dr.role_category, dr.location, COUNT(fa.app_id) as application_count
FROM fact_application fa
JOIN dim_role dr ON fa.role_id = dr.id
GROUP BY dr.role_category, dr.location
ORDER BY application_count DESC;
"""
role_location_df = pd.read_sql(query, conn)
conn.close()

# Create a grouped bar chart using Plotly
fig = px.bar(
    role_location_df,
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

st.markdown("<h3 style='text-align: center; margin-bottom: -20px;'>Company, Role, Status</h3>", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True, hide_index=True)
