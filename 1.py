#!/usr/bin/env python3
"""
select_single_row.py - Python equivalent of 1.pc
Selects a single employee record from EMP table
"""

import cx_Oracle
import sys

def main():
    # Database connection parameters (equivalent to Pro*C host variables)
    username = "scott"
    password = "tiger"
    dsn = "ORCLPDB1"
    empno = 7369  # Hardcoded employee number

    try:
        # Connect to database (equivalent to EXEC SQL CONNECT)
        connection = cx_Oracle.connect(username, password, dsn)
        cursor = connection.cursor()

        # Execute SELECT query (equivalent to EXEC SQL SELECT)
        cursor.execute("""
            SELECT ename, sal
            FROM emp
            WHERE empno = :empno
        """, empno=empno)

        # Fetch the result
        row = cursor.fetchone()

        if row:
            # Success case (equivalent to sqlca.sqlcode == 0)
            ename, sal = row
            print(f"EMPNO={empno} ENAME={ename} SAL={sal:.2f}")
        else:
            # No data found (equivalent to sqlca.sqlcode == 1403)
            print(f"No data found for EMPNO={empno}")

    except cx_Oracle.DatabaseError as e:
        # Error handling (equivalent to sql_error function)
        error, = e.args
        print(f"SELECT failed: {error.message}")
        print(f"ORA-{error.code}")
        return 1

    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    finally:
        # Clean up connections
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())