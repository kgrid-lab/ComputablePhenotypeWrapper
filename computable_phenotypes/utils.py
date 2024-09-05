import json
import pandas as pd
from computable_phenotypes.db import *
from computable_phenotypes.base_loader import Patients
from computable_phenotypes.db import *
from computable_phenotypes.json_loader import *
from computable_phenotypes.csv_loader import *
from pathlib import Path

def read_json(patients_list,db_conn):
    patients=Patients(db=db_conn) 
    for pat in patients_list:
        try:
            age=pat.get('age')
            bd=f'1/1/{2024-age}'
            pat_id=patients.add_patient(bd,pat_id=pat['patId'])
            for enc in pat.get('encounterList'):
                enc_id=patients.add_enc(pat_id,enc["admitDate"],enc["dischargeDate"],enc_id=enc.get("encounterId"))
                for dx in enc["diagnosisList"]:
                    patients.add_dx(pat_id,enc_id,dx['dx'],dx_id=dx['diagnosisId'])
        except KeyError:
            print("Invalid Input")
            quit()
    patients.print()

def collect_output(connection,file) :
  res=pd.read_sql_query("select * from dbo.NS_Final_Inclusions", connection)
  return res.to_json(file,orient ='records',indent=2,date_format='iso')
  
def process_json(patients_list: list[dict]):
  connection=connect()
  database_name="test"
  connection.autocommit=True
  print("Deleting DB")
  delete_database(connection,database_name)
  print("Creating DB")
  create_database(connection,database_name)
  print("Creating tables")
  tables_conn=connect(database_name)
  create_tables(tables_conn)
  print("Reading Input")
  read_json(patients_list,tables_conn)
  tables_conn.commit()
  print("Running Script")
  script_path=Path(__file__).resolve().parent / 'script.sql'
  run_script(script_path,database_name,'./output/script_output.txt')
  #output = collect_output(tables_conn,'./output/output.json')
  res=pd.read_sql_query("select * from dbo.NS_Final_Inclusions", tables_conn)
  output = res.to_json(orient ='records',indent=2,date_format='iso')
  tables_conn.close()
  print("Deleting DB")
  delete_database(connection,database_name)
  return output
  
  connection.close()
def process_csv(input_file):
  connection=connect()
  database_name="test"
  connection.autocommit=True
  print("Deleting DB")
  delete_database(connection,database_name)
  print("Creating DB")
  create_database(connection,database_name)
  print("Creating tables")
  tables_conn=connect(database_name)
  create_tables(tables_conn)
  print("Reading Input")
  read_csv(input_file,tables_conn)
  tables_conn.commit()
  print("Running Script")
  script_path=Path(__file__).resolve().parent / 'script.sql'
  run_script(script_path,database_name,'./output/script_output.txt')
  csv_collect_output(tables_conn,'./output/output.csv')
  tables_conn.close()
  print("Deleting DB")
  delete_database(connection,database_name)
  connection.close()  
  
def create_tables(db_conn):
  remove_table(db_conn,'dbo.Encounter')
  remove_table(db_conn,'dbo.Diagnosis')
  remove_table(db_conn,'dbo.Demographic')
  remove_table(db_conn,'dbo.PCOR_Encounters')
  encounter='''CREATE TABLE dbo.Encounter (
    PATID int,
	  ENCOUNTERID nvarchar(30) NULL,
    ADMIT_DATE datetime NULL,
    ENC_Type nvarchar(30) NULL,
    Raw_Enc_Type nvarchar(30) NULL ,
    DISCHARGE_DATE datetime NULL
    );'''
  diagnosis='''
    CREATE TABLE dbo.Diagnosis
    (
        PATID int,
        DIAGNOSISID nvarchar(10) NULL,
        DX nvarchar(10) NULL,
        DX_Type nvarchar(30) NULL,
        DX_Source nvarchar(30) NULL,
        ENCOUNTERID nvarchar(30) NULL
    );'''
  demo='''
  CREATE TABLE dbo.Demographic
  (
    PATID int,
    BIRTH_DATE datetime,
    SEX nvarchar(2),
    HISPANIC nvarchar(2),
    RACE nvarchar(2)
    );'''
  execute(db_conn,encounter)
  execute(db_conn,diagnosis)
  execute(db_conn,demo)