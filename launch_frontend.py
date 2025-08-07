#!/usr/bin/env python3
"""
Launch script for Prosora Command Center
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing frontend dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "plotly"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def ensure_data_files():
    """Ensure required data files exist"""
    print("📁 Checking data files...")
    
    os.makedirs("data", exist_ok=True)
    
    # Create empty approval file if it doesn't exist
    approval_file = "data/content_approvals.json"
    if not os.path.exists(approval_file):
        import json
        empty_approvals = {"approved": [], "rejected": [], "pending": []}
        with open(approval_file, "w") as f:
            json.dump(empty_approvals, f, indent=2)
        print("✅ Created content approvals file")
    
    # Check if demo data exists
    demo_files = [
        "data/demo_content.json",
        "data/demo_insights.json", 
        "data/demo_generated.json",
        "data/demo_report.json"
    ]
    
    missing_files = [f for f in demo_files if not os.path.exists(f)]
    
    if missing_files:
        print("⚠️  Some demo data files are missing. Run 'python3 prosora_demo.py' first.")
        print(f"   Missing: {', '.join(missing_files)}")
        return False
    
    print("✅ All data files present")
    return True

def launch_frontend():
    """Launch the Streamlit frontend"""
    print("🚀 Launching Prosora Command Center...")
    print("=" * 50)
    print("🌐 Opening in your browser...")
    print("📱 Access at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "prosora_frontend.py",
            "--server.port", "8501",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Prosora Command Center stopped")
    except Exception as e:
        print(f"❌ Error launching frontend: {e}")

def main():
    """Main launch function"""
    print("🧠 Prosora Command Center Launcher")
    print("=" * 40)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Step 2: Ensure data files exist
    if not ensure_data_files():
        print("❌ Data files missing. Please run the demo first:")
        print("   python3 prosora_demo.py")
        return
    
    # Step 3: Launch frontend
    launch_frontend()

if __name__ == "__main__":
    main()