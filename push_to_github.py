#!/usr/bin/env python3
"""
Push Prosora Intelligence Engine to GitHub repository: prosora-project-x
"""

import subprocess
import sys
import os

def check_git_status():
    """Check current git status"""
    try:
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            print("📝 Uncommitted changes found:")
            print(result.stdout)
            return False
        else:
            print("✅ All changes are committed")
            return True
            
    except subprocess.CalledProcessError:
        print("⚠️ Not in a git repository or git not available")
        return False

def add_github_remote():
    """Add GitHub remote for prosora-project-x"""
    try:
        # Check if remote already exists
        result = subprocess.run(["git", "remote", "-v"], 
                              capture_output=True, text=True, check=True)
        
        if "prosora-project-x" in result.stdout:
            print("✅ GitHub remote already configured")
            return True
        
        # Add the remote
        subprocess.run([
            "git", "remote", "add", "origin", 
            "https://github.com/YOUR_USERNAME/prosora-project-x.git"
        ], check=True)
        
        print("✅ GitHub remote added")
        print("⚠️ Replace YOUR_USERNAME with your actual GitHub username")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to add remote: {e}")
        return False

def push_to_github():
    """Push code to GitHub"""
    try:
        print("🚀 Pushing to GitHub...")
        
        # Set main branch
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        
        # Push to GitHub
        result = subprocess.run([
            "git", "push", "-u", "origin", "main"
        ], capture_output=True, text=True, check=True)
        
        print("✅ Successfully pushed to GitHub!")
        print("🌐 Your repository is now live at:")
        print("   https://github.com/YOUR_USERNAME/prosora-project-x")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Push failed: {e}")
        if "remote: Repository not found" in str(e):
            print("💡 Make sure you've created the repository on GitHub first")
        elif "Permission denied" in str(e):
            print("💡 You may need to authenticate with GitHub")
            print("   Try: gh auth login  (if you have GitHub CLI)")
        return False

def main():
    """Main push function"""
    print("📤 Pushing Prosora Intelligence Engine to GitHub")
    print("Repository: prosora-project-x")
    print("="*60)
    
    # Check git status
    if not check_git_status():
        print("❌ Please commit your changes first")
        return False
    
    # Add remote
    if not add_github_remote():
        return False
    
    # Push to GitHub
    if not push_to_github():
        return False
    
    print("\n🎉 SUCCESS! Code pushed to GitHub")
    print("\n📋 Next: Deploy to Streamlit Cloud")
    
    return True

if __name__ == "__main__":
    main()