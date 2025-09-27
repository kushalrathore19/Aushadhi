# 🚀 Deployment Guide for Aushadhi-OCR

## Quick Deployment Options

### Option 1: Streamlit Community Cloud (FREE - Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/aushadhi-ocr.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `aushadhi_ocr.py`
   - Click "Deploy"

### Option 2: Railway (PAID - Production Ready)

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables** (if needed):
   ```bash
   railway variables set PORT=8501
   ```

### Option 3: Render (FREE Tier Available)

1. **Connect GitHub Repository**:
   - Go to [render.com](https://render.com)
   - Connect your GitHub account
   - Select your repository

2. **Configure Service**:
   - Service Type: Web Service
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run aushadhi_ocr.py --server.port=$PORT --server.address=0.0.0.0`

### Option 4: Heroku (PAID)

1. **Install Heroku CLI**:
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Deploy**:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

## Important Notes

### Dependencies
- Your app uses several heavy libraries (OpenCV, EasyOCR, PyTesseract)
- Some platforms may have size limits
- Consider using lighter alternatives for production

### Environment Variables
You may need to set these environment variables:
- `PORT`: Server port (usually set automatically)
- `PYTHONPATH`: Python path for imports

### File Structure
Make sure these files are in your repository root:
- `aushadhi_ocr.py` (main app)
- `medicine_database.py` (database module)
- `requirements.txt` (dependencies)
- `Procfile` (for Heroku/Railway)
- `.streamlit/config.toml` (Streamlit config)

### Troubleshooting

1. **Import Errors**: Make sure all dependencies are in requirements.txt
2. **Port Issues**: Use `$PORT` environment variable
3. **Memory Issues**: Consider upgrading to paid tiers for heavy ML libraries
4. **Build Timeouts**: Some platforms have build time limits

## Recommended for Your App

**For Quick Testing**: Streamlit Community Cloud
**For Production**: Railway or Render
**For Enterprise**: AWS/GCP with Docker

## Next Steps

1. Choose your preferred platform
2. Push your code to GitHub
3. Follow the deployment steps above
4. Test your deployed app
5. Set up custom domain (if needed)

## Support

If you encounter issues:
1. Check platform-specific documentation
2. Review build logs
3. Test locally first
4. Consider platform limitations
