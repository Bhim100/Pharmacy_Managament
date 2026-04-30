CREATE OR REPLACE PROCEDURE proc_add_batch (
    p_medicine_id         IN NUMBER,
    p_batch_no            IN VARCHAR2,
    p_manufacturing_date  IN DATE,
    p_expiry_date         IN DATE,
    p_purchase_price      IN NUMBER,
    p_selling_price       IN NUMBER,
    p_quantity            IN NUMBER,
    p_rack_location       IN VARCHAR2
) AS
BEGIN
    INSERT INTO batches (
        batch_id, medicine_id, batch_no, manufacturing_date, expiry_date,
        purchase_price, selling_price, quantity_in_stock, received_date, rack_location
    ) VALUES (
        seq_batch.NEXTVAL, p_medicine_id, p_batch_no, p_manufacturing_date, p_expiry_date,
        p_purchase_price, p_selling_price, p_quantity, SYSDATE, p_rack_location
    );

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
