import psycopg2

USER = "postgres"
PASSWORD = "nusamatch_secure_2024"
DBNAME = "nusamatch"
HOST = "10.5.30.167"

# Connect to PostgreSQL (connect to default database first)
conn = psycopg2.connect(
    dbname=DBNAME,   # connect to the default db first
    user=USER,
    password=PASSWORD,
    host=HOST,
    port="5432"
)

cursor = conn.cursor()

def delete_table(table_name):

    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    cursor.execute(drop_table_query)
    conn.commit()
    print(f"{table_name} dropped successfully!")

    cursor.close()
    conn.close()

# delete_table("company_main_data")
# delete_table("user_daily_token")
# delete_table("service_daily_usage")
# delete_table("ai_ocr_analysis_metadata")
# delete_table("trend_country_analysis_metadata")