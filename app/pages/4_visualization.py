import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

np.random.seed(42)
PLOT_DARK = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(15,23,42,0.6)',
    font=dict(color='#94a3b8', family='DM Sans'),
    xaxis=dict(gridcolor='rgba(99,202,183,0.08)', linecolor='rgba(99,202,183,0.15)'),
    yaxis=dict(gridcolor='rgba(99,202,183,0.08)', linecolor='rgba(99,202,183,0.15)'),
    margin=dict(l=20,r=20,t=50,b=30),
)

# ── Synthetic cluster data for visualization ───────────────
@st.cache_data
def generate_cluster_data():
    n = [69252, 29536, 51212]
    labels, revs, ages, incomes, debts, credits, lates = [], [], [], [], [], [], []
    params = [
        (0.40, 49, 4382, 0.33, 6.0, 0.085),
        (0.27, 56, 4992, 9.92, 7.5, 0.055),
        (0.24, 55, 8973, 0.46, 12.1, 0.049),
    ]
    for i, (rev_m, age_m, inc_m, dr_m, cr_m, _) in enumerate(params):
        ni = n[i]
        labels.extend([i]*ni)
        revs.extend(np.clip(np.random.normal(rev_m, 0.15, ni), 0, 1))
        ages.extend(np.clip(np.random.normal(age_m, 10, ni), 18, 100))
        incomes.extend(np.clip(np.random.normal(inc_m, 1500, ni), 0, 30000))
        debts.extend(np.clip(np.random.normal(dr_m, 0.5, ni), 0, 20))
        credits.extend(np.clip(np.random.normal(cr_m, 3, ni), 0, 30))
        lates.extend(np.random.poisson(0.3 if i==0 else 0.1, ni))
    return pd.DataFrame({
        'Cluster': labels,
        'RevolvingUtilization': revs, 'age': ages,
        'MonthlyIncome': incomes, 'DebtRatio': debts,
        'OpenCredits': credits, 'LatePayments': lates,
        'ClusterLabel': [['Berisiko Tinggi','Berisiko Menengah','Berisiko Rendah'][l] for l in labels],
    })

df_c = generate_cluster_data()
COLOR_MAP = {'Berisiko Tinggi':'#f87171','Berisiko Menengah':'#fbbf24','Berisiko Rendah':'#63cab7'}

# ── Header ────────────────────────────────────────────────
st.markdown("<div class='section-header'>Visualization</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Analisis visual hasil clustering dan distribusi fitur antar segmen</div>", unsafe_allow_html=True)

# ── Cluster distribution ──────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.1rem;'>Distribusi Segmen Nasabah</div>", unsafe_allow_html=True)
v1, v2 = st.columns(2)

with v1:
    counts = df_c['ClusterLabel'].value_counts().reset_index()
    counts.columns = ['Segmen','Jumlah']
    fig = go.Figure(go.Bar(
        x=counts['Segmen'], y=counts['Jumlah'],
        marker=dict(color=[COLOR_MAP[s] for s in counts['Segmen']],
                    line=dict(color='#0a0f1e',width=1)),
        text=counts['Jumlah'].apply(lambda x: f"{x:,}"),
        textposition='outside', textfont=dict(color='#94a3b8', size=11),
    ))
    fig.update_layout(title='Jumlah Nasabah per Segmen', **PLOT_DARK,
                      showlegend=False, yaxis_title='Nasabah')
    st.plotly_chart(fig, use_container_width=True)

with v2:
    dr_data = pd.DataFrame({
        'Segmen': ['Berisiko Tinggi','Berisiko Menengah','Berisiko Rendah'],
        'Default Rate (%)': [8.48, 5.51, 4.93],
    })
    fig = go.Figure(go.Bar(
        x=dr_data['Segmen'], y=dr_data['Default Rate (%)'],
        marker=dict(color=[COLOR_MAP[s] for s in dr_data['Segmen']],
                    line=dict(color='#0a0f1e',width=1)),
        text=dr_data['Default Rate (%)'].apply(lambda x: f"{x:.2f}%"),
        textposition='outside', textfont=dict(color='#94a3b8', size=11),
    ))
    fig.update_layout(title='Default Rate per Segmen', **PLOT_DARK,
                      showlegend=False, yaxis_title='Default Rate (%)')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Scatter 2D ────────────────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.1rem;'>Sebaran Cluster - Income vs Revolving Utilization</div>", unsafe_allow_html=True)

sample = df_c.sample(3000)
fig = px.scatter(sample, x='MonthlyIncome', y='RevolvingUtilization',
                 color='ClusterLabel', color_discrete_map=COLOR_MAP,
                 opacity=0.6, size_max=5,
                 labels={'MonthlyIncome':'Pendapatan Bulanan (USD)',
                         'RevolvingUtilization':'Rasio Kredit Bergulir',
                         'ClusterLabel':'Segmen'})
