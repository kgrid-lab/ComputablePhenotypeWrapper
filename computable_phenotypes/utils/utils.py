import pandas as pd
from computable_phenotypes.utils.db import create_tables, create_database, delete_database, connect, run_script
from computable_phenotypes.utils.Patients import Patients
from pathlib import Path
import csv
import json
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
  run_script('./computable_phenotypes/script.sql',database_name,'./script_output.txt')
  
  res=pd.read_sql_query("select * from dbo.NS_Final_Inclusions", tables_conn)
  output = res.to_json(orient ='records',indent=2,date_format='iso')
  
  tables_conn.close()
  print("Deleting DB")
  delete_database(connection,database_name)
  connection.close()
  return output
  
  
def read_csv(file,db_conn):
  patients=Patients(db=db_conn)
  
  df = pd.read_csv(file,sep=',',dtype={"PatientID":"int","Age":"int","encounterid":"string","enc_date":"string","diagnosis":"string","discharge_date":"string"})
  for index, row in df.iterrows():
    age=row['Age']
    bd=f'1/1/{2024-age}'
    pat_id=patients.add_patient(bd,pat_id=row['PatientID'])
    enc_id=patients.add_enc(pat_id,row["enc_date"],row["discharge_date"],enc_id=row['encounterid'])
    if not pd.isna(row['diagnosis']):
      patients.add_dx(pat_id,enc_id,row['diagnosis'])
  patients.print()
def csv_collect_output(connection,file):
  res=pd.read_sql_query("select * from dbo.NS_Final_Inclusions", connection)
  res.to_csv(file, index=False)  
  
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
  run_script('./computable_phenotypes/script.sql',database_name,'./output/script_output.txt')
  # csv_collect_output(tables_conn,'./output/output.csv')
  
  res=pd.read_sql_query("select * from dbo.NS_Final_Inclusions", tables_conn)
  output = res.to_json(orient ='records',indent=2,date_format='iso')
  
  tables_conn.close()
  print("Deleting DB")
  delete_database(connection,database_name)
  connection.close()  
  return output

def is_json(content):
    try:
        json.loads(content)
        return True
    except json.JSONDecodeError:
        return False


def is_csv(content):
    try:
        # Convert the content to a file-like object (StringIO)
        csv_text = content.decode("utf-8")

        # Process the CSV data and append rows to the JSON variable
        csv_reader = csv.reader(csv_text.splitlines())
        header = next(csv_reader)
        # Assuming it's CSV if it has at least two columns in the first row
        if len(header) >= 2:
            return True
    except (csv.Error, StopIteration):
        pass
    return False