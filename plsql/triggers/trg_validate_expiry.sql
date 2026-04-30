CREATE OR REPLACE TRIGGER trg_validate_expiry
BEFORE INSERT OR UPDATE ON bill_items
FOR EACH ROW
DECLARE
    v_expiry_date DATE;
    v_stock NUMBER;
BEGIN
    SELECT expiry_date, quantity_in_stock
    INTO v_expiry_date, v_stock
    FROM batches
    WHERE batch_id = :NEW.batch_id;

    IF v_expiry_date < TRUNC(SYSDATE) THEN
        RAISE_APPLICATION_ERROR(-20001, 'Expired batch cannot be sold.');
    END IF;

    IF :NEW.quantity_sold > v_stock THEN
        RAISE_APPLICATION_ERROR(-20002, 'Insufficient stock in selected batch.');
    END IF;
END;
