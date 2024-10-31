import os
import urllib
from subprocess import PIPE, run

import pyodbc
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


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


def remove_table(db_conn, table_name):
    execute(
        db_conn,
        f"""if OBJECT_ID('{table_name}', 'U') is not NULL
          drop table {table_name};""",
    )


def create_tables(db_conn):
    remove_table(db_conn, "dbo.Encounter")
    remove_table(db_conn, "dbo.Diagnosis")
    remove_table(db_conn, "dbo.Demographic")
    encounter = """CREATE TABLE dbo.Encounter (
    PATID int,
	  ENCOUNTERID nvarchar(30) NULL,
    ADMIT_DATE datetime NULL,
    ENC_Type nvarchar(30) NULL,
    Raw_Enc_Type nvarchar(30) NULL ,
    DISCHARGE_DATE datetime NULL
    );"""
    diagnosis = """
    CREATE TABLE dbo.Diagnosis
    (
        PATID int,
        DIAGNOSISID nvarchar(10) NULL,
        DX nvarchar(10) NULL,
        DX_Type nvarchar(30) NULL,
        DX_Source nvarchar(30) NULL,
        ENCOUNTERID nvarchar(30) NULL
    );"""
    demo = """
  CREATE TABLE dbo.Demographic
  (
    PATID int,
    BIRTH_DATE datetime,
    SEX nvarchar(2),
    HISPANIC nvarchar(2),
    RACE nvarchar(2)
    );"""
    execute(db_conn, encounter)
    execute(db_conn, diagnosis)
    execute(db_conn, demo)
