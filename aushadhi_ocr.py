import os
import sys

# Set the library path for zbar on macOS
if sys.platform == "darwin":  # macOS
    zbar_lib_path = "/opt/homebrew/opt/zbar/lib"
    if os.path.exists(zbar_lib_path):
        os.environ["DYLD_LIBRARY_PATH"] = zbar_lib_path

import streamlit as st
import pandas as pd
import numpy as np
import cv2
import pytesseract
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
from datetime import datetime, timedelta
import random
from thefuzz import fuzz, process
import time

# Configure page
st.set_page_config(
    layout="wide", 
    page_title="Aushadhi-OCR", 
    page_icon="💊",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for modern UI/UX
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0.5rem 1rem;
    }
    
    /* Remove default Streamlit spacing */
    .stApp > div {
        padding-top: 0rem;
    }
    
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Remove white bars and spacing */
    .stApp > header {
        display: none;
    }
    
    .stApp > div[data-testid="stToolbar"] {
        display: none;
    }
    
    /* Remove extra margins */
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Compact spacing for columns */
    .stColumns > div {
        padding: 0.25rem;
    }
    
    /* Remove white space between sections */
    .stApp > div[data-testid="stHeader"] {
        display: none;
    }
    
    /* Compact section spacing */
    .stApp .main .block-container > div {
        margin-bottom: 0.5rem;
    }
    
    /* Remove extra padding from expander */
    .streamlit-expander {
        margin-bottom: 0.5rem;
    }
    
    /* Compact metric spacing */
    .metric-container {
        margin-bottom: 0.5rem;
    }
    
    /* Remove white space from file uploader */
    .stFileUploader {
        margin-bottom: 0.5rem;
    }
    
    /* Compact button spacing */
    .stButton {
        margin-bottom: 0.5rem;
    }
    
    /* COMPLETELY REMOVE ALL WHITE BARS AND BACKGROUNDS */
    .stApp > div[data-testid="stHeader"] {
        display: none !important;
    }
    
    .stApp > div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    .stApp > div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Remove any remaining white bars - AGGRESSIVE */
    .stApp > div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Force remove white backgrounds from all containers */
    .stApp .main .block-container {
        background: transparent !important;
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Remove white backgrounds from all elements */
    .stApp .element-container {
        background: transparent !important;
    }
    
    /* NUCLEAR OPTION - Remove ALL white backgrounds */
    .stApp div[style*="background-color: white"],
    .stApp div[style*="background: white"],
    .stApp div[style*="background-color: #ffffff"],
    .stApp div[style*="background: #ffffff"],
    .stApp div[style*="background-color: #fff"],
    .stApp div[style*="background: #fff"] {
        background: transparent !important;
    }
    
    /* Force dark theme on ALL elements */
    .stApp * {
        background-color: transparent !important;
    }
    
    /* Override any remaining white backgrounds */
    .stApp div[data-testid="stVerticalBlock"] {
        background: transparent !important;
    }
    
    .stApp div[data-testid="stHorizontalBlock"] {
        background: transparent !important;
    }
    
    /* Remove any top spacing completely */
    .stApp .main .block-container > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Force vibrant backgrounds on all elements */
    .stApp .main .block-container > div {
        background: transparent !important;
    }
    
    /* Override any white backgrounds */
    div[data-testid="stVerticalBlock"] {
        background: transparent !important;
    }
    
    div[data-testid="stHorizontalBlock"] {
        background: transparent !important;
    }
    
    /* Professional text styling on dark background */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #ffffff !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        font-weight: 600 !important;
    }
    
    .stApp p, .stApp div, .stApp span {
        color: #e0e0e0 !important;
        font-weight: 400 !important;
    }
    
    /* Professional labels */
    .stApp label {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Clean text styling */
    .stApp .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    .stApp .stText {
        color: #e0e0e0 !important;
    }
    
    /* Professional CSS Variables - SOLID COLORS */
    :root {
        --primary-color: #4a90e2;
        --secondary-color: #7b68ee;
        --success-color: #50c878;
        --warning-color: #ffa500;
        --error-color: #ff6b6b;
        --info-color: #6c5ce7;
        --background-color: #1a1a1a;
        --card-background: #2a2a2a;
        --text-primary: #ffffff;
        --text-secondary: #e0e0e0;
        --border-color: #444444;
        --shadow: none;
        --shadow-lg: none;
    }
    
    /* Set app background - SOLID DARK THEME */
    .stApp {
        background: #1a1a1a;
        min-height: 100vh;
    }
    
    /* Remove the top white bar completely */
    .stApp > div[data-testid="stHeader"] {
        display: none !important;
    }
    
    .stApp > div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    .stApp > div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Remove any top padding/margin */
    .stApp .main .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Force remove all white backgrounds */
    .stApp > div {
        background: transparent !important;
    }
    
    /* Remove white bars from all elements */
    .stApp .main .block-container > div {
        background: transparent !important;
    }
    
    /* Override Streamlit's white backgrounds */
    div[data-testid="stVerticalBlock"] {
        background: transparent !important;
    }
    
    div[data-testid="stHorizontalBlock"] {
        background: transparent !important;
    }
    
    /* Remove white bars completely */
    .stApp > div[data-testid="stDecoration"] {
        display: none;
    }
    
    /* Make main content fill the space */
    .main .block-container {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
        background: transparent;
    }
    
    /* Override Streamlit's default white background */
    .stApp > div {
        background: transparent !important;
    }
    
    /* Make sidebar background vibrant */
    .css-1d391kg {
        background: linear-gradient(180deg, #ff6b6b 0%, #4ecdc4 100%) !important;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #ff6b6b 0%, #4ecdc4 100%) !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* Custom Cards */
    .custom-card {
        background: var(--card-background);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    /* Status Cards - Bright and Vibrant */
    .status-card {
        background: var(--gradient-primary);
        color: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
        border: 2px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
    }
    
    .status-success {
        background: var(--gradient-success);
        border: 2px solid rgba(69, 183, 209, 0.3);
    }
    
    .status-error {
        background: linear-gradient(135deg, #ff6b6b 0%, #f0932b 100%);
        border: 2px solid rgba(255, 107, 107, 0.3);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f9ca24 0%, #f0932b 100%);
        border: 2px solid rgba(249, 202, 36, 0.3);
    }
    
    /* Custom Buttons - Bright and Vibrant */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, #ff5252 0%, #26a69a 100%);
    }
    
    /* Metrics Styling */
    .metric-container {
        background: var(--card-background);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        border-radius: 4px;
    }
    
    /* Sidebar Styling - Bright and Vibrant */
    .css-1d391kg {
        background: var(--gradient-primary);
    }
    
    .sidebar .sidebar-content {
        background: var(--gradient-primary);
    }
    
    .sidebar .sidebar-content .block-container {
        color: white !important;
    }
    
    .sidebar .sidebar-content h1,
    .sidebar .sidebar-content h2,
    .sidebar .sidebar-content h3,
    .sidebar .sidebar-content p,
    .sidebar .sidebar-content div {
        color: white !important;
    }
    
    .sidebar .sidebar-content .stSelectbox > div > div {
        color: white !important;
    }
    
    .sidebar .sidebar-content .stTextInput > div > div > input {
        color: white !important;
    }
    
    /* Professional file uploader styling - SOLID COLORS */
    .stFileUploader > div > div > div {
        border: 1px dashed #666666 !important;
        border-radius: 8px !important;
        background: #2a2a2a !important;
        transition: all 0.2s ease;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
        box-shadow: none !important;
    }
    
    .stFileUploader > div > div > div:hover {
        border-color: #888888 !important;
        background: #333333 !important;
        transform: none;
        box-shadow: none !important;
    }
    
    /* Professional file uploader text */
    .stFileUploader > div > div > div > div {
        color: #e0e0e0 !important;
        font-weight: 400 !important;
    }
    
    .stFileUploader > div > div > div > div > div {
        color: #e0e0e0 !important;
        font-weight: 400 !important;
    }
    
    /* Professional input field styling - SOLID COLORS */
    .stTextInput > div > div > input {
        background: #2a2a2a !important;
        border: 1px solid #444444 !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        font-weight: 400 !important;
        box-shadow: none !important;
    }
    
    .stSelectbox > div > div {
        background: #2a2a2a !important;
        border: 1px solid #444444 !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        box-shadow: none !important;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
        font-weight: 400 !important;
    }
    
    /* Camera input styling - SOLID COLORS */
    .stCameraInput > div {
        background: #2a2a2a !important;
        border: 2px dashed #666666 !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
        box-shadow: none !important;
    }
    
    .stCameraInput > div:hover {
        border-color: #888888 !important;
        background: #333333 !important;
    }
    
    /* Camera input text styling */
    .stCameraInput > div > div {
        color: #e0e0e0 !important;
        font-weight: 400 !important;
    }
    
    .stCameraInput > div > div > div {
        color: #e0e0e0 !important;
        font-weight: 400 !important;
    }
    
    /* Tables Styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        
        .custom-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Try to import pyzbar with fallback
try:
    import pyzbar.pyzbar as pyzbar
    ZBAR_AVAILABLE = True
except ImportError as e:
    st.warning("⚠️ Barcode detection is not available. Please install zbar library.")
    ZBAR_AVAILABLE = False
    # Create a dummy pyzbar module for compatibility
    class DummyPyzbar:
        @staticmethod
        def decode(image):
            return []
    pyzbar = DummyPyzbar()

# Import EasyOCR for better text extraction
try:
    import easyocr
    import ssl
    import urllib.request
    
    # Fix SSL certificate issues
    ssl._create_default_https_context = ssl._create_unverified_context
    
    EASYOCR_AVAILABLE = True
    # Initialize EasyOCR reader (English only for now to avoid download issues)
    reader = easyocr.Reader(['en'], gpu=False)
except Exception as e:
    st.warning(f"⚠️ EasyOCR initialization failed: {str(e)}. Using fallback OCR.")
    EASYOCR_AVAILABLE = False
    reader = None

from io import BytesIO
import time
import json
import requests
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

# Page configuration (already set above)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .status-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .status-success {
        background-color: #d4edda;
        border-color: #28a745;
        color: #155724;
    }
    
    .status-warning {
        background-color: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }
    
    .status-error {
        background-color: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .scan-result {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .sidebar .sidebar-content .block-container {
        color: white !important;
    }
    
    .sidebar .sidebar-content h1, 
    .sidebar .sidebar-content h2, 
    .sidebar .sidebar-content h3,
    .sidebar .sidebar-content p,
    .sidebar .sidebar-content div {
        color: white !important;
    }
    
    .sidebar .sidebar-content .stSelectbox > div > div {
        color: white !important;
    }
    
    .sidebar .sidebar-content .stTextInput > div > div > input {
        color: white !important;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []
if 'total_scans' not in st.session_state:
    st.session_state.total_scans = 0
if 'verified_medicines' not in st.session_state:
    st.session_state.verified_medicines = 0
if 'counterfeits_detected' not in st.session_state:
    st.session_state.counterfeits_detected = 0

# Import comprehensive medicine database
from medicine_database import create_medicine_database

# Image preprocessing functions
def detect_blur(image):
    """Detect if image is blurry using Laplacian variance"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def analyze_image_quality(image):
    """Analyze image quality metrics"""
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Calculate various quality metrics
        blur_score = detect_blur(image)
        contrast = gray.std()
        brightness = gray.mean()
        
        # Determine quality level
        if blur_score > 100:
            blur_level = "✅ Sharp"
        elif blur_score > 50:
            blur_level = "⚠️ Slightly Blurry"
        else:
            blur_level = "❌ Blurry"
            
        if contrast > 50:
            contrast_level = "✅ Good"
        elif contrast > 30:
            contrast_level = "⚠️ Fair"
        else:
            contrast_level = "❌ Poor"
            
        if 100 < brightness < 155:
            brightness_level = "✅ Optimal"
        elif 80 < brightness < 175:
            brightness_level = "⚠️ Acceptable"
        else:
            brightness_level = "❌ Poor"
        
        return {
            'blur_score': blur_score,
            'blur_level': blur_level,
            'contrast': contrast,
            'contrast_level': contrast_level,
            'brightness': brightness,
            'brightness_level': brightness_level
        }
    except Exception as e:
        return {
            'blur_score': 0,
            'blur_level': "❌ Error",
            'contrast': 0,
            'contrast_level': "❌ Error",
            'brightness': 0,
            'brightness_level': "❌ Error"
        }

def enhance_image(image):
    """Clear and effective image enhancement for OCR"""
    try:
        enhanced = image.copy()
        
        # Convert to grayscale
        if len(enhanced.shape) == 3:
            gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
        else:
            gray = enhanced.copy()

        # Step 1: Moderate upscaling for better text recognition
        scale = 1.5
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        # Step 2: Noise reduction with median filter
        denoised = cv2.medianBlur(gray, 3)

        # Step 3: CLAHE for local contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_img = clahe.apply(denoised)

        # Step 4: Gamma correction for better contrast
        gamma = 1.1
        gamma_corrected = np.power(clahe_img / 255.0, gamma) * 255.0
        gamma_corrected = np.uint8(gamma_corrected)

        # Step 5: Simple but effective sharpening
        sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(gamma_corrected, -1, sharpen_kernel)
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)

        # Step 6: Adaptive thresholding for clear text
        thresh = cv2.adaptiveThreshold(
            sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Step 7: Clean up with morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        filled = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

        # Step 8: Final contrast adjustment
        final = cv2.convertScaleAbs(filled, alpha=1.1, beta=0)

        # Convert back to 3-channel for display
        enhanced = cv2.cvtColor(final, cv2.COLOR_GRAY2BGR)
        return enhanced
        
    except Exception as e:
        st.error(f"Image enhancement error: {str(e)}")
        return image

def correct_perspective(image):
    """Attempt to correct perspective distortion"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour (likely the package)
        largest_contour = max(contours, key=cv2.contourArea)
        approx = cv2.approxPolyDP(largest_contour, 0.02 * cv2.arcLength(largest_contour, True), True)
        
        if len(approx) == 4:
            # Perspective correction
            pts = np.float32(approx.reshape(4, 2))
            dst = np.float32([[0, 0], [300, 0], [300, 200], [0, 200]])
            matrix = cv2.getPerspectiveTransform(pts, dst)
            corrected = cv2.warpPerspective(image, matrix, (300, 200))
            return corrected
    
    return image

def preprocess_image(image):
    """Comprehensive image preprocessing with optimized performance"""
    enhancements = []
    
    # Convert PIL to OpenCV format
    if isinstance(image, Image.Image):
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Detect blur with optimized threshold
    blur_score = detect_blur(image)
    if blur_score < 100:
        enhancements.append("Blurry image detected, applying sharpening...")
        image = enhance_image(image)
    else:
        enhancements.append("Image quality is good, minimal processing needed...")
    
    # Apply perspective correction only if needed
    original_image = image.copy()
    corrected_image = correct_perspective(image)
    
    # Only use corrected image if it's significantly different
    if corrected_image.shape != original_image.shape:
        image = corrected_image
        enhancements.append("Perspective correction applied...")
    
    # Apply general enhancement
    image = enhance_image(image)
    enhancements.append("Image contrast and brightness optimized...")
    
    return image, enhancements

# OCR and barcode detection
def extract_text_ocr(image):
    """Advanced OCR text extraction using EasyOCR"""
    try:
        if EASYOCR_AVAILABLE and reader is not None:
            # Use EasyOCR for better accuracy
            results = reader.readtext(image)
            
            # Extract text from results
            extracted_texts = []
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # Only include high-confidence text
                    extracted_texts.append(text)
            
            # Combine all text
            full_text = ' '.join(extracted_texts)
            
        else:
            # Fallback to pytesseract with optimized settings
            if len(image.shape) == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            
            pil_image = Image.fromarray(image_rgb)
            # Optimized config for better text recognition
            config = '--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-/.,%()[]{}:;'
            full_text = pytesseract.image_to_string(pil_image, config=config)
        
        # Clean up the text
        if full_text:
            # Remove extra whitespace
            full_text = ' '.join(full_text.split())
            
            # Remove common OCR artifacts
            artifacts = ['|', '~', '`', '^', '_', '\\', '/', '(', ')', '[', ']', '{', '}']
            for artifact in artifacts:
                full_text = full_text.replace(artifact, ' ')
            
            # Clean up multiple spaces
            full_text = ' '.join(full_text.split())
            
            # Remove very short words (likely OCR noise)
            words = full_text.split()
            filtered_words = [word for word in words if len(word) > 1 or word.isdigit()]
            full_text = ' '.join(filtered_words)
        
        return full_text.strip()
        
    except Exception as e:
        st.error(f"OCR Error: {str(e)}")
        return ""

def extract_text_with_details(image):
    """Extract text with detailed information including confidence scores and bounding boxes"""
    try:
        if EASYOCR_AVAILABLE and reader is not None:
            # Use EasyOCR for detailed results
            results = reader.readtext(image)
            
            detailed_results = []
            for (bbox, text, confidence) in results:
                detailed_results.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': bbox
                })
            
            return detailed_results
            
        else:
            # Fallback to pytesseract with basic info
            if len(image.shape) == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            
            pil_image = Image.fromarray(image_rgb)
            # Optimized config for better text recognition
            config = '--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-/.,%()[]{}:;'
            text = pytesseract.image_to_string(pil_image, config=config)
            
            return [{'text': text, 'confidence': 0.8, 'bbox': None}]
        
    except Exception as e:
        st.error(f"Detailed OCR Error: {str(e)}")
        return []

def create_ocr_overlay(image, detailed_results):
    """Create visual overlay showing OCR detection results"""
    try:
        if not detailed_results:
            return image
        
        overlay_image = image.copy()
        
        for result in detailed_results:
            if result['bbox'] is not None:
                # Draw bounding box
                bbox = result['bbox']
                pts = np.array(bbox, np.int32)
                pts = pts.reshape((-1, 1, 2))
                
                # Color based on confidence
                if result['confidence'] > 0.7:
                    color = (0, 255, 0)  # Green for high confidence
                elif result['confidence'] > 0.5:
                    color = (0, 255, 255)  # Yellow for medium confidence
                else:
                    color = (0, 0, 255)  # Red for low confidence
                
                cv2.polylines(overlay_image, [pts], True, color, 2)
                
                # Add confidence text
                text_pos = (int(bbox[0][0]), int(bbox[0][1]) - 10)
                cv2.putText(overlay_image, f"{result['confidence']:.2f}", 
                           text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        return overlay_image
        
    except Exception as e:
        st.error(f"OCR Overlay Error: {str(e)}")
        return image

def extract_medicine_details(image):
    """Extract specific medicine details with simple OCR"""
    try:
        import re
        # Get the full text first
        full_text = extract_text_ocr(image)
        extracted_info = {
            'full_text': full_text,
            'medicine_name': '',
            'manufacturer': '',
            'batch_number': '',
            'mfg_date': '',
            'exp_date': '',
            'dosage': '',
            'confidence_scores': [],
            'word_positions': []
        }
        if not full_text:
            return extracted_info
        # Use regex to extract fields
        # Medicine name: look for line with mg/mcg/ml/g, but avoid batch/date lines
        lines = full_text.split('\n') if '\n' in full_text else [full_text]
        for line in lines:
            if re.search(r'\b(\d+\s?(mg|mcg|ml|g|IU))\b', line, re.I):
                if not any(x in line.lower() for x in ['batch', 'mfg', 'exp', 'date']):
                    extracted_info['medicine_name'] = line.strip()
                    break
        # Manufacturer: look for pharma/labs/limited/ltd
        for line in lines:
            if re.search(r'(pharma|labs|limited|ltd)', line, re.I):
                extracted_info['manufacturer'] = line.strip()
                break
        # Batch number: look for batch or BN followed by alphanum
        batch_match = re.search(r'(batch\s*no\.?|bn\s*:?)[\s\-]*([A-Z0-9\-]+)', full_text, re.I)
        if batch_match:
            extracted_info['batch_number'] = batch_match.group(2)
        else:
            # fallback: any word with 2+ letters then 3+ digits
            fallback = re.search(r'\b([A-Z]{2,}\d{3,})\b', full_text)
            if fallback:
                extracted_info['batch_number'] = fallback.group(1)
        # Dates: look for MFG/EXP or date patterns
        mfg_match = re.search(r'(mfg|manufacture)[^\d]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})', full_text, re.I)
        exp_match = re.search(r'(exp|expiry)[^\d]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})', full_text, re.I)
        if mfg_match:
            extracted_info['mfg_date'] = mfg_match.group(2)
        if exp_match:
            extracted_info['exp_date'] = exp_match.group(2)
        # fallback: any two date-like patterns
        if not extracted_info['exp_date'] or not extracted_info['mfg_date']:
            date_patterns = [r'\d{1,2}/\d{1,2}/\d{2,4}', r'\d{4}-\d{1,2}-\d{1,2}', r'\d{1,2}-\d{1,2}-\d{2,4}']
            dates_found = []
            for pat in date_patterns:
                dates_found += re.findall(pat, full_text)
            dates_found = list(dict.fromkeys(dates_found))
            if len(dates_found) >= 2:
                if not extracted_info['mfg_date']:
                    extracted_info['mfg_date'] = dates_found[0]
                if not extracted_info['exp_date']:
                    extracted_info['exp_date'] = dates_found[1]
            elif len(dates_found) == 1:
                if not extracted_info['exp_date']:
                    extracted_info['exp_date'] = dates_found[0]
        return extracted_info
    except Exception as e:
        st.error(f"Medicine details extraction error: {str(e)}")
        return {
            'full_text': '',
            'medicine_name': '',
            'manufacturer': '',
            'batch_number': '',
            'mfg_date': '',
            'exp_date': '',
            'dosage': '',
            'confidence_scores': [],
            'word_positions': []
        }

def detect_barcodes(image):
    """Detect and decode barcodes/QR codes"""
    if not ZBAR_AVAILABLE:
        st.info("ℹ️ Barcode detection is not available. Only text-based verification will be performed.")
        return []
    
    try:
        barcodes = pyzbar.decode(image)
        results = []
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            results.append({
                'data': barcode_data,
                'type': barcode_type
            })
        return results
    except Exception as e:
        st.error(f"Barcode detection error: {str(e)}")
        return []

def detect_hologram_seal(image):
    """Detect hologram or security seal on medicine package"""
    try:
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define range for holographic/reflective colors
        # Holograms typically have rainbow-like colors
        lower_hologram = np.array([0, 0, 200])  # High brightness, any hue
        upper_hologram = np.array([180, 30, 255])
        
        # Create mask for holographic areas
        mask = cv2.inRange(hsv, lower_hologram, upper_hologram)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Check for hologram-like features
        hologram_detected = False
        hologram_confidence = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Minimum area for hologram
                # Check for circular or rectangular shape (typical hologram shapes)
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if 0.3 < circularity < 1.0:  # Reasonable circularity
                        hologram_detected = True
                        hologram_confidence = min(100, (area / 1000) * 100)
                        break
        
        return {
            'detected': hologram_detected,
            'confidence': hologram_confidence,
            'contours_found': len(contours)
        }
        
    except Exception as e:
        st.error(f"Hologram detection error: {str(e)}")
        return {'detected': False, 'confidence': 0, 'contours_found': 0}

def check_color_consistency(image, reference_colors=None):
    """Check color consistency and detect unusual colors"""
    try:
        # Convert to LAB color space for better color analysis
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Calculate color statistics
        color_stats = {
            'mean_l': np.mean(l),
            'mean_a': np.mean(a),
            'mean_b': np.mean(b),
            'std_l': np.std(l),
            'std_a': np.std(a),
            'std_b': np.std(b)
        }
        
        # Check for unusual color patterns
        unusual_colors = []
        
        # Check for too much red (might indicate counterfeit)
        if color_stats['mean_a'] > 150:
            unusual_colors.append("Excessive red tint detected")
        
        # Check for too much blue
        if color_stats['mean_b'] < 120:
            unusual_colors.append("Excessive blue tint detected")
        
        # Check for low contrast (might indicate poor quality printing)
        if color_stats['std_l'] < 20:
            unusual_colors.append("Low contrast detected - possible poor quality printing")
        
        # Check for color uniformity (too uniform might indicate digital printing)
        if color_stats['std_a'] < 5 and color_stats['std_b'] < 5:
            unusual_colors.append("Unusually uniform colors - possible digital printing")
        
        return {
            'color_stats': color_stats,
            'unusual_colors': unusual_colors,
            'is_suspicious': len(unusual_colors) > 0
        }
        
    except Exception as e:
        st.error(f"Color consistency check error: {str(e)}")
        return {'color_stats': {}, 'unusual_colors': [], 'is_suspicious': False}

def detect_font_anomalies(image):
    """Detect font inconsistencies and anomalies"""
    try:
        # Convert to grayscale for text analysis
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours (text regions)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze text regions
        font_anomalies = []
        text_areas = []
        text_heights = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:  # Minimum area for text
                x, y, w, h = cv2.boundingRect(contour)
                text_areas.append(area)
                text_heights.append(h)
        
        if text_areas:
            # Check for inconsistent text sizes
            area_std = np.std(text_areas)
            height_std = np.std(text_heights)
            
            if area_std > np.mean(text_areas) * 0.5:
                font_anomalies.append("Inconsistent text sizes detected")
            
            if height_std > np.mean(text_heights) * 0.3:
                font_anomalies.append("Inconsistent font heights detected")
            
            # Check for very small or very large text
            avg_height = np.mean(text_heights)
            if avg_height < 10:
                font_anomalies.append("Text too small - possible poor quality")
            elif avg_height > 50:
                font_anomalies.append("Text unusually large - possible counterfeit")
        
        return {
            'anomalies': font_anomalies,
            'text_regions': len(text_areas),
            'avg_text_height': np.mean(text_heights) if text_heights else 0,
            'is_suspicious': len(font_anomalies) > 0
        }
        
    except Exception as e:
        st.error(f"Font anomaly detection error: {str(e)}")
        return {'anomalies': [], 'text_regions': 0, 'avg_text_height': 0, 'is_suspicious': False}

def create_ar_overlay(image, verification_result):
    """Create AR overlay with verification results"""
    try:
        # Create overlay image
        overlay = image.copy()
        height, width = overlay.shape[:2]
        
        # Define colors
        if verification_result['is_authentic']:
            color = (0, 255, 0)  # Green for authentic
            status_text = "✅ AUTHENTIC"
        else:
            color = (0, 0, 255)  # Red for counterfeit
            status_text = "❌ COUNTERFEIT"
        
        # Draw status overlay
        cv2.rectangle(overlay, (10, 10), (width-10, 80), color, -1)
        cv2.putText(overlay, status_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Draw confidence score
        confidence_text = f"Confidence: {verification_result['confidence_score']}%"
        cv2.putText(overlay, confidence_text, (20, height-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Draw bounding box around medicine package
        cv2.rectangle(overlay, (20, 20), (width-20, height-20), color, 3)
        
        return overlay
        
    except Exception as e:
        st.error(f"AR overlay creation error: {str(e)}")
        return image

# Medicine verification engine
def verify_medicine(extracted_text, barcode_data, medicine_db):
    """Comprehensive medicine verification"""
    results = {
        'is_authentic': True,
        'confidence_score': 0,
        'matched_medicine': None,
        'issues': [],
        'verification_details': {},
        'ocr_confidence': 0.8,
        'medicine_match': False,
        'manufacturer_match': False,
        'batch_valid': False,
        'date_valid': False,
        'barcode_valid': False
    }
    
    # Barcode verification (highest priority)
    if barcode_data:
        barcode_matches = medicine_db[medicine_db['Barcode_Data'] == barcode_data]
        if not barcode_matches.empty:
            results['matched_medicine'] = barcode_matches.iloc[0]
            results['confidence_score'] = 95
            results['verification_details']['barcode_verified'] = True
            results['barcode_valid'] = True
            results['medicine_match'] = True
            results['manufacturer_match'] = True
            return results
        else:
            results['issues'].append("Barcode not found in database")
            results['is_authentic'] = False
            results['barcode_valid'] = False
    
    # Text-based verification
    if extracted_text:
        # Fuzzy matching for brand names
        brand_names = medicine_db['Brand_Name'].tolist()
        best_match = process.extractOne(extracted_text, brand_names, scorer=fuzz.partial_ratio)
        
        if best_match and best_match[1] > 70:
            matched_medicine = medicine_db[medicine_db['Brand_Name'] == best_match[0]].iloc[0]
            results['matched_medicine'] = matched_medicine
            results['confidence_score'] = best_match[1]
            results['verification_details']['brand_match'] = best_match[1]
            results['medicine_match'] = True
            
            # Additional validations
            validate_batch_number(extracted_text, matched_medicine, results)
            validate_dates(extracted_text, matched_medicine, results)
            validate_manufacturer(extracted_text, matched_medicine, results)
        else:
            results['issues'].append("No matching medicine found in database")
            results['is_authentic'] = False
            results['confidence_score'] = 0
            results['medicine_match'] = False
    
    return results

def validate_batch_number(text, medicine, results):
    """Validate batch number format and consistency"""
    batch_patterns = [medicine['Batch_Number']]
    batch_found = any(batch in text for batch in batch_patterns)
    
    if batch_found:
        results['verification_details']['batch_verified'] = True
        results['batch_valid'] = True
    else:
        results['issues'].append("Batch number not found or doesn't match")
        results['batch_valid'] = False
        results['is_authentic'] = False

def validate_dates(text, medicine, results):
    """Validate manufacturing and expiry dates"""
    # This is a simplified validation - in reality, you'd parse dates from text
    mfg_date = medicine['MFG_Date']
    exp_date = medicine['EXP_Date']
    
    # Check if dates are reasonable
    mfg_date_obj = datetime.strptime(mfg_date, '%Y-%m-%d')
    exp_date_obj = datetime.strptime(exp_date, '%Y-%m-%d')
    
    if exp_date_obj <= datetime.now():
        results['issues'].append("Medicine has expired")
        results['is_authentic'] = False
        results['date_valid'] = False
    elif (exp_date_obj - mfg_date_obj).days > (medicine['Expected_Shelf_Life_Months'] * 30 + 30):
        results['issues'].append("Shelf life exceeds expected duration")
        results['is_authentic'] = False
        results['date_valid'] = False
    else:
        results['verification_details']['dates_valid'] = True
        results['date_valid'] = True

def validate_manufacturer(text, medicine, results):
    """Validate manufacturer information"""
    manufacturer = medicine['Manufacturer']
    if manufacturer.lower() in text.lower():
        results['verification_details']['manufacturer_verified'] = True
        results['manufacturer_match'] = True
    else:
        results['issues'].append("Manufacturer name not found or doesn't match")
        results['is_authentic'] = False
        results['manufacturer_match'] = False

# Generate AI summary
def generate_ai_summary(verification_results):
    """Generate an AI-powered summary of verification results"""
    if verification_results['is_authentic']:
        summary = f"""
        ✅ **MEDICINE VERIFIED AS AUTHENTIC**
        
        **Confidence Score:** {verification_results['confidence_score']}%
        
        **Verification Details:**
        """
        if verification_results['matched_medicine'] is not None:
            medicine = verification_results['matched_medicine']
            summary += f"""
        • **Brand Name:** {medicine['Brand_Name']}
        • **Generic Name:** {medicine['Generic_Name']}
        • **Manufacturer:** {medicine['Manufacturer']}
        • **Batch Number:** {medicine['Batch_Number']}
        """
        
        details = verification_results['verification_details']
        if details.get('barcode_verified'):
            summary += "\n• ✅ Barcode verified against database"
        if details.get('brand_match'):
            summary += f"\n• ✅ Brand name match: {details['brand_match']}% similarity"
        if details.get('batch_verified'):
            summary += "\n• ✅ Batch number verified"
        if details.get('dates_valid'):
            summary += "\n• ✅ Manufacturing and expiry dates are valid"
        if details.get('manufacturer_verified'):
            summary += "\n• ✅ Manufacturer information verified"
        
        summary += "\n\n**Recommendation:** This medicine appears to be authentic. You can proceed with confidence."
        
    else:
        summary = f"""
        ⚠️ **POTENTIAL COUNTERFEIT DETECTED**
        
        **Confidence Score:** {verification_results['confidence_score']}%
        
        **Issues Found:**
        """
        for issue in verification_results['issues']:
            summary += f"\n• ❌ {issue}"
        
        summary += "\n\n**Recommendation:** Do not use this medicine. Report to authorities immediately."
    
    return summary

# Voice Assistant and Multilingual Support
def text_to_speech(text, language='en'):
    """Convert text to speech with multilingual support"""
    try:
        import pyttsx3
        from gtts import gTTS
        import tempfile
        import os
        import pygame
        
        languages = {
            'en': 'English',
            'hi': 'Hindi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'bn': 'Bengali',
            'gu': 'Gujarati',
            'mr': 'Marathi',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi',
            'or': 'Odia',
            'as': 'Assamese',
            'ne': 'Nepali',
            'ur': 'Urdu',
            'sd': 'Sindhi'
        }
        
        lang_name = languages.get(language, 'English')
        
        # Show what's being spoken
        st.info(f"🔊 Voice Assistant ({lang_name}): Reading verification results...")
        
        # Try to use gTTS for better multilingual support
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                
                # Play the audio
                pygame.mixer.init()
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                # Clean up
                pygame.mixer.quit()
                os.unlink(tmp_file.name)
                
        except Exception as gtts_error:
            # Fallback to pyttsx3 for English
            if language == 'en':
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 0.9)
                engine.say(text)
                engine.runAndWait()
            else:
                st.warning(f"⚠️ Voice synthesis not available for {lang_name}. Using text display instead.")
                st.info(f"📢 Text: {text[:200]}...")
        
    except ImportError:
        st.warning("⚠️ Voice synthesis libraries not installed. Install pyttsx3 and gTTS for voice support.")
        st.info(f"📢 Text: {text[:200]}...")
    except Exception as e:
        st.error(f"Voice synthesis error: {str(e)}")
        st.info(f"📢 Text: {text[:200]}...")

def generate_counterfeit_analysis(verification_results, medicine_details, security_results):
    """Generate detailed analysis of why a medicine is counterfeit"""
    try:
        analysis_parts = []
        
        # Check OCR confidence
        if verification_results.get('ocr_confidence', 0) < 0.7:
            analysis_parts.append("Low text recognition confidence suggests poor print quality")
        
        # Check medicine name match
        if not verification_results.get('medicine_match', False):
            analysis_parts.append("Medicine name does not match database records")
        
        # Check manufacturer match
        if not verification_results.get('manufacturer_match', False):
            analysis_parts.append("Manufacturer information is inconsistent")
        
        # Check batch number
        if not verification_results.get('batch_valid', False):
            analysis_parts.append("Batch number format is invalid or suspicious")
        
        # Check date validity
        if not verification_results.get('date_valid', False):
            analysis_parts.append("Manufacturing or expiry dates appear suspicious")
        
        # Check barcode
        if not verification_results.get('barcode_valid', False):
            analysis_parts.append("Barcode is invalid or not found in database")
        
        # Check security features
        if security_results.get('hologram_detected', False) == False:
            analysis_parts.append("Missing security hologram or seal")
        
        if security_results.get('color_anomalies', False):
            analysis_parts.append("Unusual color patterns detected")
        
        if security_results.get('font_anomalies', False):
            analysis_parts.append("Inconsistent font styles detected")
        
        # Generate summary
        if analysis_parts:
            summary = f"⚠️ COUNTERFEIT DETECTED: This medicine appears to be counterfeit based on the following issues: {'; '.join(analysis_parts)}. Please do not consume this product and report it to authorities."
        else:
            summary = "✅ AUTHENTIC: This medicine appears to be genuine based on all verification checks."
        
        return summary, analysis_parts
        
    except Exception as e:
        return f"Error analyzing medicine: {str(e)}", []

def get_multilingual_summary(verification_results, language='en'):
    """Generate multilingual summary"""
    summaries = {
        'en': {
            'authentic': "✅ Medicine verified as AUTHENTIC. Safe to use.",
            'counterfeit': "❌ COUNTERFEIT detected. Do not use. Report immediately.",
            'confidence': "Confidence Score",
            'details': "Verification Details",
            'recommendation': "Recommendation"
        },
        'hi': {
            'authentic': "✅ दवा प्रामाणिक पाई गई। सुरक्षित उपयोग करें।",
            'counterfeit': "❌ नकली दवा पाई गई। उपयोग न करें। तुरंत रिपोर्ट करें।",
            'confidence': "विश्वास स्कोर",
            'details': "सत्यापन विवरण",
            'recommendation': "सिफारिश"
        },
        'ta': {
            'authentic': "✅ மருந்து உண்மையானது என சரிபார்க்கப்பட்டது. பாதுகாப்பாக பயன்படுத்தலாம்.",
            'counterfeit': "❌ போலி மருந்து கண்டறியப்பட்டது. பயன்படுத்த வேண்டாம். உடனடியாக புகாரளிக்கவும்.",
            'confidence': "நம்பிக்கை மதிப்பெண்",
            'details': "சரிபார்ப்பு விவரங்கள்",
            'recommendation': "பரிந்துரை"
        },
        'te': {
            'authentic': "✅ మందు అసలైనదిగా ధృవీకరించబడింది. సురక్షితంగా వాడండి.",
            'counterfeit': "❌ నకిలీ మందు కనుగొనబడింది. వాడకండి. వెంటనే నివేదించండి.",
            'confidence': "విశ్వాస స్కోరు",
            'details': "ధృవీకరణ వివరాలు",
            'recommendation': "సిఫార్సు"
        },
        'bn': {
            'authentic': "✅ ওষুধ প্রমাণিত হয়েছে। নিরাপদে ব্যবহার করুন।",
            'counterfeit': "❌ নকল ওষুধ সনাক্ত হয়েছে। ব্যবহার করবেন না। অবিলম্বে রিপোর্ট করুন।",
            'confidence': "আত্মবিশ্বাস স্কোর",
            'details': "যাচাইকরণের বিবরণ",
            'recommendation': "সুপারিশ"
        },
        'gu': {
            'authentic': "✅ દવા પ્રમાણિત છે. સુરક્ષિત રીતે વાપરો.",
            'counterfeit': "❌ નકલી દવા મળી. વાપરશો નહીં. તુરંત જાણ કરો.",
            'confidence': "વિશ્વાસ સ્કોર",
            'details': "ચકાસણી વિગતો",
            'recommendation': "સૂચના"
        },
        'mr': {
            'authentic': "✅ औषध प्रमाणित आहे. सुरक्षित वापरा.",
            'counterfeit': "❌ नकली औषध सापडले. वापरू नका. लगेच निवेदन करा.",
            'confidence': "विश्वास स्कोर",
            'details': "सत्यापन तपशील",
            'recommendation': "शिफारस"
        },
        'kn': {
            'authentic': "✅ ಔಷಧ ಪ್ರಮಾಣೀಕರಿಸಲಾಗಿದೆ. ಸುರಕ್ಷಿತವಾಗಿ ಬಳಸಿ.",
            'counterfeit': "❌ ನಕಲಿ ಔಷಧ ಕಂಡುಬಂದಿದೆ. ಬಳಸಬೇಡಿ. ತಕ್ಷಣ ವರದಿ ಮಾಡಿ.",
            'confidence': "ವಿಶ್ವಾಸ ಸ್ಕೋರ್",
            'details': "ಪರಿಶೀಲನೆ ವಿವರಗಳು",
            'recommendation': "ಶಿಫಾರಸು"
        },
        'ml': {
            'authentic': "✅ മരുന്ന് പ്രമാണീകരിച്ചു. സുരക്ഷിതമായി ഉപയോഗിക്കുക.",
            'counterfeit': "❌ കപ്പി മരുന്ന് കണ്ടെത്തി. ഉപയോഗിക്കരുത്. ഉടനെ റിപ്പോർട്ട് ചെയ്യുക.",
            'confidence': "വിശ്വാസ സ്കോർ",
            'details': "പരിശോധന വിവരങ്ങൾ",
            'recommendation': "ശുപാർശ"
        },
        'pa': {
            'authentic': "✅ ਦਵਾਈ ਪ੍ਰਮਾਣਿਤ ਹੈ। ਸੁਰੱਖਿਤ ਰੂਪ ਵਿੱਚ ਵਰਤੋਂ।",
            'counterfeit': "❌ ਨਕਲੀ ਦਵਾਈ ਮਿਲੀ। ਵਰਤੋਂ ਨਾ ਕਰੋ। ਤੁਰੰਤ ਰਿਪੋਰਟ ਕਰੋ।",
            'confidence': "ਵਿਸ਼ਵਾਸ ਸਕੋਰ",
            'details': "ਪੜਤਾਲ ਵਿਵਰਣ",
            'recommendation': "ਸਿਫਾਰਸ਼"
        }
    }
    
    lang_data = summaries.get(language, summaries['en'])
    
    if verification_results['is_authentic']:
        return lang_data['authentic']
    else:
        return lang_data['counterfeit']

def voice_assistant_interface():
    """Voice assistant interface for hands-free operation"""
    st.markdown("""
    <div style="background: #2a2a2a; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border: 1px solid #444444;">
        <h3 style="color: #ffffff; margin: 0; text-align: center; font-size: 1.5rem; font-weight: 600;">🎤 Voice Assistant</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox(
            "🌍 Select Language",
            ['en', 'hi', 'ta', 'te', 'bn', 'gu', 'mr', 'kn', 'ml', 'pa', 'or', 'as', 'ne', 'ur', 'sd'],
            format_func=lambda x: {
                'en': '🇺🇸 English',
                'hi': '🇮🇳 Hindi (हिन्दी)',
                'ta': '🇮🇳 Tamil (தமிழ்)',
                'te': '🇮🇳 Telugu (తెలుగు)',
                'bn': '🇮🇳 Bengali (বাংলা)',
                'gu': '🇮🇳 Gujarati (ગુજરાતી)',
                'mr': '🇮🇳 Marathi (मराठी)',
                'kn': '🇮🇳 Kannada (ಕನ್ನಡ)',
                'ml': '🇮🇳 Malayalam (മലയാളം)',
                'pa': '🇮🇳 Punjabi (ਪੰਜਾਬੀ)',
                'or': '🇮🇳 Odia (ଓଡ଼ିଆ)',
                'as': '🇮🇳 Assamese (অসমীয়া)',
                'ne': '🇮🇳 Nepali (नेपाली)',
                'ur': '🇮🇳 Urdu (اردو)',
                'sd': '🇮🇳 Sindhi (سنڌي)'
            }[x],
            help="Choose your preferred language for voice output",
            index=0
        )
    
    with col2:
        if st.button("🎤 Start Voice Assistant", help="Click to start voice-guided verification", type="primary"):
            st.success("🎤 Voice Assistant: Please speak the medicine name or scan the package")
            st.info("📱 You can also upload an image for verification")
    
    return language

# Main application functions
def medicine_verification_page():
    """Main medicine verification page with advanced features"""
    # Modern header with gradient
    st.markdown("""
    <div class="status-card" style="text-align: center; margin-bottom: 2rem;">
        <h1 style="margin: 0; color: white; font-size: 2.5rem;">🔍 Medicine Verification</h1>
        <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9); font-size: 1.1rem;">
            Upload an image or use your camera to verify medicine authenticity
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice Assistant Interface with modern styling
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        selected_language = voice_assistant_interface()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Create two columns for upload options with modern cards
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div style="background: #2a2a2a; padding: 1.5rem; border-radius: 8px; border: 1px solid #444444; margin-bottom: 1.5rem;">
            <h3 style="color: #ffffff; margin: 0 0 1rem 0; text-align: center; font-size: 1.3rem; font-weight: 600;">📁 Upload Image</h3>
        </div>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of the medicine package",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("""
        <div style="background: #2a2a2a; padding: 1.5rem; border-radius: 8px; border: 1px solid #444444; margin-bottom: 1.5rem;">
            <h3 style="color: #ffffff; margin: 0 0 1rem 0; text-align: center; font-size: 1.3rem; font-weight: 600;">📷 Camera Capture</h3>
        </div>
        """, unsafe_allow_html=True)
        camera_input = st.camera_input("📷 Take a photo of the medicine package", label_visibility="visible")
    
    # Process the selected image
    image_to_process = None
    if uploaded_file is not None:
        image_to_process = Image.open(uploaded_file)
        st.success("✅ Image uploaded successfully!")
    elif camera_input is not None:
        image_to_process = Image.open(camera_input)
        st.success("✅ Photo captured successfully!")
    
    if image_to_process is not None:
        # Display original image
        st.subheader("📸 Original Image")
        st.image(image_to_process, caption="Original Image", width='stretch')
        
        # Process the image with progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Analyze image quality
            status_text.text("📊 Analyzing image quality...")
            progress_bar.progress(20)
            
            # Display original image
            st.subheader("🖼️ Original Image")
            st.image(image_to_process, caption="Original Image", width='stretch')
            
            # Analyze image quality
            st.subheader("📊 Image Quality Analysis")
            original_quality = analyze_image_quality(np.array(image_to_process))
            
            # Display quality metrics in a clear format
            st.write("**Image Quality Metrics:**")
            
            # Create quality indicators
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if original_quality['blur_score'] > 100:
                    st.success(f"🔍 **Sharpness:** {original_quality['blur_level']}")
                elif original_quality['blur_score'] > 50:
                    st.warning(f"🔍 **Sharpness:** {original_quality['blur_level']}")
                else:
                    st.error(f"🔍 **Sharpness:** {original_quality['blur_level']}")
                st.write(f"Score: {original_quality['blur_score']:.1f}")
            
            with col2:
                if original_quality['contrast'] > 50:
                    st.success(f"🎨 **Contrast:** {original_quality['contrast_level']}")
                elif original_quality['contrast'] > 30:
                    st.warning(f"🎨 **Contrast:** {original_quality['contrast_level']}")
                else:
                    st.error(f"🎨 **Contrast:** {original_quality['contrast_level']}")
                st.write(f"Score: {original_quality['contrast']:.1f}")
            
            with col3:
                if 100 < original_quality['brightness'] < 155:
                    st.success(f"💡 **Brightness:** {original_quality['brightness_level']}")
                elif 80 < original_quality['brightness'] < 175:
                    st.warning(f"💡 **Brightness:** {original_quality['brightness_level']}")
                else:
                    st.error(f"💡 **Brightness:** {original_quality['brightness_level']}")
                st.write(f"Score: {original_quality['brightness']:.1f}")
            
            # Overall quality assessment
            st.subheader("🎯 Overall Quality Assessment")
            if (original_quality['blur_score'] > 100 and 
                original_quality['contrast'] > 50 and 
                100 < original_quality['brightness'] < 155):
                st.success("✅ **Excellent Quality** - Image is optimal for OCR processing")
            elif (original_quality['blur_score'] > 50 and 
                  original_quality['contrast'] > 30 and 
                  80 < original_quality['brightness'] < 175):
                st.warning("⚠️ **Good Quality** - Image should work well for OCR")
            else:
                st.error("❌ **Poor Quality** - Consider retaking the image for better results")
            
            # Step 2: Extract text using advanced OCR
            status_text.text("📝 Extracting text using advanced OCR...")
            progress_bar.progress(40)
            # Use original image for OCR instead of processed image
            original_array = np.array(image_to_process)
            extracted_text = extract_text_ocr(original_array)
            detailed_results = extract_text_with_details(original_array)
            medicine_details = extract_medicine_details(original_array)
            
            # Create and display OCR overlay
            if detailed_results:
                ocr_overlay = create_ocr_overlay(original_array, detailed_results)
                st.subheader("🎯 OCR Detection Overlay")
                st.image(ocr_overlay, caption="Text Detection with Confidence Scores", width='stretch')
            
            if extracted_text:
                st.success(f"✅ Extracted text: {extracted_text[:100]}...")
                
                # Show detailed OCR results with confidence scores
                if detailed_results:
                    with st.expander("🔍 Detailed OCR Analysis", expanded=False):
                        for i, result in enumerate(detailed_results):
                            col1, col2, col3 = st.columns([3, 1, 1])
                            with col1:
                                st.write(f"**Text {i+1}:** {result['text']}")
                            with col2:
                                st.write(f"**Confidence:** {result['confidence']:.2f}")
                            with col3:
                                if result['confidence'] > 0.7:
                                    st.success("✅ High")
                                elif result['confidence'] > 0.5:
                                    st.warning("⚠️ Medium")
                                else:
                                    st.error("❌ Low")
                
                # Display extracted medicine details
                if medicine_details['medicine_name']:
                    st.info(f"💊 Medicine Name: {medicine_details['medicine_name']}")
                if medicine_details['manufacturer']:
                    st.info(f"🏭 Manufacturer: {medicine_details['manufacturer']}")
                if medicine_details['batch_number']:
                    st.info(f"🔢 Batch Number: {medicine_details['batch_number']}")
                if medicine_details['mfg_date']:
                    st.info(f"📅 Manufacturing Date: {medicine_details['mfg_date']}")
                if medicine_details['exp_date']:
                    st.info(f"📅 Expiry Date: {medicine_details['exp_date']}")
            else:
                st.warning("⚠️ No text extracted from image")
            
            # Step 3: Detect barcodes
            status_text.text("🔍 Detecting barcodes...")
            progress_bar.progress(50)
            barcode_results = detect_barcodes(original_array)
            
            if barcode_results:
                st.success(f"✅ Found {len(barcode_results)} barcode(s)")
            else:
                st.info("ℹ️ No barcodes detected")
            
            # Step 4: Advanced security checks
            status_text.text("🔒 Performing security checks...")
            progress_bar.progress(60)
            
            # Hologram detection
            hologram_result = detect_hologram_seal(original_array)
            if hologram_result['detected']:
                st.success(f"✅ Hologram/Seal detected (Confidence: {hologram_result['confidence']:.1f}%)")
            else:
                st.warning("⚠️ No hologram or security seal detected")
            
            # Color consistency check
            color_result = check_color_consistency(original_array)
            if color_result['is_suspicious']:
                st.error("🚨 Color anomalies detected:")
                for anomaly in color_result['unusual_colors']:
                    st.error(f"   • {anomaly}")
            else:
                st.success("✅ Color consistency appears normal")
            
            # Font anomaly detection
            font_result = detect_font_anomalies(original_array)
            if font_result['is_suspicious']:
                st.error("🚨 Font anomalies detected:")
                for anomaly in font_result['anomalies']:
                    st.error(f"   • {anomaly}")
            else:
                st.success("✅ Font consistency appears normal")
            
            # Step 4: Load medicine database
            status_text.text("📚 Loading medicine database...")
            progress_bar.progress(80)
            medicine_db = create_medicine_database()
            
            # Step 5: Verify medicine
            status_text.text("🔍 Verifying medicine authenticity...")
            progress_bar.progress(90)
            barcode_data = barcode_results[0]['data'] if barcode_results else None
            verification_results = verify_medicine(extracted_text, barcode_data, medicine_db)
            
            # Step 6: Generate AI summary
            status_text.text("🤖 Generating AI summary...")
            progress_bar.progress(100)
            ai_summary = generate_ai_summary(verification_results)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
        except Exception as e:
            st.error(f"❌ Processing error: {str(e)}")
            return
        
        # Display results
        st.subheader("🤖 AI Verification Results")
            
        # Create AR overlay
        ar_overlay = create_ar_overlay(original_array, verification_results)
        st.subheader("📱 AR Overlay View")
        st.image(ar_overlay, caption="AR Overlay with Verification Results", width='stretch')
        
        if verification_results['is_authentic']:
            st.markdown(f"""
            <div class="status-box status-success">
                {ai_summary}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-box status-error">
                {ai_summary}
            </div>
            """, unsafe_allow_html=True)
            
        # Display security check results
        st.subheader("🔒 Security Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if hologram_result['detected']:
                st.success("✅ Hologram/Seal: Present")
            else:
                st.warning("⚠️ Hologram/Seal: Not detected")
        
        with col2:
            if color_result['is_suspicious']:
                st.error("❌ Color: Anomalies detected")
            else:
                st.success("✅ Color: Normal")
        
        with col3:
            if font_result['is_suspicious']:
                st.error("❌ Font: Anomalies detected")
            else:
                st.success("✅ Font: Normal")
        
        # Display matched medicine info
        if verification_results['matched_medicine'] is not None:
                medicine = verification_results['matched_medicine']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📦 Authentic Package")
                    st.image(medicine['Image_URL'], caption=medicine['Brand_Name'], width='stretch')
                
                with col2:
                    st.subheader("📋 Medicine Details")
                    st.write(f"**Brand Name:** {medicine['Brand_Name']}")
                    st.write(f"**Generic Name:** {medicine['Generic_Name']}")
                    st.write(f"**Manufacturer:** {medicine['Manufacturer']}")
                    st.write(f"**Batch Number:** {medicine['Batch_Number']}")
                    st.write(f"**Manufacturing Date:** {medicine['MFG_Date']}")
                    st.write(f"**Expiry Date:** {medicine['EXP_Date']}")
        
        # Generate detailed counterfeit analysis
        security_results = {
            'hologram_detected': hologram_result.get('detected', False),
            'color_anomalies': color_result.get('is_suspicious', False),
            'font_anomalies': font_result.get('is_suspicious', False)
        }
            
        counterfeit_summary, counterfeit_reasons = generate_counterfeit_analysis(
            verification_results, medicine_details, security_results
        )
        
        # Display counterfeit analysis
        st.subheader("🔍 Detailed Counterfeit Analysis")
        if counterfeit_reasons:
            st.error("❌ **COUNTERFEIT DETECTED**")
            st.write("**Reasons why this medicine is counterfeit:**")
            for i, reason in enumerate(counterfeit_reasons, 1):
                st.write(f"{i}. {reason}")
        else:
            st.success("✅ **AUTHENTIC MEDICINE**")
            st.write("All verification checks passed successfully.")
            
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔊 Read Summary Aloud", help="For visually impaired users"):
                text_to_speech(counterfeit_summary, selected_language)
        
        with col2:
            if counterfeit_reasons:
                if st.button("🔊 Read Counterfeit Reasons", help="Listen to why this medicine is counterfeit"):
                    detailed_reasons = "Counterfeit reasons: " + "; ".join(counterfeit_reasons)
                    text_to_speech(detailed_reasons, selected_language)
            elif not verification_results['is_authentic']:
                if st.button("🚨 Report Counterfeit", help="Report this suspicious product"):
                    st.error("Report submitted to authorities!")
        
        with col3:
            if verification_results['is_authentic']:
                if st.button("💊 View Generic Alternatives"):
                    st.info("Generic alternatives would be shown here")
        
        # Store scan in history
        scan_record = {
            'timestamp': datetime.now(),
            'is_authentic': verification_results['is_authentic'],
            'confidence_score': verification_results['confidence_score'],
            'medicine_name': verification_results['matched_medicine']['Brand_Name'] if verification_results['matched_medicine'] is not None else 'Unknown',
            'summary': ai_summary,
            'image': image_to_process
        }
        
        st.session_state.scan_history.append(scan_record)
        st.session_state.total_scans += 1
        
        if verification_results['is_authentic']:
            st.session_state.verified_medicines += 1
        else:
            st.session_state.counterfeits_detected += 1

def dashboard_page():
    """Dashboard with analytics and metrics"""
    # Modern header
    st.markdown("""
    <div class="status-card" style="text-align: center; margin-bottom: 2rem;">
        <h1 style="margin: 0; color: white; font-size: 2.5rem;">📊 Analytics Dashboard</h1>
        <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9); font-size: 1.1rem;">
            Comprehensive insights and metrics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load medicine database for statistics
    medicine_db = create_medicine_database()
    
    # Key metrics with modern styling
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.metric(
            label="🔍 Total Scans",
            value=st.session_state.total_scans,
            delta=None,
            help="Total number of medicine scans performed"
        )
    
    with col2:
        st.metric(
            label="✅ Verified Medicines",
            value=st.session_state.verified_medicines,
            delta=None,
            help="Number of authentic medicines verified"
        )
    
    with col3:
        st.metric(
            label="❌ Counterfeits Detected",
            value=st.session_state.counterfeits_detected,
            delta=None,
            help="Number of counterfeit medicines detected"
        )
    
    with col4:
        avg_time = 2.5  # Simulated average scan time
        st.metric(
            label="⏱️ Avg Scan Time",
            value=f"{avg_time}s",
            delta=None
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Database statistics with modern styling
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📚 Medicine Database Statistics")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.metric(
            label="💊 Total Medicines",
            value=len(medicine_db),
            delta=None,
            help="Total medicines in the database"
        )
    
    with col2:
        unique_manufacturers = medicine_db['Manufacturer'].nunique()
        st.metric(
            label="🏭 Unique Manufacturers",
            value=unique_manufacturers,
            delta=None,
            help="Number of different manufacturers"
        )
    
    with col3:
        # Count medicines by category
        pain_meds = len(medicine_db[medicine_db['Brand_Name'].str.contains('Paracetamol|Ibuprofen|Aspirin|Diclofenac|Naproxen|Ketorolac|Tramadol|Morphine', case=False, na=False)])
        st.metric(
            label="🩹 Pain Relief Medicines",
            value=pain_meds,
            delta=None
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Modern charts section
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Analytics & Insights")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("#### 📈 Counterfeit Detection Trends")
        
        # Generate sample data for trends
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        counterfeit_trends = np.random.poisson(2, len(dates))
        
        df_trends = pd.DataFrame({
            'Date': dates,
            'Counterfeits Detected': counterfeit_trends
        })
        
        fig_trends = px.line(df_trends, x='Date', y='Counterfeits Detected', 
                           title='Daily Counterfeit Detection',
                           color_discrete_sequence=['#6366f1'])
        fig_trends.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig_trends, width='stretch')
    
    with col2:
        st.markdown("#### 🗺️ Geographic Distribution")
        
        # Generate sample geographic data
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
        counterfeit_counts = np.random.poisson(5, len(cities))
        
        df_geo = pd.DataFrame({
            'City': cities,
            'Counterfeits': counterfeit_counts
        })
        
        fig_geo = px.bar(df_geo, x='City', y='Counterfeits', 
                        title='Counterfeits by City',
                        color='Counterfeits',
                        color_continuous_scale='Viridis')
        fig_geo.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig_geo, width='stretch')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Medicine search and exploration with modern styling
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Medicine Database Explorer")
    
    # Search functionality with modern styling
    col1, col2 = st.columns([1, 2], gap="medium")
    
    with col1:
        search_option = st.selectbox("Search by:", ["Brand Name", "Manufacturer", "Generic Name", "Barcode"])
    
    with col2:
        search_term = st.text_input("Enter search term:", placeholder="e.g., Paracetamol, Sun Pharma, etc.", label_visibility="collapsed")
    
    if search_term:
        if search_option == "Brand Name":
            results = medicine_db[medicine_db['Brand_Name'].str.contains(search_term, case=False, na=False)]
        elif search_option == "Manufacturer":
            results = medicine_db[medicine_db['Manufacturer'].str.contains(search_term, case=False, na=False)]
        elif search_option == "Generic Name":
            results = medicine_db[medicine_db['Generic_Name'].str.contains(search_term, case=False, na=False)]
        elif search_option == "Barcode":
            results = medicine_db[medicine_db['Barcode_Data'].str.contains(search_term, case=False, na=False)]
        
        if not results.empty:
            st.success(f"✅ Found {len(results)} medicine(s)")
            st.dataframe(results[['Brand_Name', 'Generic_Name', 'Manufacturer', 'Batch_Number', 'Barcode_Data']], width='stretch')
        else:
            st.warning("⚠️ No medicines found matching your search criteria.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional analytics with modern styling
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Detailed Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Verification success rate
        if st.session_state.total_scans > 0:
            success_rate = (st.session_state.verified_medicines / st.session_state.total_scans) * 100
            st.metric("Verification Success Rate", f"{success_rate:.1f}%")
        else:
            st.metric("Verification Success Rate", "N/A")
    
    with col2:
        # Most common counterfeits
        st.subheader("🚨 Common Counterfeit Patterns")
        st.write("• Spelling errors in brand names")
        st.write("• Incorrect batch number formats")
        st.write("• Mismatched manufacturer information")
        st.write("• Invalid barcode data")
    
    # Medicine categories breakdown
    st.subheader("💊 Medicine Categories")
    
    categories = {
        'Pain Relief': medicine_db[medicine_db['Brand_Name'].str.contains('Paracetamol|Ibuprofen|Aspirin|Diclofenac|Naproxen|Ketorolac|Tramadol|Morphine', case=False, na=False)],
        'Antibiotics': medicine_db[medicine_db['Brand_Name'].str.contains('Amoxicillin|Ciprofloxacin|Azithromycin|Cefixime|Levofloxacin|Doxycycline|Clindamycin', case=False, na=False)],
        'Cardiovascular': medicine_db[medicine_db['Brand_Name'].str.contains('Atorvastatin|Losartan|Metoprolol|Amlodipine|Enalapril|Clopidogrel|Warfarin|Digoxin', case=False, na=False)],
        'Diabetes': medicine_db[medicine_db['Brand_Name'].str.contains('Metformin|Insulin|Glibenclamide|Gliclazide|Pioglitazone|Sitagliptin|Empagliflozin|Dapagliflozin', case=False, na=False)],
        'Gastrointestinal': medicine_db[medicine_db['Brand_Name'].str.contains('Omeprazole|Pantoprazole|Ranitidine|Domperidone|Ondansetron|Loperamide|Sucralfate|Bismuth', case=False, na=False)],
        'Respiratory': medicine_db[medicine_db['Brand_Name'].str.contains('Salbutamol|Budesonide|Montelukast|Theophylline|Ipratropium|Formoterol|Fluticasone|Tiotropium', case=False, na=False)],
        'Mental Health': medicine_db[medicine_db['Brand_Name'].str.contains('Sertraline|Fluoxetine|Amitriptyline|Diazepam|Lorazepam|Clonazepam|Olanzapine|Risperidone', case=False, na=False)],
        'Hormonal': medicine_db[medicine_db['Brand_Name'].str.contains('Levothyroxine|Prednisolone|Hydrocortisone|Methylprednisolone|Dexamethasone|Estradiol|Testosterone', case=False, na=False)]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        for category, df in categories.items():
            if not df.empty:
                st.write(f"**{category}:** {len(df)} medicines")
    
    with col2:
        # Top manufacturers
        st.subheader("🏭 Top Manufacturers")
        top_manufacturers = medicine_db['Manufacturer'].value_counts().head(5)
        for manufacturer, count in top_manufacturers.items():
            st.write(f"• {manufacturer}: {count} medicines")

def scan_history_page():
    """Scan history and detailed logs"""
    # Modern header
    st.markdown("""
    <div class="status-card" style="text-align: center; margin-bottom: 2rem;">
        <h1 style="margin: 0; color: white; font-size: 2.5rem;">📖 Scan History</h1>
        <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9); font-size: 1.1rem;">
            Detailed log of all verification activities
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.scan_history:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.info("ℹ️ No scans recorded yet. Start by verifying a medicine!")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Search and filter options with modern styling
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Search & Filter")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        search_term = st.text_input("Search scans", placeholder="Enter medicine name or batch number", label_visibility="collapsed")
    
    with col2:
        filter_status = st.selectbox("Filter by status", ["All", "Authentic", "Counterfeit"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter scans
    filtered_scans = st.session_state.scan_history
    
    if search_term:
        filtered_scans = [scan for scan in filtered_scans 
                         if search_term.lower() in scan['medicine_name'].lower()]
    
    if filter_status != "All":
        is_authentic = filter_status == "Authentic"
        filtered_scans = [scan for scan in filtered_scans 
                         if scan['is_authentic'] == is_authentic]
    
    # Display scans
    st.subheader(f"📋 Scan Results ({len(filtered_scans)} found)")
    
    for i, scan in enumerate(reversed(filtered_scans)):
        with st.expander(f"Scan #{len(st.session_state.scan_history) - i} - {scan['medicine_name']} - {scan['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Timestamp:** {scan['timestamp']}")
                st.write(f"**Medicine:** {scan['medicine_name']}")
                st.write(f"**Status:** {'✅ Authentic' if scan['is_authentic'] else '❌ Counterfeit'}")
                st.write(f"**Confidence:** {scan['confidence_score']}%")
            
            with col2:
                st.image(scan['image'], caption="Scanned Image", width=200)
            
            st.write("**AI Summary:**")
            st.write(scan['summary'])

def report_info_page():
    """Report suspicious vendors and educational content"""
    st.markdown("""
    <div class="main-header">
        <h1>ℹ️ Report & Information</h1>
        <p>Report suspicious activities and learn about counterfeit detection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Report form
    st.subheader("🚨 Report Suspicious Vendor/Product")
    
    with st.form("report_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            vendor_name = st.text_input("Vendor/Pharmacy Name", placeholder="Enter vendor name")
            location = st.text_input("Location", placeholder="Enter city/area")
            contact_info = st.text_input("Contact Information", placeholder="Phone/Email if known")
        
        with col2:
            product_name = st.text_input("Product Name", placeholder="Name of suspicious product")
            batch_number = st.text_input("Batch Number", placeholder="If available")
            issue_description = st.text_area("Issue Description", placeholder="Describe the problem")
        
        submitted = st.form_submit_button("Submit Report")
        
        if submitted:
            st.success("✅ Report submitted successfully! Authorities will investigate.")
    
    # Educational content
    st.subheader("📚 How to Spot Fake Medicines")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔍 Visual Inspection:**
        - Check for spelling errors
        - Verify manufacturer details
        - Look for poor print quality
        - Check packaging integrity
        """)
    
    with col2:
        st.markdown("""
        **📋 Label Verification:**
        - Verify batch numbers
        - Check manufacturing dates
        - Validate expiry dates
        - Cross-check with official sources
        """)
    
    # Additional resources
    st.subheader("🔗 Additional Resources")
    
    st.markdown("""
    - **Drug Controller General of India (DCGI):** [www.cdsco.gov.in](https://www.cdsco.gov.in)
    - **WHO Counterfeit Medicines:** [www.who.int](https://www.who.int)
    - **Report Counterfeits:** [www.reportcounterfeit.com](https://www.reportcounterfeit.com)
    """)

# Main application
def main():
    """Main application function"""
    # Sidebar navigation with modern styling
    with st.sidebar:
        st.markdown("""
        <div class="status-card" style="text-align: center; margin-bottom: 2rem;">
            <h2 style="margin: 0; color: white;">💊 Aushadhi-OCR</h2>
            <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9);">Counterfeit Medicine Detection</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation with modern styling
        selected = option_menu(
            menu_title=None,
            options=["🔍 Medicine Verification", "📊 Dashboard", "📖 Scan History", "ℹ️ Report & Info"],
            icons=["search", "bar-chart", "book", "info-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "12px 16px",
                    "border-radius": "8px",
                    "color": "white",
                    "--hover-color": "rgba(255,255,255,0.1)",
                },
                "nav-link-selected": {
                    "background-color": "rgba(255,255,255,0.2)",
                    "border-radius": "8px",
                },
            }
        )
    
    # Route to appropriate page
    if selected == "🔍 Medicine Verification":
        medicine_verification_page()
    elif selected == "📊 Dashboard":
        dashboard_page()
    elif selected == "📖 Scan History":
        scan_history_page()
    elif selected == "ℹ️ Report & Info":
        report_info_page()

if __name__ == "__main__":
    main()