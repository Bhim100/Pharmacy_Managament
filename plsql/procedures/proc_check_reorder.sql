CREATE OR REPLACE PROCEDURE proc_check_reorder AS
BEGIN
    INSERT INTO reorder_alerts (
        alert_id, medicine_id, alert_date, current_stock, reorder_level, alert_status
    )
    SELECT
        seq_reorder_alert.NEXTVAL,
        m.medicine_id,
        SYSDATE,
        NVL(SUM(b.quantity_in_stock), 0),
        m.reorder_level,
        'OPEN'
    FROM medicines m
    LEFT JOIN batches b ON b.medicine_id = m.medicine_id
    GROUP BY m.medicine_id, m.reorder_level
    HAVING NVL(SUM(b.quantity_in_stock), 0) <= m.reorder_level
       AND NOT EXISTS (
           SELECT 1
           FROM reorder_alerts r
           WHERE r.medicine_id = m.medicine_id
             AND r.alert_status = 'OPEN'
       );

    COMMIT;
END;
