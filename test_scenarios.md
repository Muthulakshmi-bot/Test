# Test Scenarios for Pro*C Files

This document outlines test scenarios for the five Pro*C programs: 1.pc, 2.pc, 3.pc, 4.pc, and 5.pc.

## Prerequisites
- Oracle Database instance (ORCLPDB1) with SCOTT schema
- Pro*C compiler (proc) installed
- Oracle client libraries
- Test data in EMP table

## Compilation Steps
For each .pc file:
1. Compile with: `proc iname=<filename>.pc oname=<filename>.c`
2. Compile C code: `gcc -o <filename> <filename>.c -I$ORACLE_HOME/precomp/public -L$ORACLE_HOME/lib -lclntsh`

## 1.pc - Select Single Row

### Test Scenario 1.1: Successful Select
- **Description**: Select employee data for existing empno
- **Preconditions**: EMP table has empno=7369
- **Steps**:
  1. Run the program
- **Expected Output**: "EMPNO=7369 ENAME=<name> SAL=<salary>"
- **Postconditions**: No changes to database

### Test Scenario 1.2: No Data Found
- **Description**: Select for non-existing empno
- **Preconditions**: Modify empno to a non-existing value (e.g., 9999)
- **Steps**:
  1. Run the program
- **Expected Output**: "No data found for EMPNO=9999"

### Test Scenario 1.3: Connection Failure
- **Description**: Test with invalid credentials
- **Preconditions**: Change username/password to invalid values
- **Steps**:
  1. Run the program
- **Expected Output**: Error message "Connect failed" with ORA error

## 1.py - Python Single Row Select

### Test Scenario 1_py.1: Successful Select (Python)
- **Description**: Execute Python script to select existing employee
- **Preconditions**: Python 3 and cx_Oracle installed, EMP table has empno=7369
- **Steps**:
  1. Run: `python 1.py`
- **Expected Output**: "EMPNO=7369 ENAME=<name> SAL=<salary>"
- **Postconditions**: No changes to database

### Test Scenario 1_py.2: No Data Found (Python)
- **Description**: Execute Python script for non-existing employee
- **Preconditions**: Modify empno in script to 9999
- **Steps**:
  1. Edit 1.py to change empno = 9999
  2. Run: `python 1.py`
- **Expected Output**: "No data found for EMPNO=9999"

### Test Scenario 1_py.3: Database Connection Failure (Python)
- **Description**: Test Python script with invalid database connection
- **Preconditions**: Change dsn/username to invalid values
- **Steps**:
  1. Run: `python 1.py`
- **Expected Output**: cx_Oracle.DatabaseError with connection failure message

## 1_plsql.sql - PL/SQL Anonymous Block

### Test Scenario 1_plsql.1: Successful Select (PL/SQL)
- **Description**: Execute PL/SQL block to select existing employee
- **Preconditions**: EMP table has empno=7369
- **Steps**:
  1. Run: `sqlplus scott/tiger@ORCLPDB1 @1_plsql.sql`
- **Expected Output**: "EMPNO=7369 ENAME=<name> SAL=<salary>"
- **Postconditions**: No changes to database

### Test Scenario 1_plsql.2: No Data Found (PL/SQL)
- **Description**: Execute PL/SQL block for non-existing employee
- **Preconditions**: Modify the empno variable to 9999
- **Steps**:
  1. Edit 1_plsql.sql to change v_empno := 9999
  2. Run the script
- **Expected Output**: "No data found for EMPNO=9999"

### Test Scenario 1_plsql.3: SQL Error Handling (PL/SQL)
- **Description**: Test error handling in PL/SQL block
- **Preconditions**: Valid EMP table data
- **Steps**:
  1. Run the script normally
- **Expected Output**: Proper error messages for any SQL errors

## 1_plsql_proc.sql - PL/SQL Stored Procedure

### Test Scenario 1_proc.1: Create and Execute Procedure
- **Description**: Create stored procedure and test execution
- **Preconditions**: None
- **Steps**:
  1. Run: `sqlplus scott/tiger@ORCLPDB1 @1_plsql_proc.sql`
  2. Execute: `EXEC select_employee(7369);`
- **Expected Output**: "EMPNO=7369 ENAME=<name> SAL=<salary>"

### Test Scenario 1_proc.2: Test with Different Parameters
- **Description**: Test procedure with various employee numbers
- **Preconditions**: Procedure created from previous test
- **Steps**:
  1. Execute: `EXEC select_employee(7499);`
  2. Execute: `EXEC select_employee(9999);`
- **Expected Output**:
  - Valid employee: Employee details displayed
  - Invalid employee: "No data found for EMPNO=9999"

### Test Scenario 1_proc.3: Procedure Recreation
- **Description**: Test CREATE OR REPLACE functionality
- **Preconditions**: Procedure already exists
- **Steps**:
  1. Run the script again
  2. Execute the procedure
