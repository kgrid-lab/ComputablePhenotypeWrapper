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
## Setting up .env file
To run, make a .env file in the root directory with the following parameters:
```bash
MSSQL_USERNAME
MSSQL_HOST
MSSQL_PASSWORD
```
