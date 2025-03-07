# Connect to the SQLite database
DB_PATH = "job_tracker.db"  # Ensure this matches the correct path in your setup
conn = sqlite3.connect(DB_PATH)

# Fetch application data over time
query = '''
SELECT date_applie AS application_date, COUNT(app_id) AS application_count
FROM fact_application
GROUP BY application_date
ORDER BY application_date;
'''
applications_over_time_df = pd.read_sql(query, conn)
conn.close()

# Convert application_date to datetime
applications_over_time_df['application_date'] = pd.to_datetime(applications_over_time_df['application_date'])

# Create a line chart with Plotly
fig = px.line(
    applications_over_time_df,
    x='application_date',
    y='application_count',
    title='Applications Over Time',
    labels={'application_date': 'Date', 'application_count': 'Number of Applications'},
    markers=True
)

# Display in Streamlit
st.markdown("<h3 style='text-align: center; margin-bottom: -20px;'>Applications Over Time</h3>", unsafe_allow_html=True)
st.plotly_chart(fig)
