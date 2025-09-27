# Aushadhi-OCR: Counterfeit Medicine Detection

A Streamlit-based application for detecting counterfeit medicines using OCR and barcode scanning.

## Features

- 🔍 **Medicine Verification**: Upload images or use camera to verify medicine authenticity
- 📊 **Analytics Dashboard**: Comprehensive insights and metrics
- 📖 **Scan History**: Detailed log of all verification activities
- ℹ️ **Report & Information**: Report suspicious activities and educational content

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Homebrew** (for macOS users)

### Setup

1. **Clone or download the project**
   ```bash
   cd /path/to/your/project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv aushadhi_env
   source aushadhi_env/bin/activate  # On Windows: aushadhi_env\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install zbar library (macOS)**
   ```bash
   brew install zbar
   ```

## Running the Application

### Option 1: Using the startup script (Recommended)
```bash
./run_app.sh
```

### Option 2: Manual execution
```bash
# Set environment variable for zbar
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/zbar/lib:$DYLD_LIBRARY_PATH"

# Activate virtual environment
source aushadhi_env/bin/activate

# Run the application
streamlit run aushadhi_ocr.py
```

### Option 3: Direct execution (with fallback)
```bash
source aushadhi_env/bin/activate
streamlit run aushadhi_ocr.py
```

## Troubleshooting

### zbar Import Error

If you encounter the error `ImportError: Unable to find zbar shared library`:

1. **Install zbar via Homebrew**:
   ```bash
   brew install zbar
   ```

2. **Set the library path**:
   ```bash
   export DYLD_LIBRARY_PATH="/opt/homebrew/opt/zbar/lib:$DYLD_LIBRARY_PATH"
   ```

3. **Use the provided startup script**:
   ```bash
   chmod +x run_app.sh
   ./run_app.sh
   ```

### Alternative Solutions

- The application includes fallback handling for when zbar is not available
- Barcode detection will be disabled, but OCR-based verification will still work
- You'll see a warning message if barcode detection is unavailable

## Features Overview

### Medicine Verification
- Upload images or capture photos of medicine packages
- Automatic image enhancement and preprocessing
- OCR text extraction
- Barcode/QR code detection
- AI-powered verification against medicine database

### Analytics Dashboard
- Total scans, verified medicines, counterfeits detected
- Geographic distribution of counterfeit detection
- Verification success rates
- Common counterfeit patterns

### Scan History
- Search and filter scan results
- Detailed verification logs
- Image storage and retrieval

### Report & Information
- Report suspicious vendors/products
- Educational content on counterfeit detection
- Links to official resources

## Technical Details

- **OCR Engine**: Tesseract (pytesseract)
- **Barcode Detection**: pyzbar (requires zbar library)
- **Image Processing**: OpenCV
- **UI Framework**: Streamlit
- **Data Visualization**: Plotly

## Requirements

See `requirements.txt` for the complete list of Python dependencies.

## License

This project is for educational and research purposes.
