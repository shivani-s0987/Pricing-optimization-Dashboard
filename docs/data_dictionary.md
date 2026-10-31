# Data Dictionary

- **FactSales:** one product line per order; IDs link to dimensions. `UnitListPrice`, `UnitSellingPrice`, and `UnitCost` are historical line-level values. Amounts are line totals. `DiscountPct` is a fraction from 0 inclusive to 1 exclusive. `GrossMarginPct = GrossProfit / SalesRevenue`; it may be negative when selling price is below cost.
- **DimProduct:** product attributes and current reference list price/unit cost. These current values are not substitutes for historical transaction values.
- **DimDate:** contiguous calendar date with year, quarter, month, year-month, week and weekend attributes.
- **DimRegion:** region, state/territory, market type.
- **DimChannel:** channel ID and channel label.
- **DimCustomerSegment:** synthetic customer segment labels; no personal/customer-level data is included.
- **Quarantined rows:** raw source lines with validation reasons. Retain for audit and do not silently discard.

Money is synthetic and no currency is asserted. Shipping, returns, taxes, payment fees, fulfillment, marketing and other operating costs are excluded.
