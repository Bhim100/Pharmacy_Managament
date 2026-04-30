CREATE OR REPLACE TRIGGER trg_update_stock
AFTER INSERT ON bill_items
FOR EACH ROW
BEGIN
    UPDATE batches
    SET quantity_in_stock = quantity_in_stock - :NEW.quantity_sold
    WHERE batch_id = :NEW.batch_id;

    INSERT INTO stock_audit (
        audit_id, batch_id, old_quantity, new_quantity, action_type, action_timestamp, remarks
    )
    SELECT
        seq_stock_audit.NEXTVAL,
        :NEW.batch_id,
        quantity_in_stock + :NEW.quantity_sold,
        quantity_in_stock,
        'SALE',
        SYSDATE,
        'Stock reduced after billing'
    FROM batches
    WHERE batch_id = :NEW.batch_id;
END;
