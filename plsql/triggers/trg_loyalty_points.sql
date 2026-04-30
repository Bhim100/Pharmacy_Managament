CREATE OR REPLACE TRIGGER trg_loyalty_points
AFTER INSERT ON bills
FOR EACH ROW
BEGIN
    IF :NEW.customer_id IS NOT NULL AND :NEW.net_amount > 0 THEN
        UPDATE customers
        SET loyalty_points = NVL(loyalty_points, 0) + FLOOR(:NEW.net_amount / 100)
        WHERE customer_id = :NEW.customer_id;
    END IF;
END;