- **Expected Output**: Procedure recreates successfully and executes properly

## 2.pc - Insert with Commit

### Test Scenario 2.1: Successful Insert
- **Description**: Insert new employee record
- **Preconditions**: empno=9001 does not exist
- **Steps**:
  1. Run the program
- **Expected Output**: "Inserted empno=9001 (committed)"
- **Postconditions**: Row inserted in EMP table

### Test Scenario 2.2: Duplicate Key Insert
- **Description**: Attempt to insert existing empno
- **Preconditions**: empno=7369 already exists
- **Steps**:
  1. Modify empno to 7369 and run
- **Expected Output**: Error message "Insert failed (rolled back)" with ORA error
- **Postconditions**: No new row inserted

### Test Scenario 2.3: Connection Failure
- **Description**: Test with invalid database connection
- **Preconditions**: Change db to invalid value
- **Steps**:
  1. Run the program
- **Expected Output**: "Connect failed" error

## 3.pc - Cursor Fetch Loop

### Test Scenario 3.1: Fetch Multiple Rows
- **Description**: Fetch all employees in dept 10
- **Preconditions**: EMP table has multiple rows for deptno=10
- **Steps**:
  1. Run the program
- **Expected Output**: List of employees with empno, ename, sal

### Test Scenario 3.2: Empty Department
- **Description**: Fetch from department with no employees
- **Preconditions**: Change deptno to a dept with no employees (e.g., 99)
- **Steps**:
  1. Run the program
- **Expected Output**: "Employees in dept 99:" with no rows listed

### Test Scenario 3.3: Connection Failure
- **Description**: Test with invalid credentials
- **Preconditions**: Change username/password
- **Steps**:
  1. Run the program
- **Expected Output**: Program exits with error code 1

## 4.pc - Call Stored Procedure

### Test Scenario 4.1: Successful Procedure Call
- **Description**: Call p_get_sal for existing employee
- **Preconditions**: Procedure p_get_sal exists and empno=7369 exists
- **Steps**:
  1. Run the program
- **Expected Output**: "Empno=7369 Salary=<value>"

### Test Scenario 4.2: Employee Not Found
- **Description**: Call procedure for non-existing empno
- **Preconditions**: Change empno to 9999
- **Steps**:
  1. Run the program
- **Expected Output**: "No employee found for 9999"

### Test Scenario 4.3: Procedure Does Not Exist
- **Description**: Call non-existing procedure
- **Preconditions**: Modify procedure name to invalid one
- **Steps**:
  1. Run the program
- **Expected Output**: Error "Proc call failed" with ORA error

### Test Scenario 4.4: Connection Failure
- **Description**: Test with invalid connection
- **Preconditions**: Change db/username
- **Steps**:
  1. Run the program
- **Expected Output**: Program exits with error code 1

## 5.pc - Bulk Employee Loading from File

### Test Scenario 5.1: Successful Bulk Load from File
- **Description**: Load all employee records from file successfully
- **Preconditions**: employee_data.txt exists with valid data, all empno values do not exist
- **Steps**:
  1. Ensure employee_data.txt contains 6 valid records
  2. Run the program
- **Expected Output**:
  - Success messages for each employee
  - "Successfully loaded: 6 records"
  - "Failed to load: 0 records"
- **Postconditions**: 6 new rows inserted in EMP table

### Test Scenario 5.2: Partial Success Load from File
- **Description**: Some records succeed, some fail due to duplicate keys
- **Preconditions**: Modify employee_data.txt so empno=9001 exists, others do not
- **Steps**:
  1. Run the program
- **Expected Output**:
  - Error for empno=9001 (duplicate key)
  - Success messages for other employees
  - "Successfully loaded: 5 records"
  - "Failed to load: 1 records"
- **Postconditions**: 5 new rows inserted, 1 failed

### Test Scenario 5.3: File Not Found
- **Description**: Test when data file is missing
- **Preconditions**: Remove or rename employee_data.txt
- **Steps**:
  1. Run the program
- **Expected Output**: "Error: Cannot open employee_data.txt file", program exits with code 1

### Test Scenario 5.4: Invalid File Format
- **Description**: Test with malformed CSV data
- **Preconditions**: Modify employee_data.txt with invalid format (missing fields)
- **Steps**:
  1. Run the program
- **Expected Output**:
  - Error messages for malformed lines
  - Program continues processing valid lines
  - Summary shows failed records

### Test Scenario 5.5: Connection Failure
- **Description**: Test with invalid database connection
- **Preconditions**: Change db/username to invalid values
- **Steps**:
  1. Run the program
- **Expected Output**: "Connect failed" error message, program exits with code 1

### Test Scenario 5.6: Data Validation
- **Description**: Verify correct parsing and loading of various data types
- **Preconditions**: employee_data.txt with diverse data types
- **Steps**:
  1. Run the program
  2. Query EMP table for loaded records
