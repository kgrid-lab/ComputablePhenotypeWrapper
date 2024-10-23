# Computable Phenotpyes Project - Knowledge Object Wrapper

## Motivation
Computable phenotypes are algorithms derived from electronic health record (EHR) data that classify patients based on the presence or absence of diseases, conditions, or clinical features. Computable phenotypes have a wide variety of use cases, including cohort identification for clinical trials and observational studies. Phenotyping also plays a role in the collection and reporting of real world data to support both clinical investigations and post-market drug or device surveillance.

Despite the importance of computable phenotypes to research, patient care, and population health, there are no standards for sharing phenotypes, or even for making critical information about a phenotype transparent, e.g. in a research publication. This lack of transparency and reusability has many serious implications for research and patient care. We study the characteristics that make computable phenotypes transparent (such that the impact of feature selection decisions can be made explicit), reproducible (such that phenotypes can be used in different contexts with similar results), and reusable (such that elements of a phenotype can be adapted for use in different contexts or applications).

## Approach
This repo contains a KGrid 2.0 Knowledge Object that is used to calculate the Inclusion/Exclusion of patients from a Nephrotic Syndrome cohort. We use the underlying approach from [Oliverio Et. al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8986057/), who use a SQL script to interpret data from various SQL tables. Our approach extends the functionality of their script by using the Knowledge object framework to allow the same underlying SQL scripts to be used with CSV and JSON inputs.

The Kgrid team also reimplemented this knowledge as a pure python script [here](https://github.com/kgrid-lab/nephroticsyndrome-computablephenotype/tree/main).

## Initial Developmental Setup
This knowledge object requires a Microsoft SQL Server instance to be accessible from the knowledge object.
### Setting Up Microsoft SQl Server
### Windows
- Install Microsoft SQL Server from the [Microsoft website](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).
### Mac
Microsoft does not provide native support for MSSQL on Mac. Therefore, we run the server from a docker container
#### Installing Docker
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
### Installing pyodbc
pyodbc is the driver that allows the python program to communicate with the MSSQL server.
- Pip install the package
```bash
pip install pyodbc
```
### Setting up .env file
To run, make a .env file in the root directory with the following parameters:
```bash
MSSQL_USERNAME
MSSQL_HOST
MSSQL_PASSWORD
```

### Install poetry
[Install Poetry](https://python-poetry.org/docs/#installation) which is a tool for dependency management and packaging in Python

## How to install, run and test the app

### Install and run the app from the code 
Clone the repository using
```zsh
git clone https://github.com/kgrid-lab/ComputablePhenotypeWrapper.git
```
Install the dependencies and the project
```zsh
poetry install 
```

#### API service
Run the API service using 
```zsh
uvicorn computable_phenotypes.api:app
```

#### CLI service
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

### Install and run the app from a distribution file
Install the app using a distribution file
```zsh
pip install https://github.com/kgrid-lab/ComputablePhenotypeWrapper/releases/download/1.0.0/computable_phenotypes-0.1.0-py3-none-any.whl
```
Then, run the app using 
```zsh
uvicorn computable_phenotypes.api:app
```

Once the app is running, you can access fastapi documentation at http://127.0.0.1:8000 to test the API. Use the test files in the input_test_data folder for testing the API.

or you can run the app using the cli command using
Run the script directly using Python's module option
```zsh
python -m computable_phenotypes.cli input_test_data/sample_input.json
```

