CREATE OR REPLACE PROCEDURE proc_generate_bill (
    p_bill_id         IN NUMBER,
    p_customer_id     IN NUMBER,
    p_prescription_id IN NUMBER DEFAULT NULL,
    p_payment_mode    IN VARCHAR2 DEFAULT 'CASH'
) AS
    v_discount NUMBER(12,2);
    v_gross    NUMBER(12,2);
    v_tax      NUMBER(12,2);
    v_net      NUMBER(12,2);
BEGIN
    INSERT INTO bills (
        bill_id, customer_id, prescription_id, bill_date, payment_mode,
        gross_amount, discount_amount, tax_amount, net_amount, bill_status
    ) VALUES (
        p_bill_id, p_customer_id, p_prescription_id, SYSDATE, p_payment_mode,
        0, 0, 0, 0, 'PAID'
    );

    v_gross := fn_calculate_total(p_bill_id);
    v_discount := fn_calculate_discount(p_customer_id, v_gross);
    v_tax := ROUND((v_gross - v_discount) * 0.05, 2);
    v_net := v_gross - v_discount + v_tax;

    UPDATE bills
    SET gross_amount = v_gross,
        discount_amount = v_discount,
        tax_amount = v_tax,
        net_amount = v_net
    WHERE bill_id = p_bill_id;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
