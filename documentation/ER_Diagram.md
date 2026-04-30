# ER Diagram Notes

Create an ER diagram with these main relationships:

- `categories` 1-to-many `medicines`
- `suppliers` 1-to-many `medicines`
- `medicines` 1-to-many `batches`
- `customers` 1-to-many `prescriptions`
- `doctors` 1-to-many `prescriptions`
- `prescriptions` 1-to-many `prescription_items`
- `customers` 1-to-many `bills`
- `bills` 1-to-many `bill_items`
- `medicines` 1-to-many `bill_items`
- `batches` 1-to-many `bill_items`

Suggested tools:

- dbdiagram.io
- draw.io
- Lucidchart
