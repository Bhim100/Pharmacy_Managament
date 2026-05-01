from db import get_connection


# Sample report data keeps the reports page usable until Oracle is connected.
SAMPLE_REPORTS = {
    "sales": {
        "monthly_revenue": 855875,
        "invoices_generated": 5288,
        "top_selling": [
            {"medicine_name": "Paracure", "units_sold": 1820, "revenue": 54600},
            {"medicine_name": "Amoxycillin", "units_sold": 940, "revenue": 79900},
            {"medicine_name": "VitaPlus", "units_sold": 615, "revenue": 73800},
        ],
        "sales_by_category": [
            {"category_name": "Painkillers", "revenue": 54600, "percent": 26.2},
            {"category_name": "Antibiotics", "revenue": 79900, "percent": 38.3},
            {"category_name": "Vitamins", "revenue": 73800, "percent": 35.5},
        ]
    },
    "inventory": {
        "low_stock": [
            {"medicine_name": "Amoxycillin", "stock": 8},
            {"medicine_name": "VitaPlus", "stock": 6},
        ],
        "expiring_soon": [
            {"batch_no": "PAR650-B4", "medicine_name": "Paracure", "days_left": 20},
            {"batch_no": "AMX500-A1", "medicine_name": "Amoxycillin", "days_left": 9},
        ],
    },
    "customers": {
        "top_customers": [
            {"customer_name": "Sneha Kapoor", "visits": 12, "spent": 8450},
            {"customer_name": "Aman Verma", "visits": 8, "spent": 4290},
            {"customer_name": "Rahul Singh", "visits": 5, "spent": 1980},
        ],
    },
}


def get_reports_summary():
    """Return grouped report data for sales, inventory, and customer reporting."""
    connection = get_connection()

    if connection is None:
        return SAMPLE_REPORTS

    with connection:
        with connection.cursor() as cursor:
            # Sales metrics are grouped together so the reports page can render one section at a time.
            cursor.execute(
                """
                SELECT NVL(SUM(net_amount), 0), COUNT(*)
                FROM bills
                WHERE TO_CHAR(bill_date, 'YYYY-MM') = TO_CHAR(SYSDATE, 'YYYY-MM')
                """
            )
            monthly_revenue, invoices_generated = cursor.fetchone()

            cursor.execute(
                """
                SELECT m.medicine_name, SUM(bi.quantity_sold) AS units_sold, SUM(bi.line_total) AS revenue
                FROM bill_items bi
                JOIN medicines m ON m.medicine_id = bi.medicine_id
                GROUP BY m.medicine_name
                ORDER BY units_sold DESC
                FETCH FIRST 5 ROWS ONLY
                """
            )
            top_selling = [
                {"medicine_name": row[0], "units_sold": row[1], "revenue": row[2]}
                for row in cursor.fetchall()
            ]

            cursor.execute(
                """
                SELECT 
                    c.category_name, 
                    SUM(bi.line_total) AS category_revenue,
                    ROUND(SUM(bi.line_total) / (SELECT SUM(line_total) FROM bill_items WHERE line_total > 0) * 100, 2) AS percent_of_total
                FROM bill_items bi
                JOIN medicines m ON bi.medicine_id = m.medicine_id
                JOIN categories c ON m.category_id = c.category_id
                GROUP BY c.category_name
                ORDER BY category_revenue DESC
                """
            )
            sales_by_category = [
                {"category_name": row[0], "revenue": row[1] or 0, "percent": row[2] or 0}
                for row in cursor.fetchall()
            ]

            # Inventory reporting highlights low-stock and expiring batches.
            cursor.execute(
                """
                SELECT m.medicine_name, NVL(SUM(b.quantity_in_stock), 0) AS stock
                FROM medicines m
                LEFT JOIN batches b ON b.medicine_id = m.medicine_id
                GROUP BY m.medicine_name, m.reorder_level
                HAVING NVL(SUM(b.quantity_in_stock), 0) <= m.reorder_level
                ORDER BY stock, m.medicine_name
                FETCH FIRST 5 ROWS ONLY
                """
            )
            low_stock = [
                {"medicine_name": row[0], "stock": row[1]}
                for row in cursor.fetchall()
            ]

            cursor.execute(
                """
                SELECT b.batch_no, m.medicine_name, TRUNC(b.expiry_date) - TRUNC(SYSDATE) AS days_left
                FROM batches b
                JOIN medicines m ON m.medicine_id = b.medicine_id
                WHERE b.expiry_date BETWEEN TRUNC(SYSDATE) AND TRUNC(SYSDATE) + 30
                  AND b.quantity_in_stock > 0
                ORDER BY b.expiry_date
                FETCH FIRST 5 ROWS ONLY
                """
            )
            expiring_soon = [
                {"batch_no": row[0], "medicine_name": row[1], "days_left": int(row[2])}
                for row in cursor.fetchall()
            ]

            # Customer reporting focuses on repeat buyers and spending patterns.
            cursor.execute(
                """
                SELECT c.customer_name, COUNT(b.bill_id) AS visits, NVL(SUM(b.net_amount), 0) AS spent
                FROM customers c
                JOIN bills b ON b.customer_id = c.customer_id
                GROUP BY c.customer_name
                ORDER BY spent DESC
                FETCH FIRST 5 ROWS ONLY
                """
            )
            top_customers = [
                {"customer_name": row[0], "visits": row[1], "spent": row[2]}
                for row in cursor.fetchall()
            ]

            return {
                "sales": {
                    "monthly_revenue": monthly_revenue,
                    "invoices_generated": invoices_generated,
                    "top_selling": top_selling,
                    "sales_by_category": sales_by_category,
                },
                "inventory": {
                    "low_stock": low_stock,
                    "expiring_soon": expiring_soon,
                },
                "customers": {
                    "top_customers": top_customers,
                },
            }

def get_sales_report_for_export():
    """Fetch all sales data for CSV export."""
    connection = get_connection()
    if not connection:
        return []
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT b.bill_id, c.customer_name, b.bill_date, b.total_amount, b.tax_amount, b.net_amount
                FROM bills b
                JOIN customers c ON b.customer_id = c.customer_id
                ORDER BY b.bill_date DESC
                """
            )
            return [
                {
                    "Bill ID": row[0],
                    "Customer": row[1],
                    "Date": row[2].strftime('%Y-%m-%d %H:%M'),
                    "Total": row[3],
                    "Tax": row[4],
                    "Net Amount": row[5]
                } for row in cursor.fetchall()
            ]

def get_customer_report_for_export():
    """Fetch all customer data for CSV export."""
    connection = get_connection()
    if not connection:
        return []
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT customer_name, phone, loyalty_points, created_at
                FROM customers
                ORDER BY loyalty_points DESC
                """
            )
            return [
                {
                    "Name": row[0],
                    "Phone": row[1] or "N/A",
                    "Loyalty Points": row[2],
                    "Joined Date": row[3].strftime('%Y-%m-%d')
                } for row in cursor.fetchall()
            ]
