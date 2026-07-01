import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Analytics", layout="wide")

@st.cache_data
def load_data():
    df  = pd.read_csv('data/clean_data.csv', parse_dates=['InvoiceDate'])
    rfm = pd.read_csv('data/rfm_segments.csv')
    return df, rfm

df, rfm = load_data()

# ── Sidebar ───────────────────────────────────────────
st.sidebar.header("Filters")
countries = ['All'] + sorted(df['Country'].unique().tolist())
selected_country = st.sidebar.selectbox("Country", countries)

if selected_country != 'All':
    df = df[df['Country'] == selected_country]

# ── Title ─────────────────────────────────────────────
st.title("🛒 E-Commerce Sales & Customer Segmentation")
st.caption("Dataset: UCI Online Retail II | 800k+ transactions | 2009–2011")

# ── KPI Cards ─────────────────────────────────────────
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue",   f"£{df['TotalPrice'].sum():,.0f}")
col2.metric("Total Orders",    f"{df['Invoice'].nunique():,}")
col3.metric("Total Customers", f"{df['Customer ID'].nunique():,}")
col4.metric("Avg Order Value", f"£{df.groupby('Invoice')['TotalPrice'].sum().mean():,.2f}")

st.divider()

# ── Monthly Revenue Trend ─────────────────────────────
st.subheader("Monthly Revenue Trend")
df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
monthly = df.groupby('Month')['TotalPrice'].sum().reset_index()
fig1 = px.line(monthly, x='Month', y='TotalPrice',
               markers=True,
               labels={'TotalPrice': 'Revenue (£)', 'Month': ''},
               color_discrete_sequence=['#3498db'])
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ── Top Products & Countries ──────────────────────────
st.subheader("Top 10 Products & Countries")
col1, col2 = st.columns(2)

with col1:
    top_p = df.groupby('Description')['TotalPrice'].sum().nlargest(10).reset_index()
    fig2  = px.bar(top_p, x='TotalPrice', y='Description', orientation='h',
                   labels={'TotalPrice': 'Revenue (£)', 'Description': ''},
                   title='Top 10 Products by Revenue',
                   color_discrete_sequence=['#2ecc71'])
    fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    top_c = df.groupby('Country')['TotalPrice'].sum().nlargest(10).reset_index()
    fig3  = px.bar(top_c, x='TotalPrice', y='Country', orientation='h',
                   labels={'TotalPrice': 'Revenue (£)', 'Country': ''},
                   title='Top 10 Countries by Revenue',
                   color_discrete_sequence=['#e67e22'])
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── Customer Segments ─────────────────────────────────
st.subheader("Customer Segmentation — RFM + K-Means (K=4)")
col1, col2 = st.columns(2)

with col1:
    seg_counts = rfm['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']
    fig4 = px.pie(seg_counts, names='Segment', values='Count',
                  title='Segment Distribution',
                  color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.markdown("**Average RFM values per segment**")
    seg_summary = rfm.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean().round(1)
    seg_summary.columns = ['Avg Recency (days)', 'Avg Frequency', 'Avg Monetary (£)']
    st.dataframe(seg_summary, use_container_width=True)

# ── Scatter Plot ──────────────────────────────────────
st.subheader("Recency vs Monetary by Segment")
fig5 = px.scatter(rfm, x='Recency', y='Monetary',
                  color='Segment', size='Frequency',
                  hover_data=['Customer ID'],
                  labels={'Recency': 'Recency (days)', 'Monetary': 'Monetary (£)'},
                  color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig5, use_container_width=True)