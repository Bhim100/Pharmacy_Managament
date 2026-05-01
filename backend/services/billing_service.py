import json
from db import get_connection

def get_billing_options():
    """Fetch medicines and their available batches for the billing dropdowns."""
    connection = get_connection()
    if not connection:
        return []

    with connection:
        with connection.cursor() as cursor:
            # We only want batches that are in stock and not expired
            cursor.execute(
                """
                SELECT m.medicine_name, b.batch_no, b.selling_price 
                FROM medicines m
                JOIN batches b ON m.medicine_id = b.medicine_id
                WHERE b.quantity_in_stock > 0
                  AND b.expiry_date >= TRUNC(SYSDATE)
                ORDER BY m.medicine_name, b.expiry_date ASC
                """
            )
            rows = cursor.fetchall()

    # Format the data for the frontend
    medicine_dict = {}
    for med_name, batch_no, price in rows:
        if med_name not in medicine_dict:
            medicine_dict[med_name] = []
        medicine_dict[med_name].append({"batch_no": batch_no, "price": float(price)})

    options = [{"name": name, "batches": batches} for name, batches in medicine_dict.items()]
    return options

def create_bill(customer_mode, customer_data, items):
    """
    Creates a bill, inserting into bills, bill_items, and updating batch quantities.
    Uses transaction management to ensure consistency.
    """
    connection = get_connection()
    if not connection:
        return {"success": False, "message": "Database not connected"}

    try:
        with connection:
            with connection.cursor() as cursor:
                # 1. Handle Customer
                customer_id = None
                if customer_mode == 'existing':
                    customer_id = customer_data.get('customer_id')
                    if not customer_id:
                        raise ValueError("Customer ID is required for existing customers")
                else:
                    # Insert new customer
                    new_id_var = cursor.var(int)
                    cursor.execute(
                        """
                        INSERT INTO customers (customer_id, customer_name, phone) 
                        VALUES (seq_customer.NEXTVAL, :1, :2)
                        RETURNING customer_id INTO :3
                        """,
                        [customer_data.get('customer_name', 'Walk-in'), customer_data.get('customer_phone'), new_id_var]
                    )
                    customer_id = new_id_var.getvalue()[0]

                # 2. Process items and calculate totals
                gross_amount = 0
                processed_items = []

                for item in items:
                    med_name = item.get('medicine_name')
                    batch_no = item.get('batch_no')
                    qty = int(item.get('quantity', 0))

                    if qty <= 0:
                        continue

                    # Get batch and medicine details
                    cursor.execute(
                        """
                        SELECT b.batch_id, b.medicine_id, b.selling_price, b.quantity_in_stock, b.expiry_date
                        FROM batches b
                        JOIN medicines m ON b.medicine_id = m.medicine_id
                        WHERE m.medicine_name = :med_name AND b.batch_no = :batch_no
                        """,
                        med_name=med_name, batch_no=batch_no
                    )
                    batch_row = cursor.fetchone()
                    
                    if not batch_row:
                        raise ValueError(f"Batch {batch_no} for {med_name} not found.")

                    batch_id, medicine_id, selling_price, stock, expiry_date = batch_row

                    if stock < qty:
                        raise ValueError(f"Insufficient stock for {med_name} (Batch {batch_no}). Available: {stock}")
                        
                    import datetime
                    if expiry_date.date() < datetime.date.today():
                        raise ValueError(f"Cannot sell expired medicine: {med_name} (Batch {batch_no}).")

                    line_total = qty * selling_price
                    gross_amount += line_total

                    processed_items.append({
                        "batch_id": batch_id,
                        "medicine_id": medicine_id,
                        "qty": qty,
                        "unit_price": selling_price,
                        "line_total": line_total
                    })

                if not processed_items:
                    raise ValueError("No valid items in the bill.")

                # Simple discount logic for demo (e.g. 0 discount)
                discount_amount = 0
                tax_amount = gross_amount * 0.05 # 5% flat tax for example
                net_amount = gross_amount - discount_amount + tax_amount

                # 3. Create Bill Record
                # Using sequences for bill_id
                bill_id_var = cursor.var(int)
                cursor.execute(
                    """
                    INSERT INTO bills (bill_id, customer_id, gross_amount, discount_amount, tax_amount, net_amount, bill_status)
                    VALUES (seq_bill.NEXTVAL, :1, :2, :3, :4, :5, 'PAID')
                    RETURNING bill_id INTO :6
                    """,
                    [customer_id, gross_amount, discount_amount, tax_amount, net_amount, bill_id_var]
                )
                bill_id = bill_id_var.getvalue()[0]

                # 4. Insert Bill Items & Deduct Stock
                for p_item in processed_items:
                    # Insert Bill Item
                    cursor.execute(
                        """
                        INSERT INTO bill_items (bill_item_id, bill_id, batch_id, medicine_id, quantity_sold, unit_price, line_total)
                        VALUES (seq_bill_item.NEXTVAL, :bill_id, :batch_id, :med_id, :qty, :price, :total)
                        """,
                        bill_id=bill_id, 
                        batch_id=p_item['batch_id'], 
                        med_id=p_item['medicine_id'], 
                        qty=p_item['qty'], 
                        price=p_item['unit_price'], 
                        total=p_item['line_total']
                    )

                    # Deduct Stock
                    cursor.execute(
                        """
                        UPDATE batches 
                        SET quantity_in_stock = quantity_in_stock - :qty 
                        WHERE batch_id = :batch_id
                        """,
                        qty=p_item['qty'],
                        batch_id=p_item['batch_id']
                    )

                # 5. Add Loyalty Points to Customer
                # For example, 1 point for every 10 Rupees spent
                points_earned = int(net_amount // 10)
                if points_earned > 0:
                    cursor.execute(
                        """
                        UPDATE customers
                        SET loyalty_points = NVL(loyalty_points, 0) + :points
                        WHERE customer_id = :customer_id
                        """,
                        points=points_earned,
                        customer_id=customer_id
                    )

            # Explicit commit is required for oracledb
            connection.commit()
            return {"success": True, "bill_id": bill_id, "message": "Bill created successfully"}

    except Exception as e:
        # Transaction is automatically rolled back on exception
        return {"success": False, "message": str(e)}
