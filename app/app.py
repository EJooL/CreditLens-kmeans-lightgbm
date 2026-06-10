import streamlit as st

st.set_page_config(
    page_title="CreditLens - Credit Risk Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ──────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0a0f1e 0%, #111827 100%);
    border-right: 1px solid rgba(99,202,183,0.15);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    padding: 0.5rem 0;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(99,202,183,0.2);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(99,202,183,0.12);
}
.metric-label {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Playfair Display', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
}
.metric-sub {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 0.3rem;
}

/* ── Section header ── */
.section-header {
    font-family: 'Playfair Display', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.02em;
    margin-bottom: 0.2rem;
}
.section-sub {
    font-size: 0.88rem;
    color: #64748b;
    margin-bottom: 1.5rem;
}

/* ── Tag / badge ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-teal  { background: rgba(26,86,219,0.15); color: #63cab7; border: 1px solid rgba(99,202,183,0.3); }
.badge-amber { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-red   { background: rgba(239,68,68,0.15);   color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,202,183,0.3), transparent);
    margin: 1.5rem 0;
}

/* ── Result card ── */
.result-card {
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin-top: 1rem;
}
.result-low    { background: linear-gradient(135deg,#064e3b,#065f46); border: 1px solid #10b981; }
.result-medium { background: linear-gradient(135deg,#78350f,#92400e); border: 1px solid #f59e0b; }
.result-high   { background: linear-gradient(135deg,#7f1d1d,#991b1b); border: 1px solid #ef4444; }
.result-title  { font-family:'Playfair Display',sans-serif; font-size:1.5rem; font-weight:800; margin-bottom:0.5rem; }
.result-desc   { font-size:0.88rem; color:rgba(255,255,255,0.75); }

/* ── Streamlit overrides ── */
.stButton > button {
    background: linear-gradient(135deg, #63cab7, #3b9e8c);
    color: #03071e;
    font-family: 'Playfair Display', sans-serif;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 2rem;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99,202,183,0.35);
}
.stSlider > div > div { color: #63cab7 !important; }
.stSelectbox label, .stSlider label, .stNumberInput label {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
[data-testid="stSidebarNav"] { display: none !important; }

/* Submit button form */
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #1a56db, #1e40af) !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    border: none !important;
    width: 100% !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #1e40af, #1e3a8a) !important;
    box-shadow: 0 6px 20px rgba(26,86,219,0.4) !important;
    transform: translateY(-2px) !important;
}
            
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.2rem 0 1.6rem 0;'>
        <div style='font-family:Playfair Display,sans-serif;font-size:1.4rem;font-weight:800;color:#63cab7;letter-spacing:-0.02em;'>
            CreditLens
        </div>
        <div style='font-size:0.72rem;color:#475569;letter-spacing:0.1em;text-transform:uppercase;margin-top:0.2rem;'>
            Credit Risk Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "",
        ["Home", "Dataset Overview", "Prediction & Analysis", "Visualization", "About"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.7rem;color:#334155;line-height:1.8;padding:0 0.5rem;'>
        UAS Data Mining<br>
        Sistem Informasi - UNESA<br>
        <span style='color:#475569;'>2024 / 2025</span>
    </div>
    """, unsafe_allow_html=True)

# ── Route to pages ────────────────────────────────────────
if   "Home"         in page: exec(open("pages/1_home.py", encoding="utf-8").read())
elif "Dataset"      in page: exec(open("pages/2_dataset.py", encoding="utf-8").read())
elif "Prediction"   in page: exec(open("pages/3_prediction.py", encoding="utf-8").read())
elif "Visualization"in page: exec(open("pages/4_visualization.py", encoding="utf-8").read())
elif "About"        in page: exec(open("pages/5_about.py", encoding="utf-8").read())
