import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os, sys

# ── Load data ─────────────────────────────────────────────
@st.cache_data
def load_data():
    paths = [
        "../dataset/cs-training.csv",
        "dataset/cs-training.csv",
        "cs-training.csv",
    ]
    for p in paths:
        if os.path.exists(p):
            return pd.read_csv(p, index_col=0)
    # Demo data jika file belum tersedia
    np.random.seed(42)
    n = 2000
    return pd.DataFrame({
        'SeriousDlqin2yrs': np.random.binomial(1, 0.067, n),
        'RevolvingUtilizationOfUnsecuredLines': np.clip(np.random.beta(0.5,2,n), 0, 1),
        'age': np.random.randint(21, 90, n),
        'NumberOfTime30-59DaysPastDueNotWorse': np.random.poisson(0.3, n),
        'DebtRatio': np.clip(np.random.exponential(0.35, n), 0, 3),
        'MonthlyIncome': np.random.lognormal(8.2, 0.6, n),
        'NumberOfOpenCreditLinesAndLoans': np.random.poisson(8, n),
        'NumberOfTimes90DaysLate': np.random.poisson(0.1, n),
        'NumberRealEstateLoansOrLines': np.random.poisson(1, n),
        'NumberOfTime60-89DaysPastDueNotWorse': np.random.poisson(0.1, n),
        'NumberOfDependents': np.random.poisson(0.8, n),
    })

df = load_data()
df_clean = df.copy()
df_clean['MonthlyIncome'].fillna(df_clean['MonthlyIncome'].median(), inplace=True)
df_clean['NumberOfDependents'].fillna(0, inplace=True)

PLOT_DARK = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(15,23,42,0.6)',
    font=dict(color='#94a3b8', family='DM Sans'),
    xaxis=dict(gridcolor='rgba(99,202,183,0.08)', linecolor='rgba(99,202,183,0.15)'),
    yaxis=dict(gridcolor='rgba(99,202,183,0.08)', linecolor='rgba(99,202,183,0.15)'),
    margin=dict(l=20,r=20,t=40,b=20),
)

# ── Header ────────────────────────────────────────────────
st.markdown("<div class='section-header'>Dataset Overview</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Give Me Some Credit - Kaggle Competition Dataset</div>", unsafe_allow_html=True)

