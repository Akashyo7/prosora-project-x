#!/usr/bin/env python3
"""
Set up sample performance data for demo
"""

from performance_tracker import ProsoraPerformanceTracker
import random
from datetime import datetime, timedelta

def create_sample_performance_data():
    """Create realistic sample performance data"""
    
    tracker = ProsoraPerformanceTracker()
    
    # Sample content pieces
    sample_content = [
        {
            'platform': 'linkedin',
            'content_type': 'insight_post',
            'content': 'AI is transforming product management in ways we never imagined...',
            'ai_confidence': 0.85,
            'source_credibility': 0.9,
            'content_quality_score': 0.8
        },
        {
            'platform': 'twitter',
            'content_type': 'twitter_thread',
            'content': 'Thread: Why cross-domain expertise matters more than ever...',
            'ai_confidence': 0.78,
            'source_credibility': 0.85,
            'content_quality_score': 0.75
        },
        {
            'platform': 'linkedin',
            'content_type': 'framework_post',
            'content': 'The Political Product Manager framework: 3 lessons from campaign strategy...',
            'ai_confidence': 0.92,
            'source_credibility': 0.95,
            'content_quality_score': 0.9
        },
        {
            'platform': 'twitter',
            'content_type': 'insight_thread',
            'content': 'FinTech regulation is creating unexpected opportunities...',
            'ai_confidence': 0.88,
            'source_credibility': 0.9,
            'content_quality_score': 0.85
        },
        {
            'platform': 'linkedin',
            'content_type': 'contrarian_post',
            'content': 'Unpopular opinion: Most AI startups are solving the wrong problems...',
            'ai_confidence': 0.75,
            'source_credibility': 0.8,
            'content_quality_score': 0.7
        }
    ]
    
    print("🚀 Creating sample performance data...")
    
    for i, content in enumerate(sample_content):
        # Track the content
        content_id = tracker.track_published_content(content)
        
        # Generate realistic performance metrics
        if content['platform'] == 'linkedin':
            # LinkedIn typically has lower volume but higher engagement rates
            views = random.randint(200, 800)
            likes = random.randint(10, 60)
            comments = random.randint(2, 20)
            shares = random.randint(1, 15)
            clicks = random.randint(5, 30)
        else:  # Twitter
            # Twitter typically has higher volume but lower engagement rates
            views = random.randint(500, 2000)
            likes = random.randint(15, 100)
            comments = random.randint(3, 25)
            shares = random.randint(2, 20)
            clicks = random.randint(8, 40)
        
        # Add some variation based on content quality
        quality_multiplier = content['content_quality_score']
        views = int(views * (0.5 + quality_multiplier))
        likes = int(likes * (0.5 + quality_multiplier))
        comments = int(comments * (0.5 + quality_multiplier))
        shares = int(shares * (0.5 + quality_multiplier))
        clicks = int(clicks * (0.5 + quality_multiplier))
        
        metrics = {
            'views': views,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'clicks': clicks
        }
        
        # Update performance metrics
        tracker.update_performance_metrics(content_id, metrics)
        
        print(f"✅ Created performance data for {content_id}")
        print(f"   Platform: {content['platform']}")
        print(f"   Engagement: {((likes + comments + shares) / views * 100):.1f}%")
        print()
    
    # Analyze patterns
    print("📊 Analyzing performance patterns...")
    patterns = tracker.analyze_performance_patterns()
    
    if "message" not in patterns:
        print("🏆 High Performers:")
        high_performers = patterns.get('high_performers', {})
        if "message" not in high_performers:
            print(f"   Count: {high_performers.get('count', 0)}")
            print(f"   Avg Engagement: {high_performers.get('avg_engagement_rate', 0):.1f}%")
            print(f"   Avg AI Confidence: {high_performers.get('avg_ai_confidence', 0):.2f}")
        
        print("\n📈 Platform Performance:")
        platform_perf = patterns.get('platform_performance', {})
        if platform_perf.get('engagement_rate'):
            for platform, engagement in platform_perf['engagement_rate'].items():
                print(f"   {platform}: {engagement:.1f}% avg engagement")
    
    # Generate improvement suggestions
    print("\n💡 AI Improvement Suggestions:")
    suggestions = tracker.generate_ai_improvement_suggestions()
    for suggestion in suggestions:
        print(f"   • {suggestion}")
    
    print("\n🎉 Sample performance data created successfully!")
    print("Launch the frontend to see the performance tracking in action.")

if __name__ == "__main__":
    create_sample_performance_data()