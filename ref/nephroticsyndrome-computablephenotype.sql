--use PlayGround;
GO



--Part 1--------------------------------------------------------------------------------------------------
--Preliminary step: Create reference table from spreadsheet of codes related to inclusions and exclusiodbo.
--Create table to contain diagnosis codes.

if OBJECT_ID('dbo.Ref_NS_Codes', 'U') is not NULL
	drop table dbo.Ref_NS_Codes;


CREATE TABLE dbo.Ref_NS_Codes
(
	Code_Type nvarchar(10) NULL,
	Diag_Code nvarchar(10) NULL,
	Incl_Excl nvarchar(10) NULL,
	Incl_Excl_Type nvarchar(30) NULL
)
GO

--Insert diagnosis code values into table
insert into dbo.Ref_NS_Codes values('ICD-9','583.89','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','582.89','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','583','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','V08','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','42','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','42.1','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','42.2','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','42.8','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','42.9','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','70.2','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','70.21','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','70.22','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','70.23','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','70.3','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','70.31','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','70.32','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','70.33','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','70.41','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','70.44','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','70.51','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','70.54','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','70.7','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','70.71','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','287','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','580','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','580.4','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','593.73','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','741.9','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','741','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','596.54','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','277.87','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','593.73','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','593.7','Exclusion','Exclude_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-9','593.70','Exclusion','Exclude_Encounter');	

insert into dbo.Ref_NS_Codes values('ICD-9','582.9','Exclusion','Neph5829_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','583.2','Exclusion','Neph5832_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','582','Exclusion','Neph5820_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','277.39','Exclusion','Amyloidosis_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-9','277.3','Exclusion','Amyloidosis_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-9','277.3','Exclusion','Amyloidosis_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-9','250.4','Exclusion','Diabetes2_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','250.43','Exclusion','Diabetes2_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','250.41','Exclusion','Diabetes1_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','250.43','Exclusion','Diabetes1_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','710','Exclusion','Lupus_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','710','Exclusion','Lupus_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-9','581.1','Inclusion','PrimaryNS_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','581.3','Inclusion','PrimaryNS_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','582.1','Inclusion','PrimaryNS_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','583.1','Inclusion','PrimaryNS_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-9','581.9','Inclusion','NSNOS_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-10','N05.1','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N06.1','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N07.1','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N03.8','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N05.9','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','Z21','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-10','B20','Exclusion','Exclude_Encounter');			
insert into dbo.Ref_NS_Codes values('ICD-10','B16.2','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B191.1','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B160','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B18.1','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B180','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B16.9','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B191.0','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B161','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B18.1','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B18.0','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B17.11','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B18.2','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B17.10','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B18.2','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B19.20','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','B192.1','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','D69.0','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N00.3','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N01.3','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N13.729','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','Q05.8','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','Q05.4','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N31.9','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','E884.0','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','E884.1','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','E884.2','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','E884.9','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','H49819','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N13.729','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N13.70','Exclusion','Exclude_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N03.9','Exclusion','Neph5829_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N05.5','Exclusion','Neph5832_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N03.2','Exclusion','Neph5820_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','E85.1','Exclusion','Amyloidosis_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-10','E853','Exclusion','Amyloidosis_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-10','E858','Exclusion','Amyloidosis_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-10','E08.21','Exclusion','Diabetes2_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-10','E08.22','Exclusion','Diabetes2_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-10','E112.9','Exclusion','Diabetes2_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-10','E102.9','Exclusion','Diabetes1_Encounter');	
insert into dbo.Ref_NS_Codes values('ICD-10','M32.10','Exclusion','Lupus_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N02.2','Inclusion','PrimaryNS_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N04.0','Inclusion','PrimaryNS_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N03.3','Inclusion','PrimaryNS_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N05.2','Inclusion','PrimaryNS_Encounter');		
insert into dbo.Ref_NS_Codes values('ICD-10','N04.9','Inclusion','NSNOS_Encounter');			



