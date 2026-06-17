# Data Quality Profiling Report
## Mexico Toy Sales � Maven Analytics Dataset

---

## Table Shapes
| Table | Rows | Columns |
|---|---|---|
| sales | 829,262 | 5 |
| products | 35 | 5 |
| stores | 50 | 5 |
| inventory | 1,593 | 3 |
| calendar | 638 | 1 |

## Issues Found
*(Fill this in manually after reviewing the printed output above)*

### Issue 1: Product_Cost and Product_Price stored as strings
- Columns: Product_Cost, Product_Price
- Problem: Dollar sign prefix prevents numeric operations
- Fix: Strip '$' and CAST to DECIMAL in staging model

### Issue 2: Date column in Sales stored as string
- Column: Date
- Problem: dtype is object not datetime
- Fix: CAST(Date AS DATE) in stg_maven_toys__sales.sql

### Issue 3: Extra files found
- calendar.csv and data_dictionary.csv found in addition to expected 4 files
- calendar.csv may replace the need to build dim_date manually in dbt

## Clean Checks
- Orphan Store_IDs in Sales: None
- Orphan Product_IDs in Sales: None
- Duplicate Sale_IDs: 0
- Duplicate Product_IDs: 0
- Duplicate Store_IDs: 0
