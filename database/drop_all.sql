-- Cleanup script

DROP VIEW vw_daily_sales_summary;
DROP VIEW vw_customer_purchase_history;
DROP VIEW vw_expiring_soon;
DROP VIEW vw_inventory_status;

DROP TABLE expired_medicine_log CASCADE CONSTRAINTS;
DROP TABLE reorder_alerts CASCADE CONSTRAINTS;
DROP TABLE stock_audit CASCADE CONSTRAINTS;
DROP TABLE bill_items CASCADE CONSTRAINTS;
DROP TABLE bills CASCADE CONSTRAINTS;
DROP TABLE prescription_items CASCADE CONSTRAINTS;
DROP TABLE prescriptions CASCADE CONSTRAINTS;
DROP TABLE doctors CASCADE CONSTRAINTS;
DROP TABLE customers CASCADE CONSTRAINTS;
DROP TABLE batches CASCADE CONSTRAINTS;
DROP TABLE medicines CASCADE CONSTRAINTS;
DROP TABLE suppliers CASCADE CONSTRAINTS;
DROP TABLE categories CASCADE CONSTRAINTS;

DROP SEQUENCE seq_expired_log;
DROP SEQUENCE seq_reorder_alert;
DROP SEQUENCE seq_stock_audit;
DROP SEQUENCE seq_bill_item;
DROP SEQUENCE seq_bill;
DROP SEQUENCE seq_prescription_item;
DROP SEQUENCE seq_prescription;
DROP SEQUENCE seq_doctor;
DROP SEQUENCE seq_customer;
DROP SEQUENCE seq_batch;
DROP SEQUENCE seq_medicine;
DROP SEQUENCE seq_supplier;
DROP SEQUENCE seq_category;
