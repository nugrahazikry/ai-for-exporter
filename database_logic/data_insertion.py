import pandas as pd
from datetime import date
import psycopg2

#######################
# Build up
# the connection
#######################

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

#######################
# Function to insert
# the data
#######################

def insert_data_logic(df, table_name):

    column_list = df.columns.to_list()
    column_target =", ".join(column_list)

    s_variable = ["%s"] * len(column_list)
    s_variable_target =", ".join(s_variable)

    # Insert Data without UNIQUE constraint on question_id
    insert_query = f"""
    INSERT INTO {table_name} ({column_target})
    VALUES ({s_variable_target});
    """  # No ON CONFLICT because question_id is not unique anymore

    # for col in df.select_dtypes(include=['datetime64[ns]']).columns:
    #     df[col] = df[col].apply(lambda x: x.to_pydatetime() if pd.notnull(x) else None)

    # Convert DataFrame to a list of tuples
    # data_to_insert = df.to_records(index=False).tolist()
    data_to_insert = [tuple(row) for row in df.itertuples(index=False, name=None)]

    # Insert the data
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()

    print(f"{table_name} Data uploaded successfully!")

#######################
# Insert main company 
# table
#######################

company_data = pd.read_excel("../data/company_main_data.xlsx",sheet_name="company_database")
company_data['user_id'] = company_data['user_id'].astype(str)
company_data['password'] = company_data['password'].astype(str)
company_data['timestamp_join'] = pd.to_datetime(company_data['timestamp_join'], unit='ns', errors='coerce')

table_name = "company_main_data"
# insert_data_logic(company_data, table_name)


#######################
# Insert user daily 
# token quota
#######################

user_daily_quota = company_data[['user_id', 'username']].copy()
user_daily_quota['quota_date'] = pd.to_datetime(date.today()).date()

user_daily_quota['daily_token_quota'] = 10
user_daily_quota['daily_token_quota'] = user_daily_quota['daily_token_quota'].astype(int)

user_daily_quota = user_daily_quota[['quota_date', 'user_id', 'username', 'daily_token_quota']]

table_name = "user_daily_token"
# insert_data_logic(user_daily_quota, table_name)

#######################
# Insert service daily
# usage
#######################

# Define the dictionary
usage_data = {
      "usage_date": ["05/10/2025", "05/10/2025"],
        "service_name": ["uncomtrade api", "google gemini api"],
      "service_key_id": ["uncomtrade_1", "gemini_1"],
      "daily_token_usage": [0, 0]
}

# Convert dictionary to DataFrame
api_usage_df = pd.DataFrame(usage_data)

# Convert usage_date to proper date format (YYYY-MM-DD)
api_usage_df['usage_date'] = pd.to_datetime(api_usage_df['usage_date'], format='%d/%m/%Y').dt.date

# Ensure daily_token_usage is integer
api_usage_df['daily_token_usage'] = api_usage_df['daily_token_usage'].astype(int)

table_name = "service_daily_usage"
insert_data_logic(api_usage_df, table_name)


#######################
# Insert image analysis
# dummy
#######################



#######################
# Insert country 
# trend analysis dummy
#######################