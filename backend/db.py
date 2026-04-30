import os


# These environment variables will later hold the real Oracle connection details.
DB_USER = os.getenv("PHARMACY_DB_USER")
DB_PASSWORD = os.getenv("PHARMACY_DB_PASSWORD")
DB_DSN = os.getenv("PHARMACY_DB_DSN")


def get_connection():
    """Return an Oracle connection when config is available, otherwise None."""
    if not DB_USER or not DB_PASSWORD or not DB_DSN:
        return None

    try:
        import oracledb
    except ImportError:
        return None

    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
