import streamlit as st
import pickle
import pandas as pd
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import io

# Page configuration
st.set_page_config(
    page_title="Spotify Premium Prediction Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling with Spotify colors
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Circular+Std:wght@400;700&display=swap');
    
    .main {
        background-color: #0a1929;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0a1929 0%, #132f4c 100%);
        font-family: 'Circular Std', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3 {
        color: #1DB954 !important;
        font-weight: 700;
    }
    
    .spotify-header {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(29, 185, 84, 0.3);
    }
    
    .spotify-header h1 {
        color: #000000 !important;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .section-container {
        background-color: #1a2332;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #2a3a4a;
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 16px rgba(29, 185, 84, 0.4);
    }
    
    .prediction-card.churn {
        background: linear-gradient(135deg, #e22134 0%, #ff3b4f 100%);
        box-shadow: 0 8px 16px rgba(226, 33, 52, 0.4);
    }
    
    .prediction-text {
        font-size: 2rem;
        font-weight: 700;
        color: #000000;
        margin: 1rem 0;
    }
    
    .confidence-text {
        font-size: 1.5rem;
        color: #000000;
        margin-top: 1rem;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #b3b3b3;
        margin-top: 3rem;
        border-top: 1px solid #2a3a4a;
    }
    
    .info-card {
        background-color: #1a2332;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1DB954;
        margin: 1rem 0;
    }
    
    .stButton>button {
        background-color: #1DB954;
        color: #000000;
        font-weight: 700;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        border: none;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #1ed760;
        transform: scale(1.05);
    }
    
    .metric-card {
        background-color: #181818;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #282828;
    }
    
    /* Enhanced Input Styling */
    /* Selectbox/Dropdown Styling */
    div[data-baseweb="select"] > div {
        background-color: #1a2332 !important;
        border: 2px solid #2a3a4a !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #1DB954 !important;
        box-shadow: 0 0 0 3px rgba(29, 185, 84, 0.2) !important;
    }
    
    div[data-baseweb="select"] > div:focus-within {
        border-color: #1DB954 !important;
        box-shadow: 0 0 0 3px rgba(29, 185, 84, 0.3) !important;
    }
    
    /* Selectbox dropdown menu */
    ul[role="listbox"] {
        background-color: #1a2332 !important;
        border: 1px solid #1DB954 !important;
        border-radius: 8px !important;
    }
    
    li[role="option"] {
        background-color: #1a2332 !important;
        color: #ffffff !important;
    }
    
    li[role="option"]:hover {
        background-color: #1DB954 !important;
        color: #000000 !important;
    }
    
    /* Slider Styling */
    .stSlider > div > div > div {
        background-color: #2a3a4a !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #1DB954 !important;
    }
    
    .stSlider > div > div > div > div > div {
        background-color: #1DB954 !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 2px 8px rgba(29, 185, 84, 0.5) !important;
    }
    
    .stSlider label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stSlider > div > div > div > div > div:hover {
        transform: scale(1.2) !important;
        box-shadow: 0 4px 12px rgba(29, 185, 84, 0.8) !important;
    }
    
    /* Hide slider value display */
    .stSlider > div > div > div > div > span {
        display: none !important;
    }
    
    /* Hide selection pointers and unwanted UI elements */
    .stSlider > div > div > div::before,
    .stSlider > div > div > div::after {
        display: none !important;
    }
    
    /* Hide radio button selection indicators that are visible */
    .stRadio input[type="radio"] {
        opacity: 0 !important;
        position: absolute !important;
    }
    
    /* Hide multiselect selection indicators */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #1DB954 !important;
        color: #000000 !important;
    }
    
    /* Hide any visible selection pointers or integers */
    .stSlider [data-testid="stMarkdownContainer"] {
        display: none !important;
    }
    
    /* Hide slider value text that might be visible */
    .stSlider span {
        display: none !important;
    }
    
    /* Ensure radio buttons don't show selection pointers */
    .stRadio label::before {
        display: none !important;
    }
    
    /* Hide any numeric indicators */
    .stSlider > div > div > div > span[style*="position"] {
        display: none !important;
    }
    
    /* Better radio button styling without visible pointers */
    .stRadio > div {
        display: flex !important;
        gap: 1rem !important;
    }
    
    .stRadio > div > label {
        position: relative !important;
    }
    
    .stRadio > div > label::after {
        content: "" !important;
        position: absolute !important;
        left: 0.5rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 12px !important;
        height: 12px !important;
        border-radius: 50% !important;
        background-color: transparent !important;
        border: 2px solid #1DB954 !important;
    }
    
    .stRadio input[type="radio"]:checked + label::after {
        background-color: #1DB954 !important;
    }
    
    /* Radio Button Styling */
    .stRadio > div {
        gap: 1rem !important;
    }
    
    .stRadio > div > label {
        background-color: #1a2332 !important;
        border: 2px solid #2a3a4a !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        color: #b3b3b3 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        font-weight: 500 !important;
    }
    
    .stRadio > div > label:hover {
        border-color: #1DB954 !important;
        background-color: #0f1620 !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(29, 185, 84, 0.3) !important;
    }
    
    .stRadio > div > label[data-testid="stRadio"] {
        background-color: #1a2332 !important;
    }
    
    /* Selected Radio Button */
    .stRadio input[type="radio"]:checked + label,
    .stRadio > div > label[data-baseweb="radio"]:has(input:checked) {
        background-color: #1DB954 !important;
        border-color: #1DB954 !important;
        color: #000000 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(29, 185, 84, 0.5) !important;
    }
    
    /* Radio button circle */
    .stRadio input[type="radio"] {
        accent-color: #1DB954 !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    /* Multiselect Styling */
    .stMultiSelect > div > div {
        background-color: #1a2332 !important;
        border: 2px solid #2a3a4a !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    .stMultiSelect > div > div:hover {
        border-color: #1DB954 !important;
        box-shadow: 0 0 0 3px rgba(29, 185, 84, 0.2) !important;
    }
    
    .stMultiSelect > div > div:focus-within {
        border-color: #1DB954 !important;
        box-shadow: 0 0 0 3px rgba(29, 185, 84, 0.3) !important;
    }
    
    /* Input Labels */
    label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Help text styling */
    .stTooltipIcon {
        color: #1DB954 !important;
    }
    
    /* Section titles enhancement */
    .section-container h4 {
        color: #1DB954 !important;
        font-size: 1.3rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        display: inline-block !important;
        font-weight: 700 !important;
    }
    
    /* Section divider styling */
    .section-container hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #1DB954, transparent) !important;
        margin: 1rem 0 1.5rem 0 !important;
    }
    
    /* Input field value display enhancement */
    .stSlider > div > div > div > div {
        box-shadow: 0 2px 8px rgba(29, 185, 84, 0.4) !important;
    }
    
    /* Better spacing between inputs */
    .section-container > div {
        margin-bottom: 1.25rem !important;
    }
    
    /* Enhanced section container hover effect */
    .section-container {
        transition: all 0.3s ease !important;
    }
    
    .section-container:hover {
        border-color: #1DB954 !important;
        box-shadow: 0 4px 12px rgba(29, 185, 84, 0.2) !important;
    }
    
    /* Input container spacing */
    .element-container {
        margin-bottom: 1.5rem !important;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        background-color: #1a2332 !important;
        border: 2px solid #2a3a4a !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #1DB954 !important;
        box-shadow: 0 0 0 3px rgba(29, 185, 84, 0.3) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background-color: #1a2332 !important;
        border: 2px dashed #2a3a4a !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #1DB954 !important;
        background-color: #1a1a1a !important;
    }
    
    /* Progress bar enhancement */
    .stProgress > div > div > div {
        background-color: #1DB954 !important;
    }
    
    /* Add glow effect to focused inputs */
    *:focus {
        outline: none !important;
    }
    
    /* Smooth transitions for all inputs */
    select, input, button, label {
        transition: all 0.3s ease !important;
    }
    
    /* Animation Container */
    .animation-container {
        text-align: center;
        padding: 3rem 2rem;
        margin: 2rem 0;
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.15) 0%, rgba(30, 215, 96, 0.15) 100%);
        border-radius: 15px;
        border: 2px solid rgba(29, 185, 84, 0.4);
        animation: fadeInUp 1s ease-out;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(29, 185, 84, 0.2);
    }
    
    .animation-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(29, 185, 84, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    .animation-container::after {
        content: '';
        position: absolute;
        top: -30%;
        right: -30%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(30, 215, 96, 0.1) 0%, transparent 70%);
        animation: rotate 15s linear infinite reverse;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            filter: drop-shadow(0 0 10px rgba(29, 185, 84, 0.5));
        }
        50% {
            transform: scale(1.1);
            filter: drop-shadow(0 0 20px rgba(29, 185, 84, 0.8));
        }
    }
    
    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    .animated-icon {
        font-size: 4rem;
        display: inline-block;
        animation: pulse 2s ease-in-out infinite;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .animated-text {
        font-size: 1.5rem;
        color: #1DB954;
        font-weight: 700;
        animation: fadeInUp 1.2s ease-out;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(29, 185, 84, 0.3);
    }
    
    .animated-subtext {
        font-size: 1rem;
        color: #b3b3b3;
        margin-top: 0.5rem;
        animation: fadeInUp 1.4s ease-out;
        position: relative;
        z-index: 1;
    }
    
    /* User Input Form Styling */
    .form-header {
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.15) 0%, rgba(30, 215, 96, 0.15) 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 4px solid #1DB954;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .form-header h3 {
        color: #1DB954 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .form-header p {
        color: #b3b3b3 !important;
        margin: 0 !important;
    }
    
    /* Landing Page Styles */
    .landing-hero {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.2) 0%, rgba(30, 215, 96, 0.1) 100%);
        border-radius: 20px;
        margin: 2rem 0;
        border: 2px solid rgba(29, 185, 84, 0.3);
    }
    
    .landing-hero h1 {
        font-size: 3rem;
        color: #1DB954;
        margin-bottom: 1rem;
        animation: fadeInUp 1s ease-out;
    }
    
    .landing-hero p {
        font-size: 1.3rem;
        color: #b3b3b3;
        margin-bottom: 2rem;
        animation: fadeInUp 1.2s ease-out;
    }
    
    .workflow-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .workflow-step {
        background: linear-gradient(135deg, #1a2332 0%, #1e2a3a 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #1DB954;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .workflow-step:hover {
        transform: translateX(10px);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.3);
    }
    
    .workflow-step h3 {
        color: #1DB954;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .workflow-step-number {
        background: #1DB954;
        color: #000000;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .workflow-step p {
        color: #b3b3b3;
        line-height: 1.8;
        font-size: 1.1rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: #1a2332;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #2a3a4a;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: #1DB954;
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(29, 185, 84, 0.2);
    }
    
    .feature-card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-card h4 {
        color: #1DB954;
        margin-bottom: 0.5rem;
    }
    
    .feature-card p {
        color: #b3b3b3;
        font-size: 0.9rem;
    }
    
    .get-started-btn {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        color: #000000;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-size: 1.3rem;
        font-weight: 700;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4);
        animation: pulse 2s ease-in-out infinite;
    }
    
    .get-started-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.6);
    }
    
    .how-it-works {
        background: #1a2332;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid #2a3a4a;
    }
    
    .how-it-works h2 {
        color: #1DB954;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .workflow-diagram {
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.5rem;
        margin: 2rem 0;
        padding: 1rem;
    }
    
    .diagram-step {
        text-align: center;
        flex: 1;
        min-width: 180px;
        max-width: 250px;
        padding: 1rem;
    }
    
    .diagram-icon {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        margin: 0 auto 1rem;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4);
        animation: pulse 2s ease-in-out infinite;
    }
    
    .diagram-arrow {
        font-size: 2rem;
        color: #1DB954;
        margin: 0 0.5rem;
        flex-shrink: 0;
    }
    
    .diagram-step h4 {
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .diagram-step p {
        color: #b3b3b3;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Responsive workflow diagram */
    @media (max-width: 768px) {
        .workflow-diagram {
            flex-direction: column;
            gap: 1rem;
        }
        
        .diagram-arrow {
            transform: rotate(90deg);
            margin: 0.5rem 0;
        }
        
        .diagram-step {
            min-width: 100%;
            max-width: 100%;
        }
        
        .diagram-icon {
            width: 60px;
            height: 60px;
            font-size: 1.5rem;
        }
        
        .workflow-step {
            padding: 1.5rem;
        }
        
        .feature-grid {
            grid-template-columns: 1fr !important;
        }
        
        .landing-hero h1 {
            font-size: 2rem !important;
        }
        
        .landing-hero p {
            font-size: 1rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .diagram-step {
            min-width: 100%;
            padding: 0.5rem;
        }
        
        .workflow-step h3 {
            font-size: 1.2rem !important;
        }
        
        .workflow-step-number {
            width: 35px !important;
            height: 35px !important;
            font-size: 1rem !important;
        }
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .spotify-header h1 {
            font-size: 1.8rem;
        }
        .prediction-text {
            font-size: 1.5rem;
        }
        .stRadio > div > label {
            padding: 0.5rem 1rem !important;
            font-size: 0.9rem !important;
        }
        .animated-icon {
            font-size: 3rem;
        }
        .animated-text {
            font-size: 1.2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Load model and feature columns
@st.cache_resource
def load_model():
    """Load the trained SVM model"""
    try:
        with open('svm_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

@st.cache_resource
def load_features():
    """Load the feature columns list"""
    try:
        with open('feature_columns.pkl', 'rb') as f:
            features = pickle.load(f)
        return features
    except Exception as e:
        st.error(f"Error loading features: {str(e)}")
        return None

# Initialize session state
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None
if 'confidence' not in st.session_state:
    st.session_state.confidence = None
if 'show_app' not in st.session_state:
    st.session_state.show_app = False

# Load model and features
model = load_model()
feature_columns = load_features()

if model is None or feature_columns is None:
    st.error("Failed to load model or features. Please ensure svm_model.pkl and feature_columns.pkl are in the directory.")
    st.stop()

# Header with Spotify branding
st.markdown("""
    <div class="spotify-header">
        <h1>🎵 Spotify Premium Subscription Prediction Dashboard</h1>
        <p style="color: #000000; font-size: 1.2rem; margin-top: 0.5rem;">Predict user subscription behavior using machine learning</p>
    </div>
""", unsafe_allow_html=True)

# Landing Page or Main App based on session state
if not st.session_state.show_app:
    # Landing Page Content
    st.markdown("""
        <div class="landing-hero">
            <h1>🎵 Welcome to Spotify Premium Prediction</h1>
            <p>Predict user subscription behavior with AI-powered machine learning</p>
        </div>
    """, unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown("""
        <div class="how-it-works">
            <h2>📊 How It Works</h2>
            <div class="workflow-diagram">
                <div class="diagram-step">
                    <div class="diagram-icon">📝</div>
                    <h4>Input Data</h4>
                    <p>Enter user demographics, listening habits, and preferences</p>
                </div>
                <div class="diagram-arrow">→</div>
                <div class="diagram-step">
                    <div class="diagram-icon">🤖</div>
                    <h4>AI Analysis</h4>
                    <p>SVM model processes 93 features to analyze patterns</p>
                </div>
                <div class="diagram-arrow">→</div>
                <div class="diagram-step">
                    <div class="diagram-icon">📊</div>
                    <h4>Get Prediction</h4>
                    <p>Receive instant prediction with confidence score</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Workflow Steps
    st.markdown("""
        <div class="workflow-container">
            <div class="workflow-step">
                <h3>
                    <span class="workflow-step-number">1</span>
                    Single User Prediction
                </h3>
                <p>
                    Fill out a comprehensive form with user demographics, listening habits, podcast preferences, 
                    and usage behavior. Our AI model will instantly predict whether the user will subscribe to 
                    Premium or churn, along with a confidence percentage.
                </p>
            </div>
            
            <div class="workflow-step">
                <h3>
                    <span class="workflow-step-number">2</span>
                    Batch Prediction
                </h3>
                <p>
                    Upload a CSV file with multiple user records to get predictions for entire user segments at once. 
                    Download the results as a CSV file for further analysis and reporting.
                </p>
            </div>
            
            <div class="workflow-step">
                <h3>
                    <span class="workflow-step-number">3</span>
                    Visual Insights
                </h3>
                <p>
                    View predictions with beautiful visualizations including gauge charts, probability bars, 
                    and confidence indicators. Understand the model's decision-making process with detailed metrics.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Features Grid
    st.markdown("""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-card-icon">🎯</div>
                <h4>Accurate Predictions</h4>
                <p>Powered by SVM machine learning model with 93 features</p>
            </div>
            <div class="feature-card">
                <div class="feature-card-icon">⚡</div>
                <h4>Instant Results</h4>
                <p>Get predictions in real-time with confidence scores</p>
            </div>
            <div class="feature-card">
                <div class="feature-card-icon">📈</div>
                <h4>Visual Analytics</h4>
                <p>Beautiful charts and graphs for data visualization</p>
            </div>
            <div class="feature-card">
                <div class="feature-card-icon">📊</div>
                <h4>Batch Processing</h4>
                <p>Process multiple users simultaneously via CSV upload</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Get Started Button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        get_started = st.button("🚀 Get Started", use_container_width=True, type="primary", key="get_started")
        if get_started:
            st.session_state.show_app = True
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
else:
    # Main App Content
    # Beautiful animation at the start
    st.markdown("""
        <div class="animation-container">
            <div class="animated-icon">🎵</div>
            <div class="animated-text">Welcome to Spotify Premium Prediction</div>
            <div class="animated-subtext">Get instant insights into user subscription behavior with AI-powered predictions</div>
        </div>
    """, unsafe_allow_html=True)

    # Add back to landing page button
    if st.button("← Back to Landing Page", use_container_width=False):
        st.session_state.show_app = False
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Main content area
    tab1, tab2 = st.tabs(["🔮 Single Prediction", "📊 Batch Prediction"])

    with tab1:
        st.markdown("""
            <div class="form-header">
                <h3>📝 User Input Form</h3>
                <p>Fill in the details below to predict subscription behavior. Default values are provided for quick testing.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Create mappings for user-friendly labels
        age_options = {
            "20-35": "Age_20-35",
            "35-60": "Age_35-60",
            "6-12": "Age_6-12",
            "60+": "Age_60+"
        }
        
        gender_options = {
            "Male": "Gender_male",
            "Others": "Gender_others"
        }
        
        music_genre_options = {
            "Classical": "fav_music_genre_classical",
            "Classical & Melody, Dance": "fav_music_genre_classical & melody, dance",
            "Electronic/Dance": "fav_music_genre_electronic/dance",
            "K-Pop": "fav_music_genre_kpop",
            "Melody": "fav_music_genre_melody",
            "Old Songs": "fav_music_genre_old songs",
            "Pop": "fav_music_genre_pop",
            "Rap": "fav_music_genre_rap",
            "Rock": "fav_music_genre_rock",
            "Trending Songs Random": "fav_music_genre_trending songs random"
        }
        
        time_slot_options = {
            "Morning": "music_time_slot_morning",
            "Night": "music_time_slot_night"
        }
        
        device_options = {
            "Smartphone": "spotify_listening_device_smartphone",
            "Computer or Laptop": "spotify_listening_device_computer or laptop",
            "Smartphone, Computer or Laptop": "spotify_listening_device_smartphone, computer or laptop",
            "Smartphone, Computer, Smart Speakers": "spotify_listening_device_smartphone, computer or laptop, smart speakers or voice assistants",
            "Smartphone, Computer, Smart Speakers, Wearables": "spotify_listening_device_smartphone, computer or laptop, smart speakers or voice assistants, wearable devices",
            "Smartphone, Computer, Wearables": "spotify_listening_device_smartphone, computer or laptop, wearable devices",
            "Smartphone, Smart Speakers": "spotify_listening_device_smartphone, smart speakers or voice assistants",
            "Smartphone, Smart Speakers, Wearables": "spotify_listening_device_smartphone, smart speakers or voice assistants, wearable devices",
            "Smartphone, Wearables": "spotify_listening_device_smartphone, wearable devices",
            "Computer, Smart Speakers": "spotify_listening_device_computer or laptop, smart speakers or voice assistants",
            "Computer, Smart Speakers, Wearables": "spotify_listening_device_computer or laptop, smart speakers or voice assistants, wearable devices",
            "Computer, Wearables": "spotify_listening_device_computer or laptop, wearable devices",
            "Smart Speakers": "spotify_listening_device_smart speakers or voice assistants",
            "Smart Speakers, Wearables": "spotify_listening_device_smart speakers or voice assistants, wearable devices",
            "Wearable Devices": "spotify_listening_device_wearable devices"
        }
        
        pod_genre_options = {
            "Comedy": "fav_pod_genre_comedy",
            "Dance and Relevant Cases": "fav_pod_genre_dance and relevant cases",
            "Educational": "fav_pod_genre_educational",
            "Everything": "fav_pod_genre_everything",
            "Finance and Current Affairs": "fav_pod_genre_finance related and current affairs",
            "Food and Cooking": "fav_pod_genre_food and cooking",
            "General Knowledge": "fav_pod_genre_general knowledge",
            "Health and Fitness": "fav_pod_genre_health and fitness",
            "Informative Stuff": "fav_pod_genre_informative stuff",
            "Lifestyle and Health": "fav_pod_genre_lifestyle and health",
            "Murder Mystery": "fav_pod_genre_murder mystery",
            "Novels": "fav_pod_genre_novels",
            "Political, Informative": "fav_pod_genre_political, informative, topics that interests me",
            "Self Help": "fav_pod_genre_self help",
            "Spiritual and Devotional": "fav_pod_genre_spiritual and devotional",
            "Sports": "fav_pod_genre_sports",
            "Stories": "fav_pod_genre_stories",
            "Technology": "fav_pod_genre_technology"
        }
        
        pod_format_options = {
            "Educational": "preffered_pod_format_educational",
            "Interview": "preffered_pod_format_interview",
            "Story Telling": "preffered_pod_format_story telling"
        }
        
        pod_host_options = {
            "Unknown Podcasters": "pod_host_preference_unknown podcasters",
            "Well Known Individuals": "pod_host_preference_well known individuals"
        }
        
        pod_duration_options = {
            "Longer": "preffered_pod_duration_longer",
            "Shorter": "preffered_pod_duration_shorter"
        }
        
        premium_plan_options = {
            "Individual Plan (Rs 119/month)": "preffered_premium_plan_individual plan- rs 119/ month",
            "Student Plan (Rs 59/month)": "preffered_premium_plan_student plan-rs 59/month",
            "Family Plan (Rs 179/month)": "preffered_premium_plan_family plan-rs 179/month"
        }
        
        subscription_plan_options = {
            "Premium (Paid Subscription)": "spotify_subscription_plan_premium (paid subscription)",
            "None": ""
        }
        
        listening_content_options = {
            "Podcast": "preferred_listening_content_podcast",
            "None": ""
        }
        
        listening_context_options = {
            "Before Bed": "beforebed",
            "Leisure Time": "leisuretime",
            "Nighttime": "nighttime",
            "Office Hours": "officehours",
            "Random": "random",
            "Social Gatherings": "socialgatherings",
            "Study Hours": "studyhours",
            "When Cooking": "whencooking",
            "While Traveling": "whiletraveling",
            "Workout Session": "workoutsession"
        }
        
        mood_options = {
            "Relaxation and Stress Relief": "relaxation and stress relief",
            "Uplifting and Motivational": "uplifting and motivational",
            "Social Gatherings or Parties": "social gatherings or parties",
            "Sadness or Melancholy": "sadness or melancholy",
            "Sadness or Melancholy (Alt)": " sadness or melancholy",
            "Social Gatherings or Parties (Alt)": " social gatherings or parties",
            "Uplifting and Motivational (Alt)": " uplifting and motivational"
        }
        
        discovery_options = {
            "Friends": "expl_friends",
            "Others": "expl_others",
            "Playlists": "expl_playlists",
            "Radio": "expl_radio",
            "Recommendations": "expl_recommendations",
            "Recommendations, Others": "expl_recommendations,others",
            "Search": "expl_search",
            "Social Media": "expl_social media"
        }
        
        # Initialize default values
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown("#### 👤 Demographics")
            st.markdown("---")
            
            age_label = st.selectbox(
            "**Age Group**",
            list(age_options.keys()),
            index=0,
            help="Select the user's age group"
            )
            age_group = age_options[age_label]
            
            gender_label = st.radio(
            "**Gender**",
            list(gender_options.keys()),
            index=0,
            horizontal=True,
            help="Select the user's gender"
            )
            gender = gender_options[gender_label]
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown("#### 🎧 Listening Habits")
            st.markdown("---")
            
            spotify_usage_period = st.slider(
            "**Spotify Usage Period (months)**",
            min_value=0,
            max_value=60,
            value=12,
            help="How long has the user been using Spotify?"
            )
            
            music_recc_rating = st.slider(
            "**Music Recommendation Rating**",
            min_value=1.0,
            max_value=5.0,
            value=4.0,
            step=0.1,
            help="Rate the quality of music recommendations (1-5)"
            )
            
            music_genre_label = st.selectbox(
            "**Favorite Music Genre**",
            list(music_genre_options.keys()),
            index=6,
            help="Select the user's favorite music genre"
            )
            fav_music_genre = music_genre_options[music_genre_label]
            
            time_slot_label = st.radio(
            "**Preferred Music Time Slot**",
            list(time_slot_options.keys()),
            index=1,
            horizontal=True,
            help="When does the user prefer to listen to music?"
            )
            music_time_slot = time_slot_options[time_slot_label]
            
            device_label = st.selectbox(
            "**Primary Listening Device**",
            list(device_options.keys()),
            index=0,
            help="Select the device(s) used for listening"
            )
            spotify_listening_device = device_options[device_label]
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown("#### 🎙️ Podcast Preferences")
            st.markdown("---")
            
            pod_lis_frequency = st.slider(
            "**Podcast Listening Frequency**",
            min_value=0.0,
            max_value=10.0,
            value=5.0,
            step=0.1,
            help="How frequently does the user listen to podcasts? (0-10)"
            )
            
            pod_variety_satisfaction = st.slider(
            "**Podcast Variety Satisfaction**",
            min_value=1.0,
            max_value=5.0,
            value=3.5,
            step=0.1,
            help="Satisfaction with podcast variety (1-5)"
            )
            
            pod_genre_label = st.selectbox(
            "**Favorite Podcast Genre**",
            list(pod_genre_options.keys()),
            index=2,
            help="Select the user's favorite podcast genre"
            )
            fav_pod_genre = pod_genre_options[pod_genre_label]
            
            pod_format_label = st.radio(
            "**Preferred Podcast Format**",
            list(pod_format_options.keys()),
            index=0,
            help="What format does the user prefer?"
            )
            preffered_pod_format = pod_format_options[pod_format_label]
            
            pod_host_label = st.radio(
            "**Podcast Host Preference**",
            list(pod_host_options.keys()),
            index=1,
            horizontal=True,
            help="Does the user prefer well-known hosts?"
            )
            pod_host_preference = pod_host_options[pod_host_label]
            
            pod_duration_label = st.radio(
            "**Preferred Podcast Duration**",
            list(pod_duration_options.keys()),
            index=0,
            horizontal=True,
            help="Does the user prefer longer or shorter podcasts?"
            )
            preffered_pod_duration = pod_duration_options[pod_duration_label]
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown("#### 📱 Usage Behavior")
            st.markdown("---")
            
            is_premium = st.radio(
            "**Current Premium Status**",
            [0, 1],
            index=0,
            format_func=lambda x: "Premium" if x == 1 else "Free",
            horizontal=True,
            help="Is the user currently on Premium?"
            )
            
            # Update subscription plan based on premium status
            subscription_keys = list(subscription_plan_options.keys())
            if is_premium == 1:
                # Find "Premium (Paid Subscription)" index
                default_subscription_index = 0 if "Premium" in subscription_keys[0] else 1
            else:
                # Find "None" index
                default_subscription_index = 1 if "None" in subscription_keys[1] else 0
            
            subscription_plan_label = st.selectbox(
            "**Spotify Subscription Plan**",
            subscription_keys,
            index=default_subscription_index,
            help="Current subscription plan"
            )
            spotify_subscription_plan = subscription_plan_options.get(subscription_plan_label, "") if subscription_plan_label else ""
            
            premium_plan_label = st.selectbox(
            "**Preferred Premium Plan**",
            list(premium_plan_options.keys()),
            index=0,
            help="Which premium plan would the user prefer?"
            )
            preffered_premium_plan = premium_plan_options[premium_plan_label]
            
            listening_content_label = st.radio(
            "**Preferred Listening Content**",
            list(listening_content_options.keys()),
            index=0,
            horizontal=True,
            help="Does the user prefer podcasts?"
            )
            preferred_listening_content = listening_content_options[listening_content_label] if listening_content_label else ""
            
            st.markdown('</div>', unsafe_allow_html=True)
    
        # Listening contexts (multiselect)
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Listening Contexts")
        st.markdown("---")
        st.markdown("Select all situations where the user listens to music:")
        
        listening_context_labels = st.multiselect(
        "**When does the user listen to music?**",
        list(listening_context_options.keys()),
        default=["Leisure Time", "While Traveling", "Workout Session"],
        help="Select all applicable listening contexts"
        )
        listening_contexts = [listening_context_options[label] for label in listening_context_labels] if listening_context_labels else []
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Music mood preferences
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown("#### 😊 Music Mood Preferences")
        st.markdown("---")
        st.markdown("Select all moods the user enjoys:")
        
        mood_labels = st.multiselect(
        "**What moods does the user prefer?**",
        list(mood_options.keys()),
        default=["Relaxation and Stress Relief", "Uplifting and Motivational"],
        help="Select all applicable mood preferences"
        )
        mood_preferences = [mood_options[label] for label in mood_labels] if mood_labels else []
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Music discovery methods
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown("#### 🔍 Music Discovery Methods")
        st.markdown("---")
        st.markdown("How does the user discover new music?")
        
        discovery_labels = st.multiselect(
        "**Discovery Methods**",
        list(discovery_options.keys()),
        default=["Recommendations", "Search"],
        help="Select all methods used to discover music"
        )
        discovery_methods = [discovery_options[label] for label in discovery_labels] if discovery_labels else []
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Predict button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            predict_button = st.button("🎵 Predict Subscription Behavior", use_container_width=True, type="primary")
        
        # Prediction logic
        if predict_button:
            # Create feature vector
            feature_dict = {col: 0 for col in feature_columns}
        
        # Set numeric features
        feature_dict['spotify_usage_period'] = spotify_usage_period
        feature_dict['music_recc_rating'] = music_recc_rating
        feature_dict['pod_lis_frequency'] = pod_lis_frequency
        feature_dict['pod_variety_satisfaction'] = pod_variety_satisfaction
        feature_dict['is_premium'] = is_premium
        
        # Set categorical features
        feature_dict[age_group] = 1
        feature_dict[gender] = 1
        feature_dict[music_time_slot] = 1
        feature_dict[fav_music_genre] = 1
        feature_dict[spotify_listening_device] = 1
        feature_dict[fav_pod_genre] = 1
        feature_dict[preffered_pod_format] = 1
        feature_dict[pod_host_preference] = 1
        feature_dict[preffered_pod_duration] = 1
        
        if spotify_subscription_plan:
            feature_dict[spotify_subscription_plan] = 1
        if preffered_premium_plan:
            feature_dict[preffered_premium_plan] = 1
        if preferred_listening_content:
            feature_dict[preferred_listening_content] = 1
        
        # Set listening contexts
        for context in listening_contexts:
            if context in feature_dict:
                feature_dict[context] = 1
        
        # Set mood preferences
        for mood in mood_preferences:
            if mood in feature_dict:
                feature_dict[mood] = 1
        
        # Set discovery methods
        for method in discovery_methods:
            if method in feature_dict:
                feature_dict[method] = 1
        
        # Convert to DataFrame in correct order
        feature_vector = pd.DataFrame([feature_dict])[feature_columns]
        
        # Make prediction
        try:
            prediction = model.predict(feature_vector)[0]
            probabilities = model.predict_proba(feature_vector)[0]
            
            # Determine confidence (probability of predicted class)
            confidence = probabilities[prediction] * 100
            
            # Store results
            st.session_state.prediction_made = True
            st.session_state.prediction_result = prediction
            st.session_state.confidence = confidence
            st.session_state.probabilities = probabilities
            
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            st.session_state.prediction_made = False
        
        # Display prediction results
        if st.session_state.prediction_made:
            prediction = st.session_state.prediction_result
            confidence = st.session_state.confidence
            probabilities = st.session_state.probabilities
        
        # Determine prediction text and color
        will_subscribe = prediction == 1
        prediction_text = "Will Subscribe to Premium" if will_subscribe else "Will Not Subscribe (Churn)"
        card_class = "" if will_subscribe else "churn"
        status_color = "#1DB954" if will_subscribe else "#e22134"
        
        # Prediction card
        st.markdown(f"""
            <div class="prediction-card {card_class}">
                <div class="prediction-text">{prediction_text}</div>
                <div class="confidence-text">Confidence: {confidence:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        st.progress(confidence / 100)
        
        # Visualization
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = confidence,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Confidence Level"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': status_color},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 100], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff")
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col_viz2:
            # Probability bar chart
            prob_df = pd.DataFrame({
                'Class': ['Will Not Subscribe', 'Will Subscribe'],
                'Probability': [probabilities[0] * 100, probabilities[1] * 100]
            })
            fig_bar = px.bar(
                prob_df,
                x='Class',
                y='Probability',
                color='Class',
                color_discrete_map={
                    'Will Not Subscribe': '#e22134',
                    'Will Subscribe': '#1DB954'
                },
                text='Probability',
                labels={'Probability': 'Probability (%)', 'Class': 'Prediction Class'}
            )
            fig_bar.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False, range=[0, 100])
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Feature importance placeholder
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown("#### 📊 Model Information")
        st.info("""
        **Model Type:** Support Vector Machine (SVM) Pipeline
        
        **Key Features Considered:**
        - Demographics (Age, Gender)
        - Listening habits and preferences
        - Podcast engagement metrics
        - Device usage patterns
        - Subscription history
        - Content discovery methods
        
        *Note: Feature importance analysis would require additional model interpretation tools. 
        The SVM model uses a combination of all features to make predictions.*
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown("### Batch Prediction")
        st.markdown("Upload a CSV file with user data to get predictions for multiple users at once.")
    
    # CSV upload
        uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file with columns matching the feature names. See template below."
        )
    
        if uploaded_file is not None:
            try:
                # Read CSV
                df = pd.read_csv(uploaded_file)
                
                st.success(f"Successfully loaded {len(df)} rows from CSV file.")
                st.dataframe(df.head(), use_container_width=True)
                
                # Process predictions
                if st.button("🔮 Predict All", type="primary"):
                    progress_bar = st.progress(0)
                status_text = st.empty()
                
                predictions = []
                confidences = []
                
                for idx, row in df.iterrows():
                    status_text.text(f"Processing row {idx + 1} of {len(df)}...")
                    progress_bar.progress((idx + 1) / len(df))
                    
                    # Create feature vector from row
                    feature_dict = {col: 0 for col in feature_columns}
                    
                    # Map row data to features
                    for col in feature_columns:
                        if col in df.columns:
                            if col in ['spotify_usage_period', 'music_recc_rating', 'pod_lis_frequency', 
                                      'pod_variety_satisfaction', 'is_premium']:
                                feature_dict[col] = float(row[col]) if pd.notna(row[col]) else 0
                            else:
                                feature_dict[col] = 1 if row[col] == 1 or row[col] == '1' or row[col] == True else 0
                    
                    # Convert to DataFrame
                    feature_vector = pd.DataFrame([feature_dict])[feature_columns]
                    
                    # Make prediction
                    try:
                        prediction = model.predict(feature_vector)[0]
                        probabilities = model.predict_proba(feature_vector)[0]
                        confidence = probabilities[prediction] * 100
                        
                        predictions.append(prediction)
                        confidences.append(confidence)
                    except Exception as e:
                        predictions.append(-1)
                        confidences.append(0)
                
                # Add predictions to dataframe
                df['Prediction'] = ['Will Subscribe' if p == 1 else 'Will Not Subscribe' if p == 0 else 'Error' for p in predictions]
                df['Confidence'] = confidences
                
                progress_bar.empty()
                status_text.empty()
                
                st.success("Predictions completed!")
                
                # Display results
                st.dataframe(df, use_container_width=True)
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Predictions as CSV",
                    data=csv,
                    file_name="spotify_predictions.csv",
                    mime="text/csv"
                )
                
                # Summary statistics
                col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
                with col_sum1:
                    st.metric("Total Users", len(df))
                with col_sum2:
                    st.metric("Will Subscribe", sum(1 for p in predictions if p == 1))
                with col_sum3:
                    st.metric("Will Churn", sum(1 for p in predictions if p == 0))
                with col_sum4:
                    st.metric("Avg Confidence", f"{np.mean(confidences):.2f}%")
            except Exception as e:
                st.error(f"Error processing CSV file: {str(e)}")
                st.info("Please ensure your CSV file has the correct format. Required columns should match the feature names.")
        else:
            st.info("""
        **CSV File Format Requirements:**
        
        Your CSV file should contain columns matching the feature names. For categorical features, use 1 for selected and 0 for not selected.
        For numeric features (spotify_usage_period, music_recc_rating, pod_lis_frequency, pod_variety_satisfaction, is_premium), 
        provide the actual numeric values.
        
        **Example columns:**
        - spotify_usage_period (numeric)
        - music_recc_rating (numeric)
        - Age_20-35 (0 or 1)
        - Gender_male (0 or 1)
        - fav_music_genre_pop (0 or 1)
        - ... (all other feature columns)
        """)

    # About This Project section at the bottom
        st.markdown("""
        <div class="info-card" style="margin-top: 3rem;">
            <h3>📚 About This Project</h3>
            <p style="color: #b3b3b3; line-height: 1.6;">
            This dashboard uses a trained Support Vector Machine (SVM) model to predict whether a Spotify user 
            will subscribe to Premium or churn. The model analyzes various factors including demographics, 
            listening habits, podcast preferences, and usage behavior to make accurate predictions. 
            Use the form above to input user data and get instant predictions, or upload a CSV file for batch predictions.
            </p>
            <p style="color: #b3b3b3; line-height: 1.6; margin-top: 1rem;">
            <strong>Key Features:</strong> The model considers 93 different features including user demographics, 
            music preferences, podcast engagement, device usage patterns, subscription history, and content discovery methods 
            to provide accurate subscription predictions with confidence scores.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer (shown on both pages)
st.markdown("""
        <div class="footer">
        <p style="font-size: 1rem; margin: 0;">Built by <strong style="color: #1DB954;">Vansh Bharat Patil</strong></p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; color: #808080;">Spotify Premium Churn Prediction Dashboard</p>
        </div>
""", unsafe_allow_html=True)

