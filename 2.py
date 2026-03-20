#!/usr/bin/env python3
"""
insert_with_commit.py - Python equivalent of 2.pc
Inserts a new employee record with transaction management
"""

import cx_Oracle
import sys
from datetime import datetime

def main():
    # Database connection parameters
    username = "scott"
    password = "tiger"
    dsn = "ORCLPDB1"

    # Employee data to insert (equivalent to Pro*C host variables)
    empno = 9001
    ename = "MUTHU"
    job = "DEV"
    mgr = 7839
    sal = 2500.0
    comm = 0.0
    deptno = 10

    try:
        # Connect to database
        connection = cx_Oracle.connect(username, password, dsn)
        cursor = connection.cursor()

        # Execute INSERT statement (equivalent to EXEC SQL INSERT)
        cursor.execute("""
            INSERT INTO emp(empno, ename, job, mgr, hiredate, sal, comm, deptno)
            VALUES (:empno, :ename, :job, :mgr, SYSDATE, :sal, :comm, :deptno)
        """, {
            'empno': empno,
            'ename': ename,
            'job': job,
            'mgr': mgr,
            'sal': sal,
            'comm': comm,
            'deptno': deptno
        })

        # Commit the transaction (equivalent to EXEC SQL COMMIT WORK)
        connection.commit()
        print(f"Inserted empno={empno} (committed)")

    except cx_Oracle.DatabaseError as e:
        # Rollback on error (equivalent to EXEC SQL ROLLBACK WORK)
        if 'connection' in locals():
            connection.rollback()

        error, = e.args
        print(f"Insert failed (rolled back): {error.message}")
        print(f"ORA-{error.code}")
        return 1

    except Exception as e:
        # Rollback on unexpected error
        if 'connection' in locals():
            connection.rollback()

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