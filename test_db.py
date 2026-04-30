import os
import sys

print("--- Database Diagnostics ---")

# 1. Check environment variables
user = os.getenv("PHARMACY_DB_USER")
pwd = os.getenv("PHARMACY_DB_PASSWORD")
dsn = os.getenv("PHARMACY_DB_DSN")

print(f"User: {'Set' if user else 'MISSING!'}")
print(f"Password: {'Set' if pwd else 'MISSING!'}")
print(f"DSN: {dsn if dsn else 'MISSING!'}")

if not user or not pwd or not dsn:
    print("\nERROR: Environment variables are not set correctly.")
    sys.exit(1)

# 2. Check Oracle package
try:
    import oracledb
    print("\nOracle package: Installed correctly")
except ImportError:
    print("\nERROR: The 'oracledb' package is not installed. Run: pip install oracledb")
    sys.exit(1)

# 3. Test Connection
print("\nAttempting connection to Docker database...")
try:
    conn = oracledb.connect(user=user, password=pwd, dsn=dsn)
    print("SUCCESS! The database is connected perfectly.")
    conn.close()
except Exception as e:
    print(f"\nFAILED to connect. Error: {e}")