- **Expected Output**:
  - All records loaded successfully
  - Verify ename, job, sal, comm, deptno values match file data
  - hiredate set to current date
- **Postconditions**: Data integrity maintained

### Test Scenario 5.7: Empty File Handling
- **Description**: Test behavior with empty data file
- **Preconditions**: Create empty employee_data.txt file
- **Steps**:
  1. Run the program
- **Expected Output**:
  - "Starting bulk load from employee_data.txt..."
  - "Total lines processed: 0"
  - "Successfully loaded: 0 records"
  - "Failed to load: 0 records"
- **Postconditions**: No database changes

### Test Scenario 5.8: File with Comments/Empty Lines
- **Description**: Test file with comments and blank lines
- **Preconditions**: employee_data.txt with comments (# lines) and empty lines
- **Steps**:
  1. Run the program
- **Expected Output**:
  - Ignores comment and empty lines
  - Processes only valid data lines
  - Correct success/failure counts

### Test Scenario 5.9: Data Type Edge Cases
- **Description**: Test boundary values and special data
- **Preconditions**: File with maximum length strings, zero values, negative numbers
- **Steps**:
  1. Run the program
- **Expected Output**:
  - Handles string truncation properly
  - Processes zero/negative values appropriately
  - Validates data ranges where applicable

### Test Scenario 5.10: Database Constraint Violations
- **Description**: Test foreign key and check constraint violations
- **Preconditions**: File with invalid deptno or mgr references
- **Steps**:
  1. Run the program
- **Expected Output**:
  - Constraint violation errors for invalid references
  - Program continues with other valid records
  - Proper error reporting

### Test Scenario 5.11: File Encoding and Special Characters
- **Description**: Test with special characters in names
- **Preconditions**: File with accented characters, quotes, or special symbols
- **Steps**:
  1. Run the program
- **Expected Output**:
  - Handles special characters appropriately
  - No parsing errors due to character encoding

### Test Scenario 5.12: Large File Performance
- **Description**: Test with larger dataset
- **Preconditions**: File with 100+ records
- **Steps**:
  1. Run the program
  2. Measure execution time
- **Expected Output**:
  - All records processed
  - Reasonable performance (under 30 seconds)
  - No memory leaks or resource exhaustion

### Test Scenario 5.13: File Permissions
- **Description**: Test with read-only file permissions
- **Preconditions**: Set employee_data.txt to read-only
- **Steps**:
  1. Run the program
- **Expected Output**:
  - Should still be able to read the file
  - Normal processing if file is readable

### Test Scenario 5.14: Concurrent Access
- **Description**: Test while another process is reading the file
- **Preconditions**: Have another process reading the file
- **Steps**:
  1. Run the program
- **Expected Output**:
  - Handles file locking gracefully
  - Either succeeds or reports appropriate error

### Test Scenario 5.15: Recovery and Restart
- **Description**: Test partial processing and restart capability
- **Preconditions**: File with mix of valid/invalid records
- **Steps**:
  1. Run program (partial success)
  2. Fix data file
  3. Run again
- **Expected Output**:
  - Second run processes remaining valid records
  - No duplicate processing of already loaded records

## 6.pc/6.py - Employee Salary Display Programs

### Test Scenario 6.1: Display All Employees (Pro*C)
- **Description**: Execute Pro*C program to display employee salary details
- **Preconditions**: EMP table populated with data
- **Steps**:
  1. Compile 6.pc to executable
  2. Run ./6
- **Expected Output**: Formatted table of employees grouped by department with totals

### Test Scenario 6.2: Display All Employees (Python)
- **Description**: Execute Python script to display employee salary details
- **Preconditions**: EMP table populated with data
- **Steps**:
  1. Run `python 6.py`
- **Expected Output**: Formatted table of employees grouped by department with totals

## employee_salary_viewer.py - Comprehensive Salary Viewer

### Test Scenario viewer.1: Generate Full Report
- **Description**: Execute comprehensive viewer application
- **Preconditions**: EMP and DEPT tables populated
- **Steps**:
  1. Run `python employee_salary_viewer.py`
  2. Enter connection details when prompted
- **Expected Output**:
  - Company summary section
  - Department-wise breakdown
  - Detailed employee list
  - Formatted report with headers

### Test Scenario viewer.2: Custom Connection Parameters
- **Description**: Test with different database connection
- **Preconditions**: Alternative database credentials available
- **Steps**:
  1. Run application with custom parameters
- **Expected Output**: Successful connection and report generation

### Test Scenario viewer.3: Empty Database
- **Description**: Test with empty or minimal EMP table
- **Preconditions**: EMP table has minimal data
- **Steps**:
  1. Run application
- **Expected Output**: Report shows available data with appropriate totals