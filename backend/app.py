from flask import Flask, render_template, request
from collections import Counter

from services.customer_service import fetch_customer_purchase_history, fetch_customers, search_customers
from services.dashboard_service import get_dashboard_stats
from services.inventory_service import get_inventory_summary
from services.medicine_service import search_medicines
from services.report_service import get_reports_summary

app = Flask(__name__)

# Billing uses a small sample catalog first so the UI can enforce valid medicine/batch choices.
BILLING_MEDICINE_OPTIONS = [
    {
        "name": "Paracure 650mg",
        "batches": ["PAR650-B4", "PAR650-C1"],
    },
    {
        "name": "Amoxycillin 500mg",
        "batches": ["AMX500-A1", "AMX500-B2"],
    },
    {
        "name": "VitaPlus Tablets",
        "batches": ["VIT-25-C2", "VIT-25-D5"],
    },
]


@app.route("/")
def home():
    # The dashboard reads one summary object so the template stays mostly presentation-only.
    dashboard_stats = get_dashboard_stats()
    return render_template("index.html", stats=dashboard_stats)


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
    # Inventory data is grouped in a single summary payload for the page.
    inventory_summary = get_inventory_summary()
    return render_template("inventory.html", inventory=inventory_summary)


@app.route("/reports")
def reports_page():
    # The reports page receives three grouped report sections: sales, inventory, and customers.
    reports = get_reports_summary()
    return render_template("reports.html", reports=reports)


@app.route("/billing")
def billing_page():
    # The billing page receives structured medicine data so dropdowns can stay in sync.
    return render_template("billing.html", medicine_options=BILLING_MEDICINE_OPTIONS)


@app.route("/settings")
def settings_page():
    return render_template("settings.html")


@app.route("/medicines/search")
def search_medicine():
    # This route reads the search term from the URL and passes it to Oracle-ready logic.
    query = request.args.get("q", "")
    medicines = search_medicines(query)
    return render_template("search_medicine.html", medicines=medicines, query=query)


if __name__ == "__main__":
    app.run(debug=True)
