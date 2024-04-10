import mysql.connector
from dotenv import load_dotenv
import pandas as pd
import os
def create_table_def(db_conn):
  db_cursor = db_conn.cursor()
  encounter='''CREATE TABLE PCOR_Encounters (
    PATID int,
    ENCOUNTERID int,
    ADMIT_DATE date,
    DISCHARGE_DATE date
    );'''
  #diagnosis=""
  #demographic=""
  db_cursor.execute(encounter)
  #db_cursor.execute(diagnosis)
  #db_cursor.execute(demographic)
def tester(database):
  sql_host=os.getenv("SQL_HOST")
  sql_username=os.getenv("SQL_USERNAME")
  sql_password=os.getenv("SQL_PASSWORD")
  mydb = mysql.connector.connect(
    host=sql_host,
    user=sql_username,
    password=sql_password,
    database=database
  )
  print("CURRENT DATABASES")
  create_table_def(mydb)
  
  

def create_database():
  load_dotenv()
  sql_host=os.getenv("SQL_HOST")
  sql_username=os.getenv("SQL_USERNAME")
  sql_password=os.getenv("SQL_PASSWORD")
  mydb = mysql.connector.connect(
    host=sql_host,
    user=sql_username,
    password=sql_password
  )
  database_name="computable_phenotypes"
  mycursor = mydb.cursor()
  mycursor.execute(f"CREATE DATABASE {database_name}")
  mycursor.execute("SHOW DATABASES")
  for x in mycursor:
    print(x)
  mycursor.execute(f"DROP DATABASE {database_name}")
  print("\n")
  mycursor.execute("SHOW DATABASES")
  for x in mycursor:
    print(x)

def encode_dataframe(df):
  return
def encode_json_input(json_file:string):
  df=pd.read_json(json_file)
  encode_dataframe(df)
  return
def encode_csv_input(csv_file:string):
  df=pd.read_json(csv_file)
  encode_dataframe(df)
  return
if __name__ == "__main__":
  create_database()