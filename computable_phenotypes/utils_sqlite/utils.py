import csv
import json

import pandas as pd
from loguru import logger
import os
from computable_phenotypes.utils_sqlite.db import (
    connect,
    create_database,
    create_tables,
    delete_database,
    run_script,
    fetch
)
from computable_phenotypes.utils_sqlite.Patients import Patients


def read_json(patients_list, database_name):
    patients = Patients(database_name=database_name)

    for pat in patients_list:
        try:
            age = pat.get("age")
            bd = f"1/1/{2024-age}"
            pat_id = patients.add_patient(bd, pat_id=pat["patId"])
            for enc in pat.get("encounterList"):
                enc_id = patients.add_enc(
                    pat_id,
                    enc["admitDate"],
                    enc["dischargeDate"],
                    enc_id=enc.get("encounterId"),
                )
                for dx in enc["diagnosisList"]:
                    patients.add_dx(pat_id, enc_id, dx["dx"], dx_id=dx["diagnosisId"])
        except KeyError:
            print("Invalid Input")
            quit()


def process_json(patients_list: list[dict]):
    database_name = "test"
    # connection.autocommit=True

    try:
        logger.info("Deleting DB")
        delete_database(database_name)

        logger.info("Creating DB")
        create_database(database_name)

        logger.info("Creating tables")
        create_tables(database_name)
        
        logger.info("Reading Input")
        read_json(patients_list, database_name)
        # tables_conn.commit()
        logger.info("Running Script")
        print(os.listdir('.'))
        run_script(
            "./computable_phenotypes/classification_script_sqlite.sql",
            database_name,
            "./script_output.txt",
        )
        
        output = fetch(database_name,"select * from NS_Final_Inclusions")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        logger.info("Deleting DB")
        delete_database(database_name)

    return output


def read_csv(file, database_name):
    patients = Patients(database_name=database_name)

    df = pd.read_csv(
        file,
        sep=",",
        dtype={
            "PatientID": "int",
            "Age": "int",
            "encounterid": "string",
            "enc_date": "string",
            "diagnosis": "string",
            "discharge_date": "string",
        },
    )
    for index, row in df.iterrows():
        age = row["Age"]
        bd = f"1/1/{2024-age}"
        pat_id = patients.add_patient(bd, pat_id=row["PatientID"])
        enc_id = patients.add_enc(
            pat_id, row["enc_date"], row["discharge_date"], enc_id=row["encounterid"]
        )
        if not pd.isna(row["diagnosis"]):
            patients.add_dx(pat_id, enc_id, row["diagnosis"])


def process_csv(input_file):
    database_name = "test"

    try:
        logger.info("Deleting DB")
        delete_database(database_name)

        logger.info("Creating DB")
        create_database(database_name)

        logger.info("Creating tables")
        create_tables(database_name)
        
        logger.info("Reading Input")
        read_csv(input_file, database_name)

        logger.info("Running Script")
        run_script(
            "./computable_phenotypes/classification_script_sqlite.sql",
            database_name,
            "./output/script_output.txt",
        )

        output = fetch(database_name,"select * from NS_Final_Inclusions")
    finally:
        logger.info("Deleting DB")
        delete_database(database_name)

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