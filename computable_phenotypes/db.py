import pyodbc
from dotenv import load_dotenv
import os
from subprocess import Popen, PIPE, run
def remove_table(db_conn,table_name):
  execute(db_conn,
          f'''if OBJECT_ID('{table_name}', 'U') is not NULL
          drop table {table_name};'''
          )
def create_database(connection,database_name):
   execute(connection,f"CREATE DATABASE {database_name};")
   connection.commit()

def delete_database(connection,database_name):
   execute(connection,
          f''' if DB_ID('{database_name}') is not NULL
          drop database {database_name};'''
          )
   connection.commit()

def execute(db_conn,command):
  db_cursor = db_conn.cursor()
  db_cursor.execute(command)
def run_script(sql_script,db,output):
    host,user,password=load_env()
    process = run([f'sqlcmd -C -U {user} -P {password} -d {db} -i {sql_script} -o {output}'], stderr=PIPE,stdout=PIPE, stdin=PIPE,shell=True)
    #process.stdin.write(password)
    #print(process.stderr)
    #print(process.stdout)
def connect(database=None):
    host,user,password=load_env()
    database_conn=""
    if database != None:
        database_conn=';database='+database
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+host+';UID='+user+';PWD='+password+';TrustServerCertificate=yes'+database_conn)
    return cnxn
def load_env():
    pyodbc.pooling = False
    load_dotenv()
    sql_host=os.getenv("MSSQL_HOST")
    sql_username=os.getenv("MSSQL_USERNAME")
    sql_password=os.getenv("MSSQL_PASSWORD")
    return sql_host,sql_username,sql_password
