import pandas as pd
import os

DATA_FOLDER = r"C:\Users\6139457\Downloads\Maven+Toys\Maven Toys Data"

print("Loading files...")

sales = pd.read_csv(os.path.join(DATA_FOLDER, "sales.csv"))
products = pd.read_csv(os.path.join(DATA_FOLDER, "products.csv"))
stores = pd.read_csv(os.path.join(DATA_FOLDER, "stores.csv"))
inventory = pd.read_csv(os.path.join(DATA_FOLDER, "inventory.csv"))
calendar = pd.read_csv(os.path.join(DATA_FOLDER, "calendar.csv"))
data_dict = pd.read_csv(os.path.join(DATA_FOLDER, "data_dictionary.csv"))

print("All 6 files loaded successfully!\n")

print("=" * 50)
print("SHAPE CHECK")
print("=" * 50)

for name, df in [("sales", sales), ("products", products),
                 ("stores", stores), ("inventory", inventory),
                 ("calendar", calendar), ("data_dict", data_dict)]:
    print(f"{name:15}: {df.shape[0]:>10,} rows  x  {df.shape[1]} columns")

print("\n" + "=" * 50)
print("COLUMN NAMES AND DATA TYPES")
print("=" * 50)

for name, df in [("sales", sales), ("products", products),
                 ("stores", stores), ("inventory", inventory),
                 ("calendar", calendar), ("data_dict", data_dict)]:
    print(f"\n--- {name.upper()} ---")
    print(df.dtypes)

print("\n" + "=" * 50)
print("NULL / MISSING VALUES")
print("=" * 50)

for name, df in [("sales", sales), ("products", products),
                 ("stores", stores), ("inventory", inventory),
                 ("calendar", calendar)]:
    print(f"\n--- {name.upper()} ---")
    null_counts = df.isnull().sum()
    null_pct = (df.isnull().sum() / len(df) * 100).round(2)
    result = pd.DataFrame({
        'null_count': null_counts,
        'null_percent': null_pct
    })
    print(result)

print("\n" + "=" * 50)
print("DUPLICATE ROWS")
print("=" * 50)

for name, df in [("sales", sales), ("products", products),
                 ("stores", stores), ("inventory", inventory),
                 ("calendar", calendar)]:
    dupes = df.duplicated().sum()
    print(f"{name:15}: {dupes} duplicate rows")

print("\n--- Duplicate Primary Keys ---")
print(f"Duplicate Sale_ID:    {sales['Sale_ID'].duplicated().sum()}")
print(f"Duplicate Product_ID: {products['Product_ID'].duplicated().sum()}")
print(f"Duplicate Store_ID:   {stores['Store_ID'].duplicated().sum()}")

print("\n" + "=" * 50)
print("FOREIGN KEY INTEGRITY CHECK")
print("=" * 50)

valid_store_ids = set(stores['Store_ID'].unique())
valid_product_ids = set(products['Product_ID'].unique())

orphan_stores_in_sales = set(sales['Store_ID'].unique()) - valid_store_ids
orphan_products_in_sales = set(sales['Product_ID'].unique()) - valid_product_ids

print(f"Orphan Store_IDs in Sales:    {orphan_stores_in_sales if orphan_stores_in_sales else 'None — All Good!'}")
print(f"Orphan Product_IDs in Sales:  {orphan_products_in_sales if orphan_products_in_sales else 'None — All Good!'}")

orphan_stores_in_inv = set(inventory['Store_ID'].unique()) - valid_store_ids
orphan_products_in_inv = set(inventory['Product_ID'].unique()) - valid_product_ids

print(f"Orphan Store_IDs in Inventory:   {orphan_stores_in_inv if orphan_stores_in_inv else 'None — All Good!'}")
print(f"Orphan Product_IDs in Inventory: {orphan_products_in_inv if orphan_products_in_inv else 'None — All Good!'}")

print("\n" + "=" * 50)
print("DEEP DIVE — PROBLEM COLUMNS")
print("=" * 50)

