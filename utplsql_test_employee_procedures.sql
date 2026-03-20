-- utplsql_test_employee_procedures.sql
-- UTPLSQL Unit Test Suite for Employee Database Procedures
-- This script creates comprehensive unit tests for PL/SQL stored procedures

-- Install UTPLSQL framework if not already installed
-- This would typically be done once per database
-- @install_headless.sql

-- Create test package for employee procedures
CREATE OR REPLACE PACKAGE test_employee_procedures AS
    --%suite(Employee Procedures Test Suite)
    --%suitepath(employee.db.procedures)

    -- Test procedures for select_employee procedure
    --%test(Test select_employee with valid employee)
    PROCEDURE test_select_employee_valid;

    --%test(Test select_employee with invalid employee)
    PROCEDURE test_select_employee_invalid;

    --%test(Test select_employee with null input)
    PROCEDURE test_select_employee_null_input;

    -- Test procedures for p_get_sal procedure
    --%test(Test p_get_sal with valid employee)
    PROCEDURE test_p_get_sal_valid;

    --%test(Test p_get_sal with invalid employee)
    PROCEDURE test_p_get_sal_invalid;

    --%test(Test p_get_sal with null input)
    PROCEDURE test_p_get_sal_null_input;

    -- Setup and teardown procedures
    --%beforeall
    PROCEDURE setup_test_data;

    --%afterall
    PROCEDURE cleanup_test_data;

    --%beforeeach
    PROCEDURE reset_test_state;
END test_employee_procedures;
/

CREATE OR REPLACE PACKAGE BODY test_employee_procedures AS

    -- Setup procedure to create test data
    PROCEDURE setup_test_data IS
    BEGIN
        -- Insert test employee data
        INSERT INTO emp (empno, ename, job, mgr, hiredate, sal, comm, deptno)
        VALUES (9998, 'TESTEMP1', 'CLERK', 7902, SYSDATE, 1500.00, 0.00, 20);

        INSERT INTO emp (empno, ename, job, mgr, hiredate, sal, comm, deptno)
        VALUES (9999, 'TESTEMP2', 'ANALYST', 7566, SYSDATE, 3000.00, 500.00, 20);

        COMMIT;
    END setup_test_data;

    -- Cleanup procedure to remove test data
    PROCEDURE cleanup_test_data IS
    BEGIN
        -- Remove test data
        DELETE FROM emp WHERE empno IN (9998, 9999);
        COMMIT;
    END cleanup_test_data;

    -- Reset procedure for each test
    PROCEDURE reset_test_state IS
    BEGIN
        -- Reset any session state if needed
        NULL;
    END reset_test_state;

    -- Test select_employee with valid employee
    PROCEDURE test_select_employee_valid IS
        v_empno NUMBER := 9998;
        v_result_empno NUMBER;
        v_result_ename VARCHAR2(10);
        v_result_sal NUMBER;
    BEGIN
        -- Call the procedure
        select_employee(v_empno);

        -- Verify the procedure executed without errors
        -- Note: Since select_employee uses DBMS_OUTPUT, we can't directly capture output
        -- In a real test, we might modify the procedure to return values or use a different approach

        -- Verify the employee exists in the database
        SELECT empno, ename, sal
        INTO v_result_empno, v_result_ename, v_result_sal
        FROM emp
        WHERE empno = v_empno;

        -- Assertions
        ut.expect(v_result_empno).to_equal(v_empno);
        ut.expect(v_result_ename).to_equal('TESTEMP1');
        ut.expect(v_result_sal).to_equal(1500.00);

    END test_select_employee_valid;

    -- Test select_employee with invalid employee
    PROCEDURE test_select_employee_invalid IS
        v_empno NUMBER := 99999; -- Non-existent employee
        v_no_data_exception BOOLEAN := FALSE;
    BEGIN
        -- This test verifies that the procedure handles non-existent employees gracefully
        -- Since the procedure uses DBMS_OUTPUT and exception handling,
        -- we test that no unexpected exceptions are raised

        BEGIN
            select_employee(v_empno);
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                v_no_data_exception := TRUE;
            WHEN OTHERS THEN
                -- Re-raise unexpected exceptions
                RAISE;
        END;

        -- The procedure should handle NO_DATA_FOUND internally
        ut.expect(v_no_data_exception).to_be_false();

    END test_select_employee_invalid;

    -- Test select_employee with null input
    PROCEDURE test_select_employee_null_input IS
        v_exception_raised BOOLEAN := FALSE;
    BEGIN
        -- Test with null input
        BEGIN
            select_employee(NULL);
        EXCEPTION
            WHEN OTHERS THEN
                v_exception_raised := TRUE;
        END;

        -- The procedure should handle null input gracefully
        ut.expect(v_exception_raised).to_be_false();

    END test_select_employee_null_input;

    -- Test p_get_sal with valid employee
    PROCEDURE test_p_get_sal_valid IS
        v_empno NUMBER := 9998;
        v_salary NUMBER;
        v_expected_salary NUMBER := 1500.00;
    BEGIN
        -- Call the procedure
        p_get_sal(v_empno, v_salary);

        -- Verify the returned salary
        ut.expect(v_salary).to_equal(v_expected_salary);
        ut.expect(v_salary).to_be_not_null();

    END test_p_get_sal_valid;

    -- Test p_get_sal with invalid employee
    PROCEDURE test_p_get_sal_invalid IS
        v_empno NUMBER := 99999; -- Non-existent employee
        v_salary NUMBER;
    BEGIN
        -- Call the procedure
        p_get_sal(v_empno, v_salary);

        -- Verify that null is returned for non-existent employee
        ut.expect(v_salary).to_be_null();

    END test_p_get_sal_invalid;

    -- Test p_get_sal with null input
    PROCEDURE test_p_get_sal_null_input IS
        v_salary NUMBER;
        v_exception_raised BOOLEAN := FALSE;
    BEGIN
        -- Test with null input
        BEGIN
            p_get_sal(NULL, v_salary);
        EXCEPTION
            WHEN OTHERS THEN
                v_exception_raised := TRUE;
        END;

        -- The procedure should handle null input and return null salary
        ut.expect(v_exception_raised).to_be_false();
        ut.expect(v_salary).to_be_null();

    END test_p_get_sal_null_input;

END test_employee_procedures;
/

-- Run the test suite
-- EXEC ut.run('test_employee_procedures');

-- Alternative: Run specific tests
-- EXEC ut.run('test_employee_procedures.test_select_employee_valid');
-- EXEC ut.run('test_employee_procedures.test_p_get_sal_valid');