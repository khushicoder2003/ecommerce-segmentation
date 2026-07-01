import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

st.set_page_config(page_title="E-Commerce Analytics", layout="wide")

@st.cache_data
def load_and_process():
    url = "https://raw.githubusercontent.com/khushicoder2003/ecommerce-segmentation/main/data/rfm_segments.csv"
    
    # Try loading rfm from GitHub first
    try:
        rfm = pd.read_csv(url)
        df  = None
        return df, rfm
    except:
        pass

    # Fallback: load local data
    if os.path.exists('data/clean_data.csv'):
        df  = pd.read_csv('data/clean_data.csv', parse_dates=['InvoiceDate'])
        rfm = pd.read_csv('data/rfm_segments.csv')
        return df, rfm

    return None, None

# ── Load ──────────────────────────────────────────────
df, rfm = load_and_process()

if rfm is None:
    st.error("Data not found. Please run 1_load_clean.py and 3_rfm_clustering.py first.")
    st.stop()

# ── Sidebar ───────────────────────────────────────────
st.sidebar.header("Filters")
segments = ['All'] + sorted(rfm['Segment'].unique().tolist())
selected_segment = st.sidebar.selectbox("Customer Segment", segments)

if selected_segment != 'All':
    rfm = rfm[rfm['Segment'] == selected_segment]

# ── Title ─────────────────────────────────────────────
st.title("🛒 E-Commerce Sales & Customer Segmentation")
st.caption("Dataset: UCI Online Retail II | 800k+ transactions | 2009–2011")

# ── KPI Cards from RFM ────────────────────────────────
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue",   f"£{rfm['Monetary'].sum():,.0f}")
col2.metric("Total Customers", f"{len(rfm):,}")
col3.metric("Avg Monetary",    f"£{rfm['Monetary'].mean():,.0f}")
col4.metric("Champions",       f"{len(rfm[rfm['Segment']=='Champions']):,}")

st.divider()

# ── Segment Distribution ──────────────────────────────
st.subheader("Customer Segmentation — RFM + K-Means (K=4)")
col1, col2 = st.columns(2)

with col1:
    seg_counts = rfm['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']
    fig1 = px.pie(seg_counts, names='Segment', values='Count',
                  title='Segment Distribution',
                  color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("**Average RFM values per segment**")
    seg_summary = rfm.groupby('Segment')[['Recency','Frequency','Monetary']].mean().round(1)
    seg_summary.columns = ['Avg Recency (days)', 'Avg Frequency', 'Avg Monetary (£)']
    st.dataframe(seg_summary, use_container_width=True)

st.divider()

# ── RFM Distributions ─────────────────────────────────
st.subheader("RFM Distribution by Segment")
col1, col2, col3 = st.columns(3)

with col1:
    fig2 = px.box(rfm, x='Segment', y='Recency', color='Segment',
                  title='Recency by Segment',
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.box(rfm, x='Segment', y='Frequency', color='Segment',
                  title='Frequency by Segment',
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

with col3:
    fig4 = px.box(rfm, x='Segment', y='Monetary', color='Segment',
                  title='Monetary by Segment',
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Scatter Plot ──────────────────────────────────────
st.subheader("Recency vs Monetary by Segment")
fig5 = px.scatter(rfm, x='Recency', y='Monetary',
                  color='Segment', size='Frequency',
                  hover_data=['Customer ID'],
                  labels={'Recency':'Recency (days)','Monetary':'Monetary (£)'},
                  color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ── High Value Customer Profile ───────────────────────
st.subheader("🏆 High-Value Customer Profile (Champions)")
champions = rfm[rfm['Segment'] == 'Champions']
col1, col2, col3 = st.columns(3)
col1.metric("Count",         f"{len(champions):,} customers")
col2.metric("Avg Spend",     f"£{champions['Monetary'].mean():,.0f}")
col3.metric("Avg Frequency", f"{champions['Frequency'].mean():.0f} orders")
st.caption("Strategy: Reward with loyalty programs and early access")