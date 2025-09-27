#!/bin/bash

# Set the zbar library path for macOS
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/zbar/lib:$DYLD_LIBRARY_PATH"

# Activate virtual environment
source aushadhi_env/bin/activate

# Run the Streamlit application
streamlit run aushadhi_ocr.py
