from db import get_connection
import settings_store


# Sample inventory data keeps the page working before Oracle data is plugged in.
SAMPLE_INVENTORY_SUMMARY = {
    "low_stock": [
        {"medicine_name": "Amoxycillin 500mg", "stock": 8, "supplier_name": "PharmaCorp", "supplier_phone": "1234567890"},
        {"medicine_name": "VitaPlus Tablets", "stock": 6, "supplier_name": "HealthMed", "supplier_phone": "0987654321"},
        {"medicine_name": "Cough Syrup C12", "stock": 4, "supplier_name": "Unknown", "supplier_phone": "N/A"},
    ],
    "expiring_soon": [
        {"batch_no": "OLD-B1", "medicine_name": "Aspirin 100mg", "days_left": -5},
        {"batch_no": "PAR650-B4", "medicine_name": "Paracure 650mg", "days_left": 20},
        {"batch_no": "VIT-25-C2", "medicine_name": "VitaPlus", "days_left": 15},
        {"batch_no": "AMX500-A1", "medicine_name": "Amoxycillin", "days_left": 9},
    ],
    "all_stock": [
        {"medicine_name": "Paracure 650mg", "batch_no": "PAR650-B4", "stock": 50},
        {"medicine_name": "Amoxycillin 500mg", "batch_no": "AMX500-A1", "stock": 8},
        {"medicine_name": "VitaPlus Tablets", "batch_no": "VIT-25-C2", "stock": 6},
        {"medicine_name": "Cough Syrup C12", "batch_no": "SYR-C12-01", "stock": 4},
    ],
}


def get_inventory_summary():
    """Return low-stock and expiring-soon data from Oracle or sample data."""
    connection = get_connection()

    if connection is None:
        return SAMPLE_INVENTORY_SUMMARY

    with connection:
        with connection.cursor() as cursor:
            # This query groups stock per medicine and joins suppliers so the UI can highlight reorder risk and who to contact.
            cursor.execute(
                """
                SELECT
                    m.medicine_name,
                    NVL(SUM(b.quantity_in_stock), 0) AS stock,
                    s.supplier_name,
                    s.phone
                FROM medicines m
                LEFT JOIN batches b ON b.medicine_id = m.medicine_id
                LEFT JOIN suppliers s ON m.supplier_id = s.supplier_id
                GROUP BY m.medicine_name, m.reorder_level, s.supplier_name, s.phone
                HAVING NVL(SUM(b.quantity_in_stock), 0) <= :thresh
                ORDER BY stock, m.medicine_name
                """,
                thresh=settings_store.APP_SETTINGS["low_stock_threshold"],
            )
            low_stock = [
                {"medicine_name": row[0], "stock": row[1], "supplier_name": row[2] or 'Unknown', "supplier_phone": row[3] or 'N/A'}
                for row in cursor.fetchall()
            ]

            # This query focuses on batches close to expiry or already expired.
            cursor.execute(
                """
                SELECT
                    b.batch_no,
                    m.medicine_name,
                    TRUNC(b.expiry_date) - TRUNC(SYSDATE) AS days_left
                FROM batches b
                JOIN medicines m ON m.medicine_id = b.medicine_id
                WHERE b.expiry_date <= TRUNC(SYSDATE) + :days
                  AND b.quantity_in_stock > 0
                ORDER BY b.expiry_date
                """,
                days=settings_store.APP_SETTINGS["expiry_alert_days"],
            )
            expiring_soon = [
                {"batch_no": row[0], "medicine_name": row[1], "days_left": int(row[2])}
                for row in cursor.fetchall()
            ]

            # Query all batches and their stock for the user to see the complete picture
            cursor.execute(
                """
                SELECT
                    m.medicine_name,
                    b.batch_no,
                    b.quantity_in_stock
                FROM batches b
                JOIN medicines m ON m.medicine_id = b.medicine_id
                WHERE b.quantity_in_stock >= 0
                ORDER BY m.medicine_name, b.batch_no
                """
            )
            all_stock = [
                {"medicine_name": row[0], "batch_no": row[1], "stock": row[2]}
                for row in cursor.fetchall()
            ]

            return {
                "low_stock": low_stock,
                "expiring_soon": expiring_soon,
                "all_stock": all_stock,
            }

def delete_batch(batch_no):
    """Delete a batch from the database by batch number."""
    connection = get_connection()
    if not connection:
        return
    with connection:
        with connection.cursor() as cursor:
            # First remove any bill_items referencing this batch to preserve FK integrity
            cursor.execute(
                "DELETE FROM bill_items WHERE batch_id = (SELECT batch_id FROM batches WHERE batch_no = :1)",
                [batch_no]
            )
            cursor.execute("DELETE FROM batches WHERE batch_no = :1", [batch_no])
            connection.commit()

def add_batch(data):
    """Insert a new stock batch into the Oracle database."""
    connection = get_connection()
    if not connection:
        print("Cannot add batch: No database connection")
        return

    with connection:
        with connection.cursor() as cursor:
            batch_no = data.get('batch_no')
            
            # Auto-generate batch_no if missing
            if not batch_no:
                import datetime
                cursor.execute("SELECT medicine_name FROM medicines WHERE medicine_id = :1", [data['medicine_id']])
                med_name_row = cursor.fetchone()
                med_prefix = med_name_row[0][:3].upper() if med_name_row else "MED"
                batch_no = f"{med_prefix}-{datetime.datetime.now().strftime('%y%m%d%H%M')}"

            cursor.execute(
                """
                INSERT INTO batches (
                    batch_id, medicine_id, batch_no, manufacturing_date, expiry_date, 
                    purchase_price, selling_price, quantity_in_stock, rack_location
                ) VALUES (
                    seq_batch.NEXTVAL, :medicine_id, :batch_no, 
                    TO_DATE(:manufacturing_date, 'YYYY-MM-DD'), 
                    TO_DATE(:expiry_date, 'YYYY-MM-DD'), 
                    :purchase_price, :selling_price, :quantity_in_stock, :rack_location
                )
                """,
                medicine_id=data['medicine_id'],
                batch_no=batch_no,
                manufacturing_date=data['manufacturing_date'],
                expiry_date=data['expiry_date'],
                purchase_price=data['purchase_price'],
                selling_price=data['selling_price'],
                quantity_in_stock=data['quantity_in_stock'],
                rack_location=data.get('rack_location')
            )
            connection.commit()

def get_all_inventory_for_export():
    """Fetch all inventory items for CSV export."""
    connection = get_connection()
    if not connection:
        return []
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    m.medicine_name, b.batch_no, b.quantity_in_stock, 
                    TO_CHAR(b.expiry_date, 'YYYY-MM-DD'), b.selling_price, 
                    s.supplier_name
                FROM batches b
                JOIN medicines m ON b.medicine_id = m.medicine_id
                LEFT JOIN suppliers s ON m.supplier_id = s.supplier_id
                ORDER BY m.medicine_name, b.expiry_date
                """
            )
            return [
                {
                    "Medicine": row[0],
                    "Batch No": row[1],
                    "Stock": row[2],
                    "Expiry": row[3],
                    "Price": row[4],
                    "Supplier": row[5] or "N/A"
                } for row in cursor.fetchall()
            ]
