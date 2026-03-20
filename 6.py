#!/usr/bin/env python3
"""
simple_emp_salary.py - Simple application to display employee salary details
Shows basic employee and salary information in a clean format
"""

import cx_Oracle
import sys

def main():
    # Database connection parameters
    username = "scott"
    password = "tiger"
    dsn = "ORCLPDB1"

    try:
        # Connect to database
        connection = cx_Oracle.connect(username, password, dsn)
        cursor = connection.cursor()

        # Get all employees with salary information
        cursor.execute("""
            SELECT empno, ename, job, sal, comm, deptno
            FROM emp
            ORDER BY deptno, sal DESC
        """)

        print("=" * 60)
        print("         EMPLOYEE SALARY DETAILS")
        print("=" * 60)
        print("<6")
        print("-" * 60)

        total_employees = 0
        total_salary = 0
        current_dept = None

        rows = cursor.fetchall()
        for row in rows:
            empno, ename, job, sal, comm, deptno = row
            total_employees += 1
            total_salary += sal

            # Group by department
            if current_dept != deptno:
                if current_dept is not None:
                    print()
                print(f"Department {deptno}:")
                current_dept = deptno

            # Format commission
            comm_display = ".2f" if comm else "     "

            print("<6")

        print("-" * 60)
        print("12.2f")
        print("=" * 60)

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Database error: {error.message}")
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