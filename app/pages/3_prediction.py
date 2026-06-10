import streamlit as st
import numpy as np
import pandas as pd
import pickle, os, json, joblib

# ── Load models ────────────────────────────────────────────
@st.cache_resource
def load_models():
    # Path absolut relatif terhadap lokasi file ini
    base = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base, "..", "..", "streamlit_app", "model")
    model_dir = os.path.normpath(model_dir)
    st.write("Model dir:", model_dir)
    st.write("Exists:", os.path.exists(model_dir))
    st.write("Files:", os.listdir(model_dir) if os.path.exists(model_dir) else "NOT FOUND")

    km, sc_cl, sc_clf, clf, meta_cl, meta_clf = None, None, None, None, {}, {}
    try:
        if os.path.exists(f"{model_dir}/kmeans_final.pkl"):
            km = joblib.load(f"{model_dir}/kmeans_final.pkl")
        if os.path.exists(f"{model_dir}/scaler_cluster.pkl"):
            sc_cl = joblib.load(f"{model_dir}/scaler_cluster.pkl")
        if os.path.exists(f"{model_dir}/lightgbm_final.pkl"):
            clf = joblib.load(f"{model_dir}/lightgbm_final.pkl")
        if os.path.exists(f"{model_dir}/scaler_final.pkl"):
            sc_clf = joblib.load(f"{model_dir}/scaler_final.pkl")
        if os.path.exists(f"{model_dir}/cluster_metadata.json"):
            meta_cl = json.load(open(f"{model_dir}/cluster_metadata.json"))
        if os.path.exists(f"{model_dir}/model_metadata.json"):
            meta_clf = json.load(open(f"{model_dir}/model_metadata.json"))
    except Exception as e:
        st.warning(f"Error loading model: {e}")
    return km, sc_cl, sc_clf, clf, meta_cl, meta_clf

km_model, scaler_cluster, scaler_clf, clf_model, metadata, meta_clf = load_models()
THRESHOLD = meta_clf.get('threshold', 0.4811)
CLF_FEATURES = meta_clf.get('feature_names', [
    'RevolvingUtilizationOfUnsecuredLines','age',
    'NumberOfTime30-59DaysPastDueNotWorse','DebtRatio','MonthlyIncome',
    'NumberOfOpenCreditLinesAndLoans','NumberOfTimes90DaysLate',
    'NumberRealEstateLoansOrLines','NumberOfTime60-89DaysPastDueNotWorse',
    'NumberOfDependents','TotalLatePayments','AgeGroup','IncomePerDependent'
])

CLUSTER_FEATURES = (metadata.get('features') or [
    'RevolvingUtilizationOfUnsecuredLines',
    'age',
    'NumberOfOpenCreditLinesAndLoans',
    'NumberRealEstateLoansOrLines',
    'DebtRatio',
    'MonthlyIncome',
])

CLUSTER_LABELS = {
    0: ('Berisiko Tinggi',   'result-high',   '🔴', 'Nasabah memiliki profil risiko kredit tinggi. Perlu pengawasan ketat dan produk kredit dengan limit rendah.'),
    1: ('Berisiko Menengah', 'result-medium', '🟡', 'Nasabah berada di zona risiko moderat. Rekomendasikan produk standar dengan pemantauan berkala.'),
    2: ('Berisiko Rendah',   'result-low',    '🟢', 'Nasabah memiliki profil keuangan sehat. Kandidat ideal untuk produk premium dan limit kredit lebih tinggi.'),
}

def rule_based_cluster(revolving, income, debt_ratio, late_total):
    score = 0
    if revolving > 0.6: score += 2
    elif revolving > 0.3: score += 1
    if income < 3000: score += 2
    elif income < 6000: score += 1
    if debt_ratio > 1.5: score += 2
    elif debt_ratio > 0.8: score += 1
    if late_total >= 3: score += 3
    elif late_total >= 1: score += 1
    if score >= 5: return 0
    elif score >= 2: return 1
    else: return 2

# ── Header ─────────────────────────────────────────────────
st.markdown("<div class='section-header'>Prediction & Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Masukkan data nasabah untuk mendapatkan prediksi segmen risiko kredit</div>", unsafe_allow_html=True)

model_status = "✅ Model loaded" if km_model else "⚠️ Demo mode (rule-based)"
badge_color  = 'teal' if km_model else 'amber'
st.markdown(f"<span class='badge badge-{badge_color}'>{model_status}</span><br><br>", unsafe_allow_html=True)

