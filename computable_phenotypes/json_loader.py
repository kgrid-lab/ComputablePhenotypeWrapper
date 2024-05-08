import json
import pandas as pd
from computable_phenotypes.db import *
from computable_phenotypes.base_loader import Patients

def read_json(file,db_conn):
  patients=Patients(db=db_conn)
  with open(file) as json_file:
      data= json.load(json_file)
      for pat in data:
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
def collect_output(connection,file):
  res=pd.read_sql_query("select * from dbo.NS_Final_Inclusions", connection)
  res.to_json(file,orient ='records',indent=2,date_format='iso')
