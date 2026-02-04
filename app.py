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

# Page configuration
st.set_page_config(
    page_title="Fleet Intelligence Management System",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-Modern Dashboard Theme with Animated Background
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* ROOT VARIABLES */
    :root {
        --neon-blue: #00f0ff;
        --neon-pink: #ff006e;
        --neon-purple: #8b5cf6;
        --neon-green: #00ff88;
        --bright-text: #ffffff;
    }
    
    /* ANIMATED GEOMETRIC BACKGROUND */
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: #0d0221;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Animated gradient mesh background */
    .stApp::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(0, 240, 255, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 0, 110, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 60% 60%, rgba(0, 255, 136, 0.1) 0%, transparent 40%);
        animation: meshFloat 20s ease-in-out infinite;
        z-index: 0;
        pointer-events: none;
    }
    
    @keyframes meshFloat {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(30px, -30px) rotate(5deg); }
        66% { transform: translate(-20px, 20px) rotate(-5deg); }
    }
    
    /* Floating geometric shapes */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image:
            linear-gradient(45deg, transparent 48%, rgba(0, 240, 255, 0.03) 49%, rgba(0, 240, 255, 0.03) 51%, transparent 52%),
            linear-gradient(-45deg, transparent 48%, rgba(255, 0, 110, 0.03) 49%, rgba(255, 0, 110, 0.03) 51%, transparent 52%);
        background-size: 100px 100px;
        animation: geometricMove 30s linear infinite;
        z-index: 0;
        pointer-events: none;
        opacity: 0.4;
    }
    
    @keyframes geometricMove {
        0% { background-position: 0 0, 0 0; }
        100% { background-position: 100px 100px, -100px 100px; }
    }
    
    /* Content above background */
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"] {
        position: relative;
        z-index: 1;
    }
    
    /* MODERN GLASS-MORPHISM SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(13, 2, 33, 0.95) 0%, 
            rgba(13, 2, 33, 0.85) 100%) !important;
        backdrop-filter: blur(20px) saturate(180%);
        border-right: 1px solid rgba(0, 240, 255, 0.2);
        box-shadow: 8px 0 32px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 300px;
        background: radial-gradient(circle at 50% 0%, rgba(0, 240, 255, 0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    
    /* VIBRANT TYPOGRAPHY */
    h1 {
        font-family: 'Poppins', sans-serif !important;
        color: var(--bright-text) !important;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, 
            var(--neon-blue) 0%, 
            var(--neon-pink) 50%, 
            var(--neon-purple) 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-shadow: 0 0 80px rgba(0, 240, 255, 0.5);
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.02em !important;
        animation: titleGlow 4s ease-in-out infinite;
        line-height: 1.2 !important;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: brightness(1) drop-shadow(0 0 20px rgba(0, 240, 255, 0.3)); }
        50% { filter: brightness(1.4) drop-shadow(0 0 40px rgba(255, 0, 110, 0.5)); }
    }
    
    h2 {
        font-family: 'Poppins', sans-serif !important;
        color: var(--bright-text) !important;
        font-weight: 700 !important;
        font-size: 2.25rem !important;
        margin: 2.5rem 0 1.5rem 0 !important;
        text-shadow: 0 2px 20px rgba(0, 0, 0, 0.5);
        letter-spacing: -0.01em !important;
    }
    
    h3 {
        font-family: 'Poppins', sans-serif !important;
        color: var(--neon-blue) !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        text-shadow: 0 0 30px rgba(0, 240, 255, 0.4);
        margin: 1.5rem 0 !important;
    }
    
    h4 {
        font-family: 'Poppins', sans-serif !important;
        color: var(--bright-text) !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
    }
    
    p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
    }
    
    /* FLOATING GLASS CARDS */
    .metric-card {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.08) 0%, 
            rgba(255, 255, 255, 0.03) 100%);
        backdrop-filter: blur(15px) saturate(180%);
        padding: 2.5rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15),
            0 0 0 1px rgba(0, 240, 255, 0.1);
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(0, 240, 255, 0.1), 
            transparent);
        transition: left 0.5s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-12px) scale(1.03);
        box-shadow: 
            0 20px 60px rgba(0, 240, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.25),
            0 0 0 2px rgba(0, 240, 255, 0.4);
        border-color: rgba(0, 240, 255, 0.5);
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, 
            var(--neon-blue) 0%, 
            var(--neon-green) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.75rem 0;
        filter: drop-shadow(0 0 20px rgba(0, 240, 255, 0.6));
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.75);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-delta {
        font-size: 1.1rem;
        color: var(--neon-green);
        margin-top: 0.75rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    /* VIBRANT NEON BADGES */
    .badge-keep {
        background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%);
        color: #0d0221;
        padding: 0.85rem 2rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.95rem;
        display: inline-block;
        box-shadow: 
            0 6px 25px rgba(0, 255, 136, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        animation: badgeFloat 3s ease-in-out infinite;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .badge-sell {
        background: linear-gradient(135deg, #ff006e 0%, #ff4d00 100%);
        color: #ffffff;
        padding: 0.85rem 2rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.95rem;
        display: inline-block;
        box-shadow: 
            0 6px 25px rgba(255, 0, 110, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        animation: badgeFloat 3s ease-in-out infinite;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .badge-inspect {
        background: linear-gradient(135deg, #ffd000 0%, #ff8c00 100%);
        color: #0d0221;
        padding: 0.85rem 2rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.95rem;
        display: inline-block;
        box-shadow: 
            0 6px 25px rgba(255, 208, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        animation: badgeFloat 3s ease-in-out infinite;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    @keyframes badgeFloat {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-5px) scale(1.05); }
    }
    
    /* FANCY INTERACTIVE BUTTONS */
    .stButton>button {
        background: linear-gradient(135deg, 
            var(--neon-blue) 0%, 
            var(--neon-purple) 100%) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px !important;
        padding: 1.25rem 3rem !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        box-shadow: 
            0 10px 30px rgba(0, 240, 255, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 
            0 15px 40px rgba(255, 0, 110, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* DOWNLOAD BUTTONS */
    .stDownloadButton>button {
        background: linear-gradient(135deg, 
            var(--neon-pink) 0%, 
            var(--neon-purple) 100%) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px !important;
        padding: 1.25rem 3rem !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        box-shadow: 
            0 10px 30px rgba(255, 0, 110, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.4s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 
            0 15px 40px rgba(139, 92, 246, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
    }
    
    /* MODERN GLASS FILE UPLOADER */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, 
            rgba(0, 240, 255, 0.08) 0%, 
            rgba(139, 92, 246, 0.08) 100%) !important;
        border: 3px dashed rgba(0, 240, 255, 0.5) !important;
        border-radius: 24px !important;
        padding: 3rem !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(255, 0, 110, 0.7) !important;
        background: linear-gradient(135deg, 
            rgba(0, 240, 255, 0.12) 0%, 
            rgba(255, 0, 110, 0.12) 100%) !important;
        box-shadow: 0 12px 48px rgba(0, 240, 255, 0.3) !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: var(--bright-text) !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* MODERN DATA TABLES */
    .dataframe {
        background: rgba(13, 2, 33, 0.7) !important;
        border-radius: 20px !important;
        overflow: hidden !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(0, 240, 255, 0.2) !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, 
            var(--neon-blue) 0%, 
            var(--neon-purple) 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        padding: 1.5rem !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        font-size: 0.95rem !important;
        box-shadow: inset 0 -1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .dataframe tbody tr {
        background: rgba(255, 255, 255, 0.03) !important;
        border-bottom: 1px solid rgba(0, 240, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .dataframe tbody tr:hover {
        background: linear-gradient(90deg, 
            rgba(0, 240, 255, 0.15) 0%, 
            rgba(255, 0, 110, 0.15) 100%) !important;
        transform: scale(1.02) !important;
        box-shadow: 
            0 6px 25px rgba(0, 240, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }
    
    .dataframe tbody tr td {
        color: var(--bright-text) !important;
        padding: 1.25rem !important;
        font-weight: 500 !important;
        border: none !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background: rgba(255, 255, 255, 0.05) !important;
    }
    
    /* MODERN EXPANDERS */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, 
            rgba(0, 240, 255, 0.12) 0%, 
            rgba(139, 92, 246, 0.08) 100%) !important;
        border-radius: 16px !important;
        border: 2px solid rgba(0, 240, 255, 0.3) !important;
        color: var(--bright-text) !important;
        font-weight: 700 !important;
        padding: 1.25rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(0, 240, 255, 0.15) !important;
        border-color: rgba(255, 0, 110, 0.5) !important;
        box-shadow: 0 6px 25px rgba(0, 240, 255, 0.3) !important;
        transform: translateX(5px);
    }
    
    /* BRIGHT METRICS */
    [data-testid="stMetricValue"] {
        color: var(--neon-blue) !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-shadow: 
            0 0 30px rgba(0, 240, 255, 0.6),
            0 0 60px rgba(0, 240, 255, 0.3) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--bright-text) !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: var(--neon-green) !important;
        font-weight: 600 !important;
    }
    
    /* VIBRANT DIVIDER */
    hr {
        border: none !important;
        height: 3px !important;
        background: linear-gradient(90deg, 
            transparent, 
            var(--neon-blue) 20%, 
            var(--neon-pink) 50%, 
            var(--neon-purple) 80%, 
            transparent) !important;
        margin: 4rem 0 !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.5) !important;
        animation: dividerGlow 3s ease-in-out infinite;
    }
    
    @keyframes dividerGlow {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    /* ENHANCED ALERT BOXES */
    .stSuccess {
        background: linear-gradient(135deg, 
            rgba(0, 255, 136, 0.15) 0%, 
            rgba(0, 212, 255, 0.1) 100%) !important;
        border-left: 5px solid var(--neon-green) !important;
        border-radius: 16px !important;
        color: var(--bright-text) !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 8px 32px rgba(0, 255, 136, 0.2) !important;
        padding: 1.5rem !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, 
            rgba(255, 208, 0, 0.15) 0%, 
            rgba(255, 140, 0, 0.1) 100%) !important;
        border-left: 5px solid #ffd000 !important;
        border-radius: 16px !important;
        color: var(--bright-text) !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 8px 32px rgba(255, 208, 0, 0.2) !important;
        padding: 1.5rem !important;
    }
    
    .stError {
        background: linear-gradient(135deg, 
            rgba(255, 0, 110, 0.15) 0%, 
            rgba(255, 77, 0, 0.1) 100%) !important;
        border-left: 5px solid var(--neon-pink) !important;
        border-radius: 16px !important;
        color: var(--bright-text) !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 8px 32px rgba(255, 0, 110, 0.2) !important;
        padding: 1.5rem !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, 
            rgba(0, 240, 255, 0.15) 0%, 
            rgba(139, 92, 246, 0.1) 100%) !important;
        border-left: 5px solid var(--neon-blue) !important;
        border-radius: 16px !important;
        color: var(--bright-text) !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 8px 32px rgba(0, 240, 255, 0.2) !important;
        padding: 1.5rem !important;
    }
    
    /* SIDEBAR NAVIGATION */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: var(--bright-text) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        padding: 0.75rem !important;
        border-radius: 12px !important;
    }
    
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        color: var(--neon-blue) !important;
        background: rgba(0, 240, 255, 0.1) !important;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.6) !important;
        transform: translateX(8px);
    }
    
    /* SIDEBAR HEADINGS */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        background: linear-gradient(120deg, 
            var(--neon-blue) 0%, 
            var(--neon-pink) 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    [data-testid="stSidebar"] p {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* SETTINGS - ALL TEXT BRIGHT */
    .main div {
        color: var(--bright-text) !important;
    }
    
    .main label {
        color: var(--bright-text) !important;
        font-weight: 700 !important;
    }
    
    .main .stSlider label {
        color: var(--bright-text) !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    div[data-testid="stVerticalBlock"] label {
        color: var(--bright-text) !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stVerticalBlock"] p {
        color: var(--bright-text) !important;
    }
    
    /* VIBRANT SCROLLBAR */
    ::-webkit-scrollbar {
        width: 14px;
        height: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 240, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, 
            var(--neon-blue) 0%, 
            var(--neon-pink) 100%);
        border-radius: 10px;
        border: 2px solid rgba(13, 2, 33, 0.5);
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, 
            var(--neon-pink) 0%, 
            var(--neon-purple) 100%);
        box-shadow: 0 0 20px rgba(255, 0, 110, 0.7);
    }
    
    /* RESPONSIVE SPACING */
    .main {
        padding: 2rem 3rem !important;
    }
    
    @media (max-width: 768px) {
        .main {
            padding: 1rem 1.5rem !important;
        }
        
        h1 {
            font-size: 2.5rem !important;
        }
        
        .metric-card {
            padding: 1.5rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)
    
    /* Animated particle background */
    .stApp {
        font-family: 'Outfit', sans-serif;
        position: relative;
        background: #0a0e27;
        overflow-x: hidden;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(236, 72, 153, 0.1) 0%, transparent 40%);
        animation: backgroundShift 15s ease infinite;
        z-index: 0;
        pointer-events: none;
    }
    
    @keyframes backgroundShift {
        0%, 100% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.1) rotate(5deg); }
    }
    
    /* Floating particles */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, rgba(255,255,255,0.2), transparent),
            radial-gradient(2px 2px at 60% 70%, rgba(99,102,241,0.3), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(236,72,153,0.2), transparent),
            radial-gradient(1px 1px at 80% 10%, rgba(139,92,246,0.2), transparent);
        background-size: 200% 200%;
        animation: particleFloat 20s linear infinite;
        z-index: 0;
        pointer-events: none;
    }
    
    @keyframes particleFloat {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 100%; }
    }
    
    /* All content above background */
    [data-testid="stVerticalBlock"] {
        position: relative;
        z-index: 1;
    }
    
    /* Glass-morphism sidebar */
    [data-testid="stSidebar"] {
        background: rgba(20, 27, 45, 0.7) !important;
        backdrop-filter: blur(20px) saturate(180%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 200px;
        background: linear-gradient(180deg, rgba(99, 102, 241, 0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    
    /* Modern headers with glow */
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        background: linear-gradient(135deg, #60efff 0%, #ec4899 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(96, 239, 255, 0.5);
        margin-bottom: 1rem !important;
        animation: headerGlow 3s ease-in-out infinite;
        letter-spacing: -0.02em;
    }
    
    @keyframes headerGlow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.3); }
    }
    
    h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin-top: 2rem !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }
    
    h3 {
        color: #60efff !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        text-shadow: 0 0 20px rgba(96, 239, 255, 0.3);
    }
    
    /* Ultra-modern metric cards with depth */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(10px) saturate(150%);
        padding: 2rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(96, 239, 255, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(99, 102, 241, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(96, 239, 255, 0.4);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60efff 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
        filter: drop-shadow(0 0 10px rgba(96, 239, 255, 0.5));
        font-family: 'Space Mono', monospace;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
    }
    
    .metric-delta {
        font-size: 1rem;
        color: #60efff;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Vibrant decision badges with pulse */
    .badge-keep {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: #ffffff;
        padding: 0.75rem 1.5rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.875rem;
        display: inline-block;
        box-shadow: 
            0 4px 20px rgba(16, 185, 129, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        animation: badgePulse 2s ease-in-out infinite;
    }
    
    .badge-sell {
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
        color: #ffffff;
        padding: 0.75rem 1.5rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.875rem;
        display: inline-block;
        box-shadow: 
            0 4px 20px rgba(239, 68, 68, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        animation: badgePulse 2s ease-in-out infinite;
    }
    
    .badge-inspect {
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: #ffffff;
        padding: 0.75rem 1.5rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.875rem;
        display: inline-block;
        box-shadow: 
            0 4px 20px rgba(245, 158, 11, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        animation: badgePulse 2s ease-in-out infinite;
    }
    
    @keyframes badgePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Modern info cards */
    .info-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.08) 100%);
        border-left: 4px solid #60efff;
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Fancy modern buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 32px rgba(236, 72, 153, 0.6) !important;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    /* Glassmorphism file uploader */
    [data-testid="stFileUploader"] {
        background: rgba(99, 102, 241, 0.08) !important;
        border: 2px dashed rgba(96, 239, 255, 0.4) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(236, 72, 153, 0.6) !important;
        background: rgba(99, 102, 241, 0.12) !important;
    }
    
    /* Modern data tables with alternating glow */
    .dataframe {
        background-color: rgba(17, 24, 39, 0.6) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 1.25rem !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-size: 0.875rem !important;
    }
    
    .dataframe tbody tr {
        background: rgba(99, 102, 241, 0.04) !important;
        border-bottom: 1px solid rgba(99, 102, 241, 0.15) !important;
        transition: all 0.3s ease !important;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(96, 239, 255, 0.1) !important;
        transform: scale(1.01) !important;
        box-shadow: 0 4px 20px rgba(96, 239, 255, 0.3) !important;
    }
    
    .dataframe tbody tr td {
        color: #ffffff !important;
        padding: 1rem !important;
        font-weight: 500 !important;
        border: none !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background: rgba(99, 102, 241, 0.06) !important;
    }
    
    /* Modern expanderswith glow */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(96, 239, 255, 0.3) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(99, 102, 241, 0.2) !important;
        border-color: rgba(236, 72, 153, 0.5) !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3) !important;
    }
    
    /* Bright metrics */
    [data-testid="stMetricValue"] {
        color: #60efff !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 20px rgba(96, 239, 255, 0.5) !important;
        font-family: 'Space Mono', monospace !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    /* Colorful divider */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #60efff 20%, #ec4899 50%, #8b5cf6 80%, transparent) !important;
        margin: 3rem 0 !important;
        opacity: 0.6 !important;
    }
    
    /* Enhanced alert boxes */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%) !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%) !important;
        border-left: 4px solid #f59e0b !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%) !important;
        border-left: 4px solid #6366f1 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Sidebar navigation - white text */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        color: #60efff !important;
        text-shadow: 0 0 10px rgba(96, 239, 255, 0.5) !important;
    }
    
    /* Sidebar headings */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        background: linear-gradient(120deg, #60efff 0%, #ec4899 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    [data-testid="stSidebar"] p {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* File uploader in sidebar */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: rgba(99, 102, 241, 0.12) !important;
        border: 2px dashed rgba(96, 239, 255, 0.5) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploader"] label {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Settings page text - all white */
    .main div {
        color: #ffffff !important;
    }
    
    .main label {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .main .stSlider label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(99, 102, 241, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
        border-radius: 10px;
        border: 2px solid rgba(10, 14, 39, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #f472b6 100%);
    }
    </style>
""", unsafe_allow_html=True)
    
    /* Data tables */
    .dataframe {
        background-color: rgba(17, 24, 39, 0.5) !important;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Fancy colored table styling */
    .dataframe thead tr th {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 1rem !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.875rem !important;
    }
    
    .dataframe tbody tr {
        background: rgba(99, 102, 241, 0.03) !important;
        border-bottom: 1px solid rgba(99, 102, 241, 0.1) !important;
        transition: all 0.2s ease;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(99, 102, 241, 0.1) !important;
        transform: scale(1.01);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    
    .dataframe tbody tr td {
        color: #e0e7ff !important;
        padding: 0.75rem !important;
        font-weight: 500 !important;
        border: none !important;
    }
    
    /* Alternating row colors */
    .dataframe tbody tr:nth-child(even) {
        background: rgba(99, 102, 241, 0.05) !important;
    }
    
    /* Settings page - FORCE ALL text white */
    .main h4 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .main p {
        color: #ffffff !important;
    }
    
    .main label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .main .stSlider label {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .main .stSlider p {
        color: #ffffff !important;
    }
    
    /* Force slider text white */
    .main .stSlider div[data-baseweb="slider"] + div {
        color: #ffffff !important;
    }
    
    .main .stSlider small {
        color: #ffffff !important;
    }
    
    /* All text elements */
    .main div {
        color: #ffffff !important;
    }
    
    .main span {
        color: #ffffff !important;
    }
    
    .main .markdown-text-container {
        color: #ffffff !important;
    }
    
    .main ul li {
        color: #ffffff !important;
    }
    
    .main strong {
        color: #60efff !important;
    }
    
    /* All markdown text in Settings */
    .main .element-container p {
        color: #ffffff !important;
    }
    
    .main .element-container li {
        color: #ffffff !important;
    }
    
    /* Slider help text */
    .main .stSlider [data-baseweb="tooltip"] {
        color: #ffffff !important;
    }
    
    /* Form labels and descriptions */
    .main .stMarkdown {
        color: #ffffff !important;
    }
    
    .main .stMarkdown p {
        color: #ffffff !important;
    }
    
    .main .stMarkdown li {
        color: #ffffff !important;
    }
    
    /* Headers with different colors */
    .main h1 {
        color: #60efff !important;
    }
    
    .main h2 {
        color: #60efff !important;
    }
    
    .main h3 {
        color: #f59e0b !important;
    }
    
    .main h4 {
        color: #10b981 !important;
    }
    
    /* Slider value text */
    .main [data-baseweb="slider"] {
        color: #ffffff !important;
    }
    
    /* Help icon text */
    .main [data-testid="stTooltipHoverTarget"] {
        color: #ffffff !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(99, 102, 241, 0.08);
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        color: #e0e7ff !important;
        font-weight: 600;
    }
    
    /* Selectbox and inputs */
    .stSelectbox, .stMultiSelect, .stSlider {
        color: #e0e7ff;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #60efff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
        font-weight: 600 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(99, 102, 241, 0.2);
        margin: 2rem 0;
    }
    
    /* Success/Warning/Error boxes */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
        border-radius: 8px;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
    }
    
    .stInfo {
        background: rgba(99, 102, 241, 0.1);
        border-left: 4px solid #6366f1;
        border-radius: 8px;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #e0e7ff !important;
    }
    
    /* Sidebar NAVIGATION ONLY - white text for radio buttons */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar headings - keep gradient */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        background: linear-gradient(120deg, #60efff 0%, #6366f1 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    /* Sidebar paragraph text - light blue */
    [data-testid="stSidebar"] p {
        color: #c7d2fe !important;
    }
    
    /* File uploader in sidebar - visible */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: rgba(99, 102, 241, 0.1) !important;
        border: 2px dashed rgba(99, 102, 241, 0.5) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploader"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploader"] small {
        color: #9ca3af !important;
    }
    
    /* Settings page text - make readable */
    .main h4 {
        color: #e0e7ff !important;
    }
    
    .main p {
        color: #c7d2fe !important;
    }
    
    /* Slider labels in main area */
    .main .stSlider label {
        color: #e0e7ff !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(99, 102, 241, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.3);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# MODEL LOADING LOGIC - COMPREHENSIVE PATH CHECKING
# ============================================================================

def load_ml_models():
    """
    Comprehensive model loading with multiple fallback paths.
    Returns (models_dict, path_used, checked_paths)
    """
    paths_to_check = []
    
    # 1. Same directory as this script
    try:
        script_dir = Path(__file__).parent.absolute()
        paths_to_check.append(script_dir / 'fleet_models.pkl')
    except:
        pass
    
    # 2. Current working directory
    cwd = Path(os.getcwd())
    paths_to_check.append(cwd / 'fleet_models.pkl')
    
    # 3. Parent directory
    paths_to_check.append(cwd.parent / 'fleet_models.pkl')
    
    # 4. Common model directories
    paths_to_check.extend([
        Path('./models/fleet_models.pkl'),
        Path('../models/fleet_models.pkl'),
        Path('./fleet_models.pkl'),
        Path('../fleet_models.pkl'),
        Path('~/fleet_models.pkl').expanduser(),
        Path('/tmp/fleet_models.pkl'),
    ])
    
    # Try loading from each path
    checked_paths = []
    for model_path in paths_to_check:
        checked_paths.append(str(model_path))
        
        if model_path.exists():
            try:
                with open(model_path, 'rb') as f:
                    models = pickle.load(f)
                return models, str(model_path), checked_paths
            except Exception as e:
                continue
    
    return None, None, checked_paths

# Initialize session state
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

# Load ML models on first run
if not st.session_state.model_load_attempted:
    st.session_state.model_load_attempted = True
    
    models, path_used, checked_paths = load_ml_models()
    
    st.session_state.models = models
    st.session_state.model_path_used = path_used
    st.session_state.checked_paths = checked_paths

# Function to make live predictions if models are loaded
def predict_with_models(df, models):
    """Use loaded ML models to make live predictions"""
    if models is None:
        return df
    
    try:
        # Prepare features (same as training)
        feature_cols = models.get('feature_names', [])
        
        if not feature_cols or not all(col in df.columns for col in feature_cols):
            st.warning("⚠️ Model feature mismatch. Using CSV predictions.")
            return df
        
        X = df[feature_cols].copy()
        
        # Encode categorical features
        for col in ['status', 'ownership_type', 'make', 'risk_category']:
            if col in X.columns and col in models['encoders']:
                X[col] = models['encoders'][col].transform(X[col].astype(str))
        
        # Fill NaN
        X = X.fillna(X.median(numeric_only=True))
        
        # Scale
        X_scaled = models['scalers']['decision'].transform(X)
        
        # Predict
        decision_encoded = models['models']['decision_classifier'].predict(X_scaled)
        decision_proba = models['models']['decision_classifier'].predict_proba(X_scaled)
        
        # Decode
        df['decision'] = models['encoders']['decision_flag'].inverse_transform(decision_encoded)
        df['decision_confidence'] = decision_proba.max(axis=1) * 100
        
        # Cost prediction
        if 'cost_predictor' in models['models'] and models['models']['cost_predictor']:
            X_scaled_cost = models['scalers']['cost'].transform(X)
            df['predicted_cost_90days'] = models['models']['cost_predictor'].predict(X_scaled_cost)
        
        # Equity prediction
        if 'equity_predictor' in models['models'] and models['models']['equity_predictor']:
            X_scaled_equity = models['scalers']['equity'].transform(X)
            df['predicted_equity_6mo'] = models['models']['equity_predictor'].predict(X_scaled_equity)
        
        # Silently succeed - no notification
        return df
        
    except Exception as e:
        st.warning(f"⚠️ Could not use models: {str(e)}. Using CSV predictions.")
        return df

# Currency formatter
def format_naira(value):
    """Format value in Nigerian Naira"""
    if pd.isna(value):
        return "₦0"
    return f"₦{value:,.0f}"

def format_naira_millions(value):
    """Format value in millions of Naira"""
    if pd.isna(value):
        return "₦0M"
    return f"₦{value/1e6:.2f}M"

# Sidebar with premium design
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 0.5rem 0;'>
            <div style='font-size: 3.5rem; margin-bottom: 0.25rem;'>🚚</div>
            <h2 style='margin: 0; background: linear-gradient(120deg, #60efff 0%, #6366f1 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                font-size: 1.5rem; line-height: 1.2;'>Fleet Intelligence</h2>
            <p style='color: #9ca3af; font-size: 0.875rem; margin-top: 0.25rem;'>Management System</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 1rem 0; border-color: rgba(99, 102, 241, 0.2);'>", unsafe_allow_html=True)
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["🏠 Executive Dashboard", "🚚 Active Fleet", "💤 Inactive Assets", 
         "📈 Predictive Analytics", "🔍 Truck Details", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='margin: 1rem 0; border-color: rgba(99, 102, 241, 0.2);'>", unsafe_allow_html=True)
    
    # Simple data upload
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
    
    # Quick stats
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
        
        # Beautiful stat cards
        if 'status' in df.columns:
            active_count = len(df[df['status'] == 'ACTIVE'])
            inactive_count = len(df[df['status'] == 'INACTIVE'])
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.05) 100%);
                        padding: 1rem; border-radius: 12px; margin: 0.5rem 0;
                        border: 1px solid rgba(16, 185, 129, 0.3);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='color: #9ca3af; font-size: 0.75rem; text-transform: uppercase;'>Total Fleet</div>
                        <div style='color: #10b981; font-size: 1.75rem; font-weight: 700;'>{len(df)}</div>
                    </div>
                    <div style='font-size: 2rem;'>🚚</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%);
                        padding: 1rem; border-radius: 12px; margin: 0.5rem 0;
                        border: 1px solid rgba(99, 102, 241, 0.3);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='color: #9ca3af; font-size: 0.75rem; text-transform: uppercase;'>Active</div>
                        <div style='color: #60efff; font-size: 1.5rem; font-weight: 700;'>{active_count}</div>
                    </div>
                    <div style='font-size: 1.5rem;'>✅</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.05) 100%);
                        padding: 1rem; border-radius: 12px; margin: 0.5rem 0;
                        border: 1px solid rgba(239, 68, 68, 0.3);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='color: #9ca3af; font-size: 0.75rem; text-transform: uppercase;'>Inactive</div>
                        <div style='color: #ef4444; font-size: 1.5rem; font-weight: 700;'>{inactive_count}</div>
                    </div>
                    <div style='font-size: 1.5rem;'>💤</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if 'fair_market_value' in df.columns:
            total_value = df['fair_market_value'].sum()
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.05) 100%);
                        padding: 1rem; border-radius: 12px; margin: 0.5rem 0;
                        border: 1px solid rgba(245, 158, 11, 0.3);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='color: #9ca3af; font-size: 0.75rem; text-transform: uppercase;'>Total Value</div>
                        <div style='color: #f59e0b; font-size: 1.25rem; font-weight: 700;'>₦{total_value/1e6:.1f}M</div>
                    </div>
                    <div style='font-size: 1.5rem;'>💰</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Helper functions
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

# Check if data is loaded
if not st.session_state.data_loaded:
    st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem;'>
            <div style='font-size: 5rem; margin-bottom: 1rem;'>🚚</div>
            <h1 style='font-size: 3rem; margin-bottom: 1rem;'>Fleet Intelligence Management System</h1>
            <p style='font-size: 1.25rem; color: #9ca3af; max-width: 600px; margin: 0 auto 2rem;'>
                AI-powered fleet management and decision intelligence platform
            </p>
            <div class='info-card' style='max-width: 700px; margin: 2rem auto;'>
                <h3 style='color: #60efff; margin-top: 0;'>👈 Upload Your Fleet Data</h3>
                <p style='color: #c7d2fe;'>Use the file uploader in the sidebar to begin analyzing your fleet.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;'>📊</div>
                <h3 style='text-align: center; color: #e0e7ff;'>Smart Analytics</h3>
                <p style='text-align: center; color: #9ca3af; font-size: 0.875rem;'>
                    AI-powered insights and predictions for every truck in your fleet
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;'>🎯</div>
                <h3 style='text-align: center; color: #e0e7ff;'>Smart Decisions</h3>
                <p style='text-align: center; color: #9ca3af; font-size: 0.875rem;'>
                    Automated KEEP, SELL, or INSPECT recommendations with confidence scores
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;'>💰</div>
                <h3 style='text-align: center; color: #e0e7ff;'>Cost Forecasting</h3>
                <p style='text-align: center; color: #9ca3af; font-size: 0.875rem;'>
                    Predict maintenance costs and equity changes for strategic planning
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.stop()

# Load data
df = st.session_state.fleet_data.copy()

# Display model status with DETAILED debug info
models_available = st.session_state.models is not None

# Only show message if there's an ERROR - hide success messages
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
        
        **Quick check - Run this command where you're running the dashboard:**
        ```
        ls -la fleet_models.pkl
        ```
        """)
        
        st.write("**Current working directory:**")
        st.code(os.getcwd())
        
        try:
            script_location = str(Path(__file__).parent.absolute())
            st.write("**Script location:**")
            st.code(script_location)
        except:
            pass

# Use live ML models if available
if models_available:
    df = predict_with_models(df, st.session_state.models)

# Apply custom threshold decisions if enabled (overrides ML)
if st.session_state.use_custom_thresholds and st.session_state.custom_decisions is not None:
    df['decision'] = st.session_state.custom_decisions

# ==============================================================================
# EXECUTIVE DASHBOARD - COMPLETE WITH ALL CHARTS
# ==============================================================================
if page == "🏠 Executive Dashboard":
    st.title("📊 Executive Fleet Overview")
    st.markdown("<p style='color: #9ca3af; font-size: 1.125rem;'>Real-time insights and AI-powered recommendations for your entire fleet</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Top KPIs with premium cards
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
    
    # Decision distribution with modern charts
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
                    marker=dict(
                        color=colors,
                        line=dict(color='rgba(99, 102, 241, 0.3)', width=2)
                    ),
                    text=decision_counts.values,
                    textposition='outside',
                    textfont=dict(size=16, color='#e0e7ff', family='Inter', weight='bold'),
                    hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                xaxis={
                    'title': None,
                    'gridcolor': 'rgba(99, 102, 241, 0.1)',
                    'showgrid': False,
                    'tickfont': {'size': 14, 'color': '#c7d2fe'}
                },
                yaxis={
                    'title': 'Number of Trucks',
                    'gridcolor': 'rgba(99, 102, 241, 0.1)',
                    'tickfont': {'size': 12, 'color': '#9ca3af'}
                },
                height=450,
                margin=dict(l=40, r=40, t=40, b=40),
                hoverlabel=dict(
                    bgcolor='rgba(20, 27, 45, 0.95)',
                    font_size=14,
                    font_family='Inter'
                )
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
                        <span style="color: #60efff; font-size: 1.5rem; font-weight: 700;">{count}</span>
                        <span style="color: #9ca3af; font-size: 1rem;">({pct:.1f}%)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Fleet composition
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚦 Fleet Status Distribution")
        
        if 'status' in df.columns:
            status_counts = df['status'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                hole=.5,
                marker=dict(
                    colors=['#10b981', '#6b7280'],
                    line=dict(color='rgba(99, 102, 241, 0.3)', width=3)
                ),
                textfont=dict(size=16, color='#ffffff', family='Inter', weight='bold'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=14)
                ),
                margin=dict(l=20, r=20, t=40, b=60),
                hoverlabel=dict(
                    bgcolor='rgba(20, 27, 45, 0.95)',
                    font_size=14,
                    font_family='Inter'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### ⚠️ Risk Distribution Analysis")
        
        if 'risk_score' in df.columns:
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=df['risk_score'],
                nbinsx=25,
                marker=dict(
                    color='#6366f1',
                    line=dict(color='rgba(99, 102, 241, 0.5)', width=1)
                ),
                opacity=0.8,
                hovertemplate='Risk Score: %{x}<br>Count: %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                xaxis={
                    'title': 'Risk Score',
                    'gridcolor': 'rgba(99, 102, 241, 0.1)',
                    'tickfont': {'size': 12, 'color': '#9ca3af'}
                },
                yaxis={
                    'title': 'Number of Trucks',
                    'gridcolor': 'rgba(99, 102, 241, 0.1)',
                    'tickfont': {'size': 12, 'color': '#9ca3af'}
                },
                height=400,
                margin=dict(l=40, r=40, t=40, b=40),
                hoverlabel=dict(
                    bgcolor='rgba(20, 27, 45, 0.95)',
                    font_size=14,
                    font_family='Inter'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Financial metrics
    st.markdown("### 💰 Financial Performance Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'equity_ratio' in df.columns:
            positive_equity = len(df[df['equity_ratio'] > 0])
            negative_equity = len(df[df['equity_ratio'] < 0])
            
            fig = go.Figure(data=[go.Box(
                y=df['equity_ratio'],
                marker=dict(color='#60efff'),
                line=dict(color='#6366f1'),
                name='Equity Ratio',
                boxmean='sd',
                hovertemplate='Equity Ratio: %{y:.1f}%<extra></extra>'
            )])
            
            fig.add_hline(y=0, line_dash="dash", line_color="#ef4444", annotation_text="Break-even")
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                yaxis={
                    'title': 'Equity Ratio (%)',
                    'gridcolor': 'rgba(99, 102, 241, 0.1)',
                    'tickfont': {'size': 12, 'color': '#9ca3af'}
                },
                height=350,
                showlegend=False,
                margin=dict(l=40, r=40, t=40, b=40),
                hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"<p style='text-align: center; color: #9ca3af;'>{positive_equity} positive • {negative_equity} negative</p>", unsafe_allow_html=True)
    
    with col2:
        if 'predicted_cost_90days' in df.columns:
            fig = go.Figure(data=[go.Histogram(
                x=df['predicted_cost_90days'],
                nbinsx=20,
                marker=dict(color='#f59e0b', line=dict(color='rgba(245, 158, 11, 0.5)', width=1)),
                opacity=0.8
            )])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                xaxis={'title': '90-Day Cost (₦)', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
                yaxis={'title': 'Count', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
                height=350,
                margin=dict(l=40, r=40, t=40, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            avg_cost = df['predicted_cost_90days'].mean()
            st.markdown(f"<p style='text-align: center; color: #9ca3af;'>Avg: ₦{avg_cost:,.0f}</p>", unsafe_allow_html=True)
    
    with col3:
        if 'predicted_equity_6mo' in df.columns:
            fig = go.Figure(data=[go.Histogram(
                x=df['predicted_equity_6mo'],
                nbinsx=20,
                marker=dict(color='#ef4444', line=dict(color='rgba(239, 68, 68, 0.5)', width=1)),
                opacity=0.8
            )])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                xaxis={'title': '6-Month Equity (₦)', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
                yaxis={'title': 'Count', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
                height=350,
                margin=dict(l=40, r=40, t=40, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# ACTIVE FLEET - COMPLETE
# ==============================================================================
elif page == "🚚 Active Fleet":
    st.title("🚚 Active Fleet Management")
    st.markdown("<p style='color: #9ca3af; font-size: 1.125rem;'>Monitor and optimize your operational trucks</p>", unsafe_allow_html=True)
    
    active_df = df[df['status'] == 'ACTIVE'].copy()
    
    if len(active_df) == 0:
        st.warning("⚠️ No active trucks found in the fleet.")
        st.stop()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPIs
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
    
    # Filters
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
    
    # Apply filters
    filtered_df = active_df.copy()
    if selected_decision != 'All' and 'decision' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['decision'] == selected_decision]
    if selected_make != 'All' and 'make' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['make'] == selected_make]
    if 'risk_score' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['risk_score'] >= risk_range[0]) & (filtered_df['risk_score'] <= risk_range[1])]
    
    st.info(f"📊 Showing {len(filtered_df)} of {len(active_df)} active trucks")
    
    # Table
    display_cols = ['Truck_ID', 'make', 'model', 'decision', 'risk_score', 'equity_ratio', 'utilization_rate']
    display_cols = [col for col in display_cols if col in filtered_df.columns]
    
    st.dataframe(filtered_df[display_cols], use_container_width=True, height=400)

# I'll continue with the complete remaining sections in the next file part due to character limit...

# ==============================================================================
# INACTIVE ASSETS PAGE - COMPLETE WITH ALL CHARTS
# ==============================================================================
elif page == "💤 Inactive Assets":
    st.title("💤 Inactive Asset Disposition")
    st.markdown("<p style='color: #9ca3af; font-size: 1.125rem;'>Manage and optimize your inactive fleet inventory</p>", unsafe_allow_html=True)
    
    inactive_df = df[df['status'] == 'INACTIVE'].copy()
    
    if len(inactive_df) == 0:
        st.warning("⚠️ No inactive trucks found in the fleet.")
        st.stop()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Inactive KPIs
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
    
    # Liquidation priority
    st.markdown("### 🎯 Liquidation Priority List")
    st.markdown("<p style='color: #9ca3af;'>Trucks sorted by equity ratio (worst first) - prioritize selling these assets</p>", unsafe_allow_html=True)
    
    priority_cols = ['Truck_ID', 'make', 'model', 'truck_age', 'months_owned',
                    'equity_ratio', 'current_equity', 'fair_market_value',
                    'decision']
    
    priority_cols = [col for col in priority_cols if col in inactive_df.columns]
    
    priority_df = inactive_df[priority_cols].sort_values('equity_ratio')
    
    # Format currency columns
    display_df = priority_df.copy()
    if 'current_equity' in display_df.columns:
        display_df['current_equity'] = display_df['current_equity'].apply(format_naira)
    if 'fair_market_value' in display_df.columns:
        display_df['fair_market_value'] = display_df['fair_market_value'].apply(format_naira)
    
    st.dataframe(display_df, use_container_width=True, height=500)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💸 Equity Distribution")
        
        if 'equity_ratio' in inactive_df.columns:
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=inactive_df['equity_ratio'],
                nbinsx=30,
                marker=dict(
                    color='#ef4444',
                    line=dict(color='rgba(239, 68, 68, 0.5)', width=1)
                ),
                opacity=0.8,
                hovertemplate='Equity Ratio: %{x:.1f}%<br>Count: %{y}<extra></extra>'
            ))
            
            fig.add_vline(x=0, line_dash="dash", line_color="#60efff",
                         annotation_text="Break-even", annotation_position="top")
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                xaxis={
                    'title': 'Equity Ratio (%)',
                    'gridcolor': 'rgba(99, 102, 241, 0.1)',
                    'tickfont': {'size': 12, 'color': '#9ca3af'}
                },
                yaxis={
                    'title': 'Number of Trucks',
                    'gridcolor': 'rgba(99, 102, 241, 0.1)',
                    'tickfont': {'size': 12, 'color': '#9ca3af'}
                },
                height=400,
                margin=dict(l=40, r=40, t=40, b=40),
                hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### ⏱️ Time Inactive")
        
        if 'months_owned' in inactive_df.columns:
            fig = go.Figure(data=[go.Box(
                y=inactive_df['months_owned'],
                marker=dict(color='#f59e0b'),
                line=dict(color='#d97706'),
                name='Months Owned',
                boxmean='sd',
                hovertemplate='Months Owned: %{y:.1f}<extra></extra>'
            )])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff', 'family': 'Inter'},
                yaxis={
                    'title': 'Months Owned',
                    'gridcolor': 'rgba(99, 102, 241, 0.1)',
                    'tickfont': {'size': 12, 'color': '#9ca3af'}
                },
                height=400,
                showlegend=False,
                margin=dict(l=40, r=40, t=40, b=40),
                hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Financial impact
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 💰 Financial Impact Analysis")
    
    if 'monthly_holding_cost' in inactive_df.columns and 'months_owned' in inactive_df.columns:
        inactive_df['total_holding_cost'] = (
            inactive_df['monthly_holding_cost'] * inactive_df['months_owned']
        )
        
        total_holding = inactive_df['total_holding_cost'].sum()
        
        st.error(f"💸 **Total capital tied up in inactive fleet: ₦{total_holding:,.0f}**")
        
        # Top cost generators
        top_cost = inactive_df.nlargest(10, 'total_holding_cost')
        
        fig = go.Figure(data=[go.Bar(
            x=top_cost['Truck_ID'].astype(str),
            y=top_cost['total_holding_cost'],
            marker=dict(
                color='#ef4444',
                line=dict(color='rgba(239, 68, 68, 0.5)', width=2)
            ),
            text=[f"₦{x:,.0f}" for x in top_cost['total_holding_cost']],
            textposition='outside',
            textfont=dict(size=12, color='#e0e7ff'),
            hovertemplate='<b>%{x}</b><br>Cost: ₦%{y:,.0f}<extra></extra>'
        )])
        
        fig.update_layout(
            title="Top 10 Cost Generators",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e7ff', 'family': 'Inter'},
            xaxis={'title': 'Truck ID', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
            yaxis={'title': 'Total Holding Cost (₦)', 'gridcolor': 'rgba(99, 102, 241, 0.1)'},
            height=450,
            margin=dict(l=40, r=40, t=60, b=40),
            hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# PREDICTIVE ANALYTICS PAGE - COMPLETE WITH ALL FORECASTS
# ==============================================================================
elif page == "📈 Predictive Analytics":
    st.title("📈 Predictive Analytics & Forecasting")
    st.markdown("<p style='color: #9ca3af; font-size: 1.125rem;'>AI-powered cost and equity predictions for strategic planning</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Cost predictions
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
    
    # Cost distribution chart
    if 'predicted_cost_90days' in df.columns:
        fig = px.histogram(
            df,
            x='predicted_cost_90days',
            color='status' if 'status' in df.columns else None,
            marginal='box',
            title="Cost Prediction Distribution by Fleet Status",
            color_discrete_map={'ACTIVE': '#10b981', 'INACTIVE': '#6b7280'},
            labels={'predicted_cost_90days': '90-Day Predicted Cost (₦)'}
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e7ff', 'family': 'Inter'},
            xaxis={'gridcolor': 'rgba(99, 102, 241, 0.1)'},
            yaxis={'gridcolor': 'rgba(99, 102, 241, 0.1)'},
            height=450,
            margin=dict(l=40, r=40, t=60, b=40),
            hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Equity projections
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
        
        # Scatter plot
        fig = px.scatter(
            df,
            x='current_equity',
            y='predicted_equity_6mo',
            color='decision' if 'decision' in df.columns else None,
            size='risk_score' if 'risk_score' in df.columns else None,
            hover_data=['Truck_ID', 'make', 'model'] if all(col in df.columns for col in ['Truck_ID', 'make', 'model']) else None,
            title="Current vs Predicted Equity (6 Months)",
            color_discrete_map={'KEEP': '#10b981', 'SELL': '#ef4444', 'INSPECT': '#f59e0b'},
            labels={'current_equity': 'Current Equity (₦)', 'predicted_equity_6mo': 'Predicted Equity (₦)'}
        )
        
        # Add diagonal reference line
        max_val = max(df['current_equity'].max(), df['predicted_equity_6mo'].max())
        min_val = min(df['current_equity'].min(), df['predicted_equity_6mo'].min())
        
        fig.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            line=dict(dash='dash', color='#60efff', width=2),
            name='No Change Line',
            hovertemplate='No Change<extra></extra>'
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e7ff', 'family': 'Inter'},
            xaxis={'gridcolor': 'rgba(99, 102, 241, 0.1)'},
            yaxis={'gridcolor': 'rgba(99, 102, 241, 0.1)'},
            height=550,
            margin=dict(l=40, r=40, t=60, b=40),
            hoverlabel=dict(bgcolor='rgba(20, 27, 45, 0.95)', font_size=14)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Top movers
    st.markdown("### 📈 Top Equity Movers (6-Month Forecast)")
    
    if 'predicted_equity_6mo' in df.columns and 'current_equity' in df.columns:
        df['equity_change'] = df['predicted_equity_6mo'] - df['current_equity']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🟢 Top Gainers")
            gainers = df.nlargest(10, 'equity_change')
            
            display_cols = ['Truck_ID', 'make', 'model', 'current_equity', 
                           'predicted_equity_6mo', 'equity_change']
            display_cols = [col for col in display_cols if col in gainers.columns]
            
            # Format display
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

# ==============================================================================
# TRUCK DETAILS - COMPLETE WITH GAUGES
# ==============================================================================
elif page == "🔍 Truck Details":
    st.title("🔍 Individual Truck Deep Dive")
    
    truck_id = st.selectbox("Select Truck", df['Truck_ID'].sort_values().unique())
    truck = df[df['Truck_ID'] == truck_id].iloc[0]
    
    # Header
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
    
    # Gauges
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


# ==============================================================================
# SETTINGS - COMPLETE WITH ALL THRESHOLD PRESETS AND MANUAL CONTROLS
# ==============================================================================
elif page == "⚙️ Settings":
    # FORCE ALL TEXT WHITE IN SETTINGS
    st.markdown("""
    <style>
    /* NUCLEAR OPTION - Force everything white in Settings */
    div[data-testid="stVerticalBlock"] label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    div[data-testid="stVerticalBlock"] p {
        color: #ffffff !important;
    }
    div[data-testid="stVerticalBlock"] li {
        color: #ffffff !important;
    }
    div[data-testid="stVerticalBlock"] div {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("⚙️ System Settings & Threshold Management")
    st.markdown("<p style='color: #9ca3af; font-size: 1.125rem;'>Customize decision criteria for your fleet's specific situation</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 🎯 Decision Threshold Configuration")
    
    st.info("💡 **Important:** Your fleet has challenging equity positions (avg -59%). Use quick presets below or adjust manually.")
    
    # Quick preset buttons at the top
    st.markdown("#### ⚡ Quick Presets (One-Click Apply)")
    st.markdown("<p style='color: #60efff; font-size: 0.9rem; margin-top: -0.5rem;'>Choose a preset strategy to instantly recalculate all decisions</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Conservative\n(More KEEP)", use_container_width=True, type="primary"):
            with st.spinner("Applying Conservative preset..."):
                df_updated = st.session_state.fleet_data.copy()
                df_updated['new_decision'] = 'INSPECT'
                
                # Conservative: Keep top 40%, Sell bottom 15%
                
                # Percentiles
                equity_15th = df_updated['equity_ratio'].quantile(0.15)
                equity_60th = df_updated['equity_ratio'].quantile(0.60)
                risk_80th = df_updated['risk_score'].quantile(0.80)
                
                # SELL: Only the absolute worst 15%
                sell_mask = (
                    (df_updated['equity_ratio'] < equity_15th) |
                    ((df_updated['equity_ratio'] < -75) & (df_updated['risk_score'] > risk_80th))
                )
                
                df_updated.loc[sell_mask, 'new_decision'] = 'SELL'
                
                # KEEP: Top 40% - most generous
                df_updated['combined_score'] = (
                    df_updated['equity_ratio'] * 0.6 + 
                    (100 - df_updated['risk_score']) * 0.4
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
                
                # PERCENTILE-BASED APPROACH
                # Calculate percentiles
                equity_25th = df_updated['equity_ratio'].quantile(0.25)
                equity_50th = df_updated['equity_ratio'].quantile(0.50)
                equity_75th = df_updated['equity_ratio'].quantile(0.75)
                
                risk_25th = df_updated['risk_score'].quantile(0.25)
                risk_75th = df_updated['risk_score'].quantile(0.75)
                
                # SELL: Bottom 30% by equity OR combination of bad factors
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
                
                # KEEP: Top 35% by combined score OR clearly good trucks
                df_updated['combined_score'] = (
                    df_updated['equity_ratio'] * 0.6 + 
                    (100 - df_updated['risk_score']) * 0.4
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
                
                # Aggressive: Keep top 20%, Sell bottom 40%
                equity_40th = df_updated['equity_ratio'].quantile(0.40)
                equity_80th = df_updated['equity_ratio'].quantile(0.80)
                risk_60th = df_updated['risk_score'].quantile(0.60)
                
                # SELL: Bottom 40% - aggressive liquidation
                sell_mask = (
                    (df_updated['equity_ratio'] < equity_40th) |
                    ((df_updated['equity_ratio'] < equity_80th) & (df_updated['risk_score'] > risk_60th)) |
                    ((df_updated['status'] == 'INACTIVE') & 
                     (df_updated['months_owned'] > 8) & 
                     (df_updated['equity_ratio'] < -40)) |
                    ((df_updated['truck_age'] > 10) & (df_updated['equity_ratio'] < -30))
                )
                
                df_updated.loc[sell_mask, 'new_decision'] = 'SELL'
                
                # KEEP: Only top 20% - very selective
                df_updated['combined_score'] = (
                    df_updated['equity_ratio'] * 0.6 + 
                    (100 - df_updated['risk_score']) * 0.4
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
        
        st.markdown("<style>.main .stSlider > label {color: #ffffff !important; font-weight: 700 !important;}</style>", unsafe_allow_html=True)
        
        keep_equity = st.slider(
            "Minimum Equity Ratio (%)",
            -100.0, 50.0, -40.0,
            help="Trucks above this equity may be kept. Current avg: -59%"
        )
        
        keep_risk = st.slider(
            "Maximum Risk Score",
            0, 100, 60,
            help="Trucks below this risk score may be kept"
        )
        
        keep_util = st.slider(
            "Minimum Utilization Rate (%) - Active Only",
            0, 100, 30,
            help="Active trucks above this utilization may be kept"
        )
        
        keep_age = st.slider(
            "Maximum Age (years)",
            0, 20, 15,
            help="Trucks younger than this may be kept if other criteria met"
        )
    
    with col2:
        st.markdown("#### 🔴 SELL Criteria (Liquidate)")
        st.markdown("<p style='color: #ef4444; font-size: 0.875rem;'>Trucks that should be sold immediately</p>", unsafe_allow_html=True)
        
        st.markdown("<style>.main .stSlider > label {color: #ffffff !important; font-weight: 700 !important;}</style>", unsafe_allow_html=True)
        
        sell_equity = st.slider(
            "Maximum Equity Ratio (%)",
            -150.0, 0.0, -70.0,
            help="Trucks below this equity should be sold. Deepest hole: -126%"
        )
        
        sell_risk = st.slider(
            "Minimum Risk Score",
            0, 100, 80,
            help="High-risk trucks above this should be sold"
        )
        
        sell_age = st.slider(
            "Minimum Age (years) with negative equity",
            0, 20, 8,
            help="Old trucks with negative equity should be sold"
        )
        
        sell_inactive_months = st.slider(
            "Inactive Duration (months)",
            0, 36, 9,
            help="Inactive trucks longer than this should be sold"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Show current status
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
                # Create new decision column
                df_updated = df.copy()
                df_updated['new_decision'] = 'INSPECT'
                
                # SELL criteria (most aggressive - do first)
                sell_mask = (
                    (df_updated['equity_ratio'] < sell_equity) |
                    (df_updated['risk_score'] > sell_risk) |
                    ((df_updated['truck_age'] > sell_age) & (df_updated['equity_ratio'] < -20)) |
                    ((df_updated['status'] == 'INACTIVE') & 
                     (df_updated['months_owned'] > sell_inactive_months) & 
                     (df_updated['equity_ratio'] < -30))
                )
                
                df_updated.loc[sell_mask, 'new_decision'] = 'SELL'
                
                # KEEP criteria
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
                
                # Store in session state
                st.session_state.custom_decisions = df_updated['new_decision'].copy()
                st.session_state.use_custom_thresholds = True
                
                st.success("✅ Decisions recalculated successfully!")
                st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Current fleet situation analysis
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
                    padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>POSITIVE EQUITY</div>
            <div style='color: #10b981; font-size: 1.75rem; font-weight: 700;'>{positive_equity}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(positive_equity/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
                    padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid rgba(239, 68, 68, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>NEGATIVE EQUITY</div>
            <div style='color: #ef4444; font-size: 1.75rem; font-weight: 700;'>{negative_equity}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(negative_equity/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)
        
        equity_color = '#10b981' if avg_equity >= 0 else '#ef4444'
        equity_status = 'Positive' if avg_equity >= 0 else 'Deeply underwater' if avg_equity < -30 else 'Challenging'
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
                    padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid rgba(99, 102, 241, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>AVERAGE EQUITY RATIO</div>
            <div style='color: {equity_color}; font-size: 1.75rem; font-weight: 700;'>{avg_equity:.1f}%</div>
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
                    padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>LOW RISK (&lt;40)</div>
            <div style='color: #10b981; font-size: 1.75rem; font-weight: 700;'>{low_risk}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(low_risk/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.05) 100%);
                    padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid rgba(245, 158, 11, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>MEDIUM RISK (40-70)</div>
            <div style='color: #f59e0b; font-size: 1.75rem; font-weight: 700;'>{medium_risk}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(medium_risk/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
                    padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid rgba(239, 68, 68, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>HIGH RISK (&gt;70)</div>
            <div style='color: #ef4444; font-size: 1.75rem; font-weight: 700;'>{high_risk}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(high_risk/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("#### <span style='color: #60efff;'>Fleet Status</span>", unsafe_allow_html=True)
        active = len(df[df['status'] == 'ACTIVE'])
        inactive = len(df[df['status'] == 'INACTIVE'])
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
                    padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>ACTIVE TRUCKS</div>
            <div style='color: #10b981; font-size: 1.75rem; font-weight: 700;'>{active}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(active/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
                    padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid rgba(239, 68, 68, 0.3);'>
            <div style='color: #9ca3af; font-size: 0.75rem;'>INACTIVE TRUCKS</div>
            <div style='color: #ef4444; font-size: 1.75rem; font-weight: 700;'>{inactive}</div>
            <div style='color: #c7d2fe; font-size: 0.875rem;'>{(inactive/len(df)*100):.1f}% of fleet</div>
        </div>
        """, unsafe_allow_html=True)
        
        if 'utilization_rate' in df.columns:
            avg_util = df[df['status'] == 'ACTIVE']['utilization_rate'].mean()
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid rgba(99, 102, 241, 0.3);'>
                <div style='color: #9ca3af; font-size: 0.75rem;'>AVG UTILIZATION (ACTIVE)</div>
                <div style='color: #60efff; font-size: 1.75rem; font-weight: 700;'>{avg_util:.1f}%</div>
                <div style='color: #c7d2fe; font-size: 0.875rem;'>Active Fleet Performance</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Recommendations
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
        
        💡 **This should give you ~40-100 KEEP, ~50-150 SELL, rest INSPECT**
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
    
    st.markdown("### 💡 Preset Details")
    st.markdown("<p style='color: #60efff; font-size: 1rem; margin-top: -1rem;'>Understand each preset strategy</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.05) 100%);
                    padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <h4 style='color: #10b981; margin-top: 0;'>🟢 Conservative</h4>
            <ul style='color: #ffffff; font-size: 0.9rem; line-height: 1.8;'>
                <li>KEEP: Top 40% of fleet</li>
                <li>SELL: Bottom 15% (worst only)</li>
                <li>Uses combined equity + risk score</li>
                <li>Best for: Maintaining fleet size</li>
                <li>Expected: ~380 KEEP, ~145 SELL, ~430 INSPECT</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.05) 100%);
                    padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.3);'>
            <h4 style='color: #f59e0b; margin-top: 0;'>🟡 Balanced ⭐</h4>
            <ul style='color: #ffffff; font-size: 0.9rem; line-height: 1.8;'>
                <li>KEEP: Top 35% of fleet</li>
                <li>SELL: Bottom 30% (clear losers)</li>
                <li>Percentile-based approach</li>
                <li>Best for: Most situations</li>
                <li>Expected: ~335 KEEP, ~285 SELL, ~335 INSPECT</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.05) 100%);
                    padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.3);'>
            <h4 style='color: #ef4444; margin-top: 0;'>🔴 Aggressive</h4>
            <ul style='color: #ffffff; font-size: 0.9rem; line-height: 1.8;'>
                <li>KEEP: Top 20% (best only)</li>
                <li>SELL: Bottom 40% (cut losses)</li>
                <li>Strict performance criteria</li>
                <li>Best for: Fleet optimization</li>
                <li>Expected: ~190 KEEP, ~380 SELL, ~385 INSPECT</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("### 📥 Export Options")
    st.markdown("<p style='color: #60efff; font-size: 1rem; margin-top: -1rem;'>Download your fleet data and reports</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
                    padding: 0.75rem; border-radius: 10px; border: 1px solid rgba(99, 102, 241, 0.3);
                    text-align: center; margin-bottom: 0.5rem;'>
            <div style='font-size: 1.5rem;'>📊</div>
            <div style='color: #60efff; font-weight: 600; font-size: 0.9rem; margin-top: 0.25rem;'>Full Dataset</div>
        </div>
        """, unsafe_allow_html=True)
        csv = df.to_csv(index=False)
        st.download_button("📊 Download", csv, "fleet_data.csv", "text/csv", use_container_width=True)
    
    with col2:
        if 'decision' in df.columns:
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
                        padding: 0.75rem; border-radius: 10px; border: 1px solid rgba(239, 68, 68, 0.3);
                        text-align: center; margin-bottom: 0.5rem;'>
                <div style='font-size: 1.5rem;'>🔴</div>
                <div style='color: #ef4444; font-weight: 600; font-size: 0.9rem; margin-top: 0.25rem;'>SELL List</div>
            </div>
            """, unsafe_allow_html=True)
            sell_csv = df[df['decision'] == 'SELL'].to_csv(index=False)
            st.download_button("🔴 Download", sell_csv, "sell_list.csv", "text/csv", use_container_width=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.05) 100%);
                    padding: 0.75rem; border-radius: 10px; border: 1px solid rgba(245, 158, 11, 0.3);
                    text-align: center; margin-bottom: 0.5rem;'>
            <div style='font-size: 1.5rem;'>📋</div>
            <div style='color: #f59e0b; font-weight: 600; font-size: 0.9rem; margin-top: 0.25rem;'>Summary</div>
        </div>
        """, unsafe_allow_html=True)
        summary = f"Fleet Report - {datetime.now().strftime('%Y-%m-%d')}\nTotal: {len(df)} trucks"
        st.download_button("📋 Download", summary, "summary.txt", "text/plain", use_container_width=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #6b7280;'>
    <p style='font-size: 0.875rem; margin: 0;'>Fleet Intelligence Pro v1.0 | Powered by AI</p>
    <p style='font-size: 0.75rem; margin-top: 0.5rem;'>© 2025 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)