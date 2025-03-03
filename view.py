def get_application_data():
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        fact_application.app_id AS Application_ID,
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

st.title("Application Overview")

data = get_application_data()
st.dataframe(data)
