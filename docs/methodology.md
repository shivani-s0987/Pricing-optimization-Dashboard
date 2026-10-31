# Methodology

Seeded synthetic transaction generation uses fixed seed 20261028, a 24-month period, 120 products in 10 categories, 5 regions, 4 channels, and 4 customer segments. Seasonal demand modifiers and controlled product cohorts create interpretable variation; they are design assumptions, not inferred market behavior. Six malformed source rows test quality controls. ETL flags and quarantines invalid quantity, discount, selling price, foreign key, duplicate line ID, and negative cost. Derived selling price and monetary measures are recalculated from primitives for the cleaned table.

Aggregation uses ratio-of-sums for weighted discount and gross margin, not averages of row percentages. Outliers are flagged for investigation, never automatically removed. A 15% margin threshold and 30% weighted discount threshold are screening rules, not universal business policies. Demand changes in scenario analysis are user inputs and not causal elasticity estimates.
