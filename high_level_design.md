# High-Level Design Document

## 1. System Overview

This system consists of four Pro*C programs that demonstrate fundamental database operations with an Oracle database. The programs provide examples of basic CRUD operations and stored procedure calls using embedded SQL in C.

## 2. Architecture

### 2.1 High-Level Architecture
```
[Pro*C Programs] <--- Embedded SQL ---> [Oracle Database]
       |
       v
[Compilation Process]
(proc precompiler + C compiler)
```

### 2.2 Components
- **Database Layer**: Oracle Database (ORCLPDB1) with SCOTT schema
- **Application Layer**: Four C programs with embedded SQL
- **Build Layer**: Pro*C precompiler and C compiler toolchain

## 3. Program Components

### 3.1 Program 1: Data Retrieval
- **Purpose**: Single record selection
- **Input**: Employee number
- **Output**: Employee details (name, salary)
- **Database Operation**: SELECT query
- **PL/SQL Versions**: Available as anonymous block (1_plsql.sql) and stored procedure (1_plsql_proc.sql)

### 3.2 Program 2: Data Insertion
- **Purpose**: Add new employee record
- **Input**: Complete employee information
- **Output**: Success/failure confirmation
- **Database Operation**: INSERT with transaction management

### 3.3 Program 3: Bulk Data Retrieval
- **Purpose**: Retrieve multiple records
- **Input**: Department number
- **Output**: List of employees in department
- **Database Operation**: Cursor-based SELECT with looping

### 3.4 Program 4: Stored Procedure Interface
- **Purpose**: Execute database procedure
- **Input**: Employee number
- **Output**: Employee salary from procedure
- **Database Operation**: Stored procedure call

### 3.5 Program 5: Bulk Data Loading from File
- **Purpose**: Load multiple employee records from CSV file
- **Input**: employee_data.txt file with CSV formatted data
- **Output**: Success/failure status for each record loaded
- **Database Operation**: Multiple INSERT operations from file data
- **Python Version**: 5.py using cx_Oracle and csv modules

### 3.6 Program 6: Employee Salary Display
- **Purpose**: Display employee salary details with department grouping
- **Input**: None (uses all EMP table data)
- **Output**: Formatted table of employees grouped by department with totals
- **Database Operation**: SELECT query with ordering and aggregation
- **Pro*C Version**: 6.pc using embedded SQL and cursors
- **Python Version**: 6.py using cx_Oracle and data grouping

### 3.7 Program employee_salary_viewer.py: Comprehensive Salary Viewer
- **Purpose**: Generate detailed multi-section employee salary reports
- **Input**: Database connection parameters (interactive)
- **Output**: Comprehensive report with company summary, department breakdown, and detailed employee list
- **Database Operation**: Multiple SELECT queries with joins (EMP, DEPT tables)
- **Features**: Interactive input, formatted output, error handling, resource cleanup

## 4. Data Flow

### 4.1 General System Flow
```
Start
  │
  ├─> Establish Database Connection
  │     │
  │     ├─> Success ──> Execute Database Operation
  │     │
  │     └─> Failure ──> Display Error & Exit
  │
  └─> Process Results
        │
        ├─> Success ──> Display Output
        │
        └─> Error ────> Display Error Message
  │
  └─> Close Connection & Exit
```

### 4.2 Program-Specific Flows

#### Program 1: Single Record Retrieval
```
Program Start
     │
     ├─> Connect to Database
     │
     ├─> Execute SELECT Query
     │     │
     │     ├─> Data Found ──> Display Employee Details
     │     │
     │     └─> No Data ────> Display "No data found"
     │
     └─> Handle SQL Errors
     │
     └─> Disconnect & Exit
```

#### Program 2: Data Insertion
```
Program Start
     │
     ├─> Connect to Database
     │
     ├─> Execute INSERT Query
     │     │
     │     ├─> Success ──> COMMIT Transaction
     │     │              └─> Display Success Message
     │     │
     │     └─> Failure ──> ROLLBACK Transaction
     │                    └─> Display Error Message
     │
     └─> Final COMMIT RELEASE
     │
     └─> Exit
```

