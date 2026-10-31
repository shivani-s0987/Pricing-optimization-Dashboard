# Executive Summary — Pricing Optimization Dashboard

**Generated:** 2026-10-28T12:03:24.506090+00:00  
**Period:** 2024-01-01 to 2025-12-31  
**Data:** synthetic, seed 20261028; findings are illustrative only.

## KPI snapshot

- Net sales revenue: **4,716,195.44**
- Gross profit: **1,438,514.27**
- Gross margin: **30.50%**
- Weighted average discount: **10.22%**
- Units sold: **51,458**
- Distinct orders: **20,000** (the generated grain uses one line per order)

## Findings calculated from this run

1. Sports has the highest observed revenue at 554,810.19 (11.8% of all revenue).
2. Sports contributes the highest category gross profit at 190,813.09.
3. Overall gross margin is 30.5%; weighted average discount is 10.2%.
4. The >30% discount band records revenue 289,314.72, gross profit 2,270.31, and margin 0.8%; this is descriptive, not causal evidence.
5. 26 products are flagged by the transparent screening rules (margin below 15%, weighted discount above 30%, or negative gross profit).

## Recommended investigations

1. Review flagged products with adequate unit volume first; a low-volume flag should be treated as weak evidence.
2. Compare discount bands within the same product/category/channel and use controlled tests before attributing demand changes to discounts.
3. Check unit costs and list prices against current approved master data before taking pricing action.
4. Investigate below-cost sales for clearance, bundles, promotions, or data defects before raising prices.

## Limitations

Synthetic observational data cannot establish causal discount elasticity or actual commercial impact. Gross profit excludes shipping, returns, taxes, payment fees, marketing, and other operating costs; it is not net profit. Competitor prices are not verified in this dataset. Currency is illustrative.
