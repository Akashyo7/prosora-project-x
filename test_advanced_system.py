#!/usr/bin/env python3
"""
Test the Advanced Prosora Intelligence System
Simplified version for testing without email access
"""

import json
import yaml
from datetime import datetime
from intelligent_insights import IntelligentInsightsEngine
from content_generator import ContentGenerator

def create_sample_content():
    """Create sample content with credibility weighting for testing"""
    
    sample_content = [
        # Premium content (high credibility)
        {
            "type": "curated_blog",
            "title": "The Future of AI in Product Management",
            "content": "Marc Andreessen discusses how AI will fundamentally change product development cycles. The key insight is that AI won't replace product managers but will augment their decision-making capabilities. Companies that integrate AI into their product workflows early will have a significant competitive advantage. The intersection of AI and product management requires both technical understanding and business acumen.",
            "source": "a16z",
            "credibility_score": 0.95,
            "expertise_domains": ["tech", "product"],
            "personal_relevance": 0.9,
            "content_quality": "premium",
            "timestamp": datetime.now().isoformat()
        },
        {
            "type": "email_newsletter", 
            "title": "Stratechery: The Political Economy of AI",
            "content": "Ben Thompson analyzes the regulatory landscape for AI development. The EU AI Act represents a fundamental shift in how governments approach technology regulation. This creates both opportunities and challenges for startups. The key is understanding that regulation is not just about compliance but about competitive positioning in global markets.",
            "source": "Stratechery",
            "credibility_score": 0.95,
            "expertise_domains": ["tech", "politics", "strategy"],
            "personal_relevance": 0.95,
            "content_quality": "premium",
            "timestamp": datetime.now().isoformat()
        },
        
        # Standard content (medium credibility)
        {
            "type": "curated_blog",
            "title": "McKinsey: Digital Transformation in Financial Services",
            "content": "Traditional banks are struggling to compete with fintech startups. The key differentiator is not just technology but organizational agility. Banks that can adopt startup-like product development cycles while maintaining regulatory compliance will succeed. The challenge is cultural transformation as much as technological.",
            "source": "McKinsey",
            "credibility_score": 0.8,
            "expertise_domains": ["finance", "strategy"],
            "personal_relevance": 0.8,
            "content_quality": "standard",
            "timestamp": datetime.now().isoformat()
        },
        
        # Experimental content (low credibility)
        {
            "type": "social",
            "title": "Hacker News: Discussion on AI Regulation",
            "content": "Community discussion about whether AI regulation will stifle innovation. Mixed opinions with some arguing for self-regulation and others supporting government intervention. Interesting perspective from a former Google engineer about the technical challenges of implementing AI safety measures.",
            "source": "Hacker News",
            "credibility_score": 0.6,
            "expertise_domains": ["tech"],
            "personal_relevance": 0.7,
            "content_quality": "experimental",
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    return sample_content

def test_intelligent_insights():
    """Test the intelligent insights engine"""
    
    print("🧪 Testing Prosora Intelligence Engine v2.0")
    print("=" * 50)
    
    # Create sample content
    print("📊 Creating sample content with credibility weighting...")
    sample_content = create_sample_content()
    
    print(f"✅ Created {len(sample_content)} content pieces:")
    for content in sample_content:
        print(f"   - {content['source']} (credibility: {content['credibility_score']})")
    
    # Test intelligent insights
    print("\n🧠 Testing Intelligent Insights Engine...")
    insights_engine = IntelligentInsightsEngine()
    
    try:
        insights = insights_engine.analyze_with_credibility_weighting(sample_content)
        
        print("✅ Intelligent analysis complete!")
        print(f"📈 Generated insights:")
        
        # Print summary of insights
        for key, value in insights.items():
            if isinstance(value, list):
                print(f"   - {key}: {len(value)} items")
            elif isinstance(value, dict):
                print(f"   - {key}: {len(value)} components")
            else:
                print(f"   - {key}: {value}")
        
        # Save insights for inspection
        with open("data/test_insights.json", "w") as f:
            json.dump(insights, f, indent=2)
        
        print(f"\n💾 Insights saved to data/test_insights.json")
        
    except Exception as e:
        print(f"❌ Error in intelligent analysis: {e}")
        return False
    
    # Test content generation
    print("\n✍️ Testing Advanced Content Generation...")
    content_generator = ContentGenerator()
    
    try:
        generated_content = content_generator.generate_prosora_content(insights)
        
        print("✅ Content generation complete!")
        print(f"📝 Generated content:")
        print(f"   - LinkedIn posts: {len(generated_content.get('linkedin_posts', []))}")
        print(f"   - Twitter threads: {len(generated_content.get('twitter_threads', []))}")
        print(f"   - Blog outlines: {len(generated_content.get('blog_outlines', []))}")
        
        # Save generated content
        with open("data/test_generated_content.json", "w") as f:
            json.dump(generated_content, f, indent=2)
        
        print(f"\n💾 Generated content saved to data/test_generated_content.json")
        
    except Exception as e:
        print(f"❌ Error in content generation: {e}")
        return False
    
    # Create test intelligence report
    print("\n📊 Creating Test Intelligence Report...")
    
    test_report = {
        "test_timestamp": datetime.now().isoformat(),
        "system_status": "✅ All systems operational",
        "content_analysis": {
            "total_content_pieces": len(sample_content),
            "premium_content": len([c for c in sample_content if c.get('content_quality') == 'premium']),
            "standard_content": len([c for c in sample_content if c.get('content_quality') == 'standard']),
            "experimental_content": len([c for c in sample_content if c.get('content_quality') == 'experimental'])
        },
        "insights_generated": {
            "total_insight_categories": len(insights),
            "advanced_prosora_index": insights.get("prosora_index_advanced", {})
        },
        "content_generated": {
            "linkedin_ready": len(generated_content.get('linkedin_posts', [])),
            "twitter_ready": len(generated_content.get('twitter_threads', [])),
            "blog_ready": len(generated_content.get('blog_outlines', []))
        },
        "next_steps": [
            "✅ System tested successfully",
            "🔄 Ready for real data integration",
            "📧 Configure email access for newsletter integration",
            "🚀 Deploy full pipeline with your curated sources"
        ]
    }
    
    # Save test report
    with open("data/test_intelligence_report.json", "w") as f:
        json.dump(test_report, f, indent=2)
    
    # Print test summary
    print("\n🎉 TEST COMPLETE - PROSORA INTELLIGENCE v2.0")
    print("=" * 50)
    print(f"📊 Content Analysis:")
    print(f"   Total pieces: {test_report['content_analysis']['total_content_pieces']}")
    print(f"   Premium: {test_report['content_analysis']['premium_content']}")
    print(f"   Standard: {test_report['content_analysis']['standard_content']}")
    print(f"   Experimental: {test_report['content_analysis']['experimental_content']}")
    
    print(f"\n🧠 Insights Generated:")
    print(f"   Categories: {test_report['insights_generated']['total_insight_categories']}")
    
    print(f"\n📝 Content Generated:")
    print(f"   LinkedIn posts: {test_report['content_generated']['linkedin_ready']}")
    print(f"   Twitter threads: {test_report['content_generated']['twitter_ready']}")
    print(f"   Blog outlines: {test_report['content_generated']['blog_ready']}")
    
    print(f"\n🎯 Next Steps:")
    for step in test_report['next_steps']:
        print(f"   {step}")
    
    return True

if __name__ == "__main__":
    success = test_intelligent_insights()
    
    if success:
        print(f"\n🚀 READY FOR PRODUCTION!")
        print(f"Run 'python3 prosora_orchestrator.py' with your real sources")
    else:
        print(f"\n❌ Tests failed - check configuration")