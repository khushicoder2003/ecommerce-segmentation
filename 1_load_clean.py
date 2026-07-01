import pandas as pd

# ── Load ──────────────────────────────────────────────
df = pd.read_csv('data/online_retail_II.csv', encoding='utf-8')
print(f"Raw shape: {df.shape}")

# ── Clean ─────────────────────────────────────────────

# 1. Drop rows with no Customer ID (can't do RFM without it)
df = df.dropna(subset=['Customer ID'])

# 2. Remove cancelled orders (Invoice starts with 'C')
df = df[~df['Invoice'].astype(str).str.startswith('C')]

# 3. Remove bad quantity and price
df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]

# 4. Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# 5. Create TotalPrice column
df['TotalPrice'] = df['Quantity'] * df['Price']

# 6. Convert Customer ID to integer
df['Customer ID'] = df['Customer ID'].astype(int)

print(f"Clean shape: {df.shape}")
print(f"\nDate range: {df['InvoiceDate'].min()} → {df['InvoiceDate'].max()}")
print(f"Unique customers: {df['Customer ID'].nunique()}")
print(f"Unique products: {df['StockCode'].nunique()}")
print(f"Total revenue: £{df['TotalPrice'].sum():,.2f}")

# 7. Save cleaned data
df.to_csv('data/clean_data.csv', index=False)
print("\n✓ Saved to data/clean_data.csv")