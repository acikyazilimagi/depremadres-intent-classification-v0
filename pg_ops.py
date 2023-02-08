import psycopg2
import os
from dotenv import load_dotenv

def get_data(conn, table_name, column_names, condition):
    cur = conn.cursor()
    query = "SELECT {} FROM {} WHERE {}".format(', '.join(column_names), table_name, condition)
    cur.execute(query)
    return cur.fetchall()

def update_data(conn, table_name, column_name, new_value, condition):
    cur = conn.cursor()
    query = "UPDATE {} SET {} = '{}' WHERE {}".format(table_name, column_name, new_value, condition)
    cur.execute(query)
    conn.commit()

def connect_to_db():
    # Load environment variables
    load_dotenv(".env")

    host = os.getenv('HOST')
    database = os.getenv('DATABASE')
    user = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    # Connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    return conn