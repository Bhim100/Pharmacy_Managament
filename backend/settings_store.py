# Central in-memory settings store.
# These are the DEFAULT values. Reset will restore to these.

DEFAULTS = {
    "pharmacy_name": "Pharma One",
    "admin_username": "Subash",
    "low_stock_threshold": 10,
    "expiry_alert_days": 30,
}

# Live settings — modified by the Settings page.
APP_SETTINGS = dict(DEFAULTS)
