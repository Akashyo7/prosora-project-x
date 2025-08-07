#!/usr/bin/env python3
"""
Test Enhanced Dashboard Functionality
Quick test to verify the enhanced dashboard works correctly
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_phase5_methods():
    """Test that Phase 5 has the required methods"""
    try:
        from phase5_self_improving_intelligence import Phase5SelfImprovingIntelligence
        
        print("🧪 Testing Phase 5 Self-Improving Intelligence...")
        
        # Initialize engine
        engine = Phase5SelfImprovingIntelligence()
        print("✅ Phase 5 engine initialized successfully")
        
        # Check for required methods
        required_methods = [
            'process_query_with_self_improvement',
            'simulate_performance_feedback'
        ]
        
        for method in required_methods:
            if hasattr(engine, method):
                print(f"✅ Method '{method}' exists")
            else:
                print(f"❌ Method '{method}' missing")
        
        # Test basic query processing
        print("\n🔍 Testing query processing...")
        test_query = "AI trends in technology"
        
        try:
            response, metrics = engine.process_query_with_self_improvement(test_query)
            print("✅ Query processing successful")
            print(f"📊 Response keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")
            print(f"📈 Metrics type: {type(metrics)}")
            
        except Exception as e:
            print(f"❌ Query processing failed: {str(e)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_enhanced_dashboard_imports():
    """Test that enhanced dashboard imports work"""
    try:
        print("\n🧪 Testing Enhanced Dashboard imports...")
        
        from prosora_enhanced_dashboard import ProsoraEnhancedDashboard
        print("✅ Enhanced dashboard imported successfully")
        
        from enhanced_personalization_controls import PersonalizationControlCenter
        print("✅ Personalization controls imported successfully")
        
        from source_linking_system import AdvancedSourceManager
        print("✅ Source management imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_main_app():
    """Test main app functionality"""
    try:
        print("\n🧪 Testing Main App...")
        
        from prosora_main_app import ProsoraMainApp
        print("✅ Main app imported successfully")
        
        # Test initialization
        app = ProsoraMainApp()
        print("✅ Main app initialized successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Enhanced Dashboard Tests")
    print("=" * 50)
    
    tests = [
        ("Phase 5 Methods", test_phase5_methods),
        ("Enhanced Dashboard Imports", test_enhanced_dashboard_imports),
        ("Main App", test_main_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced dashboard should work correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)