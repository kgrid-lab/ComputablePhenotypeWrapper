# Computable Phenotpyes Project - Knowledge Object Wrapper

## Introduction
Computable phenotypes are algorithms derived from electronic health record (EHR) data that classify patients based on the presence or absence of diseases, conditions, or clinical features. Computable phenotypes have a wide variety of use cases, including cohort identification for clinical trials and observational studies. Phenotyping also plays a role in the collection and reporting of real world data to support both clinical investigations and post-market drug or device surveillance.

Despite the importance of computable phenotypes to research, patient care, and population health, there are no standards for sharing phenotypes, or even for making critical information about a phenotype transparent, e.g. in a research publication. This lack of transparency and reusability has many serious implications for research and patient care. We study the characteristics that make computable phenotypes transparent (such that the impact of feature selection decisions can be made explicit), reproducible (such that phenotypes can be used in different contexts with similar results), and reusable (such that elements of a phenotype can be adapted for use in different contexts or applications).

## Implementation
This repo contains a [KGrid 2.0](https://kgrid.org/specs/kgrid-knowledge-objects.html#kgrid-2-0) Knowledge Object that could be used to calculate the Inclusion/Exclusion of patients from a Nephrotic Syndrome cohort. We use the underlying approach from [Oliverio Et. al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8986057/), who use a SQL script to interpret data from various SQL tables. Our approach extends the functionality of their script by developing a Python wrapper application that allows users to input their data in Json or CSV format to execute the Nephrotic Syndrome computable phenotype, using the original SQL query. The wrapper application is packaged with two common services, a command-line interface (CLI) and a web API, enabling users to supply data and run the computable phenotype as a knowledge object (KO). This KO has a persistent unique identifier and contains both descriptive and technical metadata.

The wrapper application allows users to choose between SQL Server and SQLite as the underlying database for executing the computable phenotype. No SQL expertise is required to use this wrapper. If SQLite is selected, no database setup is needed, whereas using SQL Server requires Microsoft SQL Server and Microsoft ODBC driver for SQL Server to be installed and configured. When SQL Server is used, the wrapper applies the original SQL query exactly as it was published. In contrast, the SQLite option uses an adapted version of the query that has been breifly updated to match SQLite's syntax.

The Kgrid team also reimplemented this knowledge as a pure python script [here](https://github.com/kgrid-lab/nephroticsyndrome-computablephenotype/tree/main).

You can try different ways to install and use this app in our [Google Colab Jupyter Notebook Playground](https://colab.research.google.com/drive/1NQtMlYst_TIYWrCi5DcY3sQmd1HRqF6U?usp=sharing).


https://github.com/user-attachments/assets/b14aa07d-47a5-40ff-87a3-9f916cfe082e


## Environment Setup
As mentioned earlier, this knowledge object could be executed with SQLite or SQL Server database being used in the background. If SQLite is selected, no database setup is needed, whereas using SQL Server requires Microsoft SQL Server and Microsoft ODBC driver for SQL Server to be installed and configured. 

### Installing SQL Server
#### Installing SQL Server 2022 for **Windows** and **Linux** users
You can follow the instruction and steps in Microsoft website, to [install SQL Server 2022 on Windows, Linux, and Docker containers](https://www.microsoft.com/en-us/sql-server/sql-server-downloads). For example for Linux you can use [quick start guide](https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-overview?view=sql-server-ver16#install) for installing SQL server on your prefered version of Linux. For windows you can follow SQL Server installation guide](https://learn.microsoft.com/en-us/sql/database-engine/install-windows/install-sql-server?view=sql-server-ver16)

#### Installing Docker for **MAC** users
Microsoft does not provide native support for MSSQL on Mac. Therefore, we run the server within a Docker container, which allows us to use MSSQL in a consistent, cross-platform environment on macOS.
- Go to the [download page](https://docs.docker.com/desktop/install/mac-install/) and install Docker Desktop
-Open the terminal and download the latest version of mssql
```bash
sudo docker pull mcr.microsoft.com/mssql/server:2022-latest
```
- After the download is complete, enter and run the following command.
```bash
docker run -d --name SQL_Server_Docker -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD={PASSWORD}' -p 1433:1433 mcr.microsoft.com/mssql/server:2022-latest 
```
Make sure your password follows the [Micrsoft Password Policy](https://learn.microsoft.com/en-us/sql/relational-databases/security/password-policy?view=sql-server-ver16)

- Check to make sure that your container has been deployed
```bash
mssql -u sa -p
```

#### Installing pyodbc
pyodbc is the driver that allows the python program to communicate with the MSSQL server.
Install the package using
```bash
pip install pyodbc
```
### Setting up .env file
To run, make a .env file in the root directory with the following parameters:
```bash
MSSQL_USERNAME=sa
MSSQL_HOST=localhost
MSSQL_PASSWORD=YouSQLServerPassword
```

For MSSQL_PASSWORD use the password you set when you installed and configured SQL Server.

## Usage
To use this app, you can either install it as a package or run it directly in a development environment. For installation, follow the package instructions to get started quickly. Alternatively, if you want to explore and modify the code, download the source files and set up a compatible development environment to run it locally.

You can also try different ways to install and use this app as a package in our [Google Colab Jupyter Notebook Playground](https://colab.research.google.com/drive/1NQtMlYst_TIYWrCi5DcY3sQmd1HRqF6U?usp=sharing).

### Install and run the app as a package
#### Installation
Install the app using a distribution file
```zsh
pip install https://github.com/kgrid-lab/ComputablePhenotypeWrapper/releases/download/1.0.0/computable_phenotypes-0.1.0-py3-none-any.whl
```
or directly from the github repository
```zsh
!pip install git+https://github.com/kgrid-lab/ComputablePhenotypeWrapper.git
```
#### Use API service
Then, run the app using 
```zsh
uvicorn computable_phenotypes.api:app
```

Once the app is running, you can access the Swagger editor for testing or send POST requests to its endpoints at http://127.0.0.1:8000. This app provides two endpoints:
- classification1: Accepts the database type as a query string parameter (`sqlite` and `sql_server` options available) and expects [input data in Json format](input_test_data/sample_input.json) as the request body. This endpoint processes the input data using the computable phenotype algorithm and returns the results in the response.
- classification2: Similar to the first endpoint, this also accepts the database type in the query string but expects the [input data in Json format](input_test_data/sample_input.json) as a file attachment.

Below is an example of a client application code snippet that sends a POST request to the computable phenotype wrapper API:
```python
import requests
import json

with open('sample_input.json', 'r') as file:
    patients_list  = json.load(file)
db_type = "sqlite"

json_payload = {
    "patients_list": patients_list,
    "db_type": db_type
}
url = f'http://localhost:8000/classification1?db_type={db_type}'
response = requests.post(url, json=patients_list)

# Print the response from the server
print(response.status_code)
print(json.dumps(response.json(), indent=4))
```

#### Use CLI service
Once the wrapper application is installed, you can use the following command to run the computable phenotype process with a sample input file. In this example, we use SQLite as the database for simplicity. Running this command will output a list of patients classified as inclusions.
```zsh
!nephroticsyndrome-computablephenotype --db_type input_test_data/sqlite sample_input.json
```
#### Use the knowledge object **directly from the code** to classify patients
This section demonstrates how the knowledge embedded in this Knowledge Object can be used directly in the code of a client application. Since the `ComputablePhenotypeWrapper` Knowledge Object was installed earlier using the `pip` command, the client application can import it as a package and access its modules and functions in a python application. The following code loads the contents of the sample Json input file and calls the `process_json` function from the installed KO. This function outputs the classification results.
```python

from computable_phenotypes.utils_sqlite.utils import process_json
import json

with open('path_to/sample_input.json') as f:
    data = json.load(f)
print(process_json(data))
```

### Install and run the app from the code (Development Environment)
#### Installation
For development environment you need to [install Poetry](https://python-poetry.org/docs/#installation) which is a tool for dependency management and packaging in Python

Clone the repository using
```zsh
git clone https://github.com/kgrid-lab/ComputablePhenotypeWrapper.git
```
Then install the dependencies and the project
```zsh
poetry install 
```

This app has a command-line interface (CLI) and a web API service, enabling users to supply data and run the computable phenotype 
#### Use API service
Run the API service using 
```zsh
uvicorn computable_phenotypes.api:app
```
Once the app is running, you can access the Swagger editor for testing, or send POST requests to its endpoints at http://127.0.0.1:8000. The app provides two endpoints:
- classification1: Accepts the database type as a query string parameter (options: `sqlite` or `sql_server`) and expects the [input data in Json format](input_test_data/sample_input.json) in the request body. This endpoint processes the data using the computable phenotype algorithm and returns the result in the response.
- classification2: Similar to `classification1`, this endpoint also requires the database type as a query parameter but expects the [input data in Json format](input_test_data/sample_input.json) as a file attachment in the request.


#### Use CLI service
Use one of the following approaches to configure and run the CLI:
1. Run the script directly using Python's module option
```zsh
python -m computable_phenotypes.cli input_test_data/sample_input.json
```

2. Make the script executable and run directly
```
# Make the script executable on Unix/Linux/macOS:
chmod +x computable_phenotypes/cli.py 
# Run directly
./computable_phenotypes/cli.py input_test_data/sample_input.json
```

3. Configure and use it as a command named ***classify*** anywhere from the command line:

Create a symbolic link to cli.py in a directory that is already on your PATH (e.g., /usr/local/bin/) using

```zsh
# On Unix/Linux/macOS:
ln -s /path/to/cli.py /usr/local/bin/classify
```
Note that `/usr/local/bin/` is usually in your PATH. The specific location where you should link your script might vary.

Alternatively You can add an alias in your shell configuration file (like .bashrc or .zshrc):

```zsh
alias classify='/path/to/cli.py'
```
After adding the alias, you may need to reload the shell configuration using source ~/.bashrc or restart your terminal.

call using 
```zsh
# pipe input file to the classify command and redirect the processed output to output.json
cat input_test_data/sample_input.json | classify > output.json

```

