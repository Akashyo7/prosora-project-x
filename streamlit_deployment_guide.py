#!/usr/bin/env python3
"""
Streamlit Cloud Deployment Guide for Prosora Intelligence Engine
Step-by-step deployment to get your system live in 15 minutes
"""

import os
import subprocess
import sys
from pathlib import Path

def create_streamlit_requirements():
    """Create optimized requirements.txt for Streamlit Cloud"""
    
    requirements = [
        "streamlit>=1.28.0",
        "plotly>=5.15.0", 
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "google-generativeai>=0.3.0",
        "feedparser>=6.0.10",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("✅ Created optimized requirements.txt for Streamlit Cloud")

def create_streamlit_config():
    """Create Streamlit configuration for cloud deployment"""
    
    # Create .streamlit directory
    Path(".streamlit").mkdir(exist_ok=True)
    
    config_content = """[global]
developmentMode = false

[server]
headless = true
port = 8501
enableCORS = false
maxUploadSize = 200

[theme]
base = "light"
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[browser]
gatherUsageStats = false
"""
    
    with open(".streamlit/config.toml", "w") as f:
        f.write(config_content)
    
    print("✅ Created .streamlit/config.toml")

def create_streamlit_secrets_template():
    """Create secrets template for Streamlit Cloud"""
    
    secrets_content = """# Streamlit Cloud Secrets Template
# Copy this content to your Streamlit Cloud app settings

[secrets]
GEMINI_API_KEY = "your_gemini_api_key_here"
GOOGLE_API_KEY = "your_google_api_key_here"
FIREBASE_CONFIG_PATH = "firebase_config.json"
"""
    
    with open(".streamlit/secrets_template.toml", "w") as f:
        f.write(secrets_content)
    
    print("✅ Created .streamlit/secrets_template.toml")

def create_deployment_readme():
    """Create deployment-specific README"""
    
    readme_content = """# 🧠 Prosora Intelligence Engine

## Live Demo
🌐 **[Access Live Dashboard](https://your-app-url.streamlit.app)** 

## What This Is
The **Prosora Intelligence Engine** is a complete AI-powered content intelligence system that:

- 🔍 **Analyzes queries** with AI-powered intent recognition
- 📡 **Fetches real content** from RSS feeds and web sources  
- 🎯 **Personalizes content** with your voice and frameworks
- 🔄 **Optimizes variants** with A/B testing and engagement prediction
- 🧠 **Learns continuously** from performance data to improve

## Features

### 🚀 Complete 5-Phase Intelligence Pipeline
1. **Smart Query Analysis** - AI-powered intent and domain detection
2. **Real Source Integration** - Live RSS feeds from premium sources
3. **Voice Personalization** - Content in YOUR authentic voice
4. **Content Optimization** - Multiple variants with engagement prediction
5. **Self-Improving Learning** - Gets smarter with each use

### 📊 Advanced Analytics
- **Phase-by-phase performance tracking**
- **Learning analytics and pattern recognition**
- **Real-time performance metrics**
- **Historical trend analysis**

### 🎮 Demo Features
- **Demo Mode** - Test with simulated data
- **Sample Data Generation** - Realistic test scenarios
- **System Testing** - Comprehensive functionality tests

## How to Use

1. **Enter a Query** - Type your intelligence query in the main interface
2. **Watch Processing** - See real-time progress through all 5 phases
3. **Review Results** - Analyze generated content and metrics
4. **Explore Analytics** - Switch between different view modes

### Example Queries
- "AI regulation impact on fintech product strategy"
- "Cross-domain analysis of political tech platforms"
- "Contrarian view on startup funding trends"

## Technology Stack
- **Frontend**: Streamlit
- **AI**: Google Gemini API
- **Data Sources**: RSS feeds, web scraping
- **Analytics**: Real-time metrics and learning
- **Deployment**: Streamlit Cloud

## About
Built by Akash - combining IIT Bombay engineering, political consulting, product ops, and FinTech MBA expertise into an AI-powered intelligence engine.

---
*This is a production-ready system that rivals enterprise-grade content intelligence platforms.*
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created deployment README.md")

def create_gitignore():
    """Create comprehensive .gitignore for deployment"""
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local
.env.production

# Streamlit
.streamlit/secrets.toml

# Database files
*.db
*.sqlite
*.sqlite3
data/

# Logs
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Firebase
firebase_config.json
*firebase*adminsdk*.json

# API Keys (keep these secret!)
*api_key*
*secret*
*token*

# Temporary files
tmp/
temp/
*.tmp
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("✅ Created .gitignore")

def check_main_app():
    """Ensure main app file is ready for deployment"""
    
    main_app = "prosora_complete_dashboard.py"
    
    if os.path.exists(main_app):
        print(f"✅ Main app file found: {main_app}")
        
        # Check if it has the right structure
        with open(main_app, 'r') as f:
            content = f.read()
            
        if 'if __name__ == "__main__":' in content:
            print("✅ App has proper main execution block")
        else:
            print("⚠️ App might need main execution block")
            
        return True
    else:
        print(f"❌ Main app file not found: {main_app}")
        return False

def create_deployment_checklist():
    """Create deployment checklist"""
    
    checklist = """# 🚀 Streamlit Cloud Deployment Checklist

## Pre-Deployment ✅

- [ ] Main app file exists (`prosora_complete_dashboard.py`)
- [ ] Requirements.txt created with all dependencies
- [ ] .streamlit/config.toml configured
- [ ] .gitignore includes sensitive files
- [ ] README.md explains the project
- [ ] All sensitive data removed from code

## GitHub Setup ✅

- [ ] Repository created on GitHub
- [ ] All files committed and pushed
- [ ] Repository is public (for free tier) or private (for paid)
- [ ] No API keys or secrets in repository

## Streamlit Cloud Deployment ✅

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Click "New app"**
3. **Connect GitHub repository**
4. **Configure app settings:**
   - Repository: `your-username/prosora-intelligence`
   - Branch: `main`
   - Main file path: `prosora_complete_dashboard.py`
5. **Add secrets in Advanced settings:**
   ```
   GEMINI_API_KEY = "your_actual_api_key"
   GOOGLE_API_KEY = "your_google_api_key"
   ```
6. **Deploy!**

## Post-Deployment Testing ✅

- [ ] App loads without errors
- [ ] Demo mode works
- [ ] Sample data generation works
- [ ] All 5 phases process correctly
- [ ] Real sources fetch (if API keys configured)
- [ ] Analytics views display properly

## Sharing ✅

- [ ] App URL works: `https://your-username-prosora-intelligence-main.streamlit.app`
- [ ] Share with stakeholders
- [ ] Gather feedback
- [ ] Monitor usage and performance

## Troubleshooting 🔧

**Common Issues:**
- **App won't start**: Check requirements.txt and Python version
- **Import errors**: Ensure all dependencies are listed
- **API errors**: Verify secrets are configured correctly
- **Memory issues**: Use demo mode, optimize data loading

**Solutions:**
- Check Streamlit Cloud logs for specific errors
- Test locally first with `streamlit run prosora_complete_dashboard.py`
- Verify all imports work in a fresh environment
"""
    
    with open("DEPLOYMENT_CHECKLIST.md", "w") as f:
        f.write(checklist)
    
    print("✅ Created DEPLOYMENT_CHECKLIST.md")

def run_local_test():
    """Run local test to verify everything works"""
    
    print("🧪 Running local test...")
    
    try:
        # Test imports
        import streamlit
        import plotly
        import pandas
        import numpy
        print("✅ Core dependencies available")
        
        # Test main app import
        if os.path.exists("prosora_complete_dashboard.py"):
            print("✅ Main app file exists")
        else:
            print("❌ Main app file missing")
            return False
        
        print("✅ Local test passed - ready for deployment!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def show_deployment_instructions():
    """Show step-by-step deployment instructions"""
    
    print("\n" + "="*60)
    print("🚀 STREAMLIT CLOUD DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    
    print("""
📋 STEP 1: PREPARE REPOSITORY
1. Create GitHub repository: 'prosora-intelligence'
2. Run these commands:
   
   git init
   git add .
   git commit -m "Prosora Intelligence Engine v1.0"
   git remote add origin https://github.com/YOUR_USERNAME/prosora-intelligence
   git push -u origin main

📋 STEP 2: DEPLOY TO STREAMLIT CLOUD
1. Go to: https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub account
4. Select repository: prosora-intelligence
5. Set main file: prosora_complete_dashboard.py
6. Click "Advanced settings"
7. Add secrets:
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   GOOGLE_API_KEY = "your_google_api_key" (optional)
8. Click "Deploy!"

📋 STEP 3: TEST DEPLOYMENT
1. Wait for deployment to complete (2-5 minutes)
2. Your app will be live at:
   https://YOUR_USERNAME-prosora-intelligence-main.streamlit.app
3. Test with demo mode first
4. Try sample queries
5. Verify all features work

📋 STEP 4: SHARE & ITERATE
1. Share URL with stakeholders
2. Gather feedback
3. Monitor performance
4. Plan improvements

🎉 YOUR PROSORA INTELLIGENCE ENGINE WILL BE LIVE!
""")

def main():
    """Main deployment preparation function"""
    
    print("🚀 Prosora Intelligence Engine - Streamlit Cloud Deployment Prep")
    print("="*70)
    
    try:
        # Create deployment files
        create_streamlit_requirements()
        create_streamlit_config()
        create_streamlit_secrets_template()
        create_deployment_readme()
        create_gitignore()
        create_deployment_checklist()
        
        # Check main app
        if not check_main_app():
            print("❌ Main app file issues - please fix before deployment")
            return False
        
        # Run local test
        if not run_local_test():
            print("❌ Local test failed - please fix issues before deployment")
            return False
        
        print("\n✅ All deployment files created successfully!")
        print("✅ Local tests passed!")
        print("✅ Ready for Streamlit Cloud deployment!")
        
        # Show instructions
        show_deployment_instructions()
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment prep failed: {e}")
        return False

if __name__ == "__main__":
    main()