# Technical Design Document for Pro*C Programs

## 1. Introduction

This document provides the technical design for five Pro*C programs that interact with an Oracle database. These programs demonstrate basic database operations using embedded SQL in C.

## 2. System Overview

### 2.1 Architecture
- **Language**: C with embedded SQL (Pro*C), Python 3, PL/SQL
- **Database**: Oracle Database (ORCLPDB1)
- **Schema**: SCOTT
- **Authentication**: Username/Password based

### 2.2 Components
1. **1.pc/1.py**: Single row selection program (Pro*C/Python)
2. **2.pc/2.py**: Data insertion program with transaction management
3. **3.pc/3.py**: Multi-row fetch using cursors
4. **4.pc/4.py**: Stored procedure invocation program
5. **5.pc/5.py**: Bulk data loading program from file
6. **6.pc/6.py**: Employee salary display programs
7. **employee_salary_viewer.py**: Comprehensive salary reporting application

### 2.3 Database Schema
The programs interact with the EMP table in SCOTT schema:

```sql
EMP (
    EMPNO    NUMBER(4) PRIMARY KEY,
    ENAME    VARCHAR2(10),
    JOB      VARCHAR2(9),
    MGR      NUMBER(4),
    HIREDATE DATE,
    SAL      NUMBER(7,2),
    COMM     NUMBER(7,2),
    DEPTNO   NUMBER(2)
)
```

## 3. Detailed Design

### 3.1 Program 1: select_single_row.pc

#### Purpose
Retrieves a single employee record based on employee number.

#### Components
- **Host Variables**:
  - username, password, db: Connection credentials
  - empno: Input parameter (hardcoded to 7369)
  - ename, sal: Output variables

#### Data Flow
1. Establish database connection
2. Execute SELECT query with WHERE clause
3. Handle results:
   - Success: Print employee details
   - No data: Print "No data found"
   - Error: Display SQL error

#### Error Handling
- Connection failures: Display ORA error and exit
- SQL errors: Use sql_error() function to display error details

#### Dependencies
- Oracle Pro*C precompiler
- sqlca.h (SQL Communications Area)

#### PL/SQL Equivalents
Two PL/SQL implementations are available:

**1_plsql.sql**: Anonymous PL/SQL block that replicates the exact functionality
- Uses DECLARE/BEGIN/END structure
- Exception handling with NO_DATA_FOUND and OTHERS
- DBMS_OUTPUT for result display

**1_plsql_proc.sql**: Stored procedure version for reusability
- CREATE OR REPLACE PROCEDURE syntax
- Parameterized input (p_empno)
- Can be called multiple times with different employee numbers

#### Python Equivalent
**1.py**: Python script using cx_Oracle driver
- Uses cx_Oracle.connect() for database connection
- Cursor.execute() with parameterized queries
- Exception handling with cx_Oracle.DatabaseError
- fetchone() for single row retrieval

### 3.2 Program 2: insert_with_commit.pc

#### Purpose
Inserts a new employee record into the EMP table with transaction management.

#### Components
- **Host Variables**:
  - Connection credentials (username, password, db)
  - Employee data: empno, ename, job, mgr, sal, comm, deptno

#### Data Flow
1. Connect to database
2. Execute INSERT statement with SYSDATE for hiredate
3. On success: COMMIT the transaction
4. On failure: ROLLBACK the transaction
5. Final COMMIT RELEASE to close connection

#### Transaction Management
- Uses explicit COMMIT/ROLLBACK
- Ensures data consistency
- Releases connection on exit

#### Error Handling
- Connection errors: Exit with error code 1
- Insert errors: Rollback and display error message

### 3.3 Program 3: cursor_fetch_loop.pc

#### Purpose
Retrieves and displays all employees in a specific department using a cursor.

#### Components
- **Host Variables**:
  - Connection credentials
  - deptno: Department number (hardcoded to 10)
  - empno, ename, sal: Output variables for each row

