-- Foreign keys and business constraints

ALTER TABLE medicines
    ADD CONSTRAINT fk_medicine_category
    FOREIGN KEY (category_id) REFERENCES categories(category_id);

ALTER TABLE medicines
    ADD CONSTRAINT fk_medicine_supplier
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id);

ALTER TABLE medicines
    ADD CONSTRAINT uq_medicine_name_strength
    UNIQUE (medicine_name, strength, dosage_form);

ALTER TABLE medicines
    ADD CONSTRAINT chk_medicine_price
    CHECK (unit_price > 0 AND reorder_level >= 0 AND gst_percent >= 0);

ALTER TABLE batches
    ADD CONSTRAINT fk_batch_medicine
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);

ALTER TABLE batches
    ADD CONSTRAINT chk_batch_dates
    CHECK (expiry_date > manufacturing_date);

ALTER TABLE batches
    ADD CONSTRAINT chk_batch_values
    CHECK (purchase_price >= 0 AND selling_price > 0 AND quantity_in_stock >= 0);

ALTER TABLE prescriptions
    ADD CONSTRAINT fk_prescription_customer
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

ALTER TABLE prescriptions
    ADD CONSTRAINT fk_prescription_doctor
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id);

ALTER TABLE prescription_items
    ADD CONSTRAINT fk_prescription_item_prescription
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id);

ALTER TABLE prescription_items
    ADD CONSTRAINT fk_prescription_item_medicine
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);

ALTER TABLE prescription_items
    ADD CONSTRAINT chk_prescribed_qty
    CHECK (quantity_prescribed > 0);

ALTER TABLE bills
    ADD CONSTRAINT fk_bill_customer
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

ALTER TABLE bills
    ADD CONSTRAINT fk_bill_prescription
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id);

ALTER TABLE bill_items
    ADD CONSTRAINT fk_bill_item_bill
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id);

ALTER TABLE bill_items
    ADD CONSTRAINT fk_bill_item_batch
    FOREIGN KEY (batch_id) REFERENCES batches(batch_id);

ALTER TABLE bill_items
    ADD CONSTRAINT fk_bill_item_medicine
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);

ALTER TABLE bill_items
    ADD CONSTRAINT chk_bill_item_values
    CHECK (quantity_sold > 0 AND unit_price >= 0 AND discount_percent >= 0 AND line_total >= 0);

ALTER TABLE stock_audit
    ADD CONSTRAINT fk_stock_audit_batch
    FOREIGN KEY (batch_id) REFERENCES batches(batch_id);

ALTER TABLE reorder_alerts
    ADD CONSTRAINT fk_reorder_alert_medicine
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);

ALTER TABLE expired_medicine_log
    ADD CONSTRAINT fk_expired_log_batch
    FOREIGN KEY (batch_id) REFERENCES batches(batch_id);

ALTER TABLE expired_medicine_log
    ADD CONSTRAINT fk_expired_log_medicine
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);
