import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
import pickle
import os
from pathlib import Path
warnings.filterwarnings('ignore')

GITHUB_MODEL_URL = "https://github.com/alexi517/fleet-intelligence-management-system/blob/main/fleet_models.pkl"

st.set_page_config(
    page_title="Fleet Intelligence Management System",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141b2d 0%, #1a1f3a 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.1);
    }
    [data-testid="stSidebar"] .css-1d391kg { background-color: transparent; }
    h1 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        background: linear-gradient(120deg, #60efff 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem !important;
    }
    h2 { color: #ffffff !important; font-weight: 600 !important; font-size: 1.8rem !important; margin-top: 2rem !important; }
    h3 { color: #ffffff !important; font-weight: 600 !important; }
    .metric-card {
        position: relative;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
        backdrop-filter: blur(10px);
        padding: 1rem 1.1rem;
        border-radius: 12px;
        border: 1px solid transparent;
        background-clip: padding-box;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(99, 102, 241, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 0.75rem;
        height: 108px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 12px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(96, 239, 255, 0.6) 0%, rgba(99, 102, 241, 0.5) 45%, rgba(139, 92, 246, 0.6) 100%);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
        opacity: 0.55;
        transition: opacity 0.25s ease;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        inset: -1px;
        border-radius: 13px;
        background: radial-gradient(120% 120% at 0% 0%, rgba(96, 239, 255, 0.25) 0%, rgba(99, 102, 241, 0) 60%);
        pointer-events: none;
        opacity: 0.8;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 32px rgba(99, 102, 241, 0.35), 0 0 0 1px rgba(96, 239, 255, 0.3);
    }
    .metric-card:hover::before { opacity: 1; }
    .metric-value {
        position: relative;
        z-index: 1;
        font-size: 1.6rem;
        font-weight: 700;
        line-height: 1.2;
        background: linear-gradient(120deg, #60efff 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.2rem 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .metric-label {
        position: relative;
        z-index: 1;
        font-size: 0.7rem;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .metric-delta {
        position: relative;
        z-index: 1;
        font-size: 0.75rem;
        color: #ffffff;
        margin-top: 0.1rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Feature cards (welcome screen) - auto height, no clipping */
    .feature-card {
        position: relative;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
        backdrop-filter: blur(10px);
        padding: 1.75rem 1.25rem;
        border-radius: 16px;
        border: 1px solid transparent;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(99, 102, 241, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
        height: 100%;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        text-align: center;
        overflow: hidden;
    }
    .feature-card::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 16px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(96, 239, 255, 0.6) 0%, rgba(99, 102, 241, 0.5) 45%, rgba(139, 92, 246, 0.6) 100%);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
        opacity: 0.55;
        transition: opacity 0.25s ease;
    }
    .feature-card::after {
        content: '';
        position: absolute;
        inset: -1px;
        border-radius: 17px;
        background: radial-gradient(120% 90% at 50% 0%, rgba(96, 239, 255, 0.2) 0%, rgba(99, 102, 241, 0) 60%);
        pointer-events: none;
        opacity: 0.8;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 44px rgba(99, 102, 241, 0.35), 0 0 0 1px rgba(96, 239, 255, 0.3);
    }
    .feature-card:hover::before { opacity: 1; }
    .feature-icon { position: relative; z-index: 1; font-size: 2.5rem; margin-bottom: 0.5rem; line-height: 1; }
    .feature-card h3 {
        position: relative;
        z-index: 1;
        color: #ffffff !important;
        font-size: 1.15rem !important;
        margin: 0.25rem 0 0.5rem 0 !important;
    }
    .feature-card p {
        position: relative;
        z-index: 1;
        color: #9ca3af;
        font-size: 0.875rem;
        line-height: 1.5;
        margin: 0;
    }
    .badge-keep {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff; padding: 0.5rem 1.25rem; border-radius: 24px; font-weight: 600;
        font-size: 0.875rem; display: inline-block; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .badge-sell {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: #ffffff; padding: 0.5rem 1.25rem; border-radius: 24px; font-weight: 600;
        font-size: 0.875rem; display: inline-block; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .badge-inspect {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #ffffff; padding: 0.5rem 1.25rem; border-radius: 24px; font-weight: 600;
        font-size: 0.875rem; display: inline-block; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .info-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.05) 100%);
        border-left: 4px solid #6366f1; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
	color: #ffffff; padding: 0.5rem 1.25rem; border-radius: 24px; font-weight: 600;

    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white; border: none; border-radius: 12px; padding: 0.75rem 2rem; font-weight: 600;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3); transition: all 0.2s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4); }
    [data-testid="stFileUploader"] {
        background: rgba(99, 102, 241, 0.05); border: 2px dashed rgba(99, 102, 241, 0.3);
        border-radius: 12px; padding: 1rem;
    }
    .dataframe { background-color: rgba(17, 24, 39, 0.5) !important; border-radius: 12px; overflow: hidden; }
    .dataframe thead tr th {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important; font-weight: 700 !important; padding: 1rem !important; border: none !important;
        text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.875rem !important;
    }
    .dataframe tbody tr {
        background: rgba(99, 102, 241, 0.03) !important; border-bottom: 1px solid rgba(99, 102, 241, 0.1) !important;
        transition: all 0.2s ease;
    }
    .dataframe tbody tr:hover {
        background: rgba(99, 102, 241, 0.1) !important; transform: scale(1.01); box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    .dataframe tbody tr td { color:#FFFF00 !important; padding: 0.75rem !important; font-weight: 500 !important; border: none !important; }
    .dataframe tbody tr:nth-child(even) { background: rgba(99, 102, 241, 0.05) !important; }
    .main h4 { color: #FFFF00 !important; font-weight: 600 !important; }
    .main p { color: ##FFFF00 !important; }
    .main label { color: #FFFF00 !important; font-weight: 600 !important; }
    .main .stSlider label { color: #ffffff !important; font-weight: 700 !important; }
    .main .stSlider p { color: #ffffff !important; }
    .main .stSlider div[data-baseweb="slider"] + div { color: #ffffff !important; }
    .main .stSlider small { color: #FFFF00 !important; }
    .main div { color: #FFFF00 !important; }
    .main span { color: #FFFF00 !important; }
    .main .markdown-text-container { color: #ffffff !important; }
    .main ul li { color: #ffffff !important; }
    .main strong { color: #60efff !important; }
    .main .element-container p { color: #ffffff !important; }
    .main .element-container li { color: #ffffff !important; }
    .main .stSlider [data-baseweb="tooltip"] { color: #ffffff !important; }
    .main .stMarkdown { color: #ffffff !important; }
    .main .stMarkdown p { color: #ffffff !important; }
    .main .stMarkdown li { color: #ffffff !important; }
    .main h1 { color: #60efff !important; }
    .main h2 { color: #60efff !important; }
    .main h3 { color: #f59e0b !important; }
    .main h4 { color: #10b981 !important; }
    .main [data-baseweb="slider"] { color: #ffffff !important; }
    .main [data-testid="stTooltipHoverTarget"] { color: #ffffff !important; }
    .streamlit-expanderHeader {
        background: rgba(99, 102, 241, 0.08); border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2);
        color: #e0e7ff !important; font-weight: 600;
    }
    .stSelectbox, .stMultiSelect, .stSlider { color: #FFFF00; }
    [data-testid="stMetricValue"] { color: #60efff !important; font-size: 2rem !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #9ca3af !important; font-weight: 600 !important; }
    hr { border-color: rgba(99, 102, 241, 0.2); margin: 2rem 0; }
    .stSuccess { background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; border-radius: 8px; }
    .stWarning { background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; border-radius: 8px; }
    .stError { background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; border-radius: 8px; }
    .stInfo { background: rgba(99, 102, 241, 0.1); border-left: 4px solid #6366f1; border-radius: 8px; }
    .stRadio > label { color: #e0e7ff !important; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label { color: #ffffff !important; font-weight: 500 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        background: linear-gradient(120deg, #60efff 0%, #6366f1 100%) !important;
        -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
    }
    [data-testid="stSidebar"] p { color: #c7d2fe !important; }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: rgba(99, 102, 241, 0.1) !important; border: 2px dashed rgba(99, 102, 241, 0.5) !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] label { color: #ffffff !important; font-weight: 600 !important; }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] small { color: #9ca3af !important; }
    .main h4 { color: #e0e7ff !important; }
    .main p { color: #c7d2fe !important; }
    .main .stSlider label { color: #e0e7ff !important; }
    /* Reduce default Streamlit top padding so content sits higher */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
    }

    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: rgba(99, 102, 241, 0.05); }
    ::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.3); border-radius: 5px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, 0.5); }
    </style>
""", unsafe_allow_html=True)

def load_ml_models():
    streamlit_path = '/mount/src/fleet-intelligence-management-system/fleet_models.pkl'
    local_path = 'fleet_models.pkl'
    paths_to_try = [streamlit_path, local_path]
    for path in paths_to_try:
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    models = pickle.load(f)
                return models, path, paths_to_try
            except Exception as e:
                st.error(f"❌ Error loading {path}: {str(e)}")
                continue
    st.error("❌ Model file not found in any location!")
    st.write("**Files in current directory:**")
    try:
        files = os.listdir('.')
        for file in files:
            st.write(f"- {file}")
    except:
        pass
    return None, None, paths_to_try

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'fleet_data' not in st.session_state:
    st.session_state.fleet_data = None
if 'use_custom_thresholds' not in st.session_state:
    st.session_state.use_custom_thresholds = False
if 'custom_decisions' not in st.session_state:
    st.session_state.custom_decisions = None
if 'models' not in st.session_state:
    st.session_state.models = None
if 'model_load_attempted' not in st.session_state:
    st.session_state.model_load_attempted = False
if 'model_path_used' not in st.session_state:
    st.session_state.model_path_used = None
if 'checked_paths' not in st.session_state:
    st.session_state.checked_paths = []

if not st.session_state.model_load_attempted:
    st.session_state.model_load_attempted = True
    models, path_used, checked_paths = load_ml_models()
    st.session_state.models = models
    st.session_state.model_path_used = path_used
    st.session_state.checked_paths = checked_paths

def predict_with_models(df, models):
    if models is None:
        return df
    try:
        feature_cols = models.get('feature_names', [])
        if not feature_cols or not all(col in df.columns for col in feature_cols):
            st.warning("⚠️ Model feature mismatch. Using CSV predictions.")
            return df
        X = df[feature_cols].copy()
        for col in ['status', 'ownership_type', 'make', 'risk_category']:
            if col in X.columns and col in models['encoders']:
                X[col] = models['encoders'][col].transform(X[col].astype(str))
        X = X.fillna(X.median(numeric_only=True))
        X_scaled = models['scalers']['decision'].transform(X)
        decision_encoded = models['models']['decision_classifier'].predict(X_scaled)
        decision_proba = models['models']['decision_classifier'].predict_proba(X_scaled)
        df['decision'] = models['encoders']['decision_flag'].inverse_transform(decision_encoded)
        df['decision_confidence'] = decision_proba.max(axis=1) * 100
        if 'cost_predictor' in models['models'] and models['models']['cost_predictor']:
            X_scaled_cost = models['scalers']['cost'].transform(X)
            df['predicted_cost_90days'] = models['models']['cost_predictor'].predict(X_scaled_cost)
        if 'equity_predictor' in models['models'] and models['models']['equity_predictor']:
            X_scaled_equity = models['scalers']['equity'].transform(X)
            df['predicted_equity_6mo'] = models['models']['equity_predictor'].predict(X_scaled_equity)
        return df
    except Exception as e:
        st.warning(f"⚠️ Could not use models: {str(e)}. Using CSV predictions.")
        return df

def format_naira(value):
    if pd.isna(value):
        return "₦0"
    return f"₦{value:,.0f}"

def format_naira_millions(value):
    if pd.isna(value):
        return "₦0M"
    return f"₦{value/1e6:.2f}M"

with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 0.5rem 0;'>
            <div style='font-size: 3.5rem; margin-bottom: 0;'>🚚</div>
            <h2 style='margin: 0; background: linear-gradient(120deg, #60efff 0%, #6366f1 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: #FFFFFF;
                font-size: 1.5rem; line-height: 1;'>Fleet Intelligence</h2>
            <p style='color: #FFFFFF; font-size: 0.875rem; margin-top: 0.25rem;'>Management System</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 1rem 0; border-color: rgba(99, 102, 241, 0.2);'>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["Executive Dashboard", "Active Fleet", "Inactive Assets",
         "Predictive Analytics", "Truck Details", "Settings"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin: 2rem 0; border-color: rgba(99, 102, 241, 0.2);'>", unsafe_allow_html=True)

    st.markdown("### 📁 Data Management")

    uploaded_file = st.file_uploader(
        "Upload Fleet Data",
        type=['csv'],
        help="Upload your fleet data CSV file"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.fleet_data = df
            st.session_state.data_loaded = True
            st.success(f"✅ {len(df)} trucks loaded")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    if st.session_state.data_loaded:
        st.markdown("<hr style='margin: 1rem 0; border-color: rgba(99, 102, 241, 0.2);'>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; margin: 1rem 0;'>
                <h3 style='background: linear-gradient(120deg, #60efff 0%, #6366f1 100%);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    font-size: 1.25rem; font-weight: 700; margin: 0;'>⚡ Quick Stats</h3>
            </div>
        """, unsafe_allow_html=True)

        df = st.session_state.fleet_data

        if 'status' in df.columns:
            active_count = len(df[df['status'] == 'ACTIVE'])
            inactive_count = len(df[df['status'] == 'INACTIVE'])

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.05) 100%);
                        padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0;
                        border: 1px solid rgba(16, 185, 129, 0.3);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='color: #9ca3af; font-size: 0.75rem; text-transform: uppercase;'>Total Fleet</div>
                        <div style='color: #10b981; font-size: 1.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{len(df)}</div>
                    </div>
                    <div style='font-size: 1.5rem;'>🚚</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%);
                        padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0;
                        border: 1px solid rgba(99, 102, 241, 0.3);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='color: #9ca3af; font-size: 0.75rem; text-transform: uppercase;'>Active</div>
                        <div style='color: #60efff; font-size: 1.2rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{active_count}</div>
                    </div>
                    <div style='font-size: 1.2rem;'>✅</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.05) 100%);
                        padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0;
                        border: 1px solid rgba(239, 68, 68, 0.3);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='color: #9ca3af; font-size: 0.75rem; text-transform: uppercase;'>Inactive</div>
                        <div style='color: #ef4444; font-size: 1.2rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{inactive_count}</div>
                    </div>
                    <div style='font-size: 1.2rem;'>💤</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if 'fair_market_value' in df.columns:
            total_value = df['fair_market_value'].sum()
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.05) 100%);
                        padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0;
                        border: 1px solid rgba(245, 158, 11, 0.3);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='color: #9ca3af; font-size: 0.75rem; text-transform: uppercase;'>Total Value</div>
                        <div style='color: #f59e0b; font-size: 1.1rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>₦{total_value/1e6:.1f}M</div>
                    </div>
                    <div style='font-size: 1.5rem;'>💰</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def get_decision_color(decision):
    colors = {'KEEP': '#10b981', 'SELL': '#ef4444', 'INSPECT': '#f59e0b'}
    return colors.get(decision, '#6b7280')

def create_premium_gauge(value, title, max_value=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20, 'color': '#e0e7ff', 'family': 'Inter'}},
        number={'font': {'size': 40, 'color': '#60efff'}},
        gauge={
            'axis': {'range': [0, max_value], 'tickwidth': 2, 'tickcolor': '#6366f1'},
            'bar': {'color': '#6366f1', 'thickness': 0.75},
            'bgcolor': 'rgba(99, 102, 241, 0.05)',
            'borderwidth': 3,
            'bordercolor': 'rgba(99, 102, 241, 0.3)',
            'steps': [
                {'range': [0, 33], 'color': 'rgba(16, 185, 129, 0.2)'},
                {'range': [33, 66], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [66, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
            ],
            'threshold': {
                'line': {'color': '#60efff', 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e0e7ff', 'family': 'Inter'},
        height=280,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

if not st.session_state.data_loaded:
    st.markdown("""
        <div style='text-align: center; padding: 1.25rem 2rem 0.75rem 2rem;'>
            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🚚</div>
            <h1 style='font-size: 2.1rem; margin-bottom: 0.5rem;'>Fleet Intelligence Management System</h1>
            <p style='font-size: 1.05rem; color: #9ca3af; max-width: 600px; margin: 0 auto 1.25rem;'>
                AI-powered fleet management and decision intelligence platform
            </p>
            <div class='info-card' style='max-width: 700px; margin: 1rem auto;'>
                <h3 style='color: #60efff; margin-top: 0;'>👈 Upload Your Fleet Data</h3>
                <p style='color: #c7d2fe;'>Use the file uploader in the sidebar to begin analyzing your fleet.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>📊</div>
                <h3>Smart Analytics</h3>
                <p>AI-powered insights and predictions for every truck in your fleet</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>🎯</div>
                <h3>Smart Decisions</h3>
                <p>Automated KEEP, SELL, or INSPECT recommendations with confidence scores</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>💰</div>
                <h3>Cost Forecasting</h3>
                <p>Predict maintenance costs and equity changes for strategic planning</p>
            </div>
        """, unsafe_allow_html=True)

    st.stop()

df = st.session_state.fleet_data.copy()
models_available = st.session_state.models is not None

if not models_available:
    st.warning("⚠️ **ML Models NOT Found - Using CSV Predictions**")
    with st.expander("🔍 Debug: Model Loading Information"):
        st.write("**Script is looking for:** `fleet_models.pkl`")
        st.write("**Paths checked (in order):**")
        for i, path in enumerate(st.session_state.checked_paths, 1):
            st.code(f"{i}. {path}")
        st.write("**Instructions:**")
        st.info("""
        📝 **To enable live ML predictions:**

        1. Place `fleet_models.pkl` in the **same directory** as `fleet_dashboard.py`
        2. OR place it in your current working directory
        3. Refresh the page after moving the file
        """)
        st.write("**Current working directory:**")
        st.code(os.getcwd())
        try:
            script_location = str(Path(__file__).parent.absolute())
            st.write("**Script location:**")
            st.code(script_location)
        except:
            pass

if models_available:
    df = predict_with_models(df, st.session_state.models)

if st.session_state.use_custom_thresholds and st.session_state.custom_decisions is not None:
    df['decision'] = st.session_state.custom_decisions

if page == "Executive Dashboard":
    st.title("📊 Executive Fleet Overview")
    st.markdown("<p style='color: #ffffff; font-size: 1.125rem;'>Real-time insights and AI-powered recommendations for your entire fleet</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_trucks = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Fleet Size</div>
            <div class="metric-value">{total_trucks}</div>
            <div class="metric-delta">Trucks Managed</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if 'fair_market_value' in df.columns:
            total_value = df['fair_market_value'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Fleet Market Value</div>
                <div class="metric-value">₦{total_value/1e6:.2f}M</div>
                <div class="metric-delta">Current Valuation</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        if 'current_equity' in df.columns:
            total_equity = df['current_equity'].sum()
            equity_color = '#10b981' if total_equity > 0 else '#ef4444'
            symbol = '+' if total_equity > 0 else ''
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Equity Position</div>
                <div class="metric-value" style="background: linear-gradient(120deg, {equity_color} 0%, {equity_color} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {symbol}₦{total_equity/1e6:.2f}M
                </div>
                <div class="metric-delta">Net Asset Value</div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        if 'risk_score' in df.columns:
            avg_risk = df['risk_score'].mean()
            risk_color = '#10b981' if avg_risk < 40 else '#f59e0b' if avg_risk < 70 else '#ef4444'
            risk_label = 'LOW' if avg_risk < 40 else 'MEDIUM' if avg_risk < 70 else 'HIGH'
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Average Risk Score</div>
                <div class="metric-value" style="background: linear-gradient(120deg, {risk_color} 0%, {risk_color} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {avg_risk:.1f}
                </div>
                <div class="metric-delta">{risk_label} RISK</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2.5, 1.5])

    with col1:
        st.markdown("### 🎯 AI Decision Recommendations")
        if 'decision' in df.columns:
            decision_counts = df['decision'].value_counts()
            colors = [get_decision_color(d) for d in decision_counts.index]
            fig = go.Figure(data=[
                go.Bar(
                    x=decision_counts.index,
                    y=decision_counts.values,
                    marker=dict(color=colors, line=dict(color='rgba(99, 102, 241, 0.3)', width=2)),
                    text=decision_counts.values,
                    textposition='outside',
                    textfont=dict(size=16, color='#e0e7ff', family='Inter', weight='bold'),
                    hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
                )
            ])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                xaxis={'title': None, 'gridcolor': 'rgba(99, 102, 241, 0.1)', 'showgrid': False, 'tickfont': {'size': 14, 'color': '#c7d2fe'}},
                yaxis={'title': 'Number of Trucks', 'gridcolor': 'rgba(99, 102, 241, 0.1)', 'tickfont': {'size': 12, 'color': '#9ca3af'}},
                height=450, margin=dict(l=40, r=40, t=40, b=40),
                hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14, font_family='Inter')
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📋 Summary")
        if 'decision' in df.columns:
            for decision in ['KEEP', 'SELL', 'INSPECT']:
                count = len(df[df['decision'] == decision])
                pct = (count / len(df)) * 100
                badge_class = f"badge-{decision.lower()}"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.05) 100%);
                            padding: 1.25rem; border-radius: 12px; margin-bottom: 1rem;
                            border: 1px solid rgba(99, 102, 241, 0.2);">
                    <div class="{badge_class}" style="margin-bottom: 0.75rem;">{decision}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #60efff; font-size: 1.2rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{count}</span>
                        <span style="color: #9ca3af; font-size: 1rem;">({pct:.1f}%)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🚦 Fleet Status Distribution")
        if 'status' in df.columns:
            status_counts = df['status'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=status_counts.index, values=status_counts.values, hole=.5,
                marker=dict(colors=['#10b981', '#6b7280'], line=dict(color='rgba(99, 102, 241, 0.3)', width=3)),
                textfont=dict(size=16, color='#ffffff', family='Inter', weight='bold'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', font={'color': '#e0e7ff', 'family': 'Inter'}, height=400, showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=14)),
                margin=dict(l=20, r=20, t=40, b=60),
                hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14, font_family='Inter')
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### ⚠️ Risk Distribution Analysis")
        if 'risk_score' in df.columns:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=df['risk_score'], nbinsx=25,
                marker=dict(color='#6366f1', line=dict(color='rgba(99, 102, 241, 0.5)', width=1)),
                opacity=0.8, hovertemplate='Risk Score: %{x}<br>Count: %{y}<extra></extra>'
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                xaxis={'title': 'Risk Score', 'gridcolor': 'rgba(99, 102, 241, 0.1)', 'tickfont': {'size': 12, 'color': '#9ca3af'}},
                yaxis={'title': 'Number of Trucks', 'gridcolor': 'rgba(99, 102, 241, 0.1)', 'tickfont': {'size': 12, 'color': '#9ca3af'}},
                height=400, margin=dict(l=40, r=40, t=40, b=40),
                hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14, font_family='Inter')
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 💰 Financial Performance Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        if 'equity_ratio' in df.columns:
            positive_equity = len(df[df['equity_ratio'] > 0])
            negative_equity = len(df[df['equity_ratio'] < 0])
            fig = go.Figure(data=[go.Box(
                y=df['equity_ratio'], marker=dict(color='#60efff'), line=dict(color='#6366f1'),
                name='Equity Ratio', boxmean='sd', hovertemplate='Equity Ratio: %{y:.1f}%<extra></extra>'
            )])
            fig.add_hline(y=0, line_dash="dash", line_color="#ef4444", annotation_text="Break-even")
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                yaxis={'title': 'Equity Ratio (%)', 'gridcolor': 'rgba(99, 102, 241, 0.1)', 'tickfont': {'size': 12, 'color': '#9ca3af'}},
                height=350, showlegend=False, margin=dict(l=40, r=40, t=40, b=40),
                hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"<p style='text-align: center; color: #9ca3af;'>{positive_equity} positive • {negative_equity} negative</p>", unsafe_allow_html=True)

    with col2:
        if 'predicted_cost_90days' in df.columns:
            fig = go.Figure(data=[go.Histogram(
                x=df['predicted_cost_90days'], nbinsx=20,
                marker=dict(color='#f59e0b', line=dict(color='rgba(245, 158, 11, 0.5)', width=1)), opacity=0.8
            )])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                xaxis={'title': '90-Day Cost (₦)', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
                yaxis={'title': 'Count', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
                height=350, margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
            avg_cost = df['predicted_cost_90days'].mean()
            st.markdown(f"<p style='text-align: center; color: #9ca3af;'>Avg: ₦{avg_cost:,.0f}</p>", unsafe_allow_html=True)

    with col3:
        if 'predicted_equity_6mo' in df.columns:
            fig = go.Figure(data=[go.Histogram(
                x=df['predicted_equity_6mo'], nbinsx=20,
                marker=dict(color='#ef4444', line=dict(color='rgba(239, 68, 68, 0.5)', width=1)), opacity=0.8
            )])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                xaxis={'title': '6-Month Equity (₦)', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
                yaxis={'title': 'Count', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
                height=350, margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)

elif page == "Active Fleet":
    st.title("🚚 Active Fleet Management")
    st.markdown("<p style='color: #9ca3af; font-size: 1.125rem;'>Monitor and optimize your operational trucks</p>", unsafe_allow_html=True)

    active_df = df[df['status'] == 'ACTIVE'].copy()

    if len(active_df) == 0:
        st.warning("⚠️ No active trucks found in the fleet.")
        st.stop()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Active Trucks", len(active_df))
    with col2:
        if 'utilization_rate' in active_df.columns:
            st.metric("Avg Utilization", f"{active_df['utilization_rate'].mean():.1f}%")
    with col3:
        if 'revenue_per_mile' in active_df.columns:
            st.metric("Rev/Mile", f"₦{active_df['revenue_per_mile'].mean():.2f}")
    with col4:
        if 'cost_per_mile' in active_df.columns:
            st.metric("Cost/Mile", f"₦{active_df['cost_per_mile'].mean():.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("🔍 Advanced Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            decisions = ['All'] + list(active_df['decision'].unique()) if 'decision' in active_df.columns else ['All']
            selected_decision = st.selectbox("Decision", decisions)
        with col2:
            makes = ['All'] + sorted(active_df['make'].unique()) if 'make' in active_df.columns else ['All']
            selected_make = st.selectbox("Make", makes)
        with col3:
            if 'risk_score' in active_df.columns:
                risk_range = st.slider("Risk Score", 0.0, 100.0, (0.0, 100.0))

    filtered_df = active_df.copy()
    if selected_decision != 'All' and 'decision' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['decision'] == selected_decision]
    if selected_make != 'All' and 'make' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['make'] == selected_make]
    if 'risk_score' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['risk_score'] >= risk_range[0]) & (filtered_df['risk_score'] <= risk_range[1])]

    st.info(f"📊 Showing {len(filtered_df)} of {len(active_df)} active trucks")

    display_cols = ['Truck_ID', 'make', 'model', 'decision', 'risk_score', 'equity_ratio', 'utilization_rate']
    display_cols = [col for col in display_cols if col in filtered_df.columns]
    st.dataframe(filtered_df[display_cols], use_container_width=True, height=400)

elif page == "Inactive Assets":
    st.title("💤 Inactive Asset Disposition")
    st.markdown("<p style='color: #9ca3af; font-size: 1.125rem;'>Manage and optimize your inactive fleet inventory</p>", unsafe_allow_html=True)

    inactive_df = df[df['status'] == 'INACTIVE'].copy()

    if len(inactive_df) == 0:
        st.warning("⚠️ No inactive trucks found in the fleet.")
        st.stop()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Inactive Trucks</div>
            <div class="metric-value">{len(inactive_df)}</div>
            <div class="metric-delta">Total Count</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if 'current_equity' in inactive_df.columns:
            total_equity = inactive_df['current_equity'].sum()
            equity_color = '#10b981' if total_equity > 0 else '#ef4444'
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Equity</div>
                <div class="metric-value" style="background: linear-gradient(120deg, {equity_color} 0%, {equity_color} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    ₦{total_equity/1e6:.2f}M
                </div>
                <div class="metric-delta">Combined Position</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        if 'fair_market_value' in inactive_df.columns:
            market_value = inactive_df['fair_market_value'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Market Value</div>
                <div class="metric-value">₦{market_value/1e6:.2f}M</div>
                <div class="metric-delta">Total Worth</div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        if 'monthly_holding_cost' in inactive_df.columns:
            monthly_cost = inactive_df['monthly_holding_cost'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Monthly Burn</div>
                <div class="metric-value" style="color: #ef4444;">₦{monthly_cost:,.0f}</div>
                <div class="metric-delta">Holding Cost</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Liquidation Priority List")
    st.markdown("<p style='color: #9ca3af;'>Trucks sorted by equity ratio (worst first) - prioritize selling these assets</p>", unsafe_allow_html=True)

    priority_cols = ['Truck_ID', 'make', 'model', 'truck_age', 'months_owned',
                    'equity_ratio', 'current_equity', 'fair_market_value', 'decision']
    priority_cols = [col for col in priority_cols if col in inactive_df.columns]
    priority_df = inactive_df[priority_cols].sort_values('equity_ratio')

    display_df = priority_df.copy()
    if 'current_equity' in display_df.columns:
        display_df['current_equity'] = display_df['current_equity'].apply(format_naira)
    if 'fair_market_value' in display_df.columns:
        display_df['fair_market_value'] = display_df['fair_market_value'].apply(format_naira)

    st.dataframe(display_df, use_container_width=True, height=500)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💸 Equity Distribution")
        if 'equity_ratio' in inactive_df.columns:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=inactive_df['equity_ratio'], nbinsx=30,
                marker=dict(color='#ef4444', line=dict(color='rgba(239, 68, 68, 0.5)', width=1)),
                opacity=0.8, hovertemplate='Equity Ratio: %{x:.1f}%<br>Count: %{y}<extra></extra>'
            ))
            fig.add_vline(x=0, line_dash="dash", line_color="#60efff", annotation_text="Break-even", annotation_position="top")
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                xaxis={'title': 'Equity Ratio (%)', 'gridcolor': 'rgba(99, 102, 241, 0.1)', 'tickfont': {'size': 12, 'color': '#9ca3af'}},
                yaxis={'title': 'Number of Trucks', 'gridcolor': 'rgba(99, 102, 241, 0.1)', 'tickfont': {'size': 12, 'color': '#9ca3af'}},
                height=400, margin=dict(l=40, r=40, t=40, b=40),
                hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### ⏱️ Time Inactive")
        if 'months_owned' in inactive_df.columns:
            fig = go.Figure(data=[go.Box(
                y=inactive_df['months_owned'], marker=dict(color='#f59e0b'), line=dict(color='#d97706'),
                name='Months Owned', boxmean='sd', hovertemplate='Months Owned: %{y:.1f}<extra></extra>'
            )])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                yaxis={'title': 'Months Owned', 'gridcolor': 'rgba(99, 102, 241, 0.1)', 'tickfont': {'size': 12, 'color': '#9ca3af'}},
                height=400, showlegend=False, margin=dict(l=40, r=40, t=40, b=40),
                hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 💰 Financial Impact Analysis")

    if 'monthly_holding_cost' in inactive_df.columns and 'months_owned' in inactive_df.columns:
        inactive_df['total_holding_cost'] = (inactive_df['monthly_holding_cost'] * inactive_df['months_owned'])
        total_holding = inactive_df['total_holding_cost'].sum()
        st.error(f"💸 **Total capital tied up in inactive fleet: ₦{total_holding:,.0f}**")

        top_cost = inactive_df.nlargest(10, 'total_holding_cost')
        fig = go.Figure(data=[go.Bar(
            x=top_cost['Truck_ID'].astype(str), y=top_cost['total_holding_cost'],
            marker=dict(color='#ef4444', line=dict(color='rgba(239, 68, 68, 0.5)', width=2)),
            text=[f"₦{x:,.0f}" for x in top_cost['total_holding_cost']],
            textposition='outside', textfont=dict(size=12, color='#e0e7ff'),
            hovertemplate='<b>%{x}</b><br>Cost: ₦%{y:,.0f}<extra></extra>'
        )])
        fig.update_layout(
            title="Top 10 Cost Generators", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e7ff', 'family': 'Inter'},
            xaxis={'title': 'Truck ID', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
            yaxis={'title': 'Total Holding Cost (₦)', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
            height=450, margin=dict(l=40, r=40, t=60, b=40),
            hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Predictive Analytics":
    st.title("📈 Predictive Analytics & Forecasting")
    st.markdown("<p style='color: #9ca3af; font-size: 1.125rem;'>AI-powered cost and equity predictions for strategic planning</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💰 90-Day Maintenance Cost Predictions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if 'predicted_cost_90days' in df.columns:
            total_predicted = df['predicted_cost_90days'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Predicted Cost</div>
                <div class="metric-value">₦{total_predicted:,.0f}</div>
                <div class="metric-delta">Next 90 Days</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if 'predicted_cost_90days' in df.columns:
            avg_predicted = df['predicted_cost_90days'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg per Truck</div>
                <div class="metric-value">₦{avg_predicted:,.0f}</div>
                <div class="metric-delta">90-Day Average</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        if 'predicted_cost_90days' in df.columns and 'status' in df.columns:
            active_cost = df[df['status'] == 'ACTIVE']['predicted_cost_90days'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Active Fleet Cost</div>
                <div class="metric-value">₦{active_cost:,.0f}</div>
                <div class="metric-delta">90-Day Projection</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if 'predicted_cost_90days' in df.columns:
        fig = px.histogram(
            df, x='predicted_cost_90days', color='status' if 'status' in df.columns else None,
            marginal='box', title="Cost Prediction Distribution by Fleet Status",
            color_discrete_map={'ACTIVE': '#10b981', 'INACTIVE': '#6b7280'},
            labels={'predicted_cost_90days': '90-Day Predicted Cost (₦)'}
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e7ff', 'family': 'Inter'},
            xaxis={'gridcolor': 'rgba(99, 102, 241, 0.1)'}, yaxis={'gridcolor': 'rgba(99, 102, 241, 0.1)'},
            height=450, margin=dict(l=40, r=40, t=60, b=40),
            hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📊 6-Month Equity Projections")

    if 'predicted_equity_6mo' in df.columns and 'current_equity' in df.columns:
        col1, col2 = st.columns(2)
        with col1:
            current_equity = df['current_equity'].sum()
            predicted_equity = df['predicted_equity_6mo'].sum()
            change = predicted_equity - current_equity
            change_pct = (change / abs(current_equity) * 100) if current_equity != 0 else 0
            change_color = '#10b981' if change > 0 else '#ef4444'
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Projected Fleet Equity</div>
                <div class="metric-value">₦{predicted_equity/1e6:.2f}M</div>
                <div class="metric-delta" style="color: {change_color};">
                    {'↑' if change > 0 else '↓'} ₦{abs(change)/1e6:.2f}M ({abs(change_pct):.1f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            improving = len(df[df['predicted_equity_6mo'] > df['current_equity']])
            declining = len(df[df['predicted_equity_6mo'] < df['current_equity']])
            stable = len(df) - improving - declining
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Improving", improving, delta="↑", delta_color="normal")
            with col_b:
                st.metric("Declining", declining, delta="↓", delta_color="inverse")
            with col_c:
                st.metric("Stable", stable, delta="→", delta_color="off")

        st.markdown("<br>", unsafe_allow_html=True)

        fig = px.scatter(
            df, x='current_equity', y='predicted_equity_6mo',
            color='decision' if 'decision' in df.columns else None,
            size='risk_score' if 'risk_score' in df.columns else None,
            hover_data=['Truck_ID', 'make', 'model'] if all(col in df.columns for col in ['Truck_ID', 'make', 'model']) else None,
            title="Current vs Predicted Equity (6 Months)",
            color_discrete_map={'KEEP': '#10b981', 'SELL': '#ef4444', 'INSPECT': '#f59e0b'},
            labels={'current_equity': 'Current Equity (₦)', 'predicted_equity_6mo': 'Predicted Equity (₦)'}
        )

        max_val = max(df['current_equity'].max(), df['predicted_equity_6mo'].max())
        min_val = min(df['current_equity'].min(), df['predicted_equity_6mo'].min())

        fig.add_trace(go.Scatter(
            x=[min_val, max_val], y=[min_val, max_val], mode='lines',
            line=dict(dash='dash', color='#60efff', width=2), name='No Change Line',
            hovertemplate='No Change<extra></extra>'
        ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e7ff', 'family': 'Inter'},
            xaxis={'gridcolor': 'rgba(99, 102, 241, 0.1)'}, yaxis={'gridcolor': 'rgba(99, 102, 241, 0.1)'},
            height=550, margin=dict(l=40, r=40, t=60, b=40),
            hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📈 Top Equity Movers (6-Month Forecast)")

    if 'predicted_equity_6mo' in df.columns and 'current_equity' in df.columns:
        df['equity_change'] = df['predicted_equity_6mo'] - df['current_equity']
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🟢 Top Gainers")
            gainers = df.nlargest(10, 'equity_change')
            display_cols = ['Truck_ID', 'make', 'model', 'current_equity', 'predicted_equity_6mo', 'equity_change']
            display_cols = [col for col in display_cols if col in gainers.columns]
            display_gainers = gainers[display_cols].copy()
            for col in ['current_equity', 'predicted_equity_6mo', 'equity_change']:
                if col in display_gainers.columns:
                    display_gainers[col] = display_gainers[col].apply(format_naira)
            st.dataframe(display_gainers, use_container_width=True, height=400)

        with col2:
            st.markdown("#### 🔴 Top Decliners")
            decliners = df.nsmallest(10, 'equity_change')
            display_decliners = decliners[display_cols].copy()
            for col in ['current_equity', 'predicted_equity_6mo', 'equity_change']:
                if col in display_decliners.columns:
                    display_decliners[col] = display_decliners[col].apply(format_naira)
            st.dataframe(display_decliners, use_container_width=True, height=400)

elif page == "Truck Details":
    st.title("🔍 Individual Truck Deep Dive")

    truck_id = st.selectbox("Select Truck", df['Truck_ID'].sort_values().unique())
    truck = df[df['Truck_ID'] == truck_id].iloc[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"### {truck.get('make', 'N/A')} {truck.get('model', 'N/A')}")
        st.markdown(f"**ID:** {truck_id}")
    with col2:
        decision = truck.get('decision', 'INSPECT')
        badge_class = f"badge-{decision.lower()}"
        st.markdown(f"<div class='{badge_class}'>{decision}</div>", unsafe_allow_html=True)
    with col3:
        if 'risk_score' in truck:
            st.metric("Risk Score", f"{truck['risk_score']:.1f}")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        if 'risk_score' in truck:
            fig = create_premium_gauge(truck['risk_score'], "Risk Score")
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        if 'financial_health_score' in truck:
            fig = create_premium_gauge(truck['financial_health_score'], "Financial Health")
            st.plotly_chart(fig, use_container_width=True)
    with col3:
        if 'operational_efficiency_score' in truck:
            fig = create_premium_gauge(truck['operational_efficiency_score'], "Efficiency")
            st.plotly_chart(fig, use_container_width=True)

elif page == "Settings":
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] label { color: #ffffff !important; font-weight: 700 !important; font-size: 1rem !important; }
    div[data-testid="stVerticalBlock"] p { color: #ffffff !important; }
    div[data-testid="stVerticalBlock"] li { color: #ffffff !important; }
    div[data-testid="stVerticalBlock"] div { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

    st.title("⚙️ System Settings & Threshold Management")
    st.markdown("<p style='color: #9ca3af; font-size: 1.125rem;'>Customize decision criteria for your fleet's specific situation</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Decision Threshold Configuration")
    st.info("💡 **Important:** Your fleet has challenging equity positions (avg -59%). Use quick presets below or adjust manually.")

    st.markdown("#### ⚡ Quick Presets (One-Click Apply)")
    st.markdown("<p style='color: #60efff; font-size: 0.9rem; margin-top: -0.5rem;'>Choose a preset strategy to instantly recalculate all decisions</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🟢 Conservative\n(More KEEP)", use_container_width=True, type="primary"):
            with st.spinner("Applying Conservative preset..."):
                df_updated = st.session_state.fleet_data.copy()
                df_updated['new_decision'] = 'INSPECT'
                equity_15th = df_updated['equity_ratio'].quantile(0.15)
                risk_80th = df_updated['risk_score'].quantile(0.80)
                sell_mask = (
                    (df_updated['equity_ratio'] < equity_15th) |
                    ((df_updated['equity_ratio'] < -75) & (df_updated['risk_score'] > risk_80th))
                )
                df_updated.loc[sell_mask, 'new_decision'] = 'SELL'
                df_updated['combined_score'] = (
                    df_updated['equity_ratio'] * 0.6 + (100 - df_updated['risk_score']) * 0.4
                )
                combined_60th = df_updated['combined_score'].quantile(0.60)
                keep_mask = (
                    (df_updated['combined_score'] > combined_60th) |
                    (df_updated['equity_ratio'] > 0) |
                    ((df_updated['status'] == 'ACTIVE') & (df_updated['equity_ratio'] > -60))
                )
                df_updated.loc[keep_mask, 'new_decision'] = 'KEEP'
                st.session_state.custom_decisions = df_updated['new_decision'].copy()
                st.session_state.use_custom_thresholds = True
                st.success("✅ Conservative preset applied! Check Executive Dashboard.")
                st.rerun()

    with col2:
        if st.button("🟡 Balanced\n(Recommended)", use_container_width=True, type="primary"):
            with st.spinner("Applying Balanced preset..."):
                df_updated = st.session_state.fleet_data.copy()
                df_updated['new_decision'] = 'INSPECT'
                equity_25th = df_updated['equity_ratio'].quantile(0.25)
                equity_50th = df_updated['equity_ratio'].quantile(0.50)
                risk_75th = df_updated['risk_score'].quantile(0.75)
                sell_mask = (
                    (df_updated['equity_ratio'] < equity_25th) |
                    ((df_updated['equity_ratio'] < equity_50th) & (df_updated['risk_score'] > risk_75th)) |
                    ((df_updated['status'] == 'INACTIVE') &
                     (df_updated['months_owned'] > 12) &
                     (df_updated['equity_ratio'] < equity_50th)) |
                    ((df_updated['truck_age'] > 12) &
                     (df_updated['equity_ratio'] < equity_50th) &
                     (df_updated['maintenance_frequency'] > 1.5))
                )
                df_updated.loc[sell_mask, 'new_decision'] = 'SELL'
                df_updated['combined_score'] = (
                    df_updated['equity_ratio'] * 0.6 + (100 - df_updated['risk_score']) * 0.4
                )
                combined_65th = df_updated['combined_score'].quantile(0.65)
                keep_mask = (
                    (df_updated['combined_score'] > combined_65th) |
                    (df_updated['equity_ratio'] > 0) |
                    ((df_updated['status'] == 'ACTIVE') &
                     (df_updated['equity_ratio'] > equity_50th) &
                     (df_updated['risk_score'] < risk_75th) &
                     (df_updated['utilization_rate'] > 40))
                )
                df_updated.loc[keep_mask, 'new_decision'] = 'KEEP'
                st.session_state.custom_decisions = df_updated['new_decision'].copy()
                st.session_state.use_custom_thresholds = True
                st.success("✅ Balanced preset applied! Check Executive Dashboard.")
                st.rerun()

    with col3:
        if st.button("🔴 Aggressive\n(More SELL)", use_container_width=True, type="primary"):
            with st.spinner("Applying Aggressive preset..."):
                df_updated = st.session_state.fleet_data.copy()
                df_updated['new_decision'] = 'INSPECT'
                equity_40th = df_updated['equity_ratio'].quantile(0.40)
                equity_80th = df_updated['equity_ratio'].quantile(0.80)
                risk_60th = df_updated['risk_score'].quantile(0.60)
                sell_mask = (
                    (df_updated['equity_ratio'] < equity_40th) |
                    ((df_updated['equity_ratio'] < equity_80th) & (df_updated['risk_score'] > risk_60th)) |
                    ((df_updated['status'] == 'INACTIVE') &
                     (df_updated['months_owned'] > 8) &
                     (df_updated['equity_ratio'] < -40)) |
                    ((df_updated['truck_age'] > 10) & (df_updated['equity_ratio'] < -30))
                )
                df_updated.loc[sell_mask, 'new_decision'] = 'SELL'
                df_updated['combined_score'] = (
                    df_updated['equity_ratio'] * 0.6 + (100 - df_updated['risk_score']) * 0.4
                )
                combined_80th = df_updated['combined_score'].quantile(0.80)
                keep_mask = (
                    (df_updated['combined_score'] > combined_80th) |
                    (df_updated['equity_ratio'] > 0) |
                    ((df_updated['status'] == 'ACTIVE') &
                     (df_updated['equity_ratio'] > equity_80th) &
                     (df_updated['utilization_rate'] > 50))
                )
                df_updated.loc[keep_mask, 'new_decision'] = 'KEEP'
                st.session_state.custom_decisions = df_updated['new_decision'].copy()
                st.session_state.use_custom_thresholds = True
                st.success("✅ Aggressive preset applied! Check Executive Dashboard.")
                st.rerun()

    st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("#### 🎚️ Manual Threshold Adjustment (Advanced)")
    st.markdown("<p style='color: #f59e0b; font-size: 0.9rem; margin-top: -0.5rem;'>Fine-tune decision criteria with custom thresholds</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🟢 KEEP Criteria (Keep & Operate)")
        st.markdown("<p style='color: #10b981; font-size: 0.875rem;'>Trucks that should continue operating</p>", unsafe_allow_html=True)
        keep_equity = st.slider("Minimum Equity Ratio (%)", -100.0, 50.0, -40.0, help="Trucks above this equity may be kept. Current avg: -59%")
        keep_risk = st.slider("Maximum Risk Score", 0, 100, 60, help="Trucks below this risk score may be kept")
        keep_util = st.slider("Minimum Utilization Rate (%) - Active Only", 0, 100, 30, help="Active trucks above this utilization may be kept")
        keep_age = st.slider("Maximum Age (years)", 0, 20, 15, help="Trucks younger than this may be kept if other criteria met")

    with col2:
        st.markdown("#### 🔴 SELL Criteria (Liquidate)")
        st.markdown("<p style='color: #ef4444; font-size: 0.875rem;'>Trucks that should be sold immediately</p>", unsafe_allow_html=True)
        sell_equity = st.slider("Maximum Equity Ratio (%)", -150.0, 0.0, -70.0, help="Trucks below this equity should be sold. Deepest hole: -126%")
        sell_risk = st.slider("Minimum Risk Score", 0, 100, 80, help="High-risk trucks above this should be sold")
        sell_age = st.slider("Minimum Age (years) with negative equity", 0, 20, 8, help="Old trucks with negative equity should be sold")
        sell_inactive_months = st.slider("Inactive Duration (months)", 0, 36, 9, help="Inactive trucks longer than this should be sold")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.use_custom_thresholds:
        st.info("✅ **Custom thresholds are currently active.** The dashboard is showing adjusted decisions.")
        if st.button("🔄 Reset to Original ML Decisions"):
            st.session_state.use_custom_thresholds = False
            st.session_state.custom_decisions = None
            st.success("Reset to original ML decisions!")
            st.rerun()
    else:
        st.info("🤖 **Using original ML model decisions.** Adjust thresholds above to customize.")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("🔄 Recalculate All Decisions", use_container_width=True):
            with st.spinner("Recalculating decisions with new thresholds..."):
                df_updated = df.copy()
                df_updated['new_decision'] = 'INSPECT'
                sell_mask = (
                    (df_updated['equity_ratio'] < sell_equity) |
                    (df_updated['risk_score'] > sell_risk) |
                    ((df_updated['truck_age'] > sell_age) & (df_updated['equity_ratio'] < -20)) |
                    ((df_updated['status'] == 'INACTIVE') &
                     (df_updated['months_owned'] > sell_inactive_months) &
                     (df_updated['equity_ratio'] < -30))
                )
                df_updated.loc[sell_mask, 'new_decision'] = 'SELL'
                keep_mask = (
                    (df_updated['equity_ratio'] > keep_equity) &
                    (df_updated['risk_score'] < keep_risk) &
                    (df_updated['truck_age'] < keep_age) &
                    (
                        ((df_updated['status'] == 'ACTIVE') & (df_updated['utilization_rate'] > keep_util)) |
                        ((df_updated['status'] == 'INACTIVE') & (df_updated['months_owned'] < 6) & (df_updated['equity_ratio'] > -20)) |
                        (df_updated['equity_ratio'] > 0)
                    )
                )
                df_updated.loc[keep_mask, 'new_decision'] = 'KEEP'
                st.session_state.custom_decisions = df_updated['new_decision'].copy()
                st.session_state.use_custom_thresholds = True
                st.success("✅ Decisions recalculated successfully!")
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### <span style='background: linear-gradient(120deg, #60efff 0%, #f59e0b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📊 Your Fleet's Current Situation</span>", unsafe_allow_html=True)
    st.markdown("<p style='color: #60efff; font-size: 1rem; margin-top: -1rem;'>Real-time analysis of your fleet's key metrics</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### <span style='color: #10b981;'>Equity Distribution</span>", unsafe_allow_html=True)
        positive_equity = len(df[df['equity_ratio'] > 0])
        negative_equity = len(df[df['equity_ratio'] < 0])
        avg_equity = df['equity_ratio'].mean()

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
                    padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>POSITIVE EQUITY</div>
            <div style='color: #10b981; font-size: 1.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{positive_equity}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(positive_equity/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
                    padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0; border: 1px solid rgba(239, 68, 68, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>NEGATIVE EQUITY</div>
            <div style='color: #ef4444; font-size: 1.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{negative_equity}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(negative_equity/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)

        equity_color = '#10b981' if avg_equity >= 0 else '#ef4444'
        equity_status = 'Positive' if avg_equity >= 0 else 'Deeply underwater' if avg_equity < -30 else 'Challenging'
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
                    padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0; border: 1px solid rgba(99, 102, 241, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>AVERAGE EQUITY RATIO</div>
            <div style='color: {equity_color}; font-size: 1.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{avg_equity:.1f}%</div>
            <div style='color: #60efff; font-size: 0.875rem;'>{equity_status}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### <span style='color: #f59e0b;'>Risk Profile</span>", unsafe_allow_html=True)
        low_risk = len(df[df['risk_score'] < 40])
        medium_risk = len(df[(df['risk_score'] >= 40) & (df['risk_score'] < 70)])
        high_risk = len(df[df['risk_score'] >= 70])

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
                    padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>LOW RISK (&lt;40)</div>
            <div style='color: #10b981; font-size: 1.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{low_risk}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(low_risk/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.05) 100%);
                    padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0; border: 1px solid rgba(245, 158, 11, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>MEDIUM RISK (40-70)</div>
            <div style='color: #f59e0b; font-size: 1.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{medium_risk}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(medium_risk/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
                    padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0; border: 1px solid rgba(239, 68, 68, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>HIGH RISK (&gt;70)</div>
            <div style='color: #ef4444; font-size: 1.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{high_risk}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(high_risk/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("#### <span style='color: #60efff;'>Fleet Status</span>", unsafe_allow_html=True)
        active = len(df[df['status'] == 'ACTIVE'])
        inactive = len(df[df['status'] == 'INACTIVE'])

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
                    padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>ACTIVE TRUCKS</div>
            <div style='color: #10b981; font-size: 1.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{active}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(active/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
                    padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0; border: 1px solid rgba(239, 68, 68, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>INACTIVE TRUCKS</div>
            <div style='color: #ef4444; font-size: 1.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{inactive}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(inactive/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)

        if 'utilization_rate' in df.columns:
            avg_util = df[df['status'] == 'ACTIVE']['utilization_rate'].mean()
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
                        padding: 0.65rem 0.85rem; border-radius: 10px; margin: 0.4rem 0; border: 1px solid rgba(99, 102, 241, 0.3);'>
                <div style='color: #9ca3af; font-size: 0.75rem;'>AVG UTILIZATION (ACTIVE)</div>
                <div style='color: #60efff; font-size: 1.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{avg_util:.1f}%</div>
                <div style='color: #c7d2fe; font-size: 0.875rem;'>Active Fleet Performance</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 💡 Threshold Recommendations")

    avg_equity = df['equity_ratio'].mean()

    if avg_equity < -50:
        st.error(f"""
        **🚨 Critical Equity Situation Detected (Avg: {avg_equity:.1f}%)**

        Your fleet has severe negative equity. **Recommended thresholds for better distribution:**

        **KEEP (Best Performers):**
        - Equity > **-40%** (less underwater than average)
        - Risk < **60** (acceptable risk)
        - Utilization > **30%** (being used)
        - Age < **15 years**

        **SELL (Worst Performers):**
        - Equity < **-70%** (deep losses)
        - Age > **8 years** with negative equity
        - Inactive > **9 months** with bad equity

        **INSPECT (Middle Ground):**
        - Everything else needs human review
        """)
    elif avg_equity < -20:
        st.warning(f"""
        **⚠️ Challenging Equity Position (Avg: {avg_equity:.1f}%)**

        Recommended thresholds:
        - **KEEP:** Equity > -30%, Risk < 50
        - **SELL:** Equity < -60%, Age > 10
        - Focus on operational efficiency for KEEP trucks
        """)
    else:
        st.success(f"""
        **✅ Healthy Fleet Position (Avg: {avg_equity:.1f}%)**

        Standard thresholds work well:
        - **KEEP:** Equity > 0%
        - **SELL:** Equity < -30%
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📥 Export Options")
    st.markdown("<p style='color: #60efff; font-size: 1rem; margin-top: -1rem;'>Download your fleet data and reports</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        csv = df.to_csv(index=False)
        st.download_button("📊 Download Full Dataset", csv, "fleet_data.csv", "text/csv", use_container_width=True)

    with col2:
        if 'decision' in df.columns:
            sell_csv = df[df['decision'] == 'SELL'].to_csv(index=False)
            st.download_button("🔴 Download SELL List", sell_csv, "sell_list.csv", "text/csv", use_container_width=True)

    with col3:
        summary = f"Fleet Report - {datetime.now().strftime('%Y-%m-%d')}\nTotal: {len(df)} trucks"
        st.download_button("📋 Download Summary", summary, "summary.txt", "text/plain", use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #6b7280;'>
    <p style='font-size: 0.875rem; margin: 0;'>Fleet Intelligence Pro v1.0 | Powered by AI</p>
    <p style='font-size: 0.75rem; margin-top: 0.5rem;'>© 2026 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)