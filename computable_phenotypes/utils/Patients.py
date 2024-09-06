import pprint
from computable_phenotypes.utils.db import execute
class Patients:
  def __init__(self,db=None,verbose=False):
    self.patients={}
    self.loaded=False
    self.verbose=verbose
    self.db=db
    if db is None:
      self.write=False
    else:
      self.write=True
  def add_patient(self,birthday,race=None,sex=None,hisp=None,pat_id=None):
    '''
      @birthday Dates Should be in the form Month/Day/Year
    '''
    #Check if input values are None
    race=nullify(race)
    sex=nullify(sex)
    hisp=nullify(hisp)
    #Calc Pat_id Value
    base=self.patients
    if pat_id is None:
      pat_id=len(base)
      while base.get(pat_id) is not None:
        pat_id+=1
    else:
      if base.get(pat_id) is not None:
        return pat_id
    #Add Patient
    patient_info={"pat_id":pat_id,"birthdate":date_parser(birthday),"race":race,"sex":sex,"hispanic":hisp,"encounters":{}}
    base[pat_id]=patient_info
    if self.write:
      pat_instr=f'''insert into dbo.Demographic values({patient_info['pat_id']},{patient_info['birthdate']},{patient_info['sex']},{patient_info['hispanic']},{patient_info['race']});'''
      self.log(pat_instr)
      execute(self.db,pat_instr)
    return pat_id
  def add_enc(self,pat_id,admit_date,dis_date,enc_id=None,enc_type=None,raw_enc_type=None,db=None):
    #Check Patient value
    if self.patients.get(pat_id) is None:
      raise Exception("Pat_id does not exist")
    #Calc Enc_id Value
    base=self.patients[pat_id]["encounters"]
    if enc_id is None:
      enc_id=len(base)
      while base.get(enc_id) is not None:
        enc_id+=1
    else:
      if base.get(enc_id) is not None:
        return enc_id
    #Add Enc
    enc_info={
            "enc_id":enc_id,
            "admit_date":date_parser(admit_date),
            "discharge_date":date_parser(dis_date),
            "enc_type":nullify(enc_type),
            "raw_enc_type":nullify(raw_enc_type),
            "diagnosisList":{}
            }
    base[enc_id]=enc_info
    if self.write:
      enc_instr=f'''insert into dbo.Encounter values({pat_id},{enc_info['enc_id']},{enc_info['admit_date']},{enc_info['enc_type']},{enc_info['raw_enc_type']},{enc_info['discharge_date']});'''
      self.log(enc_instr)
      execute(self.db,enc_instr)
    return enc_id
  def add_dx(self,pat_id,enc_id,code,dx_id=None,dx_source=None,db=None):
    #Check Patient value
    if self.patients.get(pat_id) is None:
      raise Exception("Pat_id does not exist")
    #Check Encounter value
    if self.patients[pat_id]["encounters"].get(enc_id) is None:
      raise Exception("Encounter does not exist")
    #Calc DX id
    base=self.patients[pat_id]["encounters"][enc_id]["diagnosisList"]
    if dx_id is None:
      dx_id=len(base)
      while base.get(dx_id) is not None:
        dx_id+=1
    else:
      if base.get(dx_id) is not None:
        return dx_id
    #Add Dx
    dx_info={"dx":string_wrap(code), "dx_id":dx_id,"dx_type":string_wrap(self.get_dx_type(code)),'dx_source':nullify(dx_source)}
    base[dx_id]=dx_info
    if self.write:
      dx_instr=f'''insert into dbo.Diagnosis values({pat_id},{dx_info['dx_id']},{dx_info['dx']},{dx_info['dx_type']},{dx_info['dx_source']},{enc_id});'''
      self.log(dx_instr)
      execute(self.db,dx_instr)
    return dx_id
  def print(self):
    pprint.pp(self.patients)
  def get_dx_type(self,code):
    try:
      float(code)
      return '09'
    except ValueError:
      return '10'

  def batch_load(self,db_connection):
    if self.loaded:
      raise Exception("Already Loaded")
    self.loaded=True

    for patid,pat in self.patients:
      #load patient
      pat_instr=f'''insert into dbo.Demographic values({pat['pat_id']},{pat['birthdate']},{pat['sex']},{pat['hispanic']},{pat['race']});'''
      self.log(pat_instr)
      execute(db_connection,pat_instr)
      for enc_id,encs in pat['encounters']:
        enc_instr=f'''insert into dbo.Encounter values({pat['pat_id']},{encs['enc_id']},{encs['admit_date']},{encs['enc_type']},{encs['raw_enc_type']},{encs['discharge_date']});'''
        self.log(enc_instr)
        execute(db_connection,enc_instr)
        for dx_id,dx in encs['diagnosis_list']:
          dx_instr=f'''insert into dbo.Diagnosis values({pat['pat_id']},{dx['dx_id']},{dx['dx']},{dx['dx_type']},{dx['dx_source']},{encs['enc_id']});'''
          self.log(dx_instr)
          execute(db_connection,dx_instr)
  def log(self,input):
    if self.verbose:
      print(input)
def string_wrap(input):
  return f'\'{input}\''
def nullify(val):
  if val is None:
    return "NULL"
  else:
    return string_wrap(val)
def date_parser(date):
  split=date.split("/")
  return f'\'{"-".join(split)}\''