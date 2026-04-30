-- Report queries

-- 1. Current inventory summary
SELECT * FROM vw_inventory_status ORDER BY medicine_name;

-- 2. Medicines expiring within next 30 days
SELECT * FROM vw_expiring_soon ORDER BY expiry_date;

-- 3. Customer purchase history
SELECT * FROM vw_customer_purchase_history WHERE customer_id = 2001 ORDER BY bill_date DESC;

-- 4. Daily sales report
SELECT * FROM vw_daily_sales_summary ORDER BY sales_date DESC;

-- 5. Top-selling medicines
SELECT
    m.medicine_name,
    SUM(bi.quantity_sold) AS total_units_sold,
    SUM(bi.line_total) AS revenue
FROM bill_items bi
JOIN medicines m ON m.medicine_id = bi.medicine_id
GROUP BY m.medicine_name
ORDER BY total_units_sold DESC;