--fake data

--if OBJECT_ID('dbo.Diagnosis', 'U') is not NULL
--	drop table dbo.Diagnosis;
--CREATE TABLE dbo.Diagnosis
--(
--	PATID int,
--	DIAGNOSISID nvarchar(10) NULL,
--	DX nvarchar(10) NULL,
--	DX_Type nvarchar(30) NULL,
--	DX_Source nvarchar(30) NULL,
--	ENCOUNTERID nvarchar(30) NULL
--)
--GO

--if OBJECT_ID('dbo.Encounter', 'U') is not NULL
--	drop table dbo.Encounter;
--CREATE TABLE dbo.Encounter
--(
--	PATID int,
--	ENCOUNTERID nvarchar(30) NULL,
--	ADMIT_DATE datetime NULL,
--	ENC_Type nvarchar(30) NULL,
--	Raw_Enc_Type nvarchar(30) NULL  ,
--	DISCHARGE_DATE datetime
--)
--GO

--if OBJECT_ID('dbo.Demographic', 'U') is not NULL
--	drop table dbo.Demographic;
--CREATE TABLE dbo.Demographic
--(
--	PATID int,
--	BIRTH_DATE datetime,
--	SEX nvarchar(2),
--	HISPANIC nvarchar(2),
--	RACE nvarchar(2)
--)
--GO
-----------

--Part 2----------------------------------------------------------------------------------------------------
--Get Diagnosis records and set flags for conditions related to each diagnosis record

if object_id('dbo.NS_EncounterConditions', 'U') is not NULL
	drop table dbo.NS_EncounterConditions;

select D.PATID, D.ENCOUNTERID
	, max(case when C.Incl_Excl_Type = 'NEPH5829_Encounter'		then 1 else 0 end) as NEPH5829_Flag
	, max(case when C.Incl_Excl_Type = 'NEPH5832_Encounter'		then 1 else 0 end) as NEPH5832_Flag
	, max(case when C.Incl_Excl_Type = 'NEPH5820_Encounter'		then 1 else 0 end) as NEPH5820_Flag
	, max(case when C.Incl_Excl_Type = 'Amyloidosis_Encounter'	then 1 else 0 end) as Amyloidosis_Flag
	, max(case when C.Incl_Excl_Type = 'Diabetes2_Encounter'	then 1 else 0 end) as Diabetes2_Flag
	, max(case when C.Incl_Excl_Type = 'Diabetes1_Encounter'	then 1 else 0 end) as Diabetes1_Flag
	, max(case when C.Incl_Excl_Type = 'Lupus_Encounter'		then 1 else 0 end) as Lupus_Flag
	, max(case when C.Incl_Excl_Type = 'PrimaryNS_Encounter'	then 1 else 0 end) as PrimaryNS_Flag
	, max(case when C.Incl_Excl_Type = 'NSNOS_Encounter'		then 1 else 0 end) as NSNOS_Flag
	, max(case when C.Incl_Excl_Type = 'Exclude_Encounter'		then 1 else 0 end) as Exclude_Code_Flag
into dbo.NS_EncounterConditions
from dbo.Diagnosis as D
	join dbo.Ref_NS_Codes as C
		on D.DX = C.Diag_Code
			and
			(
				(C.Code_Type = 'ICD-9' and D.DX_TYPE = '09')
				or
				(C.Code_Type = 'ICD-10' and D.DX_TYPE = '10')
			)
group by D.PATID, D.ENCOUNTERID
;


--Create Index
--create clustered columnstore index CCSIX_NS_EncounterConditions on dbo.NS_EncounterConditions with (DROP_EXISTING = OFF); --Error 1: can not add index

--Part 3--------------------------------------------------------------------------------------------------------------------
--Add encounter and demographic data to the diagnosis data

if OBJECT_ID('dbo.NS_Encounter_Level', 'U') is not NULL
	drop table dbo.NS_Encounter_Level;