#### Program 3: Multi-Record Retrieval
```
Program Start
     │
     ├─> Connect to Database
     │
     ├─> Declare & Open Cursor
     │
     ├─> Fetch Loop Start
     │     │
     │     ├─> Fetch Row
     │     │     │
     │     │     ├─> Data Available ──> Display Row
     │     │     │                     └─> Continue Loop
     │     │     │
     │     │     └─> No More Data ────> Exit Loop
     │     │
     │     └─> Fetch Error ──────────> Display Error & Exit Loop
     │
     ├─> Close Cursor
     │
     └─> Disconnect & Exit
```

#### Program 4: Stored Procedure Call
```
Program Start
     │
     ├─> Connect to Database
     │
     ├─> Call Stored Procedure p_get_sal
     │     │
     │     ├─> Success ──> Display Salary Information
     │     │
     │     └─> No Data ──> Display "No employee found"
     │
     └─> Handle Procedure Errors
     │
     └─> Disconnect & Exit
```

#### Program 5: Bulk Data Loading from File
```
Program Start
     │
     ├─> Open employee_data.txt File
     │     │
     │     ├─> File Not Found ──> Display Error & Exit
     │     │
     │     └─> File Opened ────> Continue
     │
     ├─> Connect to Database
     │
     ├─> For Each Line in File
     │     │
     │     ├─> Parse CSV Line
     │     │     │
     │     │     ├─> Parse Error ──> Log Error & Continue
     │     │     │
     │     │     └─> Valid Data ──> Continue
     │     │
     │     ├─> Copy Data to Host Variables
     │     │
     │     ├─> Execute INSERT Query
     │     │     │
     │     │     ├─> Success ──> COMMIT & Log Success
     │     │     │
     │     │     └─> Failure ──> ROLLBACK & Log Error
     │     │
     │     └─> Next Line
     │
     ├─> Close Data File
     │
     ├─> Display Summary Statistics
     │
     └─> Disconnect & Exit
```

### 4.3 Data Entities
- **Employee Record**: empno, ename, job, mgr, sal, comm, deptno
- **Connection Parameters**: username, password, database name
- **Query Results**: Retrieved data or status codes

## 5. Key Interfaces

### 5.1 Database Interface
- **Protocol**: Oracle Net (SQL*Net)
- **Authentication**: Username/password
- **Operations**: SELECT, INSERT, stored procedure calls

### 5.2 User Interface
- **Input**: Hardcoded parameters (for demonstration)
- **Output**: Console-based text output
- **Error Reporting**: Standard error stream with SQL error codes

## 6. Assumptions and Constraints

### 6.1 Assumptions
- Oracle database environment is available and configured
- SCOTT schema with EMP table exists
- Required privileges are granted to database user
- Pro*C development environment is set up

### 6.2 Constraints
- Single-threaded execution
- Console-based interaction (no GUI)
- Hardcoded connection parameters
- Demonstration-purpose code (not production-ready)

## 7. Technology Stack

### 7.1 Core Technologies
- **Programming Language**: C with embedded SQL
- **Database**: Oracle Database
- **Precompiler**: Oracle Pro*C
- **Compiler**: GCC

### 7.2 Development Tools
- Pro*C precompiler
- C compiler (gcc)
- Oracle client libraries
- Text editor/IDE

## 8. Deployment and Execution

### 8.1 Build Process
1. Precompile .pc files to .c files
2. Compile .c files to executables
3. Link with Oracle libraries

### 8.2 Runtime Requirements
- Oracle database connectivity
- Executable permissions
- Database user credentials

## 9. Security Considerations

### 9.1 Current State
- Basic authentication
- No encryption
- Hardcoded credentials

### 9.2 Recommended Improvements
- External configuration files
- Secure credential management
- Input validation

## 10. Performance Characteristics

### 10.1 Program Characteristics
- **Program 1**: Fast single-row lookups
- **Program 2**: Transactional inserts with immediate commit
- **Program 3**: Memory-efficient cursor processing
- **Program 4**: Procedure-based data access

### 10.2 Scalability
- Suitable for demonstration and small-scale operations
- Not optimized for high-volume processing

## 11. Testing Strategy

### 11.1 Test Types
- Unit testing of individual programs
- Integration testing with database
- Error condition testing
- Performance validation

### 11.2 Test Environment
- Dedicated test database
- Known test data sets
- Automated test scripts

## 12. Maintenance and Support

### 12.1 Code Organization
- Modular program structure
- Consistent error handling
- Clear separation of database logic

### 12.2 Documentation
- Inline code comments
- Separate design documents
- Test scenario documentation

### 12.3 Version Control
- Source code versioning
- Build artifact management
- Configuration management