# Interview Preparation

## Resume bullets (truthful)
- Built a reproducible pricing analytics pipeline in Python/Pandas for 20,000 synthetic retail sales lines across 120 products and 10 categories, including data-quality validation, foreign-key checks, reconciliation and quarantine of six malformed source records.
- Developed PostgreSQL schema/views and 20 analytical SQL queries using CTEs, window functions, rankings, MoM/YoY comparisons, rolling totals and discount-band analysis to investigate revenue, gross profit and margin patterns.
- Created an Excel analysis workbook and automated CSV/Markdown/PDF reporting; designed a Power BI star schema, DAX measure library and five-page dashboard specification with scenario assumptions and explicit causal limitations.

## One-line description
Pricing and profitability analytics solution combining Python ETL, SQL analysis, Excel reporting and a Power BI implementation specification to identify products for pricing review and explore price/demand/cost scenarios on synthetic data.

## 60–90 second project pitch
“I built a Pricing Optimization and Profitability Intelligence project to demonstrate how a retail team can go beyond revenue and understand margin and discount performance. I generated 20,000 reproducible synthetic sales lines across 120 products, 10 categories, five regions and four channels. I created a data-quality pipeline that validates quantities, prices, discounts, foreign keys and calculated metrics, while preserving invalid source rows in quarantine. I defined gross revenue before discount, discount amount, net sales, COGS, gross profit, margin and weighted discount consistently. The SQL layer includes product/category rankings, monthly growth, rolling metrics, discount-band comparisons and exception queries. The Excel workbook provides summary KPIs, category/product analysis and a chart; the report pipeline generates CSVs and a PDF. For Power BI, I prepared the star schema, DAX measures and a five-page build guide, including a what-if simulator where demand change is an explicit assumption rather than claimed elasticity. The key limitation is that the data are synthetic and observational, so the flags are investigation hypotheses, not proven commercial improvements.”

## Ten likely interview questions and strong answers

### 1. How did you define gross margin?
Gross margin is gross profit divided by net sales revenue, where gross profit equals net sales revenue minus cost of goods sold. At aggregate level I use `SUM(GrossProfit) / SUM(SalesRevenue)`, not the unweighted average of line-level margins. I use safe division for zero denominators.

### 2. Why use weighted average discount rather than average discount percentage?
A simple row average treats a small transaction and a large transaction equally. Weighted discount is total discount amount divided by gross revenue before discount, so it reflects the value of discount given across the selected transactions.

### 3. Which SQL techniques did you use and why?
CTEs make multi-step calculations readable; `CASE` defines exclusive discount bands; window functions support `LAG`, rankings, running totals and rolling three-month sums; `NULLIF` prevents divide-by-zero; joins enrich sales with product, date, region, channel and segment dimensions.

### 4. Explain the star schema.
FactSales stores transaction-grain measures and foreign keys. Date, Product, Region, Channel and Customer Segment are dimensions with one-to-many relationships into the fact. This makes filtering intuitive and avoids repeated descriptive attributes in the fact. I prefer single-direction filters unless a justified use case requires otherwise.

### 5. What does the DAX measure context mean here?
Measures recalculate under current filter context from date, category, region, channel and product selections. `CALCULATE` modifies filter context for previous periods; `DATEADD` requires a marked contiguous date table. I use `DIVIDE` for safe ratios and validate totals against reference CSV summaries.

### 6. How did you handle data quality?
I validate schema, dates, positive quantities, discount bounds, nonnegative costs, foreign keys, duplicate line IDs, and financial arithmetic. Invalid records are preserved in a quarantine file with reasons. Outliers are flagged for investigation instead of automatically deleted because they may be legitimate transactions.

### 7. What does discount effectiveness mean, and can you claim discounts caused sales growth?
In this project it means descriptive comparison of revenue, gross profit, units and margin across discount bands. No causal claim is justified because discounts may be assigned to products with different demand, seasonality, inventory or strategic roles. A controlled experiment or credible causal design would be needed to estimate impact.

### 8. How would you prioritize a low-margin product?
I would verify cost and selling-price data, check units and sample size, compare the product with its category/channel peers, review lifecycle and inventory, and assess customer/competitive context. Then I would test hypotheses such as reducing discount, renegotiating cost, or revising list price. Low margin alone is not enough to recommend a price increase.

### 9. How does the what-if simulator work?
Scenario price equals baseline realized price times one plus the price-change assumption. Scenario units equal baseline units times one plus a user-entered demand-change assumption. Scenario revenue and COGS are recalculated from those values, and gross profit is their difference. The demand input is not an elasticity estimate and price change is not applied a second time through another discount control.

### 10. What are the limitations and next steps?
The data are synthetic; no verified competitor prices or causal elasticity exist; gross profit excludes returns, taxes, shipping, payment fees and overhead. I would execute the SQL against PostgreSQL, build and validate the PBIX in Power BI Desktop, add real multi-line orders and historical cost/price records, and estimate price response through controlled tests.

## GitHub repository metadata
- Repository name: `pricing-optimization-dashboard`
- Description: `End-to-end synthetic retail pricing analytics with Python ETL, PostgreSQL SQL, Excel reporting, Power BI DAX/model specification, what-if scenarios, and automated PDF/CSV outputs.`
- Topics: `data-analytics`, `pricing-analytics`, `business-intelligence`, `sql`, `postgresql`, `excel`, `power-bi`, `dax`, `python`, `pandas`, `data-quality`, `profitability-analysis`, `dashboard`, `portfolio-project`
