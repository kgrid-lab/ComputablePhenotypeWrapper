if OBJECT_ID('dbo.Ref_NS_Codes', 'U') is not NULL
	drop table dbo.Ref_NS_Codes;


CREATE TABLE dbo.Ref_NS_Codes
(
	Code_Type nvarchar(10) NULL,
	Diag_Code nvarchar(10) NULL,
	Incl_Excl nvarchar(10) NULL,
	Incl_Excl_Type nvarchar(30) NULL
)