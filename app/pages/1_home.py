import streamlit as st

# ── Hero ───────────────────────────────────────────────────
st.markdown("""
<div style='padding: 3rem 0 1rem 0;'>
    <div style='display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem;'>
        <span class='badge badge-teal'>Data Mining · UAS 2025</span>
        <span class='badge badge-amber'>Classification + Clustering</span>
    </div>
    <h1 style='font-family:Syne,sans-serif; font-size:3.2rem; font-weight:800;
               color:#f1f5f9; letter-spacing:-0.04em; line-height:1.1; margin:0 0 1rem 0;'>
        Credit Risk<br>
        <span style='color:#63cab7;'>Intelligence</span> Platform
    </h1>
    <p style='font-size:1.05rem; color:#94a3b8; max-width:600px; line-height:1.7; margin:0;'>
        Sistem analisis risiko kredit berbasis machine learning yang membantu
        mengidentifikasi profil nasabah, memprediksi kemungkinan gagal bayar,
        dan mensegmentasi nasabah ke dalam kelompok risiko yang bermakna.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
stats = [
    ("150,000", "Total Nasabah", "Give Me Some Credit - Kaggle"),
    ("11", "Fitur Dataset", "Variabel finansial & demografis"),
    ("6.68%", "Default Rate", "Nasabah gagal bayar"),
    ("3", "Segmen Risiko", "Rendah · Menengah · Tinggi"),
]
for col, (val, label, sub) in zip([c1,c2,c3,c4], stats):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{val}</div>
            <div class='metric-sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Method cards ──────────────────────────────────────────
st.markdown("<div class='section-header'>Metode yang Digunakan</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Dua pendekatan Data Mining untuk analisis kredit menyeluruh</div>", unsafe_allow_html=True)

m1, m2 = st.columns(2)
with m1:
    st.markdown("""
    <div class='metric-card' style='padding:1.8rem;'>
        <div style='font-size:2rem;margin-bottom:0.8rem;'></div>
        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#f1f5f9;margin-bottom:0.5rem;'>
            Classification
        </div>
        <div style='font-size:0.85rem;color:#94a3b8;line-height:1.6;'>
            Prediksi kemungkinan gagal bayar (<code style='color:#63cab7;'>SeriousDlqin2yrs</code>)
            menggunakan algoritma machine learning terbaik yang dipilih melalui
            perbandingan Random Forest, XGBoost, LightGBM, dan Logistic Regression.
        </div>
        <div style='margin-top:1rem;'>
            <span class='badge badge-teal'>LightGBM</span>&nbsp;
            <span class='badge badge-teal'>SMOTE</span>&nbsp;
            <span class='badge badge-teal'>SHAP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class='metric-card' style='padding:1.8rem;'>
        <div style='font-size:2rem;margin-bottom:0.8rem;'></div>
        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#f1f5f9;margin-bottom:0.5rem;'>
            Clustering
        </div>
        <div style='font-size:0.85rem;color:#94a3b8;line-height:1.6;'>
            Segmentasi nasabah ke dalam kelompok risiko menggunakan K-Means
            dengan 6 fitur terpilih. K optimal ditentukan secara otomatis
            melalui Silhouette Score, Davies-Bouldin, dan Calinski-Harabasz.
        </div>
        <div style='margin-top:1rem;'>
            <span class='badge badge-amber'>K-Means K=3</span>&nbsp;
            <span class='badge badge-amber'>Silhouette 0.23</span>&nbsp;
            <span class='badge badge-amber'>3 Segmen</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Pipeline flow ─────────────────────────────────────────
st.markdown("<div class='section-header'>Alur Proses CRISP-DM</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Metodologi standar industri untuk proyek Data Mining</div>", unsafe_allow_html=True)

steps = [
    ("01", "Business Understanding", "Identifikasi risiko kredit sebagai permasalahan bisnis nyata"),
    ("02", "Data Understanding", "Eksplorasi 150k record nasabah dari Kaggle"),
    ("03", "Data Preparation", "Imputasi, domain clipping, IQR capping, feature engineering"),
    ("04", "Modeling", "Training Classification & Clustering dengan evaluasi komprehensif"),
    ("05", "Evaluation", "Silhouette, F1-Score, ROC-AUC, SHAP explainability"),
    ("06", "Deployment", "Aplikasi web interaktif berbasis Streamlit"),
]

cols = st.columns(3)
for i, (num, title, desc) in enumerate(steps):
    with cols[i % 3]:
        st.markdown(f"""
        <div class='metric-card' style='padding:1.2rem 1.4rem;margin-bottom:1rem;'>
            <div style='font-family:Syne,sans-serif;font-size:0.65rem;color:#334155;
                        letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.4rem;'>
                Step {num}
            </div>
            <div style='font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;
                        color:#63cab7;margin-bottom:0.4rem;'>
                {title}
            </div>
            <div style='font-size:0.78rem;color:#64748b;line-height:1.5;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Team ──────────────────────────────────────────────────
st.markdown("<div class='section-header'>Tim Pengembang</div>", unsafe_allow_html=True)

t1, t2, t3 = st.columns([1,1,2])
with t1:
    st.markdown("""
    <div class='metric-card' style='text-align:center;padding:1.5rem;'>
        <div style='font-size:2.5rem;margin-bottom:0.6rem;'></div>
        <div style='font-family:Syne,sans-serif;font-weight:700;color:#f1f5f9;font-size:0.95rem;'>Ihza Budi Cendhika</div>
        <div style='font-size:0.72rem;color:#64748b;margin-top:0.3rem;'>24051214163 · DTMG-03</div>
    </div>
    """, unsafe_allow_html=True)
with t2:
    st.markdown("""
    <div class='metric-card' style='text-align:center;padding:1.5rem;'>
        <div style='font-size:2.5rem;margin-bottom:0.6rem;'></div>
        <div style='font-family:Syne,sans-serif;font-weight:700;color:#f1f5f9;font-size:0.95rem;'>Ikfi Ardani Kharisma</div>
        <div style='font-size:0.72rem;color:#64748b;margin-top:0.3rem;'>24051214165 · DTMG-03</div>
    </div>
    """, unsafe_allow_html=True)
with t3:
    st.markdown("""
    <div class='metric-card' style='padding:1.5rem;'>
        <div style='font-family:Syne,sans-serif;font-weight:700;color:#f1f5f9;margin-bottom:0.6rem;'>Universitas Negeri Surabaya</div>
        <div style='font-size:0.82rem;color:#94a3b8;line-height:1.7;'>
            Program Studi Sistem Informasi<br>
            Mata Kuliah Data Mining<br>
            Semester Genap 2024/2025
        </div>
    </div>
    """, unsafe_allow_html=True)
