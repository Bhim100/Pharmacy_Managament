from flask import Flask, render_template, request, redirect, url_for, flash, Response
import io, csv
from collections import Counter

from services.customer_service import fetch_customer_purchase_history, fetch_customers, search_customers
from services.dashboard_service import get_dashboard_stats
from services.inventory_service import get_inventory_summary, get_all_inventory_for_export, delete_batch
from services.medicine_service import search_medicines
from services.report_service import get_reports_summary, get_sales_report_for_export, get_customer_report_for_export
from services.billing_service import get_billing_options, create_bill

app = Flask(__name__)
app.secret_key = "super_secret_pharmacy_key"

# We'll fetch real billing options from the database instead of hardcoded sample options.


@app.route("/")
def home():
    # The dashboard reads one summary object so the template stays mostly presentation-only.
    dashboard_stats = get_dashboard_stats()
    import settings_store
    return render_template("index.html", stats=dashboard_stats, settings=settings_store.APP_SETTINGS)


@app.route("/customers")
def view_customers():
    # The route stays thin by delegating data access to the service layer.
    customers = fetch_customers()
    loyalty_members = sum(1 for customer in customers if customer["loyalty_points"] >= 100)
    most_loyal_customer = max(customers, key=lambda customer: customer["loyalty_points"], default=None)
    # This aggregates purchased medicine names from customer history for a quick page-level summary.
    purchased_items = []
    for customer in customers:
        history = fetch_customer_purchase_history(customer["customer_id"])
        for record in history:
            item_text = record.get("items", "")
            purchased_items.extend(
                item.strip()
                for item in item_text.split(",")
                if item.strip()
            )
    most_purchased_item = Counter(purchased_items).most_common(1)
    return render_template(
        "customers.html",
        customers=customers,
        loyalty_members=loyalty_members,
        most_loyal_customer=most_loyal_customer,
        most_purchased_item=most_purchased_item[0][0] if most_purchased_item else "-",
    )


@app.route("/customers/<customer_id>/history")
def customer_history(customer_id):
    # The history page combines the selected customer record with bill history rows.
    customers = fetch_customers()
    selected_customer = next((customer for customer in customers if str(customer["customer_id"]) == str(customer_id)), None)
    history = fetch_customer_purchase_history(customer_id)
    return render_template("customer_history.html", customer=selected_customer, history=history)


# The top navigation search should work across app modules, not only medicines.
@app.route("/search")
def global_search():
    query = request.args.get("q", "").strip()

    # Each service returns data for one module, which keeps the route simple.
    medicine_results = search_medicines(query)
    customer_results = search_customers(query)

    return render_template(
        "search_results.html",
        query=query,
        medicines=medicine_results,
        customers=customer_results,
    )


# These routes render the dashboard pages after moving them into Flask templates.
@app.route("/inventory")
def inventory_page():
    inventory_summary = get_inventory_summary()
    return render_template("inventory.html", inventory=inventory_summary)

@app.route("/inventory/batch/remove", methods=["POST"])
def remove_batch():
    batch_no = request.form.get("batch_no")
    if batch_no:
        delete_batch(batch_no)
        flash(f"Batch '{batch_no}' has been removed.", "success")
    return redirect(url_for("inventory_page"))


@app.route("/reports")
def reports_page():
    # The reports page receives three grouped report sections: sales, inventory, and customers.
    reports = get_reports_summary()
    return render_template("reports.html", reports=reports)


@app.route("/reports/inventory/download")
def download_inventory_report():
    data = get_all_inventory_for_export()
    
    if not data:
        flash("No inventory data found to export.", "error")
        return redirect(url_for('home'))

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=inventory_report.csv"
    return response

@app.route("/reports/sales/download")
def download_sales_report():
    data = get_sales_report_for_export()
    
    if not data:
        flash("No sales data found to export.", "error")
        return redirect(url_for('reports_page'))

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=sales_report.csv"
    return response

@app.route("/reports/customers/download")
def download_customer_report():
    data = get_customer_report_for_export()
    
    if not data:
        flash("No customer data found to export.", "error")
        return redirect(url_for('reports_page'))

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=customer_report.csv"
    return response

@app.route("/billing")
def billing_page():
    medicine_options = get_billing_options()
    return render_template("billing.html", medicine_options=medicine_options)

