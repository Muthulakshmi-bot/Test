#!/usr/bin/env python3
"""
employee_salary_viewer.py - Application to display employee and salary details
Shows comprehensive employee information with formatted output
"""

import cx_Oracle
import sys
from datetime import datetime
import os

class EmployeeSalaryViewer:
    def __init__(self, username="scott", password="tiger", dsn="ORCLPDB1"):
        self.username = username
        self.password = password
        self.dsn = dsn
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = cx_Oracle.connect(self.username, self.password, self.dsn)
            self.cursor = self.connection.cursor()
            return True
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Database connection failed: {error.message}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_employee_summary(self):
        """Get summary statistics of employees"""
        try:
            self.cursor.execute("""
                SELECT
                    COUNT(*) as total_employees,
                    AVG(sal) as avg_salary,
                    MIN(sal) as min_salary,
                    MAX(sal) as max_salary,
                    SUM(sal) as total_salary
                FROM emp
            """)
            row = self.cursor.fetchone()
            return {
                'total_employees': row[0],
                'avg_salary': row[1],
                'min_salary': row[2],
                'max_salary': row[3],
                'total_salary': row[4]
            }
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Error getting summary: {error.message}")
            return None

    def get_all_employees(self):
        """Get all employee details ordered by department and salary"""
        try:
            self.cursor.execute("""
                SELECT
                    e.empno,
                    e.ename,
                    e.job,
                    e.mgr,
                    e.hiredate,
                    e.sal,
                    e.comm,
                    e.deptno,
                    d.dname,
                    m.ename as manager_name
                FROM emp e
                LEFT JOIN dept d ON e.deptno = d.deptno
                LEFT JOIN emp m ON e.mgr = m.empno
                ORDER BY e.deptno, e.sal DESC
            """)
            return self.cursor.fetchall()
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Error getting employees: {error.message}")
            return []

    def get_department_summary(self):
        """Get salary summary by department"""
        try:
            self.cursor.execute("""
                SELECT
                    d.dname,
                    COUNT(e.empno) as emp_count,
                    AVG(e.sal) as avg_salary,
                    MIN(e.sal) as min_salary,
                    MAX(e.sal) as max_salary,
                    SUM(e.sal) as total_salary
                FROM dept d
                LEFT JOIN emp e ON d.deptno = e.deptno
                GROUP BY d.deptno, d.dname
                ORDER BY d.dname
            """)
            return self.cursor.fetchall()
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Error getting department summary: {error.message}")
            return []

    def display_header(self):
        """Display application header"""
        print("=" * 80)
        print("           EMPLOYEE AND SALARY DETAILS VIEWER")
        print("=" * 80)
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    def display_summary(self, summary):
        """Display employee summary statistics"""
        print("COMPANY SUMMARY")
        print("-" * 50)
        print("2d")
        print("12.2f")
        print("12.2f")
        print("12.2f")
        print("12.2f")
        print()

    def display_department_summary(self, dept_data):
        """Display department-wise salary summary"""
        print("DEPARTMENT-WISE SALARY SUMMARY")
        print("-" * 70)
        print("<15")
        print("-" * 70)

        for row in dept_data:
            dname, emp_count, avg_sal, min_sal, max_sal, total_sal = row
            print("<15")

        print()

    def display_employees(self, employees):
        """Display detailed employee information"""
        print("DETAILED EMPLOYEE INFORMATION")
        print("-" * 120)
        print("<6")
        print("-" * 120)

        current_dept = None
        for emp in employees:
            empno, ename, job, mgr, hiredate, sal, comm, deptno, dname, mgr_name = emp

            # Print department header when department changes
            if current_dept != deptno:
                if current_dept is not None:
                    print()  # Add space between departments
                print(f"Department: {dname} (Dept No: {deptno})")
                print("-" * 50)
                current_dept = deptno

            # Format commission (handle NULL values)
            comm_display = ".2f" if comm else "     "

            # Format manager name (handle NULL values)
            mgr_display = mgr_name if mgr_name else "N/A"

            # Format hire date
            hire_date_display = hiredate.strftime('%Y-%m-%d') if hiredate else 'N/A'

            print("<6")

    def generate_report(self):
        """Generate complete employee and salary report"""
        if not self.connect():
            return False

        try:
            # Get data
            summary = self.get_employee_summary()
            dept_summary = self.get_department_summary()
            employees = self.get_all_employees()

            if not summary:
                print("Unable to retrieve summary data")
                return False

            # Display report
            self.display_header()
            self.display_summary(summary)
            self.display_department_summary(dept_summary)
            self.display_employees(employees)

            print("=" * 80)
            print("Report Complete")
            print("=" * 80)

            return True

        finally:
            self.disconnect()

def main():
    """Main application entry point"""
    print("Employee and Salary Details Viewer")
    print("===================================")

    # Allow command line arguments for connection parameters
    username = input("Username [scott]: ").strip() or "scott"
    password = input("Password [tiger]: ").strip() or "tiger"
    dsn = input("DSN [ORCLPDB1]: ").strip() or "ORCLPDB1"

    # Create viewer instance
    viewer = EmployeeSalaryViewer(username, password, dsn)

    # Generate report
    if viewer.generate_report():
        print("\nReport generated successfully!")
        return 0
    else:
        print("\nReport generation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())