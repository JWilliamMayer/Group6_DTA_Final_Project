-- E-commerce transaction tables
CREATE TABLE IF NOT EXISTS ecommerce_transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(100),
    customer_id VARCHAR(100),
    product_id VARCHAR(100),
    product_name VARCHAR(255),
    category VARCHAR(100),
    price NUMERIC(10, 2),
    quantity INTEGER,
    transaction_date TIMESTAMP,
    payment_method VARCHAR(50),
    shipping_address TEXT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer reviews tables
CREATE TABLE IF NOT EXISTS customer_reviews (
    id SERIAL PRIMARY KEY,
    review_id VARCHAR(100),
    customer_id VARCHAR(100),
    product_id VARCHAR(100),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_date TIMESTAMP,
    sentiment_score NUMERIC(4, 3),  -- Range from 0 to 1
    helpful_votes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Financial reports tables
CREATE TABLE IF NOT EXISTS financial_reports (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    report_year VARCHAR(4),
    revenue NUMERIC(14, 2),
    profit NUMERIC(14, 2),
    processed_date DATE,
    text_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products dimension table
CREATE TABLE IF NOT EXISTS dim_products (
    product_id VARCHAR(100) PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    base_price NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers dimension table
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id VARCHAR(100) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dates dimension table
CREATE TABLE IF NOT EXISTS dim_dates (
    date_id DATE PRIMARY KEY,
    day_of_week INTEGER,
    day_name VARCHAR(10),
    month INTEGER,
    month_name VARCHAR(10),
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

-- Sales fact table for analytics
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(100),
    customer_id VARCHAR(100),
    product_id VARCHAR(100),
    date_id DATE,
    quantity INTEGER,
    unit_price NUMERIC(10, 2),
    total_price NUMERIC(10, 2),
    discount NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer sentiment fact table
CREATE TABLE IF NOT EXISTS fact_customer_sentiment (
    sentiment_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100),
    product_id VARCHAR(100),
    date_id DATE,
    review_id VARCHAR(100),
    sentiment_score NUMERIC(4, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Financial performance fact table
CREATE TABLE IF NOT EXISTS fact_financial_performance (
    performance_id SERIAL PRIMARY KEY,
    report_id INTEGER,
    year INTEGER,
    quarter INTEGER,
    revenue NUMERIC(14, 2),
    profit NUMERIC(14, 2),
    profit_margin NUMERIC(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create analytics views

-- E-commerce sales analysis view
CREATE OR REPLACE VIEW view_sales_analysis AS
SELECT 
    fs.transaction_id,
    dc.customer_id,
    dc.first_name || ' ' || dc.last_name AS customer_name,
    dp.product_id,
    dp.product_name,
    dp.category,
    fs.quantity,
    fs.unit_price,
    fs.total_price,
    dd.date_id,
    dd.month_name,
    dd.quarter,
    dd.year
FROM fact_sales fs
JOIN dim_customers dc ON fs.customer_id = dc.customer_id
JOIN dim_products dp ON fs.product_id = dp.product_id
JOIN dim_dates dd ON fs.date_id = dd.date_id;

-- Customer sentiment analysis view
CREATE OR REPLACE VIEW view_sentiment_analysis AS
SELECT 
    fcs.sentiment_id,
    dc.customer_id,
    dc.first_name || ' ' || dc.last_name AS customer_name,
    dp.product_id,
    dp.product_name,
    dp.category,
    cr.review_text,
    fcs.sentiment_score,
    dd.date_id,
    dd.month_name,
    dd.quarter,
    dd.year
FROM fact_customer_sentiment fcs
JOIN dim_customers dc ON fcs.customer_id = dc.customer_id
JOIN dim_products dp ON fcs.product_id = dp.product_id
JOIN dim_dates dd ON fcs.date_id = dd.date_id
JOIN customer_reviews cr ON fcs.review_id = cr.review_id;

-- Financial performance analysis view
CREATE OR REPLACE VIEW view_financial_performance AS
SELECT 
    fr.filename,
    ffp.year,
    ffp.quarter,
    ffp.revenue,
    ffp.profit,
    ffp.profit_margin
FROM fact_financial_performance ffp
JOIN financial_reports fr ON ffp.report_id = fr.id;