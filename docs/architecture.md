# Architecture

Raw synthetic CSVs -> deterministic validation and quarantine -> cleaned fact and dimensions -> PostgreSQL relational schema and analytical views / Excel workbook / Power BI star schema -> generated CSV/Markdown/PDF summaries. Data generation, cleaning, and report generation are local Python batch processes. The database loader uses a locally configured `DATABASE_URL`. Power BI report authoring and cloud scheduling require external desktop/service setup and are not represented as completed here.
