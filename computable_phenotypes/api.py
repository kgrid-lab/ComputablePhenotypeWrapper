from enum import Enum
import json
from io import StringIO

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

import computable_phenotypes.utils_mssql.utils as mssql_utils
import computable_phenotypes.utils_sqlite.utils as sqlite_utils
from computable_phenotypes.utils import is_csv, is_json

# from nephroticsyndrome_computablephenotype.utils import is_csv, is_json, prepare_data_from_csv


class TextInput(BaseModel):
    text: str


app = FastAPI(
    title="Computable Phenotype",
    description="Computable phenotypes are algorithms derived from electronic health record (EHR) data that classify patients based on the presence or absence of diseases, conditions, or clinical features. Computable phenotypes have a wide variety of use cases, including cohort identification for clinical trials and observational studies. Phenotyping also plays a role in the collection and reporting of real world data to support both clinical investigations and post-market drug or device surveillance",
    version="1.0.0",
    contact={
        "name": "kgrid developers",
        "url": "https://kgrid.org/",
        "email": "kgrid-developers@umich.edu",
    },
)


@app.get(
    "/",
    include_in_schema=False,
)
async def root(request: Request):
    response = RedirectResponse(url="/docs")
    return response

class DatabaseType(str, Enum):
    sqlite = "sqlite"
    sql_server = "sql_server"
    
@app.post("/classification1", tags=["Nephrotic Syndrome Computable Phenotype"])
async def process_body_input( patients_list: list[dict],db_type: DatabaseType):
    """

    **Classify patients and return inclusion encounters for nephrotic syndrome:**

    This api could be used to process multiple patients data, including their encounters and diagnoses and to classify them for Nephrotic Syndrome. It receives patient data as the body of the request, applies computable phenotype,
    and returns a list of inclusion encounters.  For more detail on the implementation and input data format please check our GitHub repository.

    **Parameters:**
    :param body: Patient data.

    **Sample input data:**
    Sample input data (JSON) can be found in the GitHub repository under the 'input_test_data' folder:
    [Link to GitHub Repository](https://github.com/kgrid-lab/nephroticsyndrome-computablephenotype/tree/main/input_test_data)

    **Implementation:**
    The implementation of this app is available on GitHub:
    [Link to GitHub Repository](https://github.com/kgrid-lab/ComputablePhenotypeWrapper)

    **Returns:**
    List of inclusion encounters that meet the criteria.
    """
    if db_type==DatabaseType.sql_server:
        return json.loads(mssql_utils.process_json(patients_list))
    else:
        return json.loads(sqlite_utils.process_json(patients_list))


@app.post("/classification2", tags=["Nephrotic Syndrome Computable Phenotype"])
async def process_uploaded_file(file: UploadFile, db_type: DatabaseType):
    """

    **Classify patients and return inclusion encounters for nephrotic syndrome:**

    This api could be used to process multiple patients data, including their encounters and diagnoses and to classify them for Nephrotic Syndrome. It receives patient data in either JSON or CSV format, applies computable phenotype,
    and returns a list of inclusion encounters.  For more detail on the implementation and input data format please check our GitHub repository.

    **Parameters:**
    :param file: Patient data in JSON or CSV format.

    **Sample input data:**
    Sample input data (CSV and JSON) can be found in the GitHub repository under the 'input_test_data' folder:
    [Link to GitHub Repository](https://github.com/kgrid-lab/nephroticsyndrome-computablephenotype/tree/main/input_test_data)

    **Implementation:**
    The implementation of this app is available on GitHub:
    [Link to GitHub Repository](https://github.com/kgrid-lab/ComputablePhenotypeWrapper)

    **Returns:**
    List of inclusion encounters that meet the criteria.
    """

    content = await file.read()
    if is_csv(content):
        if db_type == DatabaseType.sql_server:
            return json.loads(mssql_utils.process_csv(StringIO(content.decode("utf-8"))))
        else:
            return json.loads(sqlite_utils.process_csv(StringIO(content.decode("utf-8"))))
    elif is_json(content):
        patients_list = json.loads(content)
        if db_type == DatabaseType.sql_server:
            return json.loads(mssql_utils.process_json(patients_list))
        else:
            return json.loads(sqlite_utils.process_json(patients_list))
    else:
        return "Input data must be json or csv"


# only runs virtual server when running this .py file directly for debugging
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
