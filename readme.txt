
## 
use where_clause.py to generate where clause for cohort
    make sure you choose correct sheet while generating where clause. default name is 'Sheet1'
use case_when.py to generate case when statement with flag
    make sure you choose correct sheet while generating where clause. default name is 'Sheet2'


things to consider before running code
Make sure excel file is in standard format
i.e 	Sheet1 to generate cohort script with 'where'clause
	Sheet2 to generate flag script with 'case when' statement
	codes are in table format
	separate column for separate codes
	codes must be separeted with either comma or space


steps to follow:
1.	Move or save excel file to working directory of python
2.	open .py file (where_clause.py or case_when.py)
3.  find(ctrl +f) @inputfilename
4.	assign excel file name to variable 'input_filename' e.g. input_filename = 'ed_afrf.xlsx'
5.	if the sheet names are different change sheet name under @inputsheetname
6.	Run the code

output file name is automatically generated based on inputfile name and text file with script will be created  in working directory python
 
for example: ed_afrf_case_when_script and ed_afrf_cohort_script





Standard format excel criteria
1. separate column for each code EX. {inc_icd9, inc_icd10, inc_proc, exc_icd9, exc_icd10, exc_proc}
2. separate column for condition
3. wild card format:
	lower case 'x' should be used in code 		EX. '945.x', 'D434.xx'
	x = range from 0-9				EX. '99.x' -> '99.0' to '99.9'
	xx = range from 00-99				EX. '99.xx' -> '99.00' to '99.99'

4. range of code format:
	for alphanumeric range , alpha character should be on both side 		EX. 'A234-A500', 'ZA34.20-ZA34.30'

	
	
