from computable_phenotypes.db import *
from computable_phenotypes.json_loader import *
from pathlib import Path
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

def run_json(input_file):
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
  read_json(input_file,tables_conn)
  tables_conn.commit()
  print("Running Script")
  script_path=Path(__file__).resolve().parent / 'script.sql'
  run_script(script_path,database_name,'output.txt')
  collect_output(tables_conn,'output.json')
  tables_conn.close()
  print("Deleting DB")
  delete_database(connection,database_name)
  connection.close()
if __name__ == "__main__":
  run()
  