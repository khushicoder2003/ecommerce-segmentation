import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('reports', exist_ok=True)

df = pd.read_csv('data/clean_data.csv', parse_dates=['InvoiceDate'])

sns.set_theme(style='darkgrid')

# ── Plot 1: Top 10 Products by Revenue ────────────────
top_products = (
    df.groupby('Description')['TotalPrice']
    .sum()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
top_products.plot(kind='barh', color='steelblue')
plt.title('Top 10 Products by Revenue')
plt.xlabel('Total Revenue (£)')
plt.tight_layout()
plt.savefig('reports/top_products.png')
plt.show()
print("✓ Plot 1 saved")

# ── Plot 2: Monthly Revenue Trend ─────────────────────
df['Month'] = df['InvoiceDate'].dt.to_period('M')
monthly = df.groupby('Month')['TotalPrice'].sum()

plt.figure(figsize=(12, 5))
monthly.plot(kind='line', marker='o', color='steelblue')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue (£)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('reports/monthly_trend.png')
plt.show()
print("✓ Plot 2 saved")

# ── Plot 3: Top 10 Countries by Revenue ───────────────
top_countries = (
    df.groupby('Country')['TotalPrice']
    .sum()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
top_countries.plot(kind='barh', color='coral')
plt.title('Top 10 Countries by Revenue')
plt.xlabel('Total Revenue (£)')
plt.tight_layout()
plt.savefig('reports/top_countries.png')
plt.show()
print("✓ Plot 3 saved")

# ── Plot 4: Revenue by Day of Week ────────────────────
df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Sunday']
day_rev = df.groupby('DayOfWeek')['TotalPrice'].sum().reindex(day_order)

plt.figure(figsize=(9, 5))
day_rev.plot(kind='bar', color='mediumseagreen')
plt.title('Revenue by Day of Week')
plt.xlabel('Day')
plt.ylabel('Revenue (£)')
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('reports/day_of_week.png')
plt.show()
print("✓ Plot 4 saved")

print("\n✓ All 4 plots saved to reports/")