# ── Key stats ─────────────────────────────────────────────
c1,c2,c3,c4,c5 = st.columns(5)
missing = df.isnull().sum().sum()
default_rate = df['SeriousDlqin2yrs'].mean()*100
stats = [
    (f"{len(df):,}", "Total Records"),
    (f"{df.shape[1]}", "Fitur"),
    (f"{missing:,}", "Missing Values"),
    (f"{default_rate:.2f}%", "Default Rate"),
    (f"{df['age'].median():.0f} thn", "Median Usia"),
]
for col, (v, l) in zip([c1,c2,c3,c4,c5], stats):
    with col:
        st.markdown(f"""
        <div class='metric-card' style='text-align:center;padding:1rem;'>
            <div class='metric-value' style='font-size:1.5rem;'>{v}</div>
            <div class='metric-label' style='margin-top:0.3rem;'>{l}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Data Dictionary ───────────────────────────────────────
with st.expander("Data Dictionary", expanded=False):
    dd = pd.DataFrame({
        'Fitur': ['SeriousDlqin2yrs','RevolvingUtilizationOfUnsecuredLines','age',
                  'NumberOfTime30-59DaysPastDueNotWorse','DebtRatio','MonthlyIncome',
                  'NumberOfOpenCreditLinesAndLoans','NumberOfTimes90DaysLate',
                  'NumberRealEstateLoansOrLines','NumberOfTime60-89DaysPastDueNotWorse',
                  'NumberOfDependents'],
        'Tipe': ['Target','Float','Int','Int','Float','Float','Int','Int','Int','Int','Int'],
        'Deskripsi': [
            'Gagal bayar serius dalam 2 tahun (1=Ya, 0=Tidak)',
            'Rasio penggunaan kredit bergulir (0–1)',
            'Usia nasabah (tahun)',
            'Jumlah keterlambatan 30-59 hari',
            'Rasio utang terhadap pendapatan',
            'Pendapatan bulanan (USD)',
            'Jumlah kredit & pinjaman aktif',
            'Jumlah keterlambatan >90 hari',
            'Jumlah kredit properti',
            'Jumlah keterlambatan 60-89 hari',
            'Jumlah tanggungan keluarga',
        ]
    })
    st.dataframe(dd, use_container_width=True, hide_index=True)

# ── Sample data ───────────────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.1rem;'>Sample Data</div>", unsafe_allow_html=True)
st.dataframe(df.head(10), use_container_width=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Charts row 1 ─────────────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.2rem;'>Distribusi & Statistik</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Target distribution
    vc = df['SeriousDlqin2yrs'].value_counts()
    fig = go.Figure(go.Pie(
        labels=['Tidak Default', 'Default'],
        values=vc.values,
        hole=0.55,
        marker=dict(colors=['#63cab7','#f87171'],
                    line=dict(color='#0a0f1e', width=3)),
        textfont=dict(color='white', size=12),
    ))
    fig.update_layout(title='Distribusi Target (Default)', **PLOT_DARK,
                      legend=dict(font=dict(color='#94a3b8')),
                      annotations=[dict(text=f"<b>{default_rate:.1f}%</b><br>Default",
                                        x=0.5, y=0.5, font_size=14,
                                        font_color='#f87171', showarrow=False)])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Age distribution
    fig = px.histogram(df_clean, x='age', nbins=40,
                       color_discrete_sequence=['#63cab7'],
                       title='Distribusi Usia Nasabah')
    fig.update_traces(marker_line_color='#0a0f1e', marker_line_width=0.5, opacity=0.85)
    fig.update_layout(**PLOT_DARK)
    st.plotly_chart(fig, use_container_width=True)

# ── Charts row 2 ─────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    # Monthly income box by default
    df_plot = df_clean[df_clean['MonthlyIncome'] < df_clean['MonthlyIncome'].quantile(0.95)].copy()
    df_plot['Status'] = df_plot['SeriousDlqin2yrs'].map({0:'Tidak Default', 1:'Default'})
    fig = px.box(df_plot, x='Status', y='MonthlyIncome',
                 color='Status',
                 color_discrete_map={'Tidak Default':'#63cab7','Default':'#f87171'},
                 title='Distribusi Pendapatan vs Status')
    fig.update_layout(**PLOT_DARK, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    # Debt ratio distribution
    df_dr = df_clean[df_clean['DebtRatio'] < df_clean['DebtRatio'].quantile(0.95)]
    fig = px.histogram(df_dr, x='DebtRatio', nbins=50,
                       color='SeriousDlqin2yrs',
                       color_discrete_sequence=['#63cab7','#f87171'],
                       barmode='overlay', opacity=0.7,
                       title='Debt Ratio: Default vs Tidak Default',
                       labels={'SeriousDlqin2yrs':'Status'})
    fig.update_layout(**PLOT_DARK,
                      legend=dict(font=dict(color='#94a3b8'),
                                  title_text='Default'))
    st.plotly_chart(fig, use_container_width=True)

# ── Correlation heatmap ───────────────────────────────────
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header' style='font-size:1.2rem;'>Korelasi Antar Fitur</div>", unsafe_allow_html=True)

corr = df_clean.corr().round(2)
fig = go.Figure(go.Heatmap(
    z=corr.values,
    x=corr.columns.tolist(),
    y=corr.index.tolist(),
    colorscale=[[0,'#f87171'],[0.5,'#1e293b'],[1,'#63cab7']],
    zmid=0,
    text=corr.values.round(2),
    texttemplate='%{text}',
    textfont=dict(size=9, color='white'),
    hoverongaps=False,
))
fig.update_layout(**{k:v for k,v in PLOT_DARK.items() if k not in ('margin','xaxis','yaxis')},
                  height=480,
                  margin=dict(l=120,r=20,t=40,b=100),
                  xaxis=dict(tickangle=-35, tickfont=dict(size=9)),
                  yaxis=dict(tickfont=dict(size=9)))
st.plotly_chart(fig, use_container_width=True)

# ── Descriptive stats ─────────────────────────────────────
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header' style='font-size:1.2rem;'>Statistik Deskriptif</div>", unsafe_allow_html=True)
st.dataframe(df_clean.describe().round(3), use_container_width=True)
