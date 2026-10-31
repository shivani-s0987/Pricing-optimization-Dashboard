-- All queries should return zero rows (except the summary checks at the end).
SELECT sales_line_id FROM fact_sales GROUP BY sales_line_id HAVING COUNT(*) > 1;
SELECT * FROM fact_sales WHERE quantity <= 0 OR discount_pct < 0 OR discount_pct >= 1 OR unit_cost < 0;
SELECT * FROM fact_sales WHERE ABS(sales_revenue - quantity * unit_selling_price) > 0.011;
SELECT * FROM fact_sales WHERE ABS(cost_of_goods_sold - quantity * unit_cost) > 0.011;
SELECT * FROM fact_sales WHERE ABS(gross_profit - (sales_revenue - cost_of_goods_sold)) > 0.011;
SELECT 'fact_rows' AS check_name, COUNT(*)::text AS result FROM fact_sales
UNION ALL SELECT 'missing_product_fk', COUNT(*)::text FROM fact_sales f LEFT JOIN dim_product p USING(product_id) WHERE p.product_id IS NULL
UNION ALL SELECT 'missing_date_fk', COUNT(*)::text FROM fact_sales f LEFT JOIN dim_date d ON d.date=f.order_date WHERE d.date IS NULL;
