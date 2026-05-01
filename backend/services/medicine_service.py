from db import get_connection


# Sample data keeps search working before the Oracle link is finished.
SAMPLE_MEDICINES = [
    {
        "medicine_id": "M-1001",
        "name": "Amoxycillin",
        "generic_name": "Amoxicillin",
        "strength": "500mg",
        "stock": 100,
        "price": 85,
    },
    {
        "medicine_id": "M-1002",
        "name": "Paracure",
        "generic_name": "Paracetamol",
        "strength": "650mg",
        "stock": 250,
        "price": 30,
    },
    {
        "medicine_id": "M-1003",
        "name": "VitaPlus",
        "generic_name": "Multivitamin",
        "strength": "One Daily",
        "stock": 60,
        "price": 120,
    },
]


def search_medicines(query):
    """Search medicines from Oracle, or fall back to sample data."""
    clean_query = (query or "").strip().lower()
    connection = get_connection()

    if connection is None:
        return _search_sample_medicines(clean_query)

    with connection:
        with connection.cursor() as cursor:
            # Joining batches lets the search page show live stock from inventory.
            cursor.execute(
                """
                SELECT
                    m.medicine_id,
                    m.medicine_name,
                    NVL(m.generic_name, '-') AS generic_name,
                    NVL(c.category_name, '-') AS category_name,
                    NVL(s.supplier_name, '-') AS supplier_name,
                    NVL(SUM(b.quantity_in_stock), 0) AS stock,
                    NVL(m.unit_price, 0) AS unit_price
                FROM medicines m
                LEFT JOIN batches b ON b.medicine_id = m.medicine_id
                LEFT JOIN categories c ON m.category_id = c.category_id
                LEFT JOIN suppliers s ON m.supplier_id = s.supplier_id
                WHERE :search_text IS NULL
                   OR LOWER(m.medicine_name) LIKE '%' || :search_text || '%'
                   OR LOWER(NVL(m.generic_name, '')) LIKE '%' || :search_text || '%'
                   OR LOWER(NVL(c.category_name, '')) LIKE '%' || :search_text || '%'
                   OR LOWER(NVL(s.supplier_name, '')) LIKE '%' || :search_text || '%'
                   OR TO_CHAR(m.medicine_id) LIKE '%' || :search_text || '%'
                GROUP BY m.medicine_id, m.medicine_name, m.generic_name, c.category_name, s.supplier_name, m.unit_price
                ORDER BY m.medicine_name
                """,
                search_text=clean_query or None,
            )

            medicines = []
            for row in cursor:
                medicines.append(
                    {
                        "medicine_id": row[0],
                        "name": row[1],
                        "generic_name": row[2],
                        "category_name": row[3],
                        "supplier_name": row[4],
                        "stock": row[5],
                        "price": row[6],
                    }
                )

            return medicines


def _search_sample_medicines(query):
    """Mirror the real search behavior while Oracle is not connected yet."""
    if not query:
        return SAMPLE_MEDICINES

    return [
        medicine
        for medicine in SAMPLE_MEDICINES
        if query in medicine["name"].lower() or query in medicine["generic_name"].lower()
    ]
