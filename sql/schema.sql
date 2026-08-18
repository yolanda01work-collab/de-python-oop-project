CREATE TABLE IF NOT EXISTS dim_customers (

    customer_id VARCHAR(20) PRIMARY KEY,

    customer_name VARCHAR(100),

    region VARCHAR(50)

);


CREATE TABLE IF NOT EXISTS dim_products (

    product_id VARCHAR(20) PRIMARY KEY,

    product_name VARCHAR(100),

    category VARCHAR(50)

);


CREATE TABLE IF NOT EXISTS stg_sales (

    order_id INTEGER PRIMARY KEY,

    order_date DATE,

    customer_id VARCHAR(20),

    product_id VARCHAR(20),

    quantity INTEGER,

    unit_price NUMERIC(10, 2),

    discount_rate NUMERIC(5, 4)

);


CREATE TABLE IF NOT EXISTS fact_sales (

    order_id INTEGER PRIMARY KEY,

    order_date DATE,

    customer_id VARCHAR(20),

    product_id VARCHAR(20),

    quantity INTEGER,

    unit_price NUMERIC(10, 2),

    discount_rate NUMERIC(5, 4),

    gross_sales NUMERIC(12, 2),

    discount_amount NUMERIC(12, 2),

    net_sales NUMERIC(12, 2),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customers(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES dim_products(product_id)

);


CREATE TABLE IF NOT EXISTS etl_rejected_sales (

    rejection_id SERIAL PRIMARY KEY,

    order_id VARCHAR(50),

    raw_record TEXT,

    reason TEXT,

    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);