fig.update_traces(marker=dict(size=4))
fig.update_layout(**PLOT_DARK, height=420,
                  legend=dict(font=dict(color='#94a3b8'), bgcolor='rgba(0,0,0,0)'))
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Box plots ─────────────────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.1rem;'>Distribusi Fitur per Segmen</div>", unsafe_allow_html=True)

feat_sel = st.selectbox("Pilih fitur:", ['MonthlyIncome','RevolvingUtilization','age','DebtRatio','OpenCredits'])
fig = px.box(df_c, x='ClusterLabel', y=feat_sel,
             color='ClusterLabel', color_discrete_map=COLOR_MAP,
             labels={'ClusterLabel':'Segmen', feat_sel: feat_sel})
fig.update_layout(**PLOT_DARK, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Radar chart ───────────────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.1rem;'>Radar Chart - Profil Rata-Rata Segmen</div>", unsafe_allow_html=True)

radar_feats = ['RevolvingUtilization','age','MonthlyIncome','DebtRatio','OpenCredits']
profile = df_c.groupby('ClusterLabel')[radar_feats].mean()

# Normalize 0-1
norm = (profile - profile.min()) / (profile.max() - profile.min())
norm = norm.fillna(0)

fig = go.Figure()
colors_radar = ['#f87171','#fbbf24','#63cab7']
fill_colors  = ['rgba(248,113,113,0.15)','rgba(251,191,36,0.15)','rgba(99,202,183,0.15)']
for i, (idx, row) in enumerate(norm.iterrows()):
    vals = row.tolist() + [row.tolist()[0]]
    cats = radar_feats + [radar_feats[0]]
    fig.add_trace(go.Scatterpolar(
        r=vals, theta=cats, fill='toself', name=idx,
        line=dict(color=colors_radar[i], width=2),
        fillcolor=fill_colors[i],
    ))

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    polar=dict(
        bgcolor='rgba(15,23,42,0.6)',
        radialaxis=dict(gridcolor='rgba(99,202,183,0.1)', linecolor='rgba(99,202,183,0.15)', tickfont=dict(size=8,color='#475569')),
        angularaxis=dict(gridcolor='rgba(99,202,183,0.1)', linecolor='rgba(99,202,183,0.15)', tickfont=dict(size=9,color='#94a3b8')),
    ),
    legend=dict(font=dict(color='#94a3b8'), bgcolor='rgba(0,0,0,0)'),
    font=dict(color='#94a3b8', family='DM Sans'),
    margin=dict(l=60,r=60,t=40,b=40),
    height=420,
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Model evaluation ──────────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.1rem;'>Evaluasi Model Clustering</div>", unsafe_allow_html=True)

e1, e2, e3 = st.columns(3)
evals = [
    ("Silhouette Score", "0.2347", "Lebih tinggi = cluster lebih terpisah", "badge-teal"),
    ("Davies-Bouldin Index", "1.572", "Lebih rendah = cluster lebih compact", "badge-amber"),
    ("Calinski-Harabasz", "39,217", "Lebih tinggi = separasi lebih baik", "badge-teal"),
]
for col, (name, val, desc, badge) in zip([e1,e2,e3], evals):
    with col:
        st.markdown(f"""
        <div class='metric-card' style='text-align:center;padding:1.2rem;'>
            <div class='metric-label'>{name}</div>
            <div class='metric-value' style='font-size:1.8rem;'>{val}</div>
            <div class='metric-sub'>{desc}</div>
            <div style='margin-top:0.6rem;'><span class='badge {badge}'>K-Means K=3</span></div>
        </div>
        """, unsafe_allow_html=True)

# ── Elbow / silhouette curve (synthetic) ──────────────────
st.markdown("<br>", unsafe_allow_html=True)
k_range = list(range(2, 9))
sil_vals = [0.1866, 0.2347, 0.2305, 0.2088, 0.2148, 0.2273, 0.2298]
inertia_vals = [724885, 590978, 501268, 451392, 409916, 384720, 361204]

fig = make_subplots(rows=1, cols=2, subplot_titles=('Silhouette Score per K', 'Elbow Method - Inertia'))
fig.add_trace(go.Scatter(x=k_range, y=sil_vals, mode='lines+markers',
    line=dict(color='#f87171', width=2.5),
    marker=dict(size=8, color=['#fbbf24' if k==3 else '#f87171' for k in k_range]),
    name='Silhouette'), row=1, col=1)
fig.add_trace(go.Scatter(x=k_range, y=inertia_vals, mode='lines+markers',
    line=dict(color='#63cab7', width=2.5),
    marker=dict(size=8, color='#63cab7'),
    name='Inertia'), row=1, col=2)
fig.add_vline(x=3, line_dash='dash', line_color='#fbbf24', line_width=1.5, row=1, col=1)
fig.update_layout(**PLOT_DARK, height=340, showlegend=False)
st.plotly_chart(fig, use_container_width=True)