select
	 E.ENCOUNTERID
	,E.PATID
	,E.ADMIT_DATE
	, coalesce(E.DISCHARGE_DATE, E.ADMIT_DATE)  as Discharge_Date  --Error 2: extra End
	,E.ENC_TYPE
	,E.Raw_Enc_Type
	,D.BIRTH_DATE
	,(0 + Convert(Char(8),E.ADMIT_DATE,112) - Convert(Char(8),D.BIRTH_DATE,112)) / 10000 AS Age
	,D.SEX
	,D.HISPANIC
	,D.RACE
	,DX.NEPH5829_Flag
	,DX.NEPH5832_Flag
	,DX.NEPH5820_Flag
	,DX.Amyloidosis_Flag
	,DX.Diabetes2_Flag
	,DX.Diabetes1_Flag
	,DX.Lupus_Flag
	,DX.PrimaryNS_Flag
	,DX.NSNOS_Flag
	,DX.Exclude_Code_Flag
into dbo.NS_Encounter_Level
from dbo.Encounter as E
	JOIN dbo.NS_EncounterConditions as DX
		on E.ENCOUNTERID = DX.ENCOUNTERID
	JOIN dbo.Demographic as D
		on E.PATID = D.PATID
where
	E.ADMIT_DATE IS NOT NULL
	and (E.Raw_Enc_Type != 'Outpatient visit within inpatient visit' or E.Raw_Enc_Type IS NULL)   --Error 3: Raw_Enc_Type does not exist in Encounter table
;

--Part 4---------------------------------------------------------------------------------------------------------------
--Sort the encounters and assign a row number.

if OBJECT_ID('dbo.NS_Encounter_Sort', 'U') is not NULL
	drop table dbo.NS_Encounter_Sort;


select *
	, ROW_NUMBER() OVER (PARTITION BY PATID ORDER BY DISCHARGE_DATE, Admit_Date, EncounterID) AS Encounter_Row
into dbo.NS_Encounter_Sort
from dbo.NS_Encounter_Level
;



--Part 5----------------------------------------------------------------------------------------------------------------
--Add dates for next visit

if OBJECT_ID('dbo.NS_Encounter_Sort_2', 'U') is not NULL
	drop table dbo.NS_Encounter_Sort_2;

Select Cur.*
	,N.ADMIT_DATE AS Next_Admit_Date
	,N.Discharge_Date AS Next_Discharge_Date
into dbo.NS_Encounter_Sort_2
from dbo.NS_Encounter_Sort as Cur
	left JOIN dbo.NS_Encounter_Sort as N
		on Cur.Encounter_Row = N.Encounter_Row - 1 and Cur.patid=N.patid
;



--Part 6------------------------------------------------------------------------------------------------------------------
--Add dates for prior visit

if OBJECT_ID('dbo.NS_Encounter_Sort_3', 'U') is not NULL
	drop table dbo.NS_Encounter_Sort_3;

Select Cur.*
	,N.ADMIT_DATE AS Prior_Admit_Date
	,N.Discharge_Date AS Prior_Discharge_Date
into dbo.NS_Encounter_Sort_3
from dbo.NS_Encounter_Sort_2 as Cur
	left JOIN dbo.NS_Encounter_Sort_2 as N
		on Cur.Encounter_Row = N.Encounter_Row + 1 and Cur.patid=N.patid
;


--Part 7--------------------------------------------------------------------------------------------------------------
--Get sums of inclusion/exclusion variables

if OBJECT_ID('dbo.NS_Encounter_Sums', 'U') is not NULL
	drop table dbo.NS_Encounter_Sums;