# ── Input form ─────────────────────────────────────────────
with st.form("prediction_form"):
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;color:#f1f5f9;margin-bottom:1rem;'>Data Demografis & Finansial</div>", unsafe_allow_html=True)

    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        age = st.slider("Usia (tahun)", 18, 100, 45, key="age")
    with r1c2:
        income = st.number_input("Pendapatan Bulanan (USD)", min_value=0, max_value=100000, value=5000, step=100, key="income")
    with r1c3:
        dependents = st.slider("Jumlah Tanggungan", 0, 10, 1, key="dependents")

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        revolving = st.slider("Rasio Kredit Bergulir (0-1)", 0.0, 1.0, 0.3, step=0.01, key="revolving")
    with r2c2:
        debt_ratio = st.slider("Debt Ratio", 0.0, 5.0, 0.35, step=0.01, key="debt_ratio")
    with r2c3:
        open_credits = st.slider("Jumlah Kredit Aktif", 0, 40, 8, key="open_credits")

    r3c1, r3c2, r3c3, r3c4 = st.columns(4)
    with r3c1:
        real_estate = st.slider("Kredit Properti", 0, 10, 1, key="real_estate")
    with r3c2:
        late_30_59 = st.slider("Keterlambatan 30-59 hari", 0, 15, 0, key="late_30_59")
    with r3c3:
        late_60_89 = st.slider("Keterlambatan 60-89 hari", 0, 15, 0, key="late_60_89")
    with r3c4:
        late_90 = st.slider("Keterlambatan >90 hari", 0, 15, 0, key="late_90")

    submitted = st.form_submit_button("Analisis Profil Nasabah")

