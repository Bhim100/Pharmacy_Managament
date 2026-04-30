-- Core schema for Pharmacy Management System

CREATE TABLE categories (
    category_id NUMBER PRIMARY KEY,
    category_name VARCHAR2(100) NOT NULL UNIQUE,
    description VARCHAR2(255)
);

CREATE TABLE suppliers (
    supplier_id NUMBER PRIMARY KEY,
    supplier_name VARCHAR2(150) NOT NULL,
    contact_person VARCHAR2(100),
    phone VARCHAR2(20),
    email VARCHAR2(120),
    city VARCHAR2(100),
    supplier_status VARCHAR2(20) DEFAULT 'ACTIVE'
        CHECK (supplier_status IN ('ACTIVE', 'INACTIVE'))
);

CREATE TABLE medicines (
    medicine_id NUMBER PRIMARY KEY,
    category_id NUMBER NOT NULL,
    supplier_id NUMBER,
    medicine_name VARCHAR2(150) NOT NULL,
    generic_name VARCHAR2(150),
    dosage_form VARCHAR2(50),
    strength VARCHAR2(50),
    unit_price NUMBER(10,2) NOT NULL,
    reorder_level NUMBER DEFAULT 10 NOT NULL,
    requires_prescription CHAR(1) DEFAULT 'N'
        CHECK (requires_prescription IN ('Y', 'N')),
    gst_percent NUMBER(5,2) DEFAULT 0,
    medicine_status VARCHAR2(20) DEFAULT 'ACTIVE'
        CHECK (medicine_status IN ('ACTIVE', 'INACTIVE')),
    created_at DATE DEFAULT SYSDATE
);

CREATE TABLE batches (
    batch_id NUMBER PRIMARY KEY,
    medicine_id NUMBER NOT NULL,
    batch_no VARCHAR2(50) NOT NULL UNIQUE,
    manufacturing_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    purchase_price NUMBER(10,2) NOT NULL,
    selling_price NUMBER(10,2) NOT NULL,
    quantity_in_stock NUMBER NOT NULL,
    received_date DATE DEFAULT SYSDATE,
    rack_location VARCHAR2(30)
);

CREATE TABLE customers (
    customer_id NUMBER PRIMARY KEY,
    customer_name VARCHAR2(150) NOT NULL,
    phone VARCHAR2(20) UNIQUE,
    email VARCHAR2(120),
    gender VARCHAR2(10),
    date_of_birth DATE,
    loyalty_points NUMBER DEFAULT 0,
    created_at DATE DEFAULT SYSDATE
);

CREATE TABLE doctors (
    doctor_id NUMBER PRIMARY KEY,
    doctor_name VARCHAR2(150) NOT NULL,
    specialization VARCHAR2(100),
    phone VARCHAR2(20),
    registration_no VARCHAR2(50) UNIQUE
);

CREATE TABLE prescriptions (
    prescription_id NUMBER PRIMARY KEY,
    customer_id NUMBER NOT NULL,
    doctor_id NUMBER,
    prescription_date DATE DEFAULT SYSDATE,
    notes VARCHAR2(255)
);

CREATE TABLE prescription_items (
    prescription_item_id NUMBER PRIMARY KEY,
    prescription_id NUMBER NOT NULL,
    medicine_id NUMBER NOT NULL,
    dosage_instruction VARCHAR2(150),
    quantity_prescribed NUMBER NOT NULL
);

CREATE TABLE bills (
    bill_id NUMBER PRIMARY KEY,
    customer_id NUMBER,
    prescription_id NUMBER,
    bill_date DATE DEFAULT SYSDATE,
    payment_mode VARCHAR2(20) DEFAULT 'CASH'
        CHECK (payment_mode IN ('CASH', 'CARD', 'UPI', 'INSURANCE')),
    gross_amount NUMBER(12,2) DEFAULT 0 NOT NULL,
    discount_amount NUMBER(12,2) DEFAULT 0 NOT NULL,
    tax_amount NUMBER(12,2) DEFAULT 0 NOT NULL,
    net_amount NUMBER(12,2) DEFAULT 0 NOT NULL,
    bill_status VARCHAR2(20) DEFAULT 'PAID'
        CHECK (bill_status IN ('PAID', 'CANCELLED', 'PENDING')),
    created_by VARCHAR2(50) DEFAULT USER
);

CREATE TABLE bill_items (
    bill_item_id NUMBER PRIMARY KEY,
    bill_id NUMBER NOT NULL,
    batch_id NUMBER NOT NULL,
    medicine_id NUMBER NOT NULL,
    quantity_sold NUMBER NOT NULL,
    unit_price NUMBER(10,2) NOT NULL,
    discount_percent NUMBER(5,2) DEFAULT 0,
    line_total NUMBER(12,2) NOT NULL
);

CREATE TABLE stock_audit (
    audit_id NUMBER PRIMARY KEY,
    batch_id NUMBER NOT NULL,
    old_quantity NUMBER,
    new_quantity NUMBER,
    action_type VARCHAR2(30) NOT NULL,
    action_timestamp DATE DEFAULT SYSDATE,
    remarks VARCHAR2(255)
);

CREATE TABLE reorder_alerts (
    alert_id NUMBER PRIMARY KEY,
    medicine_id NUMBER NOT NULL,
    alert_date DATE DEFAULT SYSDATE,
    current_stock NUMBER NOT NULL,
    reorder_level NUMBER NOT NULL,
    alert_status VARCHAR2(20) DEFAULT 'OPEN'
        CHECK (alert_status IN ('OPEN', 'RESOLVED'))
);

CREATE TABLE expired_medicine_log (
    log_id NUMBER PRIMARY KEY,
    batch_id NUMBER NOT NULL,
    medicine_id NUMBER NOT NULL,
    expiry_date DATE NOT NULL,
    quantity_disposed NUMBER NOT NULL,
    disposed_on DATE DEFAULT SYSDATE,
    remarks VARCHAR2(255)
);
