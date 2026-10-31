# Power BI Data Model

```mermaid
erDiagram
  DIM_DATE ||--o{ FACT_SALES : order_date
  DIM_PRODUCT ||--o{ FACT_SALES : product_id
  DIM_REGION ||--o{ FACT_SALES : region_id
  DIM_CHANNEL ||--o{ FACT_SALES : channel_id
  DIM_CUSTOMER_SEGMENT ||--o{ FACT_SALES : customer_segment_id
  DIM_PRODUCT { string ProductID PK string ProductName string Category string Subcategory decimal CurrentListPrice decimal CurrentUnitCost }
  DIM_DATE { date Date PK int Year string Quarter int MonthNumber string YearMonth }
  DIM_REGION { string RegionID PK string RegionName string StateOrTerritory }
  DIM_CHANNEL { string ChannelID PK string ChannelName }
  DIM_CUSTOMER_SEGMENT { string CustomerSegmentID PK string SegmentName }
  FACT_SALES { string SalesLineID PK string OrderID date OrderDate FK string ProductID FK int Quantity decimal UnitListPrice decimal UnitSellingPrice decimal UnitCost decimal SalesRevenue decimal GrossProfit }
```

Use single-direction dimension-to-fact relationships, 1:* cardinality, no bidirectional filters by default. `DimProduct[CurrentListPrice]` and `[CurrentUnitCost]` are current master attributes; they are not historical transaction prices. Historical realized price and cost are in FactSales. `DimDate[Date]` must be marked as the date table. The synthetic source has one sales line per OrderID; real data generally needs multiple lines per order and distinct order counts must remain distinct-count measures.
