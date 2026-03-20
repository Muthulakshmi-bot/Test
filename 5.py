#!/usr/bin/env python3
"""
bulk_insert_employees.py - Python equivalent of 5.pc
Loads employee data from CSV file into database
"""

import cx_Oracle
import csv
import sys
import os

def main():
    # Database connection parameters
    username = "scott"
    password = "tiger"
    dsn = "ORCLPDB1"
    data_file = "employee_data.txt"

    success_count = 0
    failure_count = 0
    total_processed = 0

    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"Error: Cannot open {data_file} file")
        return 1

    try:
        # Connect to database
        connection = cx_Oracle.connect(username, password, dsn)
        cursor = connection.cursor()

        print(f"Starting bulk load from {data_file}...")

        # Open and read CSV file
        with open(data_file, 'r') as csvfile:
            # Read CSV with comma delimiter
            csvreader = csv.reader(csvfile, delimiter=',')

            for row in csvreader:
                total_processed += 1

                # Skip empty lines
                if not row or all(not field.strip() for field in row):
                    continue

                # Parse CSV fields
                if len(row) != 7:
                    print(f"Error parsing line {total_processed}: expected 7 fields, got {len(row)}")
                    failure_count += 1
                    continue

                try:
                    empno = int(row[0])
                    ename = row[1].strip()
                    job = row[2].strip()
                    mgr = int(row[3])
                    sal = float(row[4])
                    comm = float(row[5])
                    deptno = int(row[6])

                except (ValueError, IndexError) as e:
                    print(f"Error parsing data in line {total_processed}: {e}")
                    failure_count += 1
                    continue

                try:
                    # Execute INSERT statement
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

                    # Commit each successful insert
                    connection.commit()
                    print(f"Successfully loaded employee: {empno} - {ename} (Salary: {sal:.2f})")
                    success_count += 1

                except cx_Oracle.DatabaseError as e:
                    # Rollback on error
                    connection.rollback()

                    error, = e.args
                    print(f"Failed to load employee {empno}: {error.message}")
                    print(f"ORA-{error.code}")
                    failure_count += 1

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Database connection failed: {error.message}")
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

    print("\nBulk load completed:")
    print(f"Total lines processed: {total_processed}")
    print(f"Successfully loaded: {success_count} records")
    print(f"Failed to load: {failure_count} records")

    return 1 if failure_count > 0 else 0

if __name__ == "__main__":
    sys.exit(main())