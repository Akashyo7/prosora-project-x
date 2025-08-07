#!/usr/bin/env python3
"""
Launch script for Prosora Complete Dashboard
Handles port conflicts and provides better error handling
"""

import subprocess
import sys
import os
import socket
import time

def find_available_port(start_port=8500, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['streamlit', 'plotly', 'pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    return True

def launch_dashboard():
    """Launch the complete dashboard"""
    print("🧠 Prosora Complete Intelligence Dashboard Launcher")
    print("=" * 60)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        return False
    
    # Check if dashboard file exists
    dashboard_file = "prosora_complete_dashboard.py"
    if not os.path.exists(dashboard_file):
        print(f"❌ Dashboard file '{dashboard_file}' not found!")
        return False
    
    # Find available port
    print("🔍 Finding available port...")
    port = find_available_port()
    if not port:
        print("❌ No available ports found!")
        return False
    
    print(f"✅ Using port {port}")
    
    # Launch dashboard
    print("🚀 Launching Prosora Complete Dashboard...")
    print("=" * 60)
    print(f"🌐 Dashboard will open at: http://localhost:{port}")
    print("📱 If browser doesn't open automatically, click the link above")
    print("⏹️  Press Ctrl+C to stop the dashboard")
    print("=" * 60)
    
    try:
        # Add small delay to let user read the message
        time.sleep(2)
        
        # Launch streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", dashboard_file,
            "--server.port", str(port),
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "light"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
        return True
    except Exception as e:
        print(f"❌ Failed to launch dashboard: {e}")
        return False
    
    return True

def main():
    """Main function"""
    try:
        success = launch_dashboard()
        if success:
            print("✅ Dashboard session completed successfully!")
        else:
            print("❌ Dashboard launch failed!")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()