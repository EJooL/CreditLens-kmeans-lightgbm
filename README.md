# 🔍 CreditLens — Credit Risk Analytics

> Sistem analisis risiko kredit berbasis machine learning yang mengintegrasikan
> **Classification (LightGBM)** dan **Clustering (K-Means)** untuk memberikan
> prediksi dan segmentasi nasabah secara komprehensif.

**UAS Data Mining · Sistem Informasi UNESA · 2025/2026**

---

## 📋 Deskripsi Proyek

CreditLens adalah aplikasi web interaktif berbasis Streamlit untuk menganalisis
risiko kredit nasabah menggunakan dataset **Give Me Some Credit** (Kaggle, 150.000 record).

| Pendekatan | Algoritma | Output |
|---|---|---|
| Classification | LightGBM (Optuna 50 iterasi) | Probabilitas gagal bayar |
| Clustering | K-Means (K=3) | Segmen risiko nasabah |

---

## 🏗️ Struktur Folder

```
├── app/
│   ├── app.py                  ← Entry point Streamlit
│   └── pages/
│       ├── 1_home.py           ← Halaman beranda
│       ├── 2_dataset.py        ← Dataset overview & EDA
│       ├── 3_prediction.py     ← Prediksi & analisis nasabah
│       ├── 4_visualization.py  ← Visualisasi clustering
│       └── 5_about.py          ← Metodologi & dokumentasi
├── model/
│   ├── lightgbm_final.pkl      ← Model LightGBM (joblib)
│   ├── scaler_final.pkl        ← Scaler classification
│   ├── model_metadata.json     ← Threshold & feature names
│   ├── kmeans_final.pkl        ← Model K-Means (joblib)
│   ├── scaler_cluster.pkl      ← Scaler clustering
│   └── cluster_metadata.json  ← Profil segmen & default rate
├── dataset/
│   └── cs-training.csv         ← Dataset Give Me Some Credit
├── notebook/
│   ├── UASMINING_clustering.ipynb
│   └── UASMINING_classification.ipynb
├── requirements.txt
└── README.md
```

---

## ⚙️ Cara Menjalankan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Siapkan Model & Dataset

Export model dari notebook lalu letakkan di folder `model/`:

```
model/lightgbm_final.pkl
model/scaler_final.pkl
model/model_metadata.json
model/kmeans_final.pkl
model/scaler_cluster.pkl
model/cluster_metadata.json
```

Dataset di:
```
dataset/cs-training.csv
```

> Jika model belum tersedia, aplikasi berjalan dalam **Demo Mode (Rule-Based)**.

### 3. Jalankan Aplikasi

```bash
cd app
streamlit run app.py
```

Buka browser: `http://localhost:8501`

---

## 📦 Export Model dari Notebook

```python
import joblib, json

# ── Classification ──────────────────────────────
joblib.dump(FINAL_MODEL, 'lightgbm_final.pkl')
joblib.dump(scaler, 'scaler_final.pkl')
json.dump({
    'threshold': 0.4811,
    'feature_names': feature_names  # 13 fitur
}, open('model_metadata.json', 'w'))

# ── Clustering ──────────────────────────────────
joblib.dump(kmeans, 'kmeans_final.pkl')
joblib.dump(scaler_cluster, 'scaler_cluster.pkl')
json.dump({
    'features': cluster_features_final,
    'default_rate': default_rate_per_cluster.to_dict()
}, open('cluster_metadata.json', 'w'))
```

---

## 📊 Performa Model (Hasil Aktual)

### Classification

| Model | AUC-ROC | Recall | Precision | F1-Score |
|---|---|---|---|---|
| Logistic Regression | 0,8556 | 0,7576 | 0,2042 | 0,3217 |
| Decision Tree | 0,8526 | 0,6978 | 0,2441 | 0,3617 |
| Random Forest | 0,8646 | 0,7312 | 0,2438 | 0,3657 |
| XGBoost | 0,8624 | 0,7382 | 0,2406 | 0,3629 |
| **LightGBM Tuned** | **0,8695** | **0,8329** | **0,1838** | **0,3027** |

> **Model final:** LightGBM Tuned · Threshold: **0,4811** · Gap train-test: 0,0025 (tidak overfit)

### Clustering

| Metrik | K-Means (K=3) | Agglomerative | DBSCAN |
|---|---|---|---|
| Silhouette Score | **0,2347** | 0,2185 | 0,0016 |
| Davies-Bouldin | **1,5724** | 1,6580 | 2,3251 |
| Calinski-Harabasz | **39.217** | 2.410 | 679 |

### Profil Segmen Nasabah

| Segmen | Jumlah | Proporsi | Default Rate | Income Rata-rata |
|---|---|---|---|---|
| Berisiko Tinggi (Cluster 0) | 69.252 | 46,2% | 8,5% | $4.382 |
| Berisiko Menengah (Cluster 1) | 29.536 | 19,7% | 5,5% | $4.992 |
| Berisiko Rendah (Cluster 2) | 51.212 | 34,1% | 4,9% | $8.973 |

---

## 🗂️ Dataset

**Give Me Some Credit** — Kaggle Competition (2011)

| Info | Detail |
|---|---|
| Records | 150.000 nasabah |
| Fitur awal | 11 variabel |
| Fitur setelah engineering | 14 variabel |
| Target | SeriousDlqin2yrs (binary) |
| Default Rate | 6,68% (10.026 default / 139.974 tidak) |
| Rasio imbalance | 1 : 14,0 |
| Missing MonthlyIncome | 19,8% → imputasi median |
| Missing NumberOfDependents | 2,6% → imputasi 0 |

### Feature Engineering

| Fitur Baru | Keterangan |
|---|---|
| `TotalLatePayments` | Sum semua variabel keterlambatan |
| `AgeGroup` | Kategorisasi usia (0=≤30, 1=31-45, 2=46-60, 3=>60) |
| `IncomePerDependent` | MonthlyIncome / (NumberOfDependents + 1) |

---

## 🛠️ Tech Stack

| Kategori | Library |
|---|---|
| Web Framework | Streamlit >=1.32.0 |
| Classification | LightGBM >=4.0.0 |
| Clustering | scikit-learn >=1.3.0 |
| Imbalanced Data | imbalanced-learn >=0.11.0 |
| Hyperparameter Tuning | Optuna >=3.0.0 |
| Explainability | SHAP >=0.44.0 |
| Visualization | Plotly, Matplotlib, Seaborn |
| Model Persistence | joblib >=1.3.0 |
| Dataset | kagglehub >=0.1.0 |
| DBSCAN eps detection | kneed >=0.8.0 |

---

## 👨‍💻 Tim Pengembang

| Nama | NIM | Program Studi |
|---|---|---|
| Ihza Budi Cendhika | 24051214163 | Sistem Informasi |
| Ikfi Ardani Kharisma | 24051214165 | Sistem Informasi |

**Universitas Negeri Surabaya**
Mata Kuliah: Data Mining · Semester Genap 2024/2025
