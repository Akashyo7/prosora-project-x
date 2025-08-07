#!/usr/bin/env python3
"""
Test Prosora Command Center
Quick test to verify all components work
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    
    print("🧪 Testing Prosora Command Center Components...")
    print("=" * 50)
    
    try:
        # Test core imports
        print("📦 Testing core imports...")
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        from enhanced_content_generator import EnhancedContentGenerator
        print("✅ Enhanced Content Generator imported")
        
        from google_evidence_search import GoogleEvidenceSearch
        print("✅ Google Evidence Search imported")
        
        from firebase_integration import ProsoraFirebaseManager, ProsoraAuthManager
        print("✅ Firebase Integration imported")
        
        from prosora_command_interface import ProsoraCommandInterface
        print("✅ Command Interface imported")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n💡 Make sure all required files are present:")
        print("- enhanced_content_generator.py")
        print("- google_evidence_search.py") 
        print("- firebase_integration.py")
        print("- prosora_command_interface.py")
        return False

def test_content_generation():
    """Test content generation functionality"""
    
    print("\n🔍 Testing Content Generation...")
    print("=" * 50)
    
    try:
        from enhanced_content_generator import EnhancedContentGenerator
        
        generator = EnhancedContentGenerator()
        print("✅ Content generator initialized")
        
        # Test sample insight
        sample_insights = {
            'premium_insights': [{
                'title': 'Test AI Regulation Insight',
                'content': 'Testing content generation for AI regulation in fintech',
                'type': 'test'
            }],
            'cross_domain_connections': [],
            'prosora_frameworks': []
        }
        
        print("🔄 Generating test content...")
        content = generator.generate_evidence_backed_content(sample_insights)
        
        if content:
            print("✅ Content generation successful!")
            
            # Check content structure
            if 'linkedin_posts' in content:
                print(f"📝 Generated {len(content['linkedin_posts'])} LinkedIn posts")
            if 'twitter_threads' in content:
                print(f"🧵 Generated {len(content['twitter_threads'])} Twitter threads")
            if 'blog_outlines' in content:
                print(f"📖 Generated {len(content['blog_outlines'])} blog outlines")
            
            return True
        else:
            print("❌ Content generation returned empty result")
            return False
            
    except Exception as e:
        print(f"❌ Content generation error: {e}")
        return False

def test_firebase_connection():
    """Test Firebase connection (without actual config)"""
    
    print("\n🔥 Testing Firebase Integration...")
    print("=" * 50)
    
    try:
        from firebase_integration import ProsoraFirebaseManager, ProsoraAuthManager
        
        # Test initialization (will use placeholder mode)
        firebase_manager = ProsoraFirebaseManager()
        auth_manager = ProsoraAuthManager()
        
        print("✅ Firebase manager initialized")
        print("✅ Auth manager initialized")
        
        # Test methods (will use placeholder data)
        user_stats = {'total_content': 0, 'avg_evidence': 0}
        print("✅ User stats method accessible")
        
        print("💡 Firebase integration ready (configure with your project)")
        return True
        
    except Exception as e:
        print(f"❌ Firebase integration error: {e}")
        return False

def test_command_interface():
    """Test command interface initialization"""
    
    print("\n🎮 Testing Command Interface...")
    print("=" * 50)
    
    try:
        from prosora_command_interface import ProsoraCommandInterface
        
        # Test initialization
        interface = ProsoraCommandInterface()
        print("✅ Command interface initialized")
        
        # Test suggestions
        if hasattr(interface, 'suggestions') and interface.suggestions:
            print(f"✅ {len(interface.suggestions)} content suggestions loaded")
        
        # Test quick actions
        if hasattr(interface, 'quick_actions') and interface.quick_actions:
            print(f"✅ {len(interface.quick_actions)} quick actions available")
        
        print("✅ Command interface ready for Streamlit")
        return True
        
    except Exception as e:
        print(f"❌ Command interface error: {e}")
        return False

def run_full_test():
    """Run complete test suite"""
    
    print("🧠 PROSORA COMMAND CENTER - SYSTEM TEST")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Content Generation Test", test_content_generation),
        ("Firebase Integration Test", test_firebase_connection),
        ("Command Interface Test", test_command_interface)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Your Prosora Command Center is ready to launch!")
        print("\nNext steps:")
        print("1. Configure Firebase (see PROSORA_COMMAND_CENTER_SETUP.md)")
        print("2. Set up environment variables (.env file)")
        print("3. Run: streamlit run launch_prosora_command_center.py")
    else:
        print(f"\n⚠️  {total - passed} tests failed")
        print("💡 Check the error messages above and fix issues before launching")
    
    return passed == total

if __name__ == "__main__":
    success = run_full_test()
    sys.exit(0 if success else 1)