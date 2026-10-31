-- PostgreSQL 14+; create database separately: CREATE DATABASE pricing_analytics;
CREATE TABLE IF NOT EXISTS dim_product (
 product_id varchar(8) PRIMARY KEY, product_name text NOT NULL, category text NOT NULL,
 subcategory text NOT NULL, brand text NOT NULL, current_list_price numeric(12,2) NOT NULL CHECK(current_list_price > 0),
 current_unit_cost numeric(12,2) NOT NULL CHECK(current_unit_cost >= 0), product_status text NOT NULL
);
CREATE TABLE IF NOT EXISTS dim_region (region_id varchar(8) PRIMARY KEY, region_name text NOT NULL, state_or_territory text NOT NULL, market_type text NOT NULL);
CREATE TABLE IF NOT EXISTS dim_channel (channel_id varchar(8) PRIMARY KEY, channel_name text NOT NULL);
CREATE TABLE IF NOT EXISTS dim_customer_segment (customer_segment_id varchar(8) PRIMARY KEY, segment_name text NOT NULL);
CREATE TABLE IF NOT EXISTS dim_date (date date PRIMARY KEY, year int NOT NULL, quarter varchar(2) NOT NULL, month_number int NOT NULL CHECK(month_number BETWEEN 1 AND 12), month_name text NOT NULL, year_month char(7) NOT NULL, week int NOT NULL, is_weekend boolean NOT NULL);
CREATE TABLE IF NOT EXISTS fact_sales (
 sales_line_id varchar(16) PRIMARY KEY, order_id varchar(16) NOT NULL, order_date date NOT NULL REFERENCES dim_date(date),
 product_id varchar(8) NOT NULL REFERENCES dim_product(product_id), customer_segment_id varchar(8) NOT NULL REFERENCES dim_customer_segment(customer_segment_id),
 region_id varchar(8) NOT NULL REFERENCES dim_region(region_id), channel_id varchar(8) NOT NULL REFERENCES dim_channel(channel_id),
 quantity int NOT NULL CHECK(quantity > 0), unit_list_price numeric(12,2) NOT NULL CHECK(unit_list_price > 0),
 discount_pct numeric(6,4) NOT NULL CHECK(discount_pct >= 0 AND discount_pct < 1), unit_selling_price numeric(12,2) NOT NULL CHECK(unit_selling_price >= 0),
 unit_cost numeric(12,2) NOT NULL CHECK(unit_cost >= 0), sales_revenue numeric(14,2) NOT NULL, cost_of_goods_sold numeric(14,2) NOT NULL,
 gross_profit numeric(14,2) NOT NULL, gross_margin_pct numeric(12,8)
);
CREATE INDEX IF NOT EXISTS ix_fact_sales_date ON fact_sales(order_date);
CREATE INDEX IF NOT EXISTS ix_fact_sales_product_date ON fact_sales(product_id, order_date);
CREATE INDEX IF NOT EXISTS ix_fact_sales_category_dims ON fact_sales(region_id, channel_id, customer_segment_id);