# ── Prediction ─────────────────────────────────────────────
if submitted:
    late_total = late_30_59 + late_60_89 + late_90

    # K-Means clustering
    if km_model and scaler_cluster:
        try:
            feat_map = {
                'RevolvingUtilizationOfUnsecuredLines': revolving,
                'age': age,
                'NumberOfOpenCreditLinesAndLoans': open_credits,
                'NumberRealEstateLoansOrLines': real_estate,
                'DebtRatio': debt_ratio,
                'MonthlyIncome': income,
            }
            X_in = np.array([[feat_map[f] for f in CLUSTER_FEATURES]])
            X_scaled = scaler_cluster.transform(X_in)
            cluster = int(km_model.predict(X_scaled)[0])
            if metadata.get('default_rate'):
                dr = {int(k): v for k, v in metadata['default_rate'].items()}
                sorted_c = sorted(dr, key=lambda x: dr[x], reverse=True)
                rank_map = {c: i for i, c in enumerate(sorted_c)}
                cluster = rank_map.get(cluster, cluster)
        except Exception:
            cluster = rule_based_cluster(revolving, income, debt_ratio, late_total)
    else:
        cluster = rule_based_cluster(revolving, income, debt_ratio, late_total)

    label, css_class, emoji, advice = CLUSTER_LABELS[cluster]

    # Result card cluster
    st.markdown(f"""
    <div class='result-card {css_class}'>
        <div style='font-size:3rem;margin-bottom:0.5rem;'>{emoji}</div>
        <div class='result-title'>{label}</div>
        <div class='result-desc'>{advice}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # LightGBM prediksi probabilitas default
    if clf_model and scaler_clf:
        try:
            age_group      = 0 if age<=30 else 1 if age<=45 else 2 if age<=60 else 3
            income_per_dep = income / (dependents + 1)

            clf_feat_map = {
                'RevolvingUtilizationOfUnsecuredLines': revolving,
                'age': age,
                'NumberOfTime30-59DaysPastDueNotWorse': late_30_59,
                'DebtRatio': debt_ratio,
                'MonthlyIncome': income,
                'NumberOfOpenCreditLinesAndLoans': open_credits,
                'NumberOfTimes90DaysLate': late_90,
                'NumberRealEstateLoansOrLines': real_estate,
                'NumberOfTime60-89DaysPastDueNotWorse': late_60_89,
                'NumberOfDependents': dependents,
                'TotalLatePayments': late_total,
                'AgeGroup': age_group,
                'IncomePerDependent': income_per_dep,
            }
            X_clf        = np.array([[clf_feat_map[f] for f in CLF_FEATURES]])
            X_clf_scaled = scaler_clf.transform(X_clf)
            prob_default = clf_model.predict_proba(X_clf_scaled)[0][1]
            pred_label   = 1 if prob_default >= THRESHOLD else 0

            color   = '#f87171' if prob_default >= THRESHOLD else '#fbbf24' if prob_default > 0.2 else '#63cab7'
            verdict = 'Prediksi: DEFAULT' if pred_label == 1 else 'Prediksi: TIDAK DEFAULT'

            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-header' style='font-size:1.1rem;'>Probabilitas Gagal Bayar - LightGBM</div>", unsafe_allow_html=True)

            pa, pb = st.columns([1, 2])
            with pa:
                st.markdown(f"""
                <div class='metric-card' style='text-align:center;padding:1.8rem;'>
                    <div class='metric-label'>Probabilitas Default</div>
                    <div class='metric-value' style='font-size:2.8rem;color:{color};'>{prob_default:.1%}</div>
                    <div style='margin-top:0.8rem;font-size:0.85rem;color:{color};font-weight:600;'>{verdict}</div>
                    <div style='font-size:0.72rem;color:#475569;margin-top:0.3rem;'>threshold: {THRESHOLD}</div>
                </div>
                """, unsafe_allow_html=True)
            with pb:
                st.markdown(f"""
                <div class='metric-card' style='padding:1.8rem;'>
                    <div class='metric-label' style='margin-bottom:1rem;'>Skala Risiko</div>
                    <div style='height:14px;background:#1e293b;border-radius:999px;overflow:hidden;margin-bottom:0.6rem;'>
                        <div style='height:100%;width:{prob_default*100:.1f}%;background:linear-gradient(90deg,#63cab7,#fbbf24,#f87171);border-radius:999px;'></div>
                    </div>
                    <div style='display:flex;justify-content:space-between;font-size:0.7rem;color:#475569;margin-bottom:1.2rem;'>
                        <span>0% Aman</span><span>Threshold {THRESHOLD:.0%}</span><span>100% Berbahaya</span>
                    </div>
                    <div style='font-size:0.82rem;color:#94a3b8;line-height:1.7;'>
                        Model: <span style='color:#63cab7;'>LightGBM Tuned (Optuna)</span><br>
                        AUC-ROC: <span style='color:#f1f5f9;'>0.8695</span> &nbsp;|&nbsp;
                        Recall: <span style='color:#f1f5f9;'>80.2%</span> &nbsp;|&nbsp;
                        F1: <span style='color:#f1f5f9;'>0.327</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Model classification tidak tersedia: {e}")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.info("Clustering menggambarkan profil finansial nasabah, sedangkan LightGBM memprediksi probabilitas gagal bayar berdasarkan riwayat pembayaran. Kedua hasil saling melengkapi.")

    # Profile summary
    st.markdown("<div class='section-header' style='font-size:1.1rem;'>Ringkasan Profil Nasabah</div>", unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    profiles = [
        ("Usia", f"{age} tahun"),
        ("Pendapatan", f"${income:,}"),
        ("Debt Ratio", f"{debt_ratio:.2f}"),
        ("Kredit Aktif", f"{open_credits}"),
    ]
    for col, (lbl, val) in zip([p1,p2,p3,p4], profiles):
        with col:
            st.markdown(f"""
            <div class='metric-card' style='text-align:center;padding:0.9rem;'>
                <div class='metric-label'>{lbl}</div>
                <div class='metric-value' style='font-size:1.4rem;'>{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Risk indicator bars
    st.markdown("<div class='section-header' style='font-size:1.1rem;'>Indikator Risiko</div>", unsafe_allow_html=True)
    indicators = [
        ("Rasio Kredit Bergulir", revolving, 1.0, revolving > 0.6),
        ("Debt Ratio", min(debt_ratio, 5)/5, 1.0, debt_ratio > 1.0),
        ("Riwayat Keterlambatan", min(late_total, 10)/10, 1.0, late_total > 0),
        ("Income Adequacy", min(income, 20000)/20000, 1.0, income < 3000),
    ]
    for name, val, max_val, is_risky in indicators:
        color = '#f87171' if is_risky else '#63cab7'
        pct   = val / max_val * 100
        st.markdown(f"""
        <div style='margin-bottom:1rem;'>
            <div style='display:flex;justify-content:space-between;margin-bottom:0.3rem;'>
                <span style='font-size:0.8rem;color:#94a3b8;'>{name}</span>
                <span style='font-size:0.8rem;color:{color};font-weight:600;'>{pct:.0f}%</span>
            </div>
            <div style='height:6px;background:#1e293b;border-radius:999px;overflow:hidden;'>
                <div style='height:100%;width:{pct}%;background:{color};border-radius:999px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Rekomendasi
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    recs = {
        0: ["Hindari pemberian kredit baru sementara", "Lakukan verifikasi pendapatan ulang", "Terapkan limit kredit minimum", "Wajib jaminan untuk pinjaman baru"],
        1: ["Kredit standar dapat diberikan", "Pemantauan pembayaran bulanan", "Limit kredit sesuai standar", "Notifikasi otomatis jatuh tempo"],
        2: ["Kandidat kredit premium", "Penawaran produk eksklusif", "Peningkatan limit kredit", "Program loyalitas nasabah"],
    }
    st.markdown("<div class='section-header' style='font-size:1.1rem;'>Rekomendasi Tindakan</div>", unsafe_allow_html=True)
    rc = st.columns(2)
    for i, rec in enumerate(recs[cluster]):
        with rc[i % 2]:
            st.markdown(f"""
            <div class='metric-card' style='padding:0.8rem 1rem;margin-bottom:0.6rem;font-size:0.82rem;color:#cbd5e1;'>
                {rec}
            </div>
            """, unsafe_allow_html=True)
