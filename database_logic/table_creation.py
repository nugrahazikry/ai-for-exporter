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


###########################
# Generate company 
# database table
###########################
cursor.execute("""
     CREATE TABLE IF NOT EXISTS company_main_data (
        id SERIAL PRIMARY KEY,
        timestamp_join TIMESTAMP,
        user_id VARCHAR(50),
        company_name VARCHAR(50),
        company_entrepreneur_type TEXT,
        company_product TEXT,
        export_experience TEXT,
        export_target_country TEXT,
        company_domicile TEXT,
        contact_person VARCHAR(50),
        username VARCHAR(50),
        password VARCHAR(50)
    );
""")
conn.commit()


###########################
# Generate user
# daily token quota
###########################
cursor.execute("""
     CREATE TABLE IF NOT EXISTS user_daily_token (
        id SERIAL PRIMARY KEY,
        quota_date DATE,
        user_id VARCHAR(50),
        username VARCHAR(50),
        daily_token_quota INTEGER
    );
""")
conn.commit()


###########################
# Record service api
# daily usage
###########################
cursor.execute("""
     CREATE TABLE IF NOT EXISTS service_daily_usage (
        id SERIAL PRIMARY KEY,
        usage_date DATE,
        service_name VARCHAR(50),
        service_key_id VARCHAR(50),
        daily_token_usage INTEGER
    );
""")
conn.commit()


###########################
# Record ai ocr analysis
# user metadata
###########################
cursor.execute("""
     CREATE TABLE IF NOT EXISTS ai_ocr_analysis_metadata (
        id SERIAL PRIMARY KEY,
        timestamp_process TIMESTAMP,
        user_id VARCHAR(50),
        request_id VARCHAR(50),
        is_correction BOOLEAN,
        product_name VARCHAR(50),
        product_category VARCHAR(50),
        hs_code VARCHAR(50),
        common_trade_name VARCHAR(50)
    );
""")
conn.commit()


###########################
# Record product trend
# analysis within specific countries
###########################
cursor.execute("""
     CREATE TABLE IF NOT EXISTS trend_country_analysis_metadata (
        id SERIAL PRIMARY KEY,
        timestamp_process TIMESTAMP,
        user_id VARCHAR(50),
        request_id VARCHAR(50),
        is_correction BOOLEAN,
        product_name VARCHAR(50),
        country_1 VARCHAR(50),
        detail_country_1 JSONB,
        country_2 VARCHAR(50),
        detail_country_2 JSONB,
        country_3 VARCHAR(50),
        detail_country_3 JSONB
    );
""")
conn.commit()

cursor.close()
conn.close()