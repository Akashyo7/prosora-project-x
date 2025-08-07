#!/usr/bin/env python3
"""
Prosora Intelligence Engine Setup Script
"""

import os
import subprocess
import sys

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def setup_environment():
    """Set up environment file"""
    print("🔧 Setting up environment...")
    
    if not os.path.exists(".env"):
        # Copy example env file
        with open(".env.example", "r") as example:
            content = example.read()
        
        with open(".env", "w") as env_file:
            env_file.write(content)
        
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your API keys!")
    else:
        print("✅ .env file already exists")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = ["data", "logs", "output"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/ directory")

def test_setup():
    """Test the setup"""
    print("🧪 Testing setup...")
    
    try:
        from content_aggregator import ContentAggregator
        from ai_analyzer import AIAnalyzer
        from content_generator import ContentGenerator
        print("✅ All modules imported successfully!")
        
        # Test data directory
        if os.path.exists("data"):
            print("✅ Data directory exists")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Prosora Intelligence Engine Setup")
    print("=" * 40)
    
    steps = [
        ("Installing requirements", install_requirements),
        ("Setting up environment", setup_environment),
        ("Creating directories", create_directories),
        ("Testing setup", test_setup)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python prosora_engine.py")
    print("3. Choose option 1 to run the full pipeline")
    
    return True

if __name__ == "__main__":
    main()