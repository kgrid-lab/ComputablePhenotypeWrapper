import os
import urllib
from subprocess import PIPE, run

import pyodbc
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import importlib.resources as pkg_resources


def create_database(connection, database_name):
    connection.execution_options(isolation_level="AUTOCOMMIT").execute(
        text(f"CREATE DATABASE {database_name};")
    )


def delete_database(connection, database_name):
    execute(
        connection,
        f"""IF DB_ID('{database_name}') IS NOT NULL
            DROP DATABASE {database_name};""",
        allow_transaction=False,  # Disable transaction for this command
    )


def execute(connection, command, allow_transaction=True):
    if allow_transaction:
        # For normal commands, use transactions
        with connection.begin():
            connection.execute(text(command))
    else:
        # For commands like CREATE DATABASE or DROP DATABASE, use AUTOCOMMIT
        connection.execution_options(isolation_level="AUTOCOMMIT").execute(
            text(command)
        )


def run_script(sql_script, db, output):
    host, user, password = load_env()
    process = run(
        [f"sqlcmd -C -U {user} -P {password} -d {db} -i {sql_script} "],
        stderr=PIPE,
        stdout=PIPE,
        stdin=PIPE,
        shell=True,
    )  # -o {output}
    # process.stdin.write(password)
    # print(process.stderr)
    # print(process.stdout)


def connect(database=None):
    host, user, password = load_env()
    database_conn = ""
    if database:
        database_conn = ";database=" + database
        
    conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={host};UID={user};PWD={password};TrustServerCertificate=yes{database_conn}"
    params = urllib.parse.quote_plus(conn_str)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    return engine


def load_env():
    pyodbc.pooling = False
    load_dotenv()
    sql_host = os.getenv("MSSQL_HOST")
    sql_username = os.getenv("MSSQL_USERNAME")
    sql_password = os.getenv("MSSQL_PASSWORD")
    return sql_host, sql_username, sql_password

def create_tables(db_conn, database_name):
    with pkg_resources.path("computable_phenotypes", "preparation_script_mssql.sql") as sql_file_path:
        run_script(
            str(sql_file_path),
            database_name,
            None
        )
