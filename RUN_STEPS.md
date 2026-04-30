# Pharmacy Management System Run Steps

This file explains how another person can run the project on their system.

## 1. Prerequisites

Install these first:

- Python 3
- Docker Desktop
- Oracle SQL Developer or any Oracle SQL client

## 2. Project Folder

Share the full `PharmacyManagementSystem` folder.

Important folders:

- `backend/`
- `database/`
- `plsql/`
- `queries/`
- `documentation/`

Do not rely on sharing:

- `venv/`
- your local Docker container state
- your terminal environment variables

## 3. Start Docker Database

Open Docker Desktop first.

Check all containers:

```powershell
docker ps -a
```

If the Oracle DB container already exists, start it:

```powershell
docker start pharmacy-db
```

Check that it is running:

```powershell
docker ps
```

The Oracle container should appear as `Up`.

## 4. Create and Activate Virtual Environment

Open terminal in:

```powershell
cd C:\Path\To\PharmacyManagementSystem\backend
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Then activate again:

```powershell
.\venv\Scripts\Activate
```

## 5. Install Python Packages

Install backend dependencies:

```powershell
pip install -r requirements.txt
```

## 6. Set Oracle Environment Variables

Set these in the same terminal where Flask will run:

```powershell
$env:PHARMACY_DB_USER="SYSTEM"
$env:PHARMACY_DB_PASSWORD="YourPassword123"
$env:PHARMACY_DB_DSN="localhost:1521/FREEPDB1"
```

Replace the password if needed with the real Oracle password.

## 7. Test Database Connection

Run:

```powershell
python ..\test_db.py
```

Expected result:

```text
SUCCESS! The database is connected perfectly.
```

If this fails, do not start Flask yet. Fix the Oracle connection first.

## 8. Create Database Objects

If the Oracle database is empty, execute the SQL files in this order:

1. `database/schema.sql`
2. `database/sequences.sql`
3. `database/constraints.sql`
4. `database/indexes.sql`
5. `database/sample_data.sql`
6. `database/views.sql`

Then run the PL/SQL files as needed from:

- `plsql/procedures/`
- `plsql/functions/`
- `plsql/triggers/`

## 9. Run Flask App

From the `backend/` folder:

```powershell
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

## 10. Main Working Pages

- `/` -> Dashboard
- `/customers` -> Customer records
- `/customers/<customer_id>/history` -> Customer purchase history
- `/medicines/search` -> Medicine search
- `/inventory` -> Inventory summary
- `/reports` -> Sales, inventory, and customer reports
- `/billing` -> Billing UI

## 11. Important Notes

- Docker DB and Python `venv` are separate things.
- Start Docker Oracle first.
- Then activate `venv`.
- Then set environment variables.
- Then run Flask.

- If the app shows fallback/sample data, possible reasons are:
  - Oracle is not running
  - environment variables are missing
  - Oracle tables are not created
  - wrong Oracle user/schema is being used

## 12. Useful Commands

Check running Docker containers:

```powershell
docker ps
```

Check all Docker containers:

```powershell
docker ps -a
```

Stop Oracle container:

```powershell
docker stop pharmacy-db
```

Exit Python virtual environment:

```powershell
deactivate
```
