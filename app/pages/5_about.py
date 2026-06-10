import streamlit as st

st.markdown("<div class='section-header'>About</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Dokumentasi proyek, metode, dan dataset</div>", unsafe_allow_html=True)

# ── Project overview ──────────────────────────────────────
st.markdown("""
<div class='metric-card' style='padding:1.8rem;margin-bottom:1.5rem;'>
    <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#63cab7;margin-bottom:0.8rem;'>
        Tentang Proyek
    </div>
    <div style='font-size:0.88rem;color:#94a3b8;line-height:1.8;'>
        Proyek ini dikembangkan sebagai tugas akhir (UAS) mata kuliah <strong style='color:#f1f5f9;'>Data Mining</strong>
        di Program Studi Sistem Informasi, Universitas Negeri Surabaya. Tujuannya adalah membangun
        sistem analisis risiko kredit yang mampu mengidentifikasi nasabah berisiko tinggi menggunakan
        dua metode data mining: <strong style='color:#63cab7;'>Classification</strong> dan
        <strong style='color:#63cab7;'>Clustering</strong>.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Dataset ───────────────────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.1rem;'>Dataset</div>", unsafe_allow_html=True)

d1, d2 = st.columns(2)
with d1:
    st.markdown("""
    <div class='metric-card' style='padding:1.4rem;'>
        <div style='font-family:Syne,sans-serif;font-weight:700;color:#f1f5f9;margin-bottom:0.8rem;'>Give Me Some Credit</div>
        <div style='font-size:0.82rem;color:#94a3b8;line-height:1.8;'>
            <b style='color:#cbd5e1;'>Sumber:</b> Kaggle Competition<br>
            <b style='color:#cbd5e1;'>Records:</b> 150,000 nasabah<br>
            <b style='color:#cbd5e1;'>Fitur:</b> 11 variabel finansial<br>
            <b style='color:#cbd5e1;'>Target:</b> SeriousDlqin2yrs (binary)<br>
            <b style='color:#cbd5e1;'>Missing:</b> MonthlyIncome (19.8%), Dependents (2.6%)<br>
            <b style='color:#cbd5e1;'>Imbalance:</b> 93.3% : 6.7%
        </div>
    </div>
    """, unsafe_allow_html=True)
with d2:
    st.markdown("""
    <div class='metric-card' style='padding:1.4rem;'>
        <div style='font-family:Syne,sans-serif;font-weight:700;color:#f1f5f9;margin-bottom:0.8rem;'>Preprocessing Pipeline</div>
        <div style='font-size:0.82rem;color:#94a3b8;line-height:1.8;'>
            ① Imputasi median untuk MonthlyIncome & Dependents<br>
            ② Domain clipping (RevolvingUtil 0–1, age 18–100)<br>
            ③ IQR capping (multiplier=3.0) untuk income & kredit<br>
            ④ Feature engineering: TotalLatePayments, AgeGroup, IncomePerDependent<br>
            ⑤ SMOTE untuk menangani class imbalance (Classification)<br>
            ⑥ StandardScaler sebelum Clustering
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Methods ───────────────────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.1rem;'>Metode Data Mining</div>", unsafe_allow_html=True)

m1, m2 = st.columns(2)
with m1:
    st.markdown("""
    <div class='metric-card' style='padding:1.6rem;'>
        <div style='font-family:Syne,sans-serif;font-weight:700;color:#63cab7;margin-bottom:0.8rem;'>
            Classification - LightGBM
        </div>
        <div style='font-size:0.82rem;color:#94a3b8;line-height:1.8;'>
            <b style='color:#cbd5e1;'>Algoritma:</b> LightGBM (Gradient Boosting)<br>
            <b style='color:#cbd5e1;'>Pembanding:</b> Random Forest, XGBoost, Logistic Regression<br>
            <b style='color:#cbd5e1;'>Penanganan imbalance:</b> SMOTE<br>
            <b style='color:#cbd5e1;'>Explainability:</b> SHAP values<br>
            <b style='color:#cbd5e1;'>Evaluasi:</b> ROC-AUC, F1-Score, Precision, Recall<br>
            <br>
            <b style='color:#cbd5e1;'>Kelebihan LightGBM:</b><br>
            Training cepat pada data besar, menangani nilai hilang secara otomatis,
            performa tinggi pada data tabular, mendukung feature importance.
        </div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class='metric-card' style='padding:1.6rem;'>
        <div style='font-family:Syne,sans-serif;font-weight:700;color:#fbbf24;margin-bottom:0.8rem;'>
            Clustering - K-Means (K=3)
        </div>
        <div style='font-size:0.82rem;color:#94a3b8;line-height:1.8;'>
            <b style='color:#cbd5e1;'>Algoritma:</b> K-Means<br>
            <b style='color:#cbd5e1;'>Pembanding:</b> Agglomerative (Ward), DBSCAN<br>
            <b style='color:#cbd5e1;'>Fitur:</b> 6 fitur berbasis SHAP importance<br>
            <b style='color:#cbd5e1;'>K optimal:</b> Otomatis dari Silhouette Score<br>
            <b style='color:#cbd5e1;'>Evaluasi:</b> Silhouette, Davies-Bouldin, Calinski-Harabasz<br>
            <br>
            <b style='color:#cbd5e1;'>Alasan K=3:</b><br>
            Silhouette tertinggi (0.2347), distribusi cluster seimbang
            (46%/20%/34%), dan sesuai domain knowledge 3 segmen risiko kredit.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Methodology ───────────────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.1rem;'>Framework: CRISP-DM</div>", unsafe_allow_html=True)

steps = [
    ("Business Understanding", "Identifikasi masalah risiko kredit perbankan. Tujuan: prediksi default dan segmentasi nasabah untuk keputusan kredit yang lebih tepat."),
    ("Data Understanding", "Eksplorasi dataset 150k nasabah: distribusi fitur, missing values, outlier detection, korelasi antar variabel."),
    ("Data Preparation", "Imputasi median, domain clipping, IQR capping, feature engineering (TotalLatePayments, IncomePerDependent), SMOTE, StandardScaler."),
    ("Modeling", "Training LightGBM (Classification) dan K-Means K=3 (Clustering) dengan perbandingan terhadap algoritma alternatif."),
    ("Evaluation", "Classification: ROC-AUC, F1, Precision, Recall, SHAP. Clustering: Silhouette=0.23, DB=1.57, CH=39217."),
    ("Deployment", "Aplikasi web Streamlit dengan 5 halaman: Home, Dataset, Prediction, Visualization, About."),
]

for i, (title, desc) in enumerate(steps):
    st.markdown(f"""
    <div style='display:flex;gap:1rem;margin-bottom:0.8rem;align-items:flex-start;'>
        <div style='background:#63cab7;color:#0a0f1e;font-family:Syne,sans-serif;font-weight:800;
                    font-size:0.75rem;min-width:28px;height:28px;border-radius:50%;
                    display:flex;align-items:center;justify-content:center;margin-top:0.2rem;'>
            {i+1}
        </div>
        <div class='metric-card' style='padding:0.9rem 1.2rem;flex:1;'>
            <div style='font-family:Syne,sans-serif;font-weight:700;color:#f1f5f9;
                        font-size:0.88rem;margin-bottom:0.3rem;'>{title}</div>
            <div style='font-size:0.8rem;color:#94a3b8;'>{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Tech stack ────────────────────────────────────────────
st.markdown("<div class='section-header' style='font-size:1.1rem;'>Tech Stack</div>", unsafe_allow_html=True)

tech = [
    ("Python 3.11", "Bahasa pemrograman utama"),
    ("Streamlit", "Framework aplikasi web"),
    ("LightGBM", "Model classification"),
    ("scikit-learn", "K-Means, preprocessing, evaluasi"),
    ("Plotly", "Visualisasi interaktif"),
    ("SHAP", "Explainable AI"),
    ("imbalanced-learn", "SMOTE oversampling"),
    ("Pandas / NumPy", "Data manipulation"),
]
tc = st.columns(4)
for i, (name, desc) in enumerate(tech):
    with tc[i % 4]:
        st.markdown(f"""
        <div class='metric-card' style='text-align:center;padding:0.9rem;margin-bottom:0.8rem;'>
            <div style='font-family:Syne,sans-serif;font-weight:700;color:#63cab7;font-size:0.85rem;'>{name}</div>
            <div style='font-size:0.72rem;color:#475569;margin-top:0.2rem;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;padding:1rem 0;font-size:0.75rem;color:#334155;'>
    UAS Data Mining · Sistem Informasi UNESA · 2024/2025<br>
    <span style='color:#1e293b;'>Built with Streamlit + Plotly</span>
</div>
""", unsafe_allow_html=True)