print("\n--- Products: Cost and Price samples ---")
print(products[['Product_Name', 'Product_Cost', 'Product_Price']].head(10))

print("\n--- Sales: Date column samples ---")
print(sales['Date'].head(10))
print(f"Date dtype: {sales['Date'].dtype}")

print("\n--- Sales: Units range ---")
print(f"Min units:      {sales['Units'].min()}")
print(f"Max units:      {sales['Units'].max()}")
print(f"Negative units: {(sales['Units'] < 0).sum()}")
print(f"Zero units:     {(sales['Units'] == 0).sum()}")

print("\n--- Stores: Location unique values ---")
print(stores['Store_Location'].value_counts())

print("\n--- Products: Category unique values ---")
print(products['Product_Category'].value_counts())

print("\n" + "=" * 50)
print("DATE RANGE CHECK")
print("=" * 50)

sales['Date_temp'] = pd.to_datetime(sales['Date'])
print(f"Earliest sale: {sales['Date_temp'].min()}")
print(f"Latest sale:   {sales['Date_temp'].max()}")
print(f"Total days:    {(sales['Date_temp'].max() - sales['Date_temp'].min()).days}")
print(f"Unique dates:  {sales['Date_temp'].nunique()}")
sales.drop(columns=['Date_temp'], inplace=True)

print("\n" + "=" * 50)
print("DESCRIPTIVE STATISTICS")
print("=" * 50)

for name, df in [("sales", sales), ("products", products),
                 ("stores", stores), ("inventory", inventory)]:
    print(f"\n--- {name.upper()} ---")
    print(df.describe(include='all'))

print("\n" + "=" * 50)
print("SAVING data_quality_notes.md ...")
print("=" * 50)

with open("data_quality_notes.md", "w") as f:
    f.write("# Data Quality Profiling Report\n")
    f.write("## Mexico Toy Sales — Maven Analytics Dataset\n\n")
    f.write("---\n\n")

    f.write("## Table Shapes\n")
    f.write("| Table | Rows | Columns |\n")
    f.write("|---|---|---|\n")
    for name, df in [("sales", sales), ("products", products),
                     ("stores", stores), ("inventory", inventory),
                     ("calendar", calendar)]:
        f.write(f"| {name} | {df.shape[0]:,} | {df.shape[1]} |\n")

    f.write("\n## Issues Found\n")
    f.write("*(Fill this in manually after reviewing the printed output above)*\n\n")
    f.write("### Issue 1: Product_Cost and Product_Price stored as strings\n")
    f.write("- Columns: Product_Cost, Product_Price\n")
    f.write("- Problem: Dollar sign prefix prevents numeric operations\n")
    f.write("- Fix: Strip '$' and CAST to DECIMAL in staging model\n\n")
    f.write("### Issue 2: Date column in Sales stored as string\n")
    f.write("- Column: Date\n")
    f.write("- Problem: dtype is object not datetime\n")
    f.write("- Fix: CAST(Date AS DATE) in stg_maven_toys__sales.sql\n\n")
    f.write("### Issue 3: Extra files found\n")
    f.write("- calendar.csv and data_dictionary.csv found in addition to expected 4 files\n")
    f.write("- calendar.csv may replace the need to build dim_date manually in dbt\n\n")

    f.write("## Clean Checks\n")
    f.write(f"- Orphan Store_IDs in Sales: {orphan_stores_in_sales if orphan_stores_in_sales else 'None'}\n")
    f.write(f"- Orphan Product_IDs in Sales: {orphan_products_in_sales if orphan_products_in_sales else 'None'}\n")
    f.write(f"- Duplicate Sale_IDs: {sales['Sale_ID'].duplicated().sum()}\n")
    f.write(f"- Duplicate Product_IDs: {products['Product_ID'].duplicated().sum()}\n")
    f.write(f"- Duplicate Store_IDs: {stores['Store_ID'].duplicated().sum()}\n")

print("Saved! Check data_quality_notes.md in your folder.")
print("\nPROFILING COMPLETE!")
