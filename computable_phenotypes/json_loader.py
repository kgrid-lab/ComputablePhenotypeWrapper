import json
from computable_phenotypes.db import *
def null_grab(dict,key):
  out=dict.get(key)
  if out==None:
    out='NULL'
  return out
def get_dx_type(dx):
   if isinstance(dx, float):
      return 9
   return 10
def read_json(file,db_conn):
   with open(file) as json_file:
      data= json.load(json_file)
      for pat in data:
        try:
            add_patient(pat,db_conn)
        except KeyError:
            print("Invalid Input")
            quit()
def add_patient(input,db_conn):
  '''
  insert into dbo.demo values('1','1/1/2000','M','No', 'W');
    insert into dbo.Encounter values('1','1','1/1/2024','Not Needed', 'Not Needed','1/5/2024');
    insert into dbo.Diagnosis values('1','1','imp, from info','ICD-9/ICD-9==9/10','1');
    '''
  patient_id=input['patId']
  #if patient_id==None:
  #  patient_id=get_pat_id()
  age=null_grab(input,'age')
  birthdate=null_grab(input,'birthdate')
  race=null_grab(input,'race')
  sex=null_grab(input,'sex')
  hispanic=null_grab(input,'hispanic')

  demo=f'''insert into dbo.Demographic values({patient_id},{birthdate},{sex},{hispanic},{race});'''
  print(demo)
  execute(db_conn,demo)
  encounter_num=0
  for enc in input.get('encounterList'):

    encounter_id=enc.get("encounterId")
    if encounter_id==None:
        encounter_id=encounter_num
    encounter_num+=1

    admit_date=enc.get("admitDate")
    dis_date=enc.get("dischargeDate")
    enc_type=null_grab(enc,'ENC_Type')
    raw_enc_type=null_grab(enc,'Raw_Enc_Type')
    enc_com=f'''insert into dbo.Encounter values({patient_id},{encounter_id},{admit_date},{enc_type},{raw_enc_type},{dis_date});'''
    print(enc_com)
    execute(db_conn,enc_com)
    diagnosis_num=0
    for d in enc["diagnosisList"]:
        diagnosis_id=d.get("diagnosisId")
        if diagnosis_id==None:
            diagnosis_id=diagnosis_num
        diagnosis_num+=1
        dx=d['dx']
        dx_type=get_dx_type(dx)
        dx_source=null_grab(d,'DX_Source')
        diagnosis=f'''insert into dbo.Diagnosis values({patient_id},{diagnosis_id},{dx},{dx_type},{dx_source},{encounter_id});'''
        print(diagnosis)
        execute(db_conn,diagnosis)
