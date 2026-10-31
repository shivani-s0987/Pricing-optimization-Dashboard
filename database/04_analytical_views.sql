CREATE OR REPLACE VIEW v_sales_enriched AS
SELECT f.*, p.product_name, p.category, p.subcategory, p.brand, r.region_name, c.channel_name, s.segment_name, d.year, d.quarter, d.month_number, d.month_name, d.year_month,
       f.quantity*f.unit_list_price AS gross_revenue_before_discount,
       f.quantity*(f.unit_list_price-f.unit_selling_price) AS discount_amount
FROM fact_sales f JOIN dim_product p USING(product_id) JOIN dim_region r USING(region_id)
JOIN dim_channel c USING(channel_id) JOIN dim_customer_segment s USING(customer_segment_id) JOIN dim_date d ON d.date=f.order_date;
CREATE OR REPLACE VIEW v_product_profitability AS
SELECT product_id, product_name, category, SUM(sales_revenue) net_sales_revenue, SUM(cost_of_goods_sold) cogs,
 SUM(gross_profit) gross_profit, SUM(gross_profit)/NULLIF(SUM(sales_revenue),0) gross_margin_pct,
 SUM(quantity) units_sold, SUM(discount_amount)/NULLIF(SUM(gross_revenue_before_discount),0) weighted_discount_pct,
 SUM(sales_revenue)/NULLIF(COUNT(DISTINCT order_id),0) revenue_per_order
FROM v_sales_enriched GROUP BY product_id,product_name,category;
CREATE OR REPLACE VIEW v_monthly_performance AS
SELECT year_month, MIN(order_date) month_start, SUM(sales_revenue) net_sales_revenue, SUM(gross_profit) gross_profit,
 SUM(gross_profit)/NULLIF(SUM(sales_revenue),0) gross_margin_pct, SUM(quantity) units_sold,
 SUM(discount_amount)/NULLIF(SUM(gross_revenue_before_discount),0) weighted_discount_pct
FROM v_sales_enriched GROUP BY year_month;
