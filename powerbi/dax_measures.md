# Power BI DAX Measures

Assumptions: import `fact_sales_clean.csv` as `FactSales`; dimensions as `DimProduct`, `DimDate`, `DimRegion`, `DimChannel`, `DimCustomerSegment`. Create active one-to-many relationships from each dimension key to the corresponding fact key. Mark `DimDate[Date]` as the date table. Currency units are illustrative. Create the following as measures unless marked calculated column.

```DAX
Gross Revenue Before Discount = SUMX(FactSales, FactSales[Quantity] * FactSales[UnitListPrice])
Discount Amount = SUMX(FactSales, FactSales[Quantity] * (FactSales[UnitListPrice] - FactSales[UnitSellingPrice]))
Net Sales Revenue = SUM(FactSales[SalesRevenue])
Cost of Goods Sold = SUM(FactSales[CostOfGoodsSold])
Gross Profit = [Net Sales Revenue] - [Cost of Goods Sold]
Gross Margin % = DIVIDE([Gross Profit], [Net Sales Revenue], 0)
Weighted Average Discount % = DIVIDE([Discount Amount], [Gross Revenue Before Discount], 0)
Units Sold = SUM(FactSales[Quantity])
Distinct Orders = DISTINCTCOUNT(FactSales[OrderID])
Average Selling Price = DIVIDE([Net Sales Revenue], [Units Sold], 0)
Profit per Unit = DIVIDE([Gross Profit], [Units Sold], 0)
Revenue per Order = DIVIDE([Net Sales Revenue], [Distinct Orders], 0)
Revenue Previous Month = CALCULATE([Net Sales Revenue], DATEADD(DimDate[Date], -1, MONTH))
Revenue MoM Change = [Net Sales Revenue] - [Revenue Previous Month]
Revenue MoM Growth % = DIVIDE([Revenue MoM Change], [Revenue Previous Month], BLANK())
Gross Profit Previous Month = CALCULATE([Gross Profit], DATEADD(DimDate[Date], -1, MONTH))
Gross Profit MoM Change = [Gross Profit] - [Gross Profit Previous Month]
Revenue Previous Year = CALCULATE([Net Sales Revenue], DATEADD(DimDate[Date], -1, YEAR))
Revenue YoY Growth % = DIVIDE([Net Sales Revenue] - [Revenue Previous Year], [Revenue Previous Year], BLANK())
Gross Profit YoY Growth % = DIVIDE([Gross Profit] - CALCULATE([Gross Profit], DATEADD(DimDate[Date], -1, YEAR)), CALCULATE([Gross Profit], DATEADD(DimDate[Date], -1, YEAR)), BLANK())
Revenue Share % = DIVIDE([Net Sales Revenue], CALCULATE([Net Sales Revenue], ALLSELECTED(DimProduct)), 0)
Profit Contribution % = DIVIDE([Gross Profit], CALCULATE([Gross Profit], ALLSELECTED(DimProduct)), 0)
Product Rank by Revenue = RANKX(ALLSELECTED(DimProduct[ProductName]), [Net Sales Revenue],, DESC, DENSE)
Product Rank by Gross Profit = RANKX(ALLSELECTED(DimProduct[ProductName]), [Gross Profit],, DESC, DENSE)
Rolling 3-Month Revenue = CALCULATE([Net Sales Revenue], DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -3, MONTH))
Rolling 3-Month Gross Profit = CALCULATE([Gross Profit], DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -3, MONTH))
Selected Period Revenue = [Net Sales Revenue]
Low-Margin Product Flag = IF([Gross Margin %] < SELECTEDVALUE('Pricing Targets'[Target Margin], 0.15), 1, 0)
High-Discount Product Flag = IF([Weighted Average Discount %] > 0.30, 1, 0)
Pricing Review Flag = IF([Low-Margin Product Flag] = 1 || [High-Discount Product Flag] = 1 || [Gross Profit] < 0, 1, 0)
```

Create `Pricing Targets` as a disconnected table with a numeric `Target Margin` column (e.g. 0.10, 0.15, 0.20, 0.25); set default via slicer or replace with a constant. For dynamic discount bands, create a calculated column on FactSales:

```DAX
Discount Band = SWITCH(TRUE(), FactSales[DiscountPct] = 0, "0%", FactSales[DiscountPct] <= 0.05, ">0-5%", FactSales[DiscountPct] <= 0.10, ">5-10%", FactSales[DiscountPct] <= 0.20, ">10-20%", FactSales[DiscountPct] <= 0.30, ">20-30%", ">30%")
```

`Low-Margin Product Flag`, `High-Discount Product Flag`, and `Pricing Review Flag` are measures and should be used in product-level visuals. A product flag may behave differently when no product is in filter context; use in a product table. `Selected Period Revenue` follows the current filter context; it is not a separate parameter. Time intelligence requires a contiguous, marked date table. Previous-month/year results are blank where no matching comparison period exists. Format revenue/profit/ASP as currency, percentages as percentages, and units/orders as whole numbers.

## What-if scenario parameters

Create numeric parameter tables (Modeling > New parameter, or disconnected tables) with a single selected value each: `Price Change %` (-0.20 to +0.20, step .01), `Demand Change %` (-0.50 to +0.50, step .01), `Cost Change %` (-0.20 to +0.20, step .01). This implementation uses a price change on the baseline realized selling price; do not also apply a second discount change.

```DAX
Scenario Price Change % = SELECTEDVALUE('Price Change %'[Price Change % Value], 0)
Scenario Demand Change % = SELECTEDVALUE('Demand Change %'[Demand Change % Value], 0)
Scenario Cost Change % = SELECTEDVALUE('Cost Change %'[Cost Change % Value], 0)
Scenario Revenue = SUMX(FactSales, FactSales[UnitSellingPrice] * (1 + [Scenario Price Change %]) * FactSales[Quantity] * (1 + [Scenario Demand Change %]))
Scenario COGS = SUMX(FactSales, FactSales[UnitCost] * (1 + [Scenario Cost Change %]) * FactSales[Quantity] * (1 + [Scenario Demand Change %]))
Scenario Gross Profit = [Scenario Revenue] - [Scenario COGS]
Scenario Gross Margin % = DIVIDE([Scenario Gross Profit], [Scenario Revenue], 0)
Revenue Difference = [Scenario Revenue] - [Net Sales Revenue]
Gross Profit Difference = [Scenario Gross Profit] - [Gross Profit]
Break-even Scenario Units = DIVIDE([Scenario COGS], SUMX(FactSales, FactSales[UnitSellingPrice] * (1 + [Scenario Price Change %])), BLANK())
```

These formulas assume demand scales uniformly over the filtered baseline units and prices/costs. They do not estimate elasticity. For real pricing decisions, constrain scenarios with inventory, capacity, competitive and customer-segment context.
