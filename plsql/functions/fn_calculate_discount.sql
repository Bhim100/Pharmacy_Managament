CREATE OR REPLACE FUNCTION fn_calculate_discount (
    p_customer_id IN NUMBER,
    p_gross_amount IN NUMBER
) RETURN NUMBER AS
    v_points NUMBER;
BEGIN
    SELECT NVL(loyalty_points, 0)
    INTO v_points
    FROM customers
    WHERE customer_id = p_customer_id;

    IF p_gross_amount >= 2000 THEN
        RETURN ROUND(p_gross_amount * 0.10, 2);
    ELSIF v_points >= 100 THEN
        RETURN ROUND(p_gross_amount * 0.05, 2);
    ELSE
        RETURN 0;
    END IF;
END;
