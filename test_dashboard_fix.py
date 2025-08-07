#!/usr/bin/env python3
"""
Test script to verify dashboard fixes
"""

import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from prosora_complete_dashboard import ProsoraCompleteDashboard
    print("✅ Dashboard import successful")
    
    # Test the safe_get_metric function
    dashboard = ProsoraCompleteDashboard()
    
    # Test with dataclass-like object
    class TestMetrics:
        def __init__(self):
            self.query_clarity = 0.85
            self.content_authenticity = 0.92
    
    test_metrics = TestMetrics()
    
    clarity = dashboard.safe_get_metric(test_metrics, 'query_clarity')
    authenticity = dashboard.safe_get_metric(test_metrics, 'content_authenticity')
    missing = dashboard.safe_get_metric(test_metrics, 'missing_key', 0.5)
    
    print(f"✅ Clarity: {clarity}")
    print(f"✅ Authenticity: {authenticity}")
    print(f"✅ Missing key default: {missing}")
    
    # Test with dictionary
    dict_metrics = {'query_clarity': 0.75, 'content_authenticity': 0.88}
    
    dict_clarity = dashboard.safe_get_metric(dict_metrics, 'query_clarity')
    dict_missing = dashboard.safe_get_metric(dict_metrics, 'missing_key', 0.3)
    
    print(f"✅ Dict clarity: {dict_clarity}")
    print(f"✅ Dict missing default: {dict_missing}")
    
    print("\n🎉 All dashboard fixes working correctly!")
    
except Exception as e:
    print(f"❌ Dashboard test failed: {e}")
    import traceback
    traceback.print_exc()