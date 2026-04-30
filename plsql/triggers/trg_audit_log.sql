CREATE OR REPLACE TRIGGER trg_audit_log
AFTER UPDATE OF quantity_in_stock ON batches
FOR EACH ROW
BEGIN
    IF :OLD.quantity_in_stock <> :NEW.quantity_in_stock THEN
        INSERT INTO stock_audit (
            audit_id, batch_id, old_quantity, new_quantity, action_type, action_timestamp, remarks
        ) VALUES (
            seq_stock_audit.NEXTVAL,
            :NEW.batch_id,
            :OLD.quantity_in_stock,
            :NEW.quantity_in_stock,
            'STOCK_UPDATE',
            SYSDATE,
            'Quantity modified in batch'
        );
    END IF;
END;