select 
	 PATID 
	,ENCOUNTERID
	,ADMIT_DATE
	,DISCHARGE_DATE
	,ENC_TYPE
	,BIRTH_DATE
	,Age
	,SEX
	,HISPANIC
	,RACE
	,NEPH5829_Flag
	,SUM(NEPH5829_Flag) OVER (PARTITION BY PATID ORDER BY Encounter_Row) AS NEPH5829_Total
	,NEPH5832_Flag
	,SUM(NEPH5832_Flag) OVER (PARTITION BY PATID ORDER BY Encounter_Row) AS NEPH5832_Total
	,NEPH5820_Flag
	,SUM(NEPH5820_Flag) OVER (PARTITION BY PATID ORDER BY Encounter_Row) AS NEPH5820_Total
	,Amyloidosis_Flag
	,SUM(Amyloidosis_Flag) OVER (PARTITION BY PATID ORDER BY Encounter_Row) AS Amyloidosis_Total
	,Diabetes2_Flag
	,SUM(Diabetes2_Flag) OVER (PARTITION BY PATID ORDER BY Encounter_Row) AS Diabetes2_Total
	,Diabetes1_Flag
	,SUM(Diabetes1_Flag) OVER (PARTITION BY PATID ORDER BY Encounter_Row) AS Diabetes1_Total
	,Lupus_Flag
	,SUM(Lupus_Flag) OVER (PARTITION BY PATID ORDER BY Encounter_Row) AS Lupus_Total
	,PrimaryNS_Flag
	,SUM(PrimaryNS_Flag) OVER (PARTITION BY PATID ORDER BY Encounter_Row) AS PrimaryNS_Total
	,NSNOS_Flag
	,SUM(NSNOS_Flag) OVER (PARTITION BY PATID ORDER BY Encounter_Row) AS NSNOS_Total
	,Exclude_Code_Flag
	,SUM(Exclude_Code_Flag) OVER (PARTITION BY PATID ORDER BY Encounter_Row) AS Exclude_Code_Total
	,Encounter_Row
	,Next_Admit_Date
	,Next_Discharge_Date
	,Prior_Admit_Date
	,Prior_Discharge_Date
into dbo.NS_Encounter_Sums
from dbo.NS_Encounter_Sort_3
; 



--Part 8-------------------------------------------------------------------------------------------
--Identify Possible Inclusions based on the criteria specified in the WHERE clause.

if OBJECT_ID('dbo.NS_Possible_Inclusions', 'U') is not NULL
	drop table dbo.NS_Possible_Inclusions;

select
	PATID
	,EncounterID
	,Age
	,PrimaryNS_Total
	,NSNOS_Total
	,1 as Possible_Inclusion
into dbo.NS_Possible_Inclusions
from
	dbo.NS_Encounter_Sums
where
	PrimaryNS_Total > 1 
	or ((PrimaryNS_Total + NSNOS_Total) > 1 and Age < 20)
;



--Part 9--------------------------------------------------------------------------------------------
--Identify Possible Exclusions based on the criteria specified in the WHERE clause.

if OBJECT_ID('dbo.NS_Possible_Exclusions', 'U') is not NULL
	drop table dbo.NS_Possible_Exclusions;

select
	PATID
	,EncounterID
	,Age
	,NEPH5829_Total
	,NEPH5832_Total
	,NEPH5820_Total
	,Amyloidosis_Total
	,Diabetes2_Total
	,Diabetes1_Total
	,Lupus_Total
	,Exclude_Code_Total
	,1 as Possible_Exclusion
into dbo.NS_Possible_Exclusions
from
	dbo.NS_Encounter_Sums
where
	NEPH5829_Total > 1
	or NEPH5832_Total > 1
	or NEPH5820_Total > 1
	or Amyloidosis_Total > 1
	or Diabetes2_Total > 1
	or Diabetes1_Total > 1
	or Lupus_Total > 1
	or Exclude_Code_Total > 0
;



--Part 10---------------------------------------------------------------------------------------------
--Join possible inclusions and exclusions with sum data

if OBJECT_ID('dbo.NS_Possible', 'U') is not NULL
	drop table dbo.NS_Possible;

