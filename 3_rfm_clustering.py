import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

os.makedirs('reports', exist_ok=True)

df = pd.read_csv('data/clean_data.csv', parse_dates=['InvoiceDate'])

# ── RFM Calculation ───────────────────────────────────
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('Customer ID').agg(
    Recency   = ('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
    Frequency = ('Invoice',     'nunique'),
    Monetary  = ('TotalPrice',  'sum')
).reset_index()

print("RFM Table Sample:")
print(rfm.head())
print(f"\nShape: {rfm.shape}")

# ── Scale & cluster ───────────────────────────────────
rfm_log    = np.log1p(rfm[['Recency', 'Frequency', 'Monetary']])
scaler     = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_log)

# ── Elbow Method ──────────────────────────────────────
inertia = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(rfm_scaled)
    inertia.append(km.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inertia, marker='o', color='steelblue')
plt.title('Elbow Method — Choosing Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.tight_layout()
plt.savefig('reports/elbow_curve.png')
plt.show()
print("✓ Elbow curve saved")

# ── K-Means with K=4 ──────────────────────────────────
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

# ── Cluster summary ───────────────────────────────────
summary = rfm.groupby('Cluster').agg(
    Recency   = ('Recency',      'mean'),
    Frequency = ('Frequency',    'mean'),
    Monetary  = ('Monetary',     'mean'),
    Count     = ('Customer ID',  'count')
).round(1)

print("\nCluster Summary:")
print(summary)

# ── Label clusters ────────────────────────────────────
# Hard-code based on what the cluster summary clearly shows
labels = {
    0: 'Champions',
    1: 'At-Risk',
    2: 'Loyal Customers',
    3: 'New Customers'
}
rfm['Segment'] = rfm['Cluster'].map(labels)

print("\nSegment counts:")
print(rfm['Segment'].value_counts())

# ── Plot 1: Segment Pie Chart ─────────────────────────
plt.figure(figsize=(7, 7))
rfm['Segment'].value_counts().plot(
    kind='pie', autopct='%1.1f%%',
    colors=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'],
    startangle=140
)
plt.title('Customer Segment Distribution')
plt.ylabel('')
plt.tight_layout()
plt.savefig('reports/segment_pie.png')
plt.show()
print("✓ Segment pie chart saved")

# ── Plot 2: RFM Boxplots ──────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, col in zip(axes, ['Recency', 'Frequency', 'Monetary']):
    sns.boxplot(data=rfm, x='Segment', y=col, hue='Segment',
                ax=ax, palette='Set2', legend=False)
    ax.set_title(f'{col} by Segment')
    ax.tick_params(axis='x', rotation=15)
plt.tight_layout()
plt.savefig('reports/rfm_boxplots.png')
plt.show()
print("✓ RFM boxplots saved")

# ── Plot 3: Scatter Recency vs Monetary ───────────────
plt.figure(figsize=(10, 6))
colors = {'Champions': '#2ecc71', 'Loyal Customers': '#3498db',
          'At-Risk': '#e74c3c', 'New Customers': '#f39c12'}
for seg, group in rfm.groupby('Segment'):
    plt.scatter(group['Recency'], group['Monetary'],
                label=seg, alpha=0.5, color=colors[seg], s=20)
plt.title('Customer Segments — Recency vs Monetary')
plt.xlabel('Recency (days)')
plt.ylabel('Monetary (£)')
plt.legend()
plt.tight_layout()
plt.savefig('reports/segment_scatter.png')
plt.show()
print("✓ Scatter plot saved")

# ── Save RFM data ─────────────────────────────────────
rfm.to_csv('data/rfm_segments.csv', index=False)
print("\n✓ RFM data saved to data/rfm_segments.csv")
print("Done! Check reports/ for all charts.")