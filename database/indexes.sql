-- Performance-oriented indexes

CREATE INDEX idx_medicines_category ON medicines(category_id);
CREATE INDEX idx_medicines_supplier ON medicines(supplier_id);
CREATE INDEX idx_medicines_name ON medicines(medicine_name);
CREATE INDEX idx_batches_medicine ON batches(medicine_id);
CREATE INDEX idx_batches_expiry ON batches(expiry_date);
CREATE INDEX idx_batches_stock ON batches(quantity_in_stock);
CREATE INDEX idx_prescriptions_customer ON prescriptions(customer_id);
CREATE INDEX idx_bills_customer ON bills(customer_id);
CREATE INDEX idx_bills_date ON bills(bill_date);
CREATE INDEX idx_bill_items_bill ON bill_items(bill_id);
CREATE INDEX idx_bill_items_medicine ON bill_items(medicine_id);
CREATE INDEX idx_reorder_alert_status ON reorder_alerts(alert_status);
