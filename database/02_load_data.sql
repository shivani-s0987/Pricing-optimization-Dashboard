-- Run from psql after schema creation. Update the absolute paths for your machine.
-- Prefer COPY from psql client using \copy, which reads files on the client machine.
\copy dim_product(product_id,product_name,category,subcategory,brand,current_list_price,current_unit_cost,product_status) FROM 'data/processed/dim_product.csv' WITH (FORMAT csv, HEADER true)
\copy dim_region(region_id,region_name,state_or_territory,market_type) FROM 'data/processed/dim_region.csv' WITH (FORMAT csv, HEADER true)
\copy dim_channel(channel_id,channel_name) FROM 'data/processed/dim_channel.csv' WITH (FORMAT csv, HEADER true)
\copy dim_customer_segment(customer_segment_id,segment_name) FROM 'data/processed/dim_customer_segment.csv' WITH (FORMAT csv, HEADER true)
\copy dim_date(date,year,quarter,month_number,month_name,year_month,week,is_weekend) FROM 'data/processed/dim_date.csv' WITH (FORMAT csv, HEADER true)
\copy fact_sales(sales_line_id,order_id,order_date,product_id,customer_segment_id,region_id,channel_id,quantity,unit_list_price,discount_pct,unit_selling_price,unit_cost,sales_revenue,cost_of_goods_sold,gross_profit,gross_margin_pct) FROM 'data/processed/fact_sales_clean.csv' WITH (FORMAT csv, HEADER true)
