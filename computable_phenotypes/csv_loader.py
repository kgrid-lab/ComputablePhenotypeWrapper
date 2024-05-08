import pandas as pd
import json
from computable_phenotypes.db import *
from computable_phenotypes.base_loader import *
def read_csv(file,db_conn):
  patients=Patients(db=db_conn)
  with open(file) as csv_file:
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
