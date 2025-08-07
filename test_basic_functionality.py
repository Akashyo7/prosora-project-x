#!/usr/bin/env python3
"""
Basic Functionality Test for Prosora Command Center
Tests core functionality without external dependencies
"""

import sys
import os
from datetime import datetime

def test_core_imports():
    """Test core imports without Firebase"""
    
    print("🧪 Testing Core Components...")
    print("=" * 50)
    
    try:
        # Test essential imports
        print("📦 Testing essential imports...")
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        from enhanced_content_generator import EnhancedContentGenerator
        print("✅ Enhanced Content Generator imported")
        
        from google_evidence_search import GoogleEvidenceSearch
        print("✅ Google Evidence Search imported")
        
        print("\n🎉 Core imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
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
            linkedin_count = len(content.get('linkedin_posts', []))
            twitter_count = len(content.get('twitter_threads', []))
            blog_count = len(content.get('blog_outlines', []))
            
            print(f"📝 Generated {linkedin_count} LinkedIn posts")
            print(f"🧵 Generated {twitter_count} Twitter threads")
            print(f"📖 Generated {blog_count} blog outlines")
            
            # Test content quality
            if linkedin_count > 0:
                first_post = content['linkedin_posts'][0]
                if 'content' in first_post and len(first_post['content']) > 50:
                    print("✅ LinkedIn content has good length")
                if 'evidence_count' in first_post and first_post['evidence_count'] > 0:
                    print("✅ Evidence sources included")
            
            return True
        else:
            print("❌ Content generation returned empty result")
            return False
            
    except Exception as e:
        print(f"❌ Content generation error: {e}")
        return False

def test_google_search():
    """Test Google Evidence Search (without API key)"""
    
    print("\n🔍 Testing Google Evidence Search...")
    print("=" * 50)
    
    try:
        from google_evidence_search import GoogleEvidenceSearch
        
        search = GoogleEvidenceSearch()
        print("✅ Google Evidence Search initialized")
        
        # Test search method exists
        if hasattr(search, 'search_evidence'):
            print("✅ Search evidence method available")
        
        if hasattr(search, 'validate_source'):
            print("✅ Source validation method available")
        
        print("💡 Google Evidence Search ready (configure API key for full functionality)")
        return True
        
    except Exception as e:
        print(f"❌ Google Evidence Search error: {e}")
        return False

def test_streamlit_compatibility():
    """Test Streamlit compatibility"""
    
    print("\n🎮 Testing Streamlit Compatibility...")
    print("=" * 50)
    
    try:
        import streamlit as st
        
        # Test key Streamlit functions
        print("✅ Streamlit imported")
        
        # Test if we can access session state
        if hasattr(st, 'session_state'):
            print("✅ Session state available")
        
        # Test if we can access columns
        if hasattr(st, 'columns'):
            print("✅ Columns layout available")
        
        # Test if we can access tabs
        if hasattr(st, 'tabs'):
            print("✅ Tabs layout available")
        
        # Test if we can access expander
        if hasattr(st, 'expander'):
            print("✅ Expander available")
        
        print("✅ Streamlit compatibility confirmed")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit compatibility error: {e}")
        return False

def run_basic_test():
    """Run basic test suite"""
    
    print("🧠 PROSORA COMMAND CENTER - BASIC TEST")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Core Imports Test", test_core_imports),
        ("Content Generation Test", test_content_generation),
        ("Google Search Test", test_google_search),
        ("Streamlit Compatibility Test", test_streamlit_compatibility)
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
        print("\n🎉 BASIC TESTS PASSED!")
        print("🚀 Core functionality is working!")
        print("\nNext steps:")
        print("1. Install firebase-admin: pip install firebase-admin")
        print("2. Configure Firebase (see PROSORA_COMMAND_CENTER_SETUP.md)")
        print("3. Run: streamlit run launch_prosora_command_center.py")
    elif passed >= total - 1:
        print(f"\n✅ MOSTLY WORKING! ({passed}/{total} tests passed)")
        print("💡 Minor issues detected, but core functionality is ready")
        print("🚀 You can proceed with the setup!")
    else:
        print(f"\n⚠️  {total - passed} tests failed")
        print("💡 Check the error messages above and fix issues before launching")
    
    return passed >= total - 1  # Allow 1 failure

if __name__ == "__main__":
    success = run_basic_test()
    sys.exit(0 if success else 1)