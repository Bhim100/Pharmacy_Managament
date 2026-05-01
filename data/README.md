# Excel Data Folder

This folder stores sample Excel files for loading real-looking data into Oracle.

## Files

- `01_categories.xlsx`
- `02_suppliers.xlsx`
- `03_medicines.xlsx`
- `04_batches.xlsx`
- `05_customers.xlsx`
- `06_doctors.xlsx`

## Why these are useful

- They contain records that are clearly different from the current fallback/sample Flask data.
- They can be loaded into Oracle with `load_excel_to_oracle.py`.

## How to load them

From the project root, after activating the backend virtual environment and setting Oracle env vars:

```powershell
python load_excel_to_oracle.py --replace
```

Use `--replace` when you want to clear existing imported table data before loading again.
