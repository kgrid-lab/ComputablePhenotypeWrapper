import csv
import json

import pandas as pd
from loguru import logger

from computable_phenotypes.utils_mssql.db import (
    connect,
    create_database,
    create_tables,
    delete_database,
    run_script,
)
from computable_phenotypes.utils_mssql.Patients import Patients
import importlib.resources as pkg_resources

def read_json(patients_list, connection):
    patients = Patients(db=connection)

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
    db_engine = connect()
    database_name = "test"
    # connection.autocommit=True

    try:
        logger.info("Deleting DB")
        with db_engine.connect() as conn:
            delete_database(conn, database_name)

        logger.info("Creating DB")
        with db_engine.connect() as conn:
            create_database(conn, database_name)

        logger.info("Creating tables")
        tables_engine = connect(database_name)
        with tables_engine.connect() as tables_conn:
            create_tables(tables_conn, database_name)
            logger.info("Reading Input")
            read_json(patients_list, tables_conn)
            # tables_conn.commit()
            logger.info("Running Script")
            with pkg_resources.path("computable_phenotypes", "classification_script_mssql.sql") as sql_file_path:
                run_script(
                    sql_file_path,
                    database_name,
                    "./script_output.txt",
                )

            res = pd.read_sql_query(
                "select * from dbo.NS_Final_Inclusions", tables_conn
            )
            output = res.to_json(orient="records", indent=2, date_format="iso")
        tables_engine.dispose()
    finally:
        logger.info("Deleting DB")
        with db_engine.connect() as drop_conn:
            delete_database(drop_conn, database_name)

    return output


def read_csv(file, connection):
    patients = Patients(db=connection)

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
    db_engine = connect()
    database_name = "test"

    try:
        logger.info("Deleting DB")
        with db_engine.connect() as conn:
            delete_database(conn, database_name)

        logger.info("Creating DB")
        with db_engine.connect() as conn:
            create_database(conn, database_name)

        logger.info("Creating tables")
        tables_engine = connect(database_name)
        with tables_engine.connect() as tables_conn:
            create_tables(tables_conn)

            logger.info("Reading Input")
            read_csv(input_file, tables_conn)

            logger.info("Running Script")
            with pkg_resources.path("computable_phenotypes", "classification_script_mssql.sql") as sql_file_path:
                run_script(
                    sql_file_path,
                    database_name,
                    "./output/script_output.txt",
                )

            res = pd.read_sql_query(
                "select * from dbo.NS_Final_Inclusions", tables_conn
            )
            output = res.to_json(orient="records", indent=2, date_format="iso")
        tables_engine.dispose()
    finally:
        logger.info("Deleting DB")
        with db_engine.connect() as drop_conn:
            delete_database(drop_conn, database_name)

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