#### Data Flow
1. Connect to database
2. Declare cursor for SELECT query with ORDER BY
3. Open cursor
4. Fetch rows in a loop:
   - Print employee details
   - Break on NO_DATA_FOUND (sqlcode 1403)
   - Handle other errors
5. Close cursor
6. Commit and release connection

#### Cursor Management
- Explicit cursor declaration, open, fetch, close
- Loop-based fetching for multiple rows
- Ordered results by employee number

#### Error Handling
- Connection failures: Exit with code 1
- Fetch errors: Display ORA error and break loop

### 3.4 Program 4: call_proc_in_out.pc

#### Purpose
Calls a stored procedure to retrieve employee salary information.

#### Components
- **Host Variables**:
  - Connection credentials
  - empno: Input parameter (hardcoded to 7369)
  - out_sal: Output parameter (DOUBLE)

#### Data Flow
1. Connect to database
2. Execute stored procedure call: p_get_sal(empno, out_sal)
3. Handle results:
   - Success: Print empno and salary
   - No data: Print "No employee found"
   - Error: Display SQL error
4. Commit and release connection

#### Stored Procedure Interface
- Procedure name: p_get_sal
- Input: empno (INTEGER)
- Output: salary (DOUBLE)
- Assumes procedure exists in database

#### Error Handling
- Connection failures: Exit with code 1
- Procedure errors: Display ORA error details

### 3.5 Program 5: bulk_insert_employees.pc

#### Purpose
Performs bulk loading of employee records from a CSV file into the EMP table with individual transaction management.

#### Components
- **Host Variables**:
  - Connection credentials
  - Employee data fields: empno, ename, job, mgr, sal, comm, deptno

#### Data Structures
- **File Input**: CSV format file "employee_data.txt"
- **CSV Parsing**: Comma-separated values with 7 fields per record
- **Counters**: success_count, failure_count, total_processed for tracking operations

#### Data Flow
1. Open employee_data.txt file for reading
2. Connect to database
3. For each line in the file:
   - Parse CSV line into individual fields
   - Validate data format
   - Copy data to host variables
   - Execute INSERT statement
   - On success: COMMIT and increment success counter
   - On failure: ROLLBACK and increment failure counter
4. Close data file
5. Display summary statistics
6. Final commit and release connection

#### File Format
- **Format**: CSV (Comma-Separated Values)
- **Fields**: empno,ename,job,mgr,sal,comm,deptno
- **Data Types**: int,string,string,int,float,float,int
- **Example**: 9001,MUTHU,DEV,7839,2500.0,0.0,10

#### Transaction Management
- Individual COMMIT/ROLLBACK per record
- Partial success handling (some records may succeed, others fail)
- Final COMMIT RELEASE for connection cleanup

#### Error Handling
- File open failures: Exit with error message
- CSV parsing errors: Log error and continue with next record
- Database connection failures: Exit with code 1
- Insert errors: Rollback individual transaction, log error, continue processing
- Summary reporting of successes and failures

#### Performance Considerations
- Sequential file reading and processing
- Individual commits (not optimal for very large datasets)
- File-based data source with CSV parsing overhead

### 3.6 Program 6: Employee Salary Display Programs

#### Purpose
Display comprehensive employee salary information with department grouping and totals.

#### Components (Pro*C - 6.pc)
- **Host Variables**:
  - Connection credentials
  - Employee data fields: empno, ename, job, sal, comm, deptno

#### Components (Python - 6.py)
- **Variables**: Database connection parameters
- **Data Structures**: Lists for department grouping
- **Output**: Formatted console display with headers and totals

#### Data Flow
1. Connect to database
2. Execute SELECT query with department ordering
3. Group results by department
4. Display formatted output with subtotals
5. Show grand totals
6. Clean up connections

#### Error Handling
- Connection failures: Exit with error code 1
- Query errors: Display database error messages
- Resource cleanup on all exit paths

#### Python Implementation Features
- cx_Oracle connection and cursor management
- Dictionary-based department grouping
- Formatted output with proper alignment
- Exception handling with specific error types

