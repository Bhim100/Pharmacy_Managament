-- Advanced SQL queries

-- 1. Running monthly sales using analytic function
SELECT
    TRUNC(bill_date, 'MM') AS sales_month,
    SUM(net_amount) AS monthly_sales,
    SUM(SUM(net_amount)) OVER (ORDER BY TRUNC(bill_date, 'MM')) AS running_total
FROM bills
WHERE bill_status = 'PAID'
GROUP BY TRUNC(bill_date, 'MM')
ORDER BY sales_month;

-- 2. Rank medicines by revenue
SELECT
    m.medicine_name,
    SUM(bi.line_total) AS revenue,
    RANK() OVER (ORDER BY SUM(bi.line_total) DESC) AS revenue_rank
FROM bill_items bi
JOIN medicines m ON m.medicine_id = bi.medicine_id
GROUP BY m.medicine_name;

-- 3. Find slow-moving stock
SELECT
    m.medicine_name,
    NVL(SUM(b.quantity_in_stock), 0) AS available_stock,
    NVL(SUM(bi.quantity_sold), 0) AS sold_quantity
FROM medicines m
LEFT JOIN batches b ON b.medicine_id = m.medicine_id
LEFT JOIN bill_items bi ON bi.medicine_id = m.medicine_id
GROUP BY m.medicine_name
HAVING NVL(SUM(bi.quantity_sold), 0) < 10;

-- 4. Most loyal customers
SELECT
    c.customer_name,
    COUNT(bl.bill_id) AS total_visits,
    SUM(bl.net_amount) AS lifetime_value,
    DENSE_RANK() OVER (ORDER BY SUM(bl.net_amount) DESC) AS customer_rank
FROM customers c
JOIN bills bl ON bl.customer_id = c.customer_id
GROUP BY c.customer_name;
