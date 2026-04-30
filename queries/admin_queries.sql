-- Maintenance and admin queries

-- 1. Resolve duplicate open reorder alerts
SELECT medicine_id, COUNT(*)
FROM reorder_alerts
WHERE alert_status = 'OPEN'
GROUP BY medicine_id
HAVING COUNT(*) > 1;

-- 2. Check expired batches that still have stock
SELECT batch_id, medicine_id, batch_no, expiry_date, quantity_in_stock
FROM batches
WHERE expiry_date < TRUNC(SYSDATE)
  AND quantity_in_stock > 0;

-- 3. Check medicines without supplier mapping
SELECT medicine_id, medicine_name
FROM medicines
WHERE supplier_id IS NULL;

-- 4. Check bills with mismatch between gross and net
SELECT bill_id, gross_amount, discount_amount, tax_amount, net_amount
FROM bills
WHERE ROUND(gross_amount - discount_amount + tax_amount, 2) <> net_amount;