select
	Sums.*
	,case
		when I.possible_inclusion = 1 then 1 else 0 
	 end as Possible_Inclusion
	,case
		when ex.possible_exclusion = 1 then 1 else 0 
	 end as Possible_Exclusion
into dbo.NS_Possible
from dbo.NS_Encounter_Sums as Sums
	left join dbo.NS_Possible_Inclusions as I
		on Sums.encounterid = I.encounterid
	left join dbo.NS_Possible_Exclusions as Ex
		on Sums.ENCOUNTERID = Ex.EncounterID
;



--Part 11-------------------------------------------------------------------------------------
--Flag final inclusions 

if OBJECT_ID('dbo.NS_Final_Inclusions_Flag', 'U') is not NULL
	drop table dbo.NS_Final_Inclusions_Flag;

select
	 P.*
	,1 as Final_Inclusion_Flag
	,P.Prior_Discharge_Date AS Entry_Date
into dbo.NS_Final_Inclusions_Flag
from dbo.NS_Possible as P
where P.possible_inclusion = 1 and P.possible_exclusion != 1
;


--Part 12------------------------------------------------------------------------------------
--Identify first qualified inclusion (once included, always included)

if OBJECT_ID('dbo.NS_Final_Inclusions', 'U') is not NULL
	drop table dbo.NS_Final_Inclusions;


select
	  patid AS PatientID
	, ENCOUNTERID as Anchor_EncounterID
	, Entry_Date
	, ADMIT_DATE as Anchor_Admit_Date
	, DISCHARGE_DATE as Anchor_Discharge_Date
	, BIRTH_DATE as Birth_Date
	, Age
	, RACE as Race
	, SEX as Sex
	, Hispanic
into dbo.NS_Final_Inclusions
from
(
       select *, ROW_NUMBER() OVER(PARTITION BY patid ORDER BY Encounter_Row) as RowNum
       from dbo.NS_Final_Inclusions_Flag
) as OrderedSet
where RowNum = 1
;



--Part 13------------------------------------------------------------------------------------------
--Identify inclusions based on a specified date

if OBJECT_ID('dbo.NS_Final_Inclusions_Output', 'U') is not NULL
	drop table dbo.NS_Final_Inclusions_Output; 

DECLARE @MyDate date;
SET @MyDate = '01-01-2018'; -- As of this date, who has already been included?

select 
	 PatientID
	, Entry_Date as Cohort_Entry_Date
	, Anchor_EncounterID
	, Anchor_Admit_Date
	, Anchor_Discharge_Date
	, Birth_Date
	, Age
	, Race
	, Sex
	, Hispanic
into dbo.NS_Final_Inclusions_Output
from dbo.NS_Final_Inclusions
where Entry_Date <= @MyDate
;



--Part 14---------------------------------------------------------------------------------------------
--Generate output file using sqlcmd and the command line--

/*

***** Below, change SERVERNAME, DATABASENAME, PATH for output, and SCHEMA prefix for table name
***** After you change SERVERNAME, DATABASENAME, PATH for output, and SCHEMA prefix for table name, run the command below from the command line:

sqlcmd -S SERVERNAME -d DATABASENAME -E -o "PATH\Nephrotic_Syndrome_Patients.csv" -Q "Set NOCOUNT ON; Select * from NS.NS_Final_Inclusions_Output" -W -w 999 -s","

*/


/***** ALTERNATIVE: If you have the appropriate permissions, you can run the command below from SQL Server instead:
****** Again change SERVERNAME, DATABASENAME, PATH for output, and SCHEMA prefix for table name.*/

Exec xp_cmdshell 'sqlcmd -S (localdb)\MSSQLLocalDB -d PlayGround -E -o "c:\test\Nephrotic_Syndrome_Patients.csv" -Q "Set NOCOUNT ON; Select * from dbo.NS_Final_Inclusions_Output" -W -w 999 -s","'
select * from dbo.NS_Final_Inclusions_Output

--END of script---------------------------------------------------------------------------------------------





