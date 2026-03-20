-- select_single_row.sql - PL/SQL equivalent of 1.pc
-- This script selects a single employee record and displays the results

DECLARE
    -- Declare variables equivalent to host variables in Pro*C
    v_empno    NUMBER := 7369;  -- Hardcoded empno like in the C program
    v_ename    VARCHAR2(10);    -- Employee name
    v_sal      NUMBER(7,2);     -- Employee salary

    -- Variables for error handling
    v_error_msg VARCHAR2(4000);

BEGIN
    -- Main processing logic equivalent to the SELECT in Pro*C
    BEGIN
        -- Select employee data (equivalent to EXEC SQL SELECT)
        SELECT ename, sal
        INTO v_ename, v_sal
        FROM emp
        WHERE empno = v_empno;

        -- If successful (equivalent to sqlca.sqlcode == 0)
        DBMS_OUTPUT.PUT_LINE('EMPNO=' || v_empno || ' ENAME=' || v_ename || ' SAL=' || TO_CHAR(v_sal, '99999.99'));

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            -- Equivalent to sqlca.sqlcode == 1403
            DBMS_OUTPUT.PUT_LINE('No data found for EMPNO=' || v_empno);

        WHEN OTHERS THEN
            -- Equivalent to other sqlca.sqlcode errors
            v_error_msg := SQLERRM;
            DBMS_OUTPUT.PUT_LINE('SELECT failed: ' || v_error_msg);
            DBMS_OUTPUT.PUT_LINE('ORA-' || SQLCODE);
    END;

EXCEPTION
    WHEN OTHERS THEN
        -- Handle any unexpected errors
        v_error_msg := SQLERRM;
        DBMS_OUTPUT.PUT_LINE('Unexpected error: ' || v_error_msg);
        DBMS_OUTPUT.PUT_LINE('ORA-' || SQLCODE);

END;
/