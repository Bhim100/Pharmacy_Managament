from db import get_connection


# Sample data keeps the page usable until Oracle is wired in fully.
SAMPLE_CUSTOMERS = [
    {
        "customer_id": "C-2001",
        "name": "Aman Verma",
        "phone": "9012345678",
        "loyalty_points": 48,
        "last_purchase": "23 Apr 2026",
        "status": "Active",
    },
    {
        "customer_id": "C-2002",
        "name": "Sneha Kapoor",
        "phone": "9123456780",
        "loyalty_points": 112,
        "last_purchase": "22 Apr 2026",
        "status": "Premium",
    },
    {
        "customer_id": "C-2003",
        "name": "Rahul Singh",
        "phone": "9345678910",
        "loyalty_points": 16,
        "last_purchase": "20 Apr 2026",
        "status": "Regular",
    },
]

SAMPLE_CUSTOMER_HISTORY = {
    "C-2001": [
        {"bill_id": 9001, "bill_date": "23 Apr 2026", "items": "Paracure, VitaPlus", "amount": 150},
        {"bill_id": 8988, "bill_date": "10 Apr 2026", "items": "Amoxycillin", "amount": 85},
    ],
    "C-2002": [
        {"bill_id": 9004, "bill_date": "22 Apr 2026", "items": "VitaPlus", "amount": 120},
    ],
    "C-2003": [
        {"bill_id": 8990, "bill_date": "20 Apr 2026", "items": "Paracure", "amount": 60},
    ],
}


def fetch_customers():
    """Fetch customer rows from Oracle, or fall back to sample data."""
    connection = get_connection()

    if connection is None:
        return SAMPLE_CUSTOMERS

    with connection:
        with connection.cursor() as cursor:
            # This query is kept simple first so it is easy to test and explain.
            cursor.execute(
                """
                SELECT
                    customer_id,
                    customer_name,
                    phone,
                    NVL(loyalty_points, 0) AS loyalty_points,
                    TO_CHAR(created_at, 'DD Mon YYYY') AS last_purchase
                FROM customers
                ORDER BY customer_id
                """
            )

            customers = []
            for row in cursor:
                customers.append(
                    {
                        "customer_id": row[0],
                        "name": row[1],
                        "phone": row[2] or "-",
                        "loyalty_points": row[3],
                        "last_purchase": row[4] or "-",
                        "status": _customer_status(row[3]),
                    }
                )

            return customers


def search_customers(query):
    """Search customers for the global top-bar search."""
    clean_query = (query or "").strip().lower()
    connection = get_connection()

    if connection is None:
        return _search_sample_customers(clean_query)

    with connection:
        with connection.cursor() as cursor:
            # The global search checks both customer name and phone for quick lookup.
            cursor.execute(
                """
                SELECT
                    customer_id,
                    customer_name,
                    NVL(phone, '-') AS phone,
                    NVL(loyalty_points, 0) AS loyalty_points,
                    TO_CHAR(created_at, 'DD Mon YYYY') AS last_purchase
                FROM customers
                WHERE :search_text IS NULL
                   OR LOWER(customer_name) LIKE '%' || :search_text || '%'
                   OR LOWER(NVL(phone, '')) LIKE '%' || :search_text || '%'
                ORDER BY customer_name
                """,
                search_text=clean_query or None,
            )

            results = []
            for row in cursor:
                results.append(
                    {
                        "customer_id": row[0],
                        "name": row[1],
                        "phone": row[2],
                        "loyalty_points": row[3],
                        "last_purchase": row[4] or "-",
                        "status": _customer_status(row[3]),
                    }
                )

            return results


def fetch_customer_purchase_history(customer_id):
    """Fetch bill history for one customer so the UI can show past purchases."""
    connection = get_connection()

    if connection is None:
        return SAMPLE_CUSTOMER_HISTORY.get(str(customer_id), [])

    with connection:
        with connection.cursor() as cursor:
            # LISTAGG keeps multiple bill items readable in a single history row.
            cursor.execute(
                """
                SELECT
                    b.bill_id,
                    TO_CHAR(b.bill_date, 'DD Mon YYYY') AS bill_date,
                    LISTAGG(m.medicine_name, ', ') WITHIN GROUP (ORDER BY m.medicine_name) AS items,
                    b.net_amount
                FROM bills b
                JOIN bill_items bi ON bi.bill_id = b.bill_id
                JOIN medicines m ON m.medicine_id = bi.medicine_id
                WHERE b.customer_id = :customer_id
                GROUP BY b.bill_id, b.bill_date, b.net_amount
                ORDER BY b.bill_date DESC
                """,
                customer_id=customer_id,
            )

            return [
                {"bill_id": row[0], "bill_date": row[1], "items": row[2], "amount": row[3]}
                for row in cursor.fetchall()
            ]


def _search_sample_customers(query):
    """Mirror the real customer search until Oracle is connected."""
    if not query:
        return SAMPLE_CUSTOMERS

    return [
        customer
        for customer in SAMPLE_CUSTOMERS
        if query in customer["name"].lower() or query in customer["phone"].lower()
    ]


def _customer_status(loyalty_points):
    """Map loyalty points to a simple UI status badge."""
    if loyalty_points >= 100:
        return "Premium"
    if loyalty_points > 0:
        return "Active"
    return "Regular"
