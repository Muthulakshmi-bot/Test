# Oracle Database Programs - Multiple Implementations

This project contains Oracle database programs implemented in three different ways:
- **Pro*C** (.pc files): C programs with embedded SQL
- **Python** (.py files): Modern Python scripts using cx_Oracle
- **PL/SQL** (.sql files): Database-side stored procedures

## Files Overview

### Pro*C Programs (.pc)
- `1.pc` - Select single employee record
- `2.pc` - Insert new employee with transaction management
- `3.pc` - Fetch multiple employees using cursor
- `4.pc` - Call stored procedure for salary
- `5.pc` - Bulk load employees from CSV file
- `6.pc` - Display employee and salary details

### Python Programs (.py)
- `1.py` - Python equivalent of 1.pc
- `2.py` - Python equivalent of 2.pc
- `3.py` - Python equivalent of 3.pc
- `4.py` - Python equivalent of 4.pc
- `5.py` - Python equivalent of 5.pc
- `6.py` - Simple employee salary display
- `employee_salary_viewer.py` - Comprehensive employee salary viewer application

### PL/SQL Programs (.sql)
- `1_plsql.sql` - Anonymous PL/SQL block equivalent of 1.pc
- `1_plsql_proc.sql` - Stored procedure version of 1.pc

### Data Files
- `employee_data.txt` - CSV data file for bulk loading (used by 5.pc and 5.py)
- `requirements.txt` - Python dependencies

## Prerequisites

### For Pro*C Programs
- Oracle Pro*C precompiler
- C compiler (gcc)
- Oracle client libraries
- Database connectivity

### For Python Programs
- Python 3.6+
- cx_Oracle package
- Oracle client libraries
- Database connectivity

### For PL/SQL Programs
- Oracle SQL*Plus or SQL Developer
- Database connectivity

## Setup Instructions

### Pro*C Setup
```bash
# Precompile and compile each .pc file
proc iname=X.pc oname=X.c
gcc -o X X.c -I$ORACLE_HOME/precomp/public -L$ORACLE_HOME/lib -lclntsh
```

### Python Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Ensure Oracle client is available
# On Windows: Install Oracle Instant Client
# On Linux: Install oracle-instantclient packages
```

### PL/SQL Setup
```bash
# Connect to database
sqlplus username/password@database
```

## Execution Examples

### Pro*C Programs
```bash
# After compilation
./1  # Select single employee
./2  # Insert employee
./3  # Cursor fetch
./4  # Call procedure
./5  # Bulk load from file
./6  # Display salary details
```

### Python Programs
```bash
python 1.py              # Select single employee
python 2.py              # Insert employee
python 3.py              # Cursor fetch
python 4.py              # Call procedure
python 5.py              # Bulk load from file
python 6.py              # Simple salary display
python employee_salary_viewer.py  # Comprehensive viewer
```

### PL/SQL Programs
```bash
# Anonymous block
sqlplus scott/tiger@ORCLPDB1 @1_plsql.sql

# Stored procedure
sqlplus scott/tiger@ORCLPDB1 @1_plsql_proc.sql
EXEC select_employee(7369);
```

## Database Schema

All programs work with the SCOTT.EMP table:

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

## Program 4 Requirements

Program 4 (both Pro*C and Python versions) requires a stored procedure `p_get_sal`:

```sql
CREATE OR REPLACE PROCEDURE p_get_sal (
    p_empno IN NUMBER,
    p_salary OUT NUMBER
) AS
BEGIN
    SELECT sal INTO p_salary
    FROM emp
    WHERE empno = p_empno;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        p_salary := NULL;
END;
/
```

## Testing

See `test_scenarios.md` for comprehensive test cases covering:
- Functional testing
- Error conditions
- Edge cases
- Performance scenarios

## Documentation

- `high_level_design.md` - High-level system overview
- `technical_design.md` - Detailed technical specifications
- `test_scenarios.md` - Comprehensive test scenarios

## Comparison of Implementations

| Aspect | Pro*C | Python | PL/SQL |
|--------|-------|--------|--------|
| Compilation | Required | No | No |
| Dependencies | Oracle Pro*C | cx_Oracle + Python | None |
| Performance | Fastest | Moderate | Fast |
| Portability | Platform dependent | Cross-platform | Database only |
| Maintenance | Complex | Simple | Simple |
| Deployment | Binary | Source | Database objects |

## Troubleshooting

### Pro*C Issues
- Ensure ORACLE_HOME is set
- Check Pro*C license
- Verify compiler compatibility

### Python Issues
- Install correct cx_Oracle version for Python architecture
- Set ORACLE_HOME or use instant client
- Check Python and Oracle client bitness match

### PL/SQL Issues
- Ensure proper database privileges
- Check for compilation errors
- Verify procedure exists (for program 4)

## Contributing

When adding new programs:
1. Implement in all three languages (Pro*C, Python, PL/SQL)
2. Update documentation
3. Add test scenarios
4. Test on target platform
