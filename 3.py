#!/usr/bin/env python3
"""
cursor_fetch_loop.py - Python equivalent of 3.pc
Fetches multiple employee records using cursor for a specific department
"""

import cx_Oracle
import sys

def main():
    # Database connection parameters
    username = "scott"
    password = "tiger"
    dsn = "ORCLPDB1"
    deptno = 10  # Department number to query

    try:
        # Connect to database
        connection = cx_Oracle.connect(username, password, dsn)
        cursor = connection.cursor()

        # Execute SELECT query with cursor (equivalent to DECLARE CURSOR and OPEN)
        cursor.execute("""
            SELECT empno, ename, sal
            FROM emp
            WHERE deptno = :deptno
            ORDER BY empno
        """, deptno=deptno)

        print(f"Employees in dept {deptno}:")

        # Fetch and display rows (equivalent to FETCH loop)
        row_count = 0
        while True:
            row = cursor.fetchone()
            if row is None:
                break  # No more rows (equivalent to sqlca.sqlcode == 1403)

            empno, ename, sal = row
            print(f"  {empno} {ename:<10} {sal:.2f}")
            row_count += 1

        if row_count == 0:
            print("  No employees found in this department")

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Query failed: {error.message}")
        print(f"ORA-{error.code}")
        return 1

    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    finally:
        # Clean up connections (equivalent to CLOSE CURSOR and COMMIT RELEASE)
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())