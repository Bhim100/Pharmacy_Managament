from db import get_connection


# Sample dashboard data keeps the landing page alive before Oracle is connected.
SAMPLE_DASHBOARD_STATS = {
    "inventory_status": "Good",
    "monthly_revenue": 855875,
    "total_medicines": 298,
    "shortage_count": 1,
    "medicine_groups": 24,
    "medicines_sold": 70856,
    "invoices_generated": 5288,
    "total_suppliers": 4,
    "total_users": 5,
    "total_customers": 845,
    "frequently_bought_item": "Adalimumab",
}


def get_dashboard_stats():
    """Return dashboard cards and summary metrics from Oracle or sample data."""
    connection = get_connection()

    if connection is None:
        return SAMPLE_DASHBOARD_STATS

    with connection:
        with connection.cursor() as cursor:
            # These small aggregate queries keep the dashboard route easy to explain and debug.
            cursor.execute("SELECT COUNT(*) FROM medicines")
            total_medicines = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM customers")
            total_customers = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM medicines m
                LEFT JOIN batches b ON b.medicine_id = m.medicine_id
                GROUP BY m.medicine_id, m.reorder_level
                HAVING NVL(SUM(b.quantity_in_stock), 0) <= m.reorder_level
                """
            )
            shortage_rows = cursor.fetchall()
            shortage_count = len(shortage_rows)

            cursor.execute("SELECT COUNT(DISTINCT category_id) FROM medicines")
            medicine_groups = cursor.fetchone()[0]

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
                SELECT NVL(SUM(quantity_sold), 0)
                FROM bill_items bi
                JOIN bills b ON b.bill_id = bi.bill_id
                WHERE TO_CHAR(b.bill_date, 'YYYY-MM') = TO_CHAR(SYSDATE, 'YYYY-MM')
                """
            )
            medicines_sold = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM suppliers")
            total_suppliers = cursor.fetchone()[0]

            # A basic user count placeholder is used until a users table is added.
            total_users = 5

            cursor.execute(
                """
                SELECT medicine_name
                FROM (
                    SELECT m.medicine_name, SUM(bi.quantity_sold) AS total_sold
                    FROM bill_items bi
                    JOIN medicines m ON m.medicine_id = bi.medicine_id
                    GROUP BY m.medicine_name
                    ORDER BY total_sold DESC
                )
                WHERE ROWNUM = 1
                """
            )
            top_item = cursor.fetchone()

            return {
                "inventory_status": "Good" if shortage_count == 0 else "Attention",
                "monthly_revenue": monthly_revenue,
                "total_medicines": total_medicines,
                "shortage_count": shortage_count,
                "medicine_groups": medicine_groups,
                "medicines_sold": medicines_sold,
                "invoices_generated": invoices_generated,
                "total_suppliers": total_suppliers,
                "total_users": total_users,
                "total_customers": total_customers,
                "frequently_bought_item": top_item[0] if top_item else "-",
            }
