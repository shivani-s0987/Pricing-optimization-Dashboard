# Portfolio Case Study: Pricing Optimization and Profitability Intelligence

## Business challenge
Retail teams can over-focus on revenue while missing margin erosion from deep discounts, high unit costs, or inconsistent pricing. The analytical objective is to surface where product-level investigation may be valuable.

## Analytical process
Created a seeded synthetic dataset with 20,000 clean line items across 120 products and 10 categories. Built a validation pipeline that quarantines six intentionally invalid source records. Defined gross revenue, discount amount, net sales, COGS, gross profit, gross margin and weighted discount consistently. Prepared PostgreSQL schema/views and 20 analytical queries, a structured Excel workbook, Power BI star-schema/DAX/page specifications, and a report generator that emits CSV, Markdown and PDF artifacts.

## Output and decision support
The current generated run has 4,716,195.44 in net sales revenue, 1,438,514.27 gross profit, and a 30.50% aggregate gross margin. Screening rules flag 26 products for review. These are calculated synthetic values only. Product-level findings should be checked against volume, strategic role, costs, inventory and customer response before action.

## Limitations and next steps
No real customer/company data, verified competitor benchmark, causal elasticity, or experimentally measured price impact is included. PostgreSQL execution and Power BI PBIX validation remain external setup steps. The next step is to build the PBIX, reconcile it against generated CSV outputs, and validate candidate pricing hypotheses through controlled experiments.
