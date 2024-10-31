import json
import os
import urllib
from subprocess import PIPE, run

import sqlite3
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import importlib.resources as pkg_resources

def create_database(database_name):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    return cursor


def delete_database(database_name):
    if os.path.exists(database_name):
        os.remove(database_name)


def execute(database_name, command):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute(command)
    connection.commit()
def run_script(sql_script, database_name, output):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    with open(sql_script, 'r') as file:
        sql_script_content = file.read()
        cursor.executescript(sql_script_content)
    connection.commit()
    connection.close()

def connect(database=None):
    # host, user, password = load_env()
    # database_conn = ""
    # if database:
    #     database_conn = ";database=" + database
        
    # conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={host};UID={user};PWD={password};TrustServerCertificate=yes{database_conn}"
    # params = urllib.parse.quote_plus(conn_str)
    # engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    return cursor

def fetch(database_name, query):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    # Run the SELECT query
    query = query
    cursor.execute(query)

    # Fetch the results and column names
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    # Convert to a list of dictionaries
    data = [dict(zip(column_names, row)) for row in rows]

    # Convert to JSON
    json_data = json.dumps(data, indent=4)

    # Close the database connection
    connection.close()
    return json_data

   
def create_tables(database_name):
    with pkg_resources.path("computable_phenotypes", "preparation_script_sqlite.sql") as sql_file_path:
        run_script(
            str(sql_file_path),
            database_name,
            None
        )