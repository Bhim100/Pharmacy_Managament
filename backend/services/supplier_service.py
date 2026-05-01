from db import get_connection

def fetch_suppliers():
    connection = get_connection()
    if not connection:
        return [
            {"supplier_id": "S-1", "name": "PharmaCorp", "contact_person": "Rahul", "phone": "1234567890", "email": "rahul@pharmacorp.com", "address": "Delhi"},
        ]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    supplier_id, supplier_name, contact_person, phone, email, city
                FROM suppliers
                ORDER BY supplier_name
                """
            )
            return [
                {
                    "supplier_id": row[0],
                    "name": row[1],
                    "contact_person": row[2] or "-",
                    "phone": row[3] or "-",
                    "email": row[4] or "-",
                    "city": row[5] or "-"
                }
                for row in cursor.fetchall()
            ]

def add_supplier(data):
    """Insert a new supplier into the Oracle database."""
    connection = get_connection()
    if not connection:
        print("Cannot add supplier: No database connection")
        return False

    try:
        with connection:
            with connection.cursor() as cursor:
                # Fetch max ID to manually increment if no sequence exists, though sequence is better.
                # Assuming no sequence based on previous code, let's use NVL(MAX(supplier_id), 0) + 1
                cursor.execute("SELECT NVL(MAX(supplier_id), 0) + 1 FROM suppliers")
                new_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO suppliers (
                        supplier_id, supplier_name, contact_person, phone, email, city, supplier_status
                    ) VALUES (
                        :supplier_id, :supplier_name, :contact_person, :phone, :email, :city, 'ACTIVE'
                    )
                    """,
                    supplier_id=new_id,
                    supplier_name=data.get('supplier_name'),
                    contact_person=data.get('contact_person'),
                    phone=data.get('phone'),
                    email=data.get('email'),
                    city=data.get('city')
                )
                connection.commit()
                return True
    except Exception as e:
        print(f"Error adding supplier: {e}")
        return False
