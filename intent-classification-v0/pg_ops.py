import psycopg2
import os
from dotenv import load_dotenv
from typing import List, Tuple, Any

def get_data(conn: psycopg2.connection, table_name: str, column_names: List[str], condition: str) -> List[Tuple]:
    """ Get data from the table

    Args:
        conn: PostgreSQL connection object
        table_name: Table name to get data
        column_names: Name of the columns to select
        condition: WHERE condition

    Returns:
        Query results
    """
    cur = conn.cursor()
    query = "SELECT {} FROM {} WHERE {}".format(', '.join(column_names), table_name, condition)
    # query for filtering data with multiple claueses
    # query = "SELECT {} FROM {} WHERE is_done = True AND intent_result = ''".format(', '.join(column_names), table_name)
    cur.execute(query)
    return cur.fetchall()

def update_data(conn: psycopg2.connection, table_name: str, column_name: str, new_value: Any, condition: str) -> None:
    """ Update data in the table

    Args:
        conn: PostgreSQL connection object
        table_name: Table name to update data
        column_name: Name of the column to update
        new_value: New value for the column
        condition: WHERE condition
    """

    cur = conn.cursor()
    query = "UPDATE {} SET {} = '{}' WHERE {}".format(table_name, column_name, new_value, condition)
    cur.execute(query)
    conn.commit()

def connect_to_db():
    """ Connect to the database

    Returns:
        PostgreSQL connection object
    """
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