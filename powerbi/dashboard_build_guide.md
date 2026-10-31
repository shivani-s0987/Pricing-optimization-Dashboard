# Power BI Desktop Build Guide (5 pages)

## Import and model
1. Open Power BI Desktop and Get Data > Text/CSV for `data/processed/fact_sales_clean.csv` and all five dimension CSVs.
2. Set `OrderDate`/`Date` to Date, IDs to Text, rates to Decimal Number, quantities to Whole Number, and currency amounts to Fixed Decimal where available.
3. Rename tables as `FactSales`, `DimProduct`, `DimDate`, `DimRegion`, `DimChannel`, `DimCustomerSegment`. Create relationships shown in `data_model.md`, single-direction, dimensions filter fact. Mark DimDate as date table.
4. Add measures from `dax_measures.md`. Set report canvas to 16:9. Import `theme.json` via View > Themes > Browse for themes.
5. Add global date/category/region/channel slicers where useful. Enable sync slicers across pages; keep page-specific slicers clearly labeled. Use a report-level tooltip and clear page navigation buttons.

## Page 1 — Executive Pricing Overview
- Six KPI cards: Net Sales Revenue, Gross Profit, Gross Margin %, Weighted Average Discount %, Units Sold, Average Selling Price.
- Line chart by DimDate[YearMonth] with revenue and gross profit (prefer separate aligned charts if scale differences hide profit movement).
- Clustered bar for category revenue; separate profit chart or small multiples for profit.
- Matrix: Category, revenue, gross profit, margin, weighted discount; conditional format margin.
- Top products bar chart by revenue; table of product review flags; cards for MoM change and growth.

## Page 2 — Product & Category Profitability
- Matrix Category > Subcategory > ProductName with revenue, COGS, profit, margin, units and weighted discount.
- Top/bottom 10 product visuals; rank measures filtered by rank <= 10, plus separate bottom list sorted ascending.
- Margin distribution histogram using a calculated margin grouping or bins on a product-level summary table (not transaction-row margin).
- Drill-through page/filter on ProductID or ProductName; add product revenue/profit trend and channel/region breakdown.

## Page 3 — Discount Effectiveness
- Column chart by Discount Band for revenue and a separate chart for gross profit; line/bar for margin and weighted discount.
- Matrix Category x Discount Band with margin and profit; table of deep-discount products with low/negative profit.
- Tooltip explains discount band boundaries and warns that observational patterns are not causal evidence.

## Page 4 — Pricing Opportunity & Exceptions
- Product exception table: Product, Category, Revenue, Gross Profit, Margin, Weighted Discount, Units, Review reason.
- Flag margin below a configurable target, weighted discount >30%, negative gross profit, selling price below cost, and price/master-data exceptions. Current list price is not a competitor benchmark. No verified competitor benchmark exists in the dataset.
- Add a note: price changes require validation of demand, inventory, product lifecycle, strategic role, and cost freshness.

## Page 5 — What-if Pricing Simulator
- Numeric parameter slicers for price change, assumed demand change, and unit-cost change. Display baseline revenue/profit, scenario revenue/profit/margin, revenue difference, profit difference, and break-even volume measure.
- Price change applies to baseline realized selling price; demand assumption scales units. Do not also apply a separate discount parameter unless a new explicit price-formation formula is designed.
- Add a visible caveat: demand change is a user-entered assumption, not estimated elasticity; all results are illustrative.

## Finish and validate
- Use white/light neutral background, navy text, restrained teal accent, orange/red only for risk. Set titles, subtitle, reporting period, and refresh timestamp (Power BI's refresh timestamp should be sourced from a refresh table or Power Query; do not hardcode it as live).
- Add tooltips and conditional formatting, verify cross-filtering and slicer sync, validate all page metrics against `reports/*.csv`, then save as `powerbi/pricing_optimization_dashboard.pbix` from Desktop. This environment does not include Power BI Desktop authoring, so no PBIX is claimed or supplied.
