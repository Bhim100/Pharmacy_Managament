CREATE OR REPLACE FUNCTION fn_search_medicine (
    p_keyword IN VARCHAR2
) RETURN SYS_REFCURSOR AS
    v_cursor SYS_REFCURSOR;
BEGIN
    OPEN v_cursor FOR
        SELECT
            m.medicine_id,
            m.medicine_name,
            m.generic_name,
            m.strength,
            m.unit_price,
            NVL(SUM(b.quantity_in_stock), 0) AS available_stock
        FROM medicines m
        LEFT JOIN batches b ON b.medicine_id = m.medicine_id
        WHERE UPPER(m.medicine_name) LIKE '%' || UPPER(p_keyword) || '%'
           OR UPPER(m.generic_name) LIKE '%' || UPPER(p_keyword) || '%'
        GROUP BY m.medicine_id, m.medicine_name, m.generic_name, m.strength, m.unit_price;

    RETURN v_cursor;
END;