### 3.7 Program employee_salary_viewer.py: Comprehensive Salary Viewer

#### Purpose
Generate detailed multi-section reports on employee salaries with company and department summaries.

#### Components
- **EmployeeSalaryViewer Class**:
  - Connection management methods
  - Data retrieval methods (summary, department, employees)
  - Display formatting methods
  - Report generation orchestration

#### Key Methods
- `connect()`: Establish database connection
- `get_employee_summary()`: Calculate company-wide statistics
- `get_department_summary()`: Department-wise salary breakdown
- `get_all_employees()`: Detailed employee information with joins
- `display_*()`: Formatted output methods
- `generate_report()`: Main report generation workflow

#### Data Flow
1. Prompt for connection parameters
2. Establish database connection
3. Retrieve summary statistics
4. Retrieve department breakdown
5. Retrieve detailed employee data
6. Generate formatted report sections
7. Clean up database connections

#### Features
- Interactive connection parameter input
- Multi-table joins (EMP, DEPT)
- Comprehensive error handling
- Formatted console output with headers
- Department grouping and subtotals
- Manager name resolution via self-joins

#### Error Handling
- Connection failures with user feedback
- Query failures with specific error messages
- Graceful handling of missing data (NULL values)
- Resource cleanup in finally blocks

#### Performance Considerations
- Single comprehensive queries for efficiency
- Client-side data processing and formatting
- Memory usage scales with employee count

## 4. Common Components

### 4.1 SQL Communications Area (SQLCA)
All programs include sqlca for error handling:
- sqlca.sqlcode: SQL return code
- sqlca.sqlerrm: Error message structure

### 4.2 Connection Management
- All programs use EXEC SQL CONNECT
- Credentials hardcoded (not recommended for production)
- Connection released with COMMIT WORK RELEASE

### 4.3 Error Handling Functions
- sql_error(): Common function for displaying SQL errors
- Uses sqlca.sqlerrm for error details

## 5. Assumptions and Constraints

### 5.1 Assumptions
- Oracle database ORCLPDB1 is available and accessible
- SCOTT schema exists with EMP table
- User SCOTT has necessary privileges (SELECT, INSERT)
- For program 4: Stored procedure p_get_sal exists

### 5.2 Constraints
- Hardcoded connection parameters
- No input validation
- Limited error handling
- Single-threaded execution

## 6. Dependencies

### 6.1 Software Dependencies
- Oracle Pro*C Precompiler
- Oracle Client Libraries
- C Compiler (gcc)
- Oracle Database Server

### 6.2 Build Process
1. Precompile .pc to .c: `proc iname=file.pc oname=file.c`
2. Compile .c to executable: `gcc -o file file.c -I$ORACLE_HOME/precomp/public -L$ORACLE_HOME/lib -lclntsh`

## 7. Security Considerations

### 7.1 Current Issues
- Hardcoded credentials in source code
- No encryption of sensitive data
- Direct database access from application

### 7.2 Recommendations
- Use external configuration for credentials
- Implement connection pooling
- Add input validation and sanitization
- Use parameterized queries (though Pro*C handles this)

## 8. Performance Considerations

### 8.1 Program 1
- Single row SELECT: Efficient for indexed lookups
- Minimal resource usage

### 8.2 Program 2
- INSERT with COMMIT: Immediate persistence
- Consider batch inserts for multiple records

### 8.3 Program 3
- Cursor-based fetch: Memory efficient for large result sets
- ORDER BY may impact performance on large tables

### 8.4 Program 4
- Stored procedure call: Encapsulates business logic
- Network round-trip for each call

## 9. Testing Approach

Refer to test_scenarios.md for detailed test cases covering:
- Functional testing
- Error scenarios
- Edge cases
- Database state validation

## 10. Maintenance and Support

### 10.1 Code Organization
- Modular structure with clear separation of concerns
- Consistent error handling patterns
- Comments for complex SQL operations

### 10.2 Monitoring
- SQL error codes for troubleshooting
- Program exit codes for automation
- Database logs for transaction monitoring