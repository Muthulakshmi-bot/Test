-- employee_procedures.sql
-- PL/SQL Stored Procedures for Employee Database Operations
-- This script creates the stored procedures used by the Pro*C and Python programs

-- Procedure to select and display a single employee record
CREATE OR REPLACE PROCEDURE select_employee (
    p_empno IN NUMBER
) AS
    v_ename VARCHAR2(10);
    v_sal NUMBER(7,2);
BEGIN
    -- Select employee data
    SELECT ename, sal
    INTO v_ename, v_sal
    FROM emp
    WHERE empno = p_empno;

    -- Display the results
    DBMS_OUTPUT.PUT_LINE('EMPNO=' || p_empno || ' ENAME=' || v_ename || ' SAL=' || TO_CHAR(v_sal, '99999.99'));

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No data found for EMPNO=' || p_empno);
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error in select_employee: ' || SQLERRM);
        RAISE_APPLICATION_ERROR(-20001, 'Error in select_employee: ' || SQLERRM);
END select_employee;
/

-- Procedure to get employee salary (used by program 4)
CREATE OR REPLACE PROCEDURE p_get_sal (
    p_empno IN NUMBER,
    p_salary OUT NUMBER
) AS
BEGIN
    SELECT sal
    INTO p_salary
    FROM emp
    WHERE empno = p_empno;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        p_salary := NULL;
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error in p_get_sal: ' || SQLERRM);
        RAISE;
END p_get_sal;
/

-- Additional utility procedures for testing and validation

-- Procedure to validate employee data
CREATE OR REPLACE PROCEDURE validate_employee_data (
    p_empno IN NUMBER,
    p_valid OUT BOOLEAN,
    p_error_msg OUT VARCHAR2
) AS
    v_count NUMBER;
BEGIN
    p_valid := TRUE;
    p_error_msg := NULL;

    -- Check if employee exists
    SELECT COUNT(*)
    INTO v_count
    FROM emp
    WHERE empno = p_empno;

    IF v_count = 0 THEN
        p_valid := FALSE;
        p_error_msg := 'Employee does not exist';
        RETURN;
    END IF;

    -- Additional validation could be added here
    -- (e.g., check salary ranges, department validity, etc.)

EXCEPTION
    WHEN OTHERS THEN
        p_valid := FALSE;
        p_error_msg := 'Validation error: ' || SQLERRM;
END validate_employee_data;
/

-- Procedure to get employee count by department
CREATE OR REPLACE PROCEDURE get_dept_employee_count (
    p_deptno IN NUMBER,
    p_count OUT NUMBER
) AS
BEGIN
    SELECT COUNT(*)
    INTO p_count
    FROM emp
    WHERE deptno = p_deptno;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        p_count := 0;
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error in get_dept_employee_count: ' || SQLERRM);
        RAISE_APPLICATION_ERROR(-20001, 'Error in get_dept_employee_count: ' || SQLERRM);
END get_dept_employee_count;
/

-- Grant execute permissions on procedures (adjust schema name as needed)
-- GRANT EXECUTE ON select_employee TO PUBLIC;
-- GRANT EXECUTE ON p_get_sal TO PUBLIC;
-- GRANT EXECUTE ON validate_employee_data TO PUBLIC;
-- GRANT EXECUTE ON get_dept_employee_count TO PUBLIC;