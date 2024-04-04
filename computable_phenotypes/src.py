import pyodbc
from dotenv import load_dotenv
import os
from subprocess import Popen, PIPE, run

pyodbc.pooling = False
load_dotenv()
sql_host=os.getenv("MSSQL_HOST")
sql_username=os.getenv("MSSQL_USERNAME")
sql_password=os.getenv("MSSQL_PASSWORD")

cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+sql_host+';UID='+sql_username+';PWD='+sql_password+';TrustServerCertificate=yes')
cnxn.autocommit = True
rows = cnxn.execute("SELECT name from sys.databases;").fetchall()
print("Available Databases")
print(rows)
print("Creating New Database")
cnxn.execute("CREATE DATABASE test;")
''''''
database='test'
conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+sql_host+';UID='+sql_username+';PWD='+sql_password+';database='+database+';TrustServerCertificate=yes')
curs = conn.cursor()
print("Creating New Table")
curs.execute("CREATE table idtoname(id int,name varchar(255));")
print("Insert into table")
curs.execute("insert into idtoname (id,name) values (1,\'Anurag\'),(2,\'Bill\'),(3,\'Bob\');")
print("Returning from table")
rows = curs.execute("Select name from idtoname where id=2;").fetchall()
print(f"Selected: {rows}")
print("Deleting table")
curs.execute("Drop table idtoname")
curs.close()
conn.close()
''''''
print("Running Script")
db="dbo"
sql_script="script.sql"
process = run([f'mssql -u {sql_username} -d {db} -p {sql_password}','select * from sys.databases\n','pwd'], stderr=PIPE,stdout=PIPE, stdin=PIPE,shell=True)
#process.stdin.write(f'select * from sys.databases\n')
#process.stdin.flush()
print(process.stdout)
#process = run(['mssql','-p ', , '-d','dbo'],
#                stdout=PIPE, stdin=PIPE,shell=True)
#process.stdin.write(f'{sql_password}\n')
#process.stdin.flush()
#output = process.communicate('source ' + sql_script)[0]
#print(output)

''''''
print("Deleting database")
cnxn.execute("Drop database test;")
print("Remaining databases")
rows = cnxn.execute("SELECT name from sys.databases;").fetchall()
print(rows)
cnxn.close()