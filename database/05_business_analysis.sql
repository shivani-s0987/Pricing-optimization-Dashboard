-- 1. Category revenue/profit/margin ranking
SELECT category, SUM(sales_revenue) revenue, SUM(gross_profit) gross_profit, SUM(gross_profit)/NULLIF(SUM(sales_revenue),0) margin
FROM v_sales_enriched GROUP BY category ORDER BY revenue DESC;
-- 2. Product profit and weighted discount
SELECT * FROM v_product_profitability ORDER BY gross_profit DESC;
-- 3. High revenue but low margin (threshold is an investigation rule, not a universal standard)
SELECT * FROM v_product_profitability WHERE net_sales_revenue >= (SELECT percentile_cont(.75) WITHIN GROUP (ORDER BY net_sales_revenue) FROM v_product_profitability) AND gross_margin_pct < .20 ORDER BY net_sales_revenue DESC;
-- 4. Discount band performance with exclusive boundaries
WITH banded AS (SELECT *, CASE WHEN discount_pct=0 THEN '0%' WHEN discount_pct<=.05 THEN '>0-5%' WHEN discount_pct<=.10 THEN '>5-10%' WHEN discount_pct<=.20 THEN '>10-20%' WHEN discount_pct<=.30 THEN '>20-30%' ELSE '>30%' END discount_band FROM v_sales_enriched)
SELECT discount_band, SUM(sales_revenue) revenue, SUM(gross_profit) gross_profit, SUM(gross_profit)/NULLIF(SUM(sales_revenue),0) margin, SUM(discount_amount)/NULLIF(SUM(gross_revenue_before_discount),0) weighted_discount
FROM banded GROUP BY discount_band ORDER BY MIN(discount_pct);
-- 5. Monthly trend and month-over-month change
WITH m AS (SELECT year_month, SUM(sales_revenue) revenue, SUM(gross_profit) profit FROM v_sales_enriched GROUP BY year_month)
SELECT *, revenue-LAG(revenue) OVER(ORDER BY year_month) revenue_mom_change,
 (revenue/NULLIF(LAG(revenue) OVER(ORDER BY year_month),0))-1 revenue_mom_growth FROM m ORDER BY year_month;
-- 6. Year-over-year comparison
WITH m AS (SELECT date_trunc('month',order_date)::date month_start,SUM(sales_revenue) revenue,SUM(gross_profit) profit FROM v_sales_enriched GROUP BY 1)
SELECT a.month_start,a.revenue, b.revenue prior_year_revenue, a.revenue/NULLIF(b.revenue,0)-1 yoy_growth FROM m a LEFT JOIN m b ON b.month_start=(a.month_start-INTERVAL '1 year')::date ORDER BY a.month_start;
-- 7. Product rank within category
SELECT product_id,product_name,category,gross_profit, RANK() OVER(PARTITION BY category ORDER BY gross_profit DESC) category_profit_rank FROM v_product_profitability;
-- 8. Product contribution to revenue and profit
SELECT *, net_sales_revenue/NULLIF(SUM(net_sales_revenue) OVER(),0) revenue_share, gross_profit/NULLIF(SUM(gross_profit) OVER(),0) profit_contribution FROM v_product_profitability;
-- 9. Three-month rolling revenue/profit
WITH m AS (SELECT year_month,MIN(order_date) month_start,SUM(sales_revenue) revenue,SUM(gross_profit) profit FROM v_sales_enriched GROUP BY year_month)
SELECT *,SUM(revenue) OVER(ORDER BY month_start ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) rolling_3m_revenue,
 SUM(profit) OVER(ORDER BY month_start ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) rolling_3m_profit FROM m ORDER BY month_start;
-- 10. Deep discount, weak/negative profit lines
SELECT product_id,product_name,category,SUM(sales_revenue) revenue,SUM(gross_profit) gross_profit,SUM(gross_profit)/NULLIF(SUM(sales_revenue),0) margin,AVG(discount_pct) avg_discount
FROM v_sales_enriched GROUP BY product_id,product_name,category HAVING AVG(discount_pct)>.30 AND SUM(gross_profit)<=0 ORDER BY revenue DESC;
-- 11. Below-cost price lines
SELECT sales_line_id,order_date,product_id,unit_selling_price,unit_cost,quantity,gross_profit FROM fact_sales WHERE unit_selling_price < unit_cost ORDER BY order_date;
-- 12. Region/channel performance
SELECT region_name,channel_name,SUM(sales_revenue) revenue,SUM(gross_profit) profit,SUM(gross_profit)/NULLIF(SUM(sales_revenue),0) margin FROM v_sales_enriched GROUP BY region_name,channel_name ORDER BY profit DESC;
-- 13. Category and subcategory discount comparison
SELECT category,subcategory,SUM(sales_revenue) revenue,SUM(gross_profit) profit,SUM(discount_amount)/NULLIF(SUM(gross_revenue_before_discount),0) weighted_discount FROM v_sales_enriched GROUP BY category,subcategory ORDER BY category,revenue DESC;
-- 14. Low margin products with cautious volume context
SELECT *,CASE WHEN units_sold<30 THEN 'LOW VOLUME - interpret cautiously' ELSE 'REVIEW MARGIN' END review_context FROM v_product_profitability WHERE gross_margin_pct<.15 ORDER BY gross_margin_pct;
-- 15. High list price / realized-price gap by product
SELECT product_id,product_name,category, SUM(gross_revenue_before_discount) list_value,SUM(sales_revenue) realized_revenue,
 1-SUM(sales_revenue)/NULLIF(SUM(gross_revenue_before_discount),0) weighted_discount FROM v_sales_enriched GROUP BY product_id,product_name,category ORDER BY weighted_discount DESC;
-- 16. Monthly moving average and cumulative revenue
WITH m AS (SELECT year_month,MIN(order_date) month_start,SUM(sales_revenue) revenue FROM v_sales_enriched GROUP BY year_month)
SELECT *,AVG(revenue) OVER(ORDER BY month_start ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) avg_3m_revenue,SUM(revenue) OVER(ORDER BY month_start) cumulative_revenue FROM m;
-- 17. Product performance by channel
SELECT product_id,product_name,channel_name,SUM(sales_revenue) revenue,SUM(gross_profit) profit FROM v_sales_enriched GROUP BY product_id,product_name,channel_name ORDER BY product_id,revenue DESC;
-- 18. Outlier flags using percentile thresholds (investigate, do not auto-delete)
WITH p AS (SELECT percentile_cont(.99) WITHIN GROUP (ORDER BY sales_revenue) p99 FROM fact_sales)
SELECT f.* FROM fact_sales f CROSS JOIN p WHERE f.sales_revenue>p.p99 ORDER BY f.sales_revenue DESC;
-- 19. Monthly date/region/channel slice
SELECT year_month,region_name,channel_name,SUM(sales_revenue) revenue,SUM(gross_profit) profit FROM v_sales_enriched GROUP BY year_month,region_name,channel_name;
-- 20. Unit economics and price realization
SELECT product_id,product_name,SUM(quantity) units,SUM(sales_revenue)/NULLIF(SUM(quantity),0) avg_selling_price,
 SUM(gross_profit)/NULLIF(SUM(quantity),0) profit_per_unit,SUM(sales_revenue)/NULLIF(COUNT(DISTINCT order_id),0) revenue_per_order FROM v_sales_enriched GROUP BY product_id,product_name;
