CREATE OR REPLACE PROCEDURE proc_dispose_expired AS
BEGIN
    SAVEPOINT before_disposal;

    INSERT INTO expired_medicine_log (
        log_id, batch_id, medicine_id, expiry_date, quantity_disposed, disposed_on, remarks
    )
    SELECT
        seq_expired_log.NEXTVAL,
        batch_id,
        medicine_id,
        expiry_date,
        quantity_in_stock,
        SYSDATE,
        'Auto disposal of expired batch'
    FROM batches
    WHERE expiry_date < TRUNC(SYSDATE)
      AND quantity_in_stock > 0;

    UPDATE batches
    SET quantity_in_stock = 0
    WHERE expiry_date < TRUNC(SYSDATE)
      AND quantity_in_stock > 0;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK TO before_disposal;
        RAISE;
END;
