#!/usr/bin/env python3
"""
Quick test script for Gemini integration
"""

import google.generativeai as genai
from config import Config

def test_gemini_connection():
    """Test basic Gemini connection"""
    print("🧪 Testing Gemini connection...")
    
    try:
        config = Config()
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple test prompt
        prompt = """
        You are Akash - an IIT Bombay engineer, political consultant, product ops lead, and FinTech MBA student.
        
        Generate a quick LinkedIn post about why cross-domain expertise matters in today's world.
        Keep it under 200 words, professional but engaging.
        """
        
        response = model.generate_content(prompt)
        
        print("✅ Gemini connection successful!")
        print("\n📝 Sample generated content:")
        print("-" * 40)
        print(response.text)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini connection failed: {e}")
        return False

def test_prosora_framework():
    """Test Prosora Framework generation"""
    print("\n🎯 Testing Prosora Framework generation...")
    
    try:
        from gemini_optimizer import GeminiOptimizer
        
        optimizer = GeminiOptimizer()
        
        # Test framework content
        framework_content = optimizer.generate_prosora_framework_content(
            topic="AI regulation in fintech",
            insights=[
                {"pattern": "Technical complexity meets regulatory uncertainty"},
                {"contrarian_take": "Over-regulation might benefit big players"}
            ]
        )
        
        if framework_content:
            print("✅ Prosora Framework generation successful!")
            print("\n📋 Generated framework:")
            print("-" * 40)
            print(framework_content.get('content', 'No content generated'))
            print("-" * 40)
        else:
            print("❌ No framework content generated")
            
    except Exception as e:
        print(f"❌ Framework generation failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Prosora Intelligence Engine - Gemini Tests")
    print("=" * 50)
    
    # Test 1: Basic connection
    if not test_gemini_connection():
        print("\n❌ Basic test failed. Check your API key in config.py")
        return
    
    # Test 2: Framework generation
    test_prosora_framework()
    
    print("\n🎉 All tests completed!")
    print("\nNext step: Run 'python prosora_engine.py' for full pipeline")

if __name__ == "__main__":
    main()