@app.route("/api/billing/checkout", methods=["POST"])
def checkout_bill():
    data = request.json
    customer_mode = data.get("customer_mode")
    customer_data = data.get("customer_data", {})
    items = data.get("items", [])
    
    result = create_bill(customer_mode, customer_data, items)
    if result["success"]:
        return {"success": True, "bill_id": result["bill_id"]}
    else:
        return {"success": False, "message": result.get("message", "Unknown error")}, 400


@app.route("/suppliers")
def suppliers_page():
    from services.supplier_service import fetch_suppliers
    suppliers = fetch_suppliers()
    return render_template("suppliers.html", suppliers=suppliers)

@app.route("/suppliers/new", methods=["GET", "POST"])
def add_supplier_page():
    if request.method == "POST":
        data = {
            "supplier_name": request.form.get("supplier_name"),
            "contact_person": request.form.get("contact_person"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "city": request.form.get("city")
        }
        from services.supplier_service import add_supplier
        if add_supplier(data):
            flash("Supplier successfully added!", "success")
        else:
            flash("Failed to add supplier.", "error")
        return redirect(url_for("suppliers_page"))
    return render_template("add_supplier.html")

@app.route("/settings", methods=["GET", "POST"])
def settings_page():
    import settings_store
    if request.method == "POST":
        action = request.form.get("action")
        if action == "reset":
            settings_store.APP_SETTINGS.update(settings_store.DEFAULTS)
            flash("Settings reset to defaults!", "success")
        else:
            try:
                settings_store.APP_SETTINGS["pharmacy_name"] = request.form.get("pharmacy_name", "Pharma One").strip() or "Pharma One"
                settings_store.APP_SETTINGS["admin_username"] = request.form.get("admin_username", "Subash").strip() or "Subash"
                settings_store.APP_SETTINGS["low_stock_threshold"] = int(request.form.get("low_stock_threshold", 10))
                settings_store.APP_SETTINGS["expiry_alert_days"] = int(request.form.get("expiry_alert_days", 30))
                flash("Settings saved successfully!", "success")
            except ValueError:
                flash("Please enter valid numbers for thresholds.", "error")
        return redirect(url_for("settings_page"))
    return render_template("settings.html", settings=settings_store.APP_SETTINGS)


@app.route("/medicines/search")
def search_medicine():
    # This route reads the search term from the URL and passes it to Oracle-ready logic.
    query = request.args.get("q", "")
    medicines = search_medicines(query)
    return render_template("search_medicine.html", medicines=medicines, query=query)

@app.route("/inventory/medicine/new", methods=["GET", "POST"])
def add_medicine_page():
    if request.method == "POST":
        data = {
            "category_id": request.form.get("category_id"),
            "supplier_id": request.form.get("supplier_id"),
            "medicine_name": request.form.get("medicine_name"),
            "generic_name": request.form.get("generic_name"),
            "dosage_form": request.form.get("dosage_form"),
            "strength": request.form.get("strength"),
            "unit_price": float(request.form.get("unit_price") or 0),
            "reorder_level": int(request.form.get("reorder_level") or 10),
            "requires_prescription": request.form.get("requires_prescription") or 'N',
            "gst_percent": float(request.form.get("gst_percent") or 0)
        }
        from services.inventory_service import add_medicine
        add_medicine(data)
        return redirect(url_for("inventory_page"))
    
    from services.inventory_service import get_categories, get_suppliers
    categories = get_categories()
    suppliers = get_suppliers()
    return render_template("add_medicine.html", categories=categories, suppliers=suppliers)

@app.route("/inventory/stock/new", methods=["GET", "POST"])
def add_stock_page():
    if request.method == "POST":
        data = {
            "medicine_id": request.form.get("medicine_id"),
            "batch_no": request.form.get("batch_no"),
            "manufacturing_date": request.form.get("manufacturing_date"),
            "expiry_date": request.form.get("expiry_date"),
            "purchase_price": float(request.form.get("purchase_price") or 0),
            "selling_price": float(request.form.get("selling_price") or 0),
            "quantity_in_stock": int(request.form.get("quantity_in_stock") or 0),
            "rack_location": request.form.get("rack_location")
        }
        from services.inventory_service import add_batch
        add_batch(data)
        flash("Stock batch successfully added!", "success")
        return redirect(url_for("inventory_page"))
    
    from services.medicine_service import search_medicines
    medicines = search_medicines("")
    return render_template("add_stock.html", medicines=medicines)

if __name__ == "__main__":
    app.run(debug=True)
