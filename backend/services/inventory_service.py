from db import get_connection


# Sample inventory data keeps the page working before Oracle data is plugged in.
SAMPLE_INVENTORY_SUMMARY = {
    "low_stock": [
        {"medicine_name": "Amoxycillin 500mg", "stock": 8},
        {"medicine_name": "VitaPlus Tablets", "stock": 6},
        {"medicine_name": "Cough Syrup C12", "stock": 4},
    ],
    "expiring_soon": [
        {"batch_no": "PAR650-B4", "medicine_name": "Paracure 650mg", "days_left": 20},
        {"batch_no": "VIT-25-C2", "medicine_name": "VitaPlus", "days_left": 15},
        {"batch_no": "AMX500-A1", "medicine_name": "Amoxycillin", "days_left": 9},
    ],
}


def get_inventory_summary():
    """Return low-stock and expiring-soon data from Oracle or sample data."""
    connection = get_connection()

    if connection is None:
        return SAMPLE_INVENTORY_SUMMARY

    with connection:
        with connection.cursor() as cursor:
            # This query groups stock per medicine so the UI can highlight reorder risk.
            cursor.execute(
                """
                SELECT
                    m.medicine_name,
                    NVL(SUM(b.quantity_in_stock), 0) AS stock
                FROM medicines m
                LEFT JOIN batches b ON b.medicine_id = m.medicine_id
                GROUP BY m.medicine_name, m.reorder_level
                HAVING NVL(SUM(b.quantity_in_stock), 0) <= m.reorder_level
                ORDER BY stock, m.medicine_name
                """
            )
            low_stock = [
                {"medicine_name": row[0], "stock": row[1]}
                for row in cursor.fetchall()
            ]

            # This query focuses on batches close to expiry because pharmacies are batch-sensitive.
            cursor.execute(
                """
                SELECT
                    b.batch_no,
                    m.medicine_name,
                    TRUNC(b.expiry_date) - TRUNC(SYSDATE) AS days_left
                FROM batches b
                JOIN medicines m ON m.medicine_id = b.medicine_id
                WHERE b.expiry_date BETWEEN TRUNC(SYSDATE) AND TRUNC(SYSDATE) + 30
                  AND b.quantity_in_stock > 0
                ORDER BY b.expiry_date
                """
            )
            expiring_soon = [
                {"batch_no": row[0], "medicine_name": row[1], "days_left": int(row[2])}
                for row in cursor.fetchall()
            ]

            return {
                "low_stock": low_stock,
                "expiring_soon": expiring_soon,
            }
