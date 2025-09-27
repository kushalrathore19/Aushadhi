#!/bin/bash

echo "🚀 Setting up Aushadhi-OCR for deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Aushadhi-OCR Medicine Verification App"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if all required files exist
echo "🔍 Checking deployment files..."

required_files=("aushadhi_ocr.py" "medicine_database.py" "requirements.txt" "Procfile" ".streamlit/config.toml")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file is missing"
    fi
done

echo ""
echo "🎯 Deployment Options:"
echo "1. Streamlit Community Cloud (FREE)"
echo "   - Push to GitHub and deploy at share.streamlit.io"
echo ""
echo "2. Railway (PAID - $5/month)"
echo "   - Run: railway login && railway up"
echo ""
echo "3. Render (FREE tier available)"
echo "   - Connect GitHub repo at render.com"
echo ""
echo "4. Heroku (PAID - $7/month)"
echo "   - Run: heroku create && git push heroku main"
echo ""

echo "📋 Next Steps:"
echo "1. Choose your deployment platform"
echo "2. Push to GitHub: git remote add origin <your-repo-url> && git push -u origin main"
echo "3. Follow the deployment guide in DEPLOYMENT_GUIDE.md"
echo ""

echo "🔧 To push to GitHub:"
echo "git remote add origin https://github.com/YOUR_USERNAME/aushadhi-ocr.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""

echo "✨ Setup complete! Your app is ready for deployment."
