# Data files

All records are synthetic, generated with fixed seed `20261028`; no real customers or business results are represented. `raw/` contains source CSVs including six deliberately imperfect transaction records. `processed/` contains validated fact and dimension CSVs plus quarantined rows and a JSON quality report. Rebuild with `python python/generate_dataset.py`.

Grain: one row per order product line. `OrderID` is unique per line in this demonstration dataset, so distinct order count is equivalent to distinct `OrderID`; in real multi-line orders it would not be. Currency is illustrative and not tied to a specified currency.
