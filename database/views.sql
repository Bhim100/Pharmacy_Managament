-- Useful views for reporting and frontend display

CREATE OR REPLACE VIEW vw_inventory_status AS
SELECT
    m.medicine_id,
    m.medicine_name,
    m.strength,
    c.category_name,
    SUM(b.quantity_in_stock) AS total_stock,
    MIN(b.expiry_date) AS nearest_expiry,
    m.reorder_level
FROM medicines m
JOIN categories c ON c.category_id = m.category_id
JOIN batches b ON b.medicine_id = m.medicine_id
GROUP BY m.medicine_id, m.medicine_name, m.strength, c.category_name, m.reorder_level;

CREATE OR REPLACE VIEW vw_expiring_soon AS
SELECT
    m.medicine_name,
    b.batch_no,
    b.expiry_date,
    b.quantity_in_stock
FROM medicines m
JOIN batches b ON b.medicine_id = m.medicine_id
WHERE b.expiry_date BETWEEN TRUNC(SYSDATE) AND TRUNC(SYSDATE) + 30
  AND b.quantity_in_stock > 0;

CREATE OR REPLACE VIEW vw_customer_purchase_history AS
SELECT
    c.customer_id,
    c.customer_name,
    bl.bill_id,
    bl.bill_date,
    m.medicine_name,
    bi.quantity_sold,
    bi.line_total
FROM customers c
JOIN bills bl ON bl.customer_id = c.customer_id
JOIN bill_items bi ON bi.bill_id = bl.bill_id
JOIN medicines m ON m.medicine_id = bi.medicine_id;

CREATE OR REPLACE VIEW vw_daily_sales_summary AS
SELECT
    TRUNC(bill_date) AS sales_date,
    COUNT(*) AS total_bills,
    SUM(net_amount) AS total_sales
FROM bills
WHERE bill_status = 'PAID'
GROUP BY TRUNC(bill_date);
