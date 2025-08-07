#!/usr/bin/env python3
"""
Verify Prosora Intelligence Engine is ready for Streamlit Cloud deployment
"""

import os
import sys
import importlib.util

def check_file_exists(filename, description):
    """Check if a file exists"""
    if os.path.exists(filename):
        print(f"✅ {description}: {filename}")
        return True
    else:
        print(f"❌ Missing {description}: {filename}")
        return False

def check_requirements():
    """Check if requirements.txt has all needed packages"""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt missing")
        return False
    
    with open("requirements.txt", "r") as f:
        requirements = f.read()
    
    required_packages = [
        "streamlit", "plotly", "pandas", "numpy", 
        "google-generativeai", "feedparser", "beautifulsoup4",
        "requests", "python-dotenv", "pyyaml"
    ]
    
    missing = []
    for package in required_packages:
        if package not in requirements:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages in requirements.txt: {', '.join(missing)}")
        return False
    else:
        print("✅ All required packages in requirements.txt")
        return True

def check_imports():
    """Check if all critical imports work"""
    critical_imports = [
        "streamlit", "plotly", "pandas", "numpy", 
        "json", "datetime", "typing"
    ]
    
    failed_imports = []
    for module in critical_imports:
        try:
            __import__(module)
        except ImportError:
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ Failed imports: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All critical imports successful")
        return True

def check_main_app():
    """Check main app file structure"""
    main_file = "prosora_complete_dashboard.py"
    
    if not os.path.exists(main_file):
        print(f"❌ Main app file missing: {main_file}")
        return False
    
    with open(main_file, "r") as f:
        content = f.read()
    
    # Check for critical components
    checks = [
        ("streamlit import", "import streamlit"),
        ("main function", "def main()"),
        ("main execution", 'if __name__ == "__main__"'),
        ("dashboard class", "class ProsoraCompleteDashboard")
    ]
    
    all_good = True
    for check_name, check_pattern in checks:
        if check_pattern in content:
            print(f"✅ {check_name} found")
        else:
            print(f"❌ {check_name} missing")
            all_good = False
    
    return all_good

def check_sensitive_data():
    """Check for sensitive data that shouldn't be in repo"""
    sensitive_patterns = [
        "AIzaSy",  # Google API keys
        "sk-",     # OpenAI keys
        "firebase_config.json",
        "adminsdk"
    ]
    
    issues = []
    
    # Check main files
    files_to_check = [
        "prosora_complete_dashboard.py",
        "config.py",
        ".env"
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                content = f.read()
                
            for pattern in sensitive_patterns:
                if pattern in content:
                    issues.append(f"{filename} contains {pattern}")
    
    if issues:
        print("⚠️ Potential sensitive data found:")
        for issue in issues:
            print(f"   • {issue}")
        print("   Make sure to use Streamlit secrets for API keys!")
        return False
    else:
        print("✅ No sensitive data found in code")
        return True

def check_gitignore():
    """Check if .gitignore is properly configured"""
    if not os.path.exists(".gitignore"):
        print("⚠️ .gitignore missing - create one to protect sensitive files")
        return False
    
    with open(".gitignore", "r") as f:
        gitignore = f.read()
    
    important_ignores = [
        ".env", "*.db", "firebase_config.json", 
        "__pycache__", "*.log"
    ]
    
    missing = []
    for ignore in important_ignores:
        if ignore not in gitignore:
            missing.append(ignore)
    
    if missing:
        print(f"⚠️ .gitignore missing: {', '.join(missing)}")
        return False
    else:
        print("✅ .gitignore properly configured")
        return True

def check_streamlit_config():
    """Check Streamlit configuration"""
    config_file = ".streamlit/config.toml"
    
    if os.path.exists(config_file):
        print("✅ Streamlit config found")
        return True
    else:
        print("⚠️ Streamlit config missing - using defaults")
        return True  # Not critical

def estimate_deployment_time():
    """Estimate deployment time based on file sizes"""
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk("."):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if not file.startswith('.') and not file.endswith('.pyc'):
                filepath = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(filepath)
                    file_count += 1
                except:
                    pass
    
    size_mb = total_size / (1024 * 1024)
    
    print(f"📊 Repository stats:")
    print(f"   • Files: {file_count}")
    print(f"   • Size: {size_mb:.1f} MB")
    
    if size_mb < 10:
        print("⚡ Estimated deployment time: 2-3 minutes")
    elif size_mb < 50:
        print("⏱️ Estimated deployment time: 3-5 minutes")
    else:
        print("🐌 Estimated deployment time: 5-10 minutes")

def main():
    """Main verification function"""
    print("🔍 Prosora Intelligence Engine - Deployment Readiness Check")
    print("="*65)
    
    checks = [
        ("Main app file", lambda: check_file_exists("prosora_complete_dashboard.py", "Main app")),
        ("Requirements file", lambda: check_file_exists("requirements.txt", "Requirements")),
        ("README file", lambda: check_file_exists("README.md", "README")),
        ("Requirements content", check_requirements),
        ("Critical imports", check_imports),
        ("Main app structure", check_main_app),
        ("Sensitive data check", check_sensitive_data),
        ("Gitignore configuration", check_gitignore),
        ("Streamlit config", check_streamlit_config)
    ]
    
    passed = 0
    total = len(checks)
    
    print("\n🧪 Running deployment readiness checks...\n")
    
    for check_name, check_func in checks:
        print(f"Checking {check_name}...")
        if check_func():
            passed += 1
        print()
    
    print("="*65)
    print(f"📊 RESULTS: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED - READY FOR DEPLOYMENT!")
        print("\n🚀 Next steps:")
        print("1. Create GitHub repository")
        print("2. Push code to GitHub")
        print("3. Deploy on Streamlit Cloud")
        print("4. Add your API keys to Streamlit secrets")
        
        estimate_deployment_time()
        
    elif passed >= total - 2:
        print("⚠️ MOSTLY READY - Minor issues to fix")
        print("You can proceed with deployment but fix the issues above")
        
    else:
        print("❌ NOT READY - Please fix the issues above before deployment")
        return False
    
    print("\n🔗 Deployment URL will be:")
    print("https://YOUR_USERNAME-prosora-intelligence-main.streamlit.app")
    
    return True

if __name__ == "__main__":
    main()