-- Minimal sample data for demo/testing

INSERT INTO categories VALUES (seq_category.NEXTVAL, 'Antibiotics', 'Bacterial infection medicines');
INSERT INTO categories VALUES (seq_category.NEXTVAL, 'Pain Relief', 'Pain management medicines');
INSERT INTO categories VALUES (seq_category.NEXTVAL, 'Vitamins', 'Nutritional supplements');

INSERT INTO suppliers VALUES (seq_supplier.NEXTVAL, 'MedLife Distributors', 'Ravi Mehta', '9876543210', 'medlife@example.com', 'Delhi', 'ACTIVE');
INSERT INTO suppliers VALUES (seq_supplier.NEXTVAL, 'HealthFirst Pharma', 'Anita Shah', '9988776655', 'healthfirst@example.com', 'Mumbai', 'ACTIVE');

INSERT INTO medicines (
    medicine_id, category_id, supplier_id, medicine_name, generic_name, dosage_form,
    strength, unit_price, reorder_level, requires_prescription, gst_percent, medicine_status
) VALUES (
    seq_medicine.NEXTVAL, 1, 1, 'Amoxycillin', 'Amoxicillin', 'Capsule',
    '500mg', 85, 20, 'Y', 5, 'ACTIVE'
);

INSERT INTO medicines (
    medicine_id, category_id, supplier_id, medicine_name, generic_name, dosage_form,
    strength, unit_price, reorder_level, requires_prescription, gst_percent, medicine_status
) VALUES (
    seq_medicine.NEXTVAL, 2, 2, 'Paracure', 'Paracetamol', 'Tablet',
    '650mg', 30, 40, 'N', 5, 'ACTIVE'
);

INSERT INTO medicines (
    medicine_id, category_id, supplier_id, medicine_name, generic_name, dosage_form,
    strength, unit_price, reorder_level, requires_prescription, gst_percent, medicine_status
) VALUES (
    seq_medicine.NEXTVAL, 3, 2, 'VitaPlus', 'Multivitamin', 'Tablet',
    'One Daily', 120, 15, 'N', 12, 'ACTIVE'
);

INSERT INTO batches VALUES (seq_batch.NEXTVAL, 1001, 'AMX500-A1', DATE '2025-01-10', DATE '2027-01-09', 60, 85, 100, SYSDATE, 'R1-A');
INSERT INTO batches VALUES (seq_batch.NEXTVAL, 1002, 'PAR650-B4', DATE '2025-07-01', DATE '2026-11-30', 18, 30, 250, SYSDATE, 'R2-C');
INSERT INTO batches VALUES (seq_batch.NEXTVAL, 1003, 'VIT-25-C2', DATE '2025-03-15', DATE '2026-08-14', 75, 120, 60, SYSDATE, 'R3-B');

INSERT INTO customers VALUES (seq_customer.NEXTVAL, 'Aman Verma', '9012345678', 'aman@example.com', 'Male', DATE '2001-02-18', 0, SYSDATE);
INSERT INTO customers VALUES (seq_customer.NEXTVAL, 'Sneha Kapoor', '9123456780', 'sneha@example.com', 'Female', DATE '1999-06-10', 0, SYSDATE);

INSERT INTO doctors VALUES (seq_doctor.NEXTVAL, 'Dr. R. Sharma', 'General Physician', '9898989898', 'REG1001');
INSERT INTO doctors VALUES (seq_doctor.NEXTVAL, 'Dr. Priya Nair', 'Pediatrician', '9777777777', 'REG1002');

COMMIT;
