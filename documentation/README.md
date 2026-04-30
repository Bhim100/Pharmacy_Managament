# Pharmacy Management System

## Overview

This project is a college-level DBMS application built for managing pharmacy operations such as medicine records, batch-wise inventory, prescriptions, billing, sales tracking, and customer history.

## Modules Included

- Medicine and category management
- Supplier and doctor management
- Batch-wise stock tracking
- Prescription and prescription item tracking
- Billing with bill items and discount handling
- Expiry validation and automatic stock reduction
- Reorder alert and expired stock disposal modules
- Basic frontend pages for demo presentation

## Suggested Enhancements Added

- Supplier table for procurement tracking
- Doctor table for prescription reference
- Loyalty points for repeat customers
- Reorder alerts for low stock control
- Stock audit log for accountability
- Expired medicine disposal log

## Schema Improvements

- Added master tables: `categories`, `suppliers`, `doctors`
- Split prescription details into `prescriptions` and `prescription_items`
- Added audit and alert tables for operational tracking
- Included check constraints, unique constraints, and indexes

## Advanced SQL Features Covered

- Joins and grouped reports
- Views for inventory and sales summaries
- Analytic functions such as `RANK()` and running totals
- Maintenance queries for admin checks

## PL/SQL Features Covered

- Procedures for billing, batch insertion, reorder checks, and expired stock disposal
- Functions for total calculation, discount logic, and medicine search
- Triggers for stock updates, expiry validation, audit logging, and loyalty points
- Transactions with `COMMIT`, `ROLLBACK`, and `SAVEPOINT`

## Real-World Features That Make It Stand Out

- Prevent sale of expired medicines
- Track low-stock medicines automatically
- Maintain customer purchase history
- Include supplier, doctor, and prescription linkage
- Support loyalty points and repeat customer benefits
- Provide analytical reports for better decision making

## Folder Structure

```text
PharmacyManagementSystem/
|-- database/
|-- plsql/
|-- queries/
|-- frontend/
|-- documentation/
`-- outputs/
```

## How to Run

1. Execute `database/schema.sql`
2. Execute `database/sequences.sql`
3. Execute `database/constraints.sql`
4. Execute `database/indexes.sql`
5. Execute `database/sample_data.sql`
6. Execute `database/views.sql`
7. Execute the PL/SQL files
8. Run report queries from the `queries/` folder

## Frontend Suggestions

- Add stock status badges
- Show expiry warnings in red/yellow
- Use cards and summary widgets on dashboard
- Add simple search and filter UI
- Include printable invoice layout
