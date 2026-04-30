CREATE OR REPLACE FUNCTION fn_calculate_total (
    p_bill_id IN NUMBER
) RETURN NUMBER AS
    v_total NUMBER(12,2);
BEGIN
    SELECT NVL(SUM(line_total), 0)
    INTO v_total
    FROM bill_items
    WHERE bill_id = p_bill_id;

    RETURN v_total;
END;
