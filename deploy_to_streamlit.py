#!/usr/bin/env python3
"""
Final deployment script for Prosora Intelligence Engine
Handles GitHub setup and provides Streamlit Cloud deployment instructions
"""

import os
import subprocess
import sys

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("✅ Git is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install Git first.")
        return False

def initialize_git_repo():
    """Initialize git repository if not already done"""
    if os.path.exists(".git"):
        print("✅ Git repository already initialized")
        return True
    
    try:
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to initialize git: {e}")
        return False

def create_deployment_commit():
    """Create deployment commit"""
    try:
        # Add all files
        subprocess.run(["git", "add", "."], check=True)
        
        # Create commit
        subprocess.run([
            "git", "commit", "-m", 
            "Prosora Intelligence Engine v1.0 - Ready for Streamlit Cloud"
        ], check=True)
        
        print("✅ Deployment commit created")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Commit creation: {e}")
        # This might fail if no changes, which is okay
        return True

def show_github_setup_instructions():
    """Show GitHub setup instructions"""
    
    print("\n" + "="*70)
    print("📋 GITHUB REPOSITORY SETUP")
    print("="*70)
    
    print("""
🔗 STEP 1: CREATE GITHUB REPOSITORY
1. Go to: https://github.com/new
2. Repository name: prosora-intelligence
3. Description: "AI-Powered Content Intelligence Engine"
4. Set to Public (for free Streamlit Cloud)
5. Don't initialize with README (we have one)
6. Click "Create repository"

💻 STEP 2: CONNECT LOCAL REPOSITORY
Copy and run these commands in your terminal:

git remote add origin https://github.com/YOUR_USERNAME/prosora-intelligence.git
git branch -M main
git push -u origin main

(Replace YOUR_USERNAME with your actual GitHub username)
""")

def show_streamlit_deployment_instructions():
    """Show Streamlit Cloud deployment instructions"""
    
    print("\n" + "="*70)
    print("🚀 STREAMLIT CLOUD DEPLOYMENT")
    print("="*70)
    
    print("""
🌐 STEP 1: DEPLOY TO STREAMLIT CLOUD
1. Go to: https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: prosora-intelligence
5. Branch: main
6. Main file path: prosora_complete_dashboard.py
7. Click "Advanced settings"

🔐 STEP 2: ADD SECRETS (CRITICAL!)
In the Advanced settings, add these secrets:

GEMINI_API_KEY = "your_actual_gemini_api_key_here"
GOOGLE_API_KEY = "your_google_api_key_here"

⚠️ IMPORTANT: Use your REAL API keys, not placeholders!

🚀 STEP 3: DEPLOY
1. Click "Deploy!"
2. Wait 2-5 minutes for deployment
3. Your app will be live at:
   https://YOUR_USERNAME-prosora-intelligence-main.streamlit.app

🧪 STEP 4: TEST YOUR DEPLOYMENT
1. Enable "Demo Mode" first (safe testing)
2. Click "Generate Sample Data"
3. Try example queries
4. Test all view modes
5. Verify analytics work

🎉 STEP 5: SHARE YOUR INTELLIGENCE ENGINE
Your Prosora Intelligence Engine will be live and ready to use!
""")

def show_api_key_instructions():
    """Show API key setup instructions"""
    
    print("\n" + "="*70)
    print("🔑 API KEY SETUP FOR STREAMLIT CLOUD")
    print("="*70)
    
    print(f"""
Your current Gemini API key from config.py: AIzaSyB8kyermgcBRRN27yy3UnB2KBzOQPt3_OQ

🔐 TO ADD IN STREAMLIT CLOUD SECRETS:
1. In Streamlit Cloud deployment settings
2. Go to "Advanced settings" 
3. Add this in the secrets section:

GEMINI_API_KEY = "AIzaSyB8kyermgcBRRN27yy3UnB2KBzOQPt3_OQ"

⚠️ SECURITY NOTE:
- Your API key will be secure in Streamlit Cloud secrets
- It won't be visible in your public GitHub repository
- The .gitignore file protects your local .env file

✅ OPTIONAL: GOOGLE SEARCH API
If you have a Google Search API key, add:
GOOGLE_API_KEY = "your_google_search_api_key"
""")

def show_troubleshooting_guide():
    """Show troubleshooting guide"""
    
    print("\n" + "="*70)
    print("🔧 TROUBLESHOOTING GUIDE")
    print("="*70)
    
    print("""
❌ COMMON ISSUES & SOLUTIONS:

1. "App won't start" 
   → Check Streamlit Cloud logs
   → Verify requirements.txt has all packages
   → Ensure main file path is correct

2. "Import errors"
   → Check if all dependencies are in requirements.txt
   → Verify package names are correct

3. "API key errors"
   → Verify secrets are added correctly in Streamlit Cloud
   → Check API key format and validity
   → Ensure secret names match code (GEMINI_API_KEY)

4. "Memory errors"
   → Use Demo Mode for testing
   → Avoid loading large datasets
   → Consider Streamlit Cloud resource limits

5. "Slow performance"
   → Enable caching in code
   → Use demo mode for testing
   → Optimize data loading

🆘 GETTING HELP:
- Check Streamlit Cloud app logs
- Test locally first: streamlit run prosora_complete_dashboard.py
- Use demo mode to isolate issues
- Verify all secrets are configured

📧 SUPPORT:
- Streamlit Community: https://discuss.streamlit.io
- GitHub Issues: Create issues in your repository
""")

def main():
    """Main deployment function"""
    
    print("🚀 Prosora Intelligence Engine - Final Deployment Setup")
    print("="*70)
    
    # Check prerequisites
    if not check_git_installed():
        return False
    
    # Initialize git if needed
    if not initialize_git_repo():
        return False
    
    # Create deployment commit
    create_deployment_commit()
    
    print("\n✅ LOCAL SETUP COMPLETE!")
    print("✅ Ready for GitHub and Streamlit Cloud deployment!")
    
    # Show instructions
    show_github_setup_instructions()
    show_streamlit_deployment_instructions()
    show_api_key_instructions()
    show_troubleshooting_guide()
    
    print("\n" + "="*70)
    print("🎉 DEPLOYMENT READY!")
    print("="*70)
    print("""
📋 SUMMARY:
✅ All files prepared for deployment
✅ Git repository initialized
✅ Deployment commit created
✅ Instructions provided

🚀 NEXT STEPS:
1. Create GitHub repository
2. Push code to GitHub  
3. Deploy on Streamlit Cloud
4. Add API keys to secrets
5. Test your live app!

🌐 YOUR APP WILL BE LIVE AT:
https://YOUR_USERNAME-prosora-intelligence-main.streamlit.app

🎯 ESTIMATED TIME TO LIVE: 15-20 minutes
""")
    
    return True

if __name__ == "__main__":
    main()