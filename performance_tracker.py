#!/usr/bin/env python3
"""
Prosora Performance Tracker
Simple but powerful system to track content performance and improve AI output
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from dataclasses import dataclass
import pandas as pd

@dataclass
class ContentPerformance:
    """Content performance data structure"""
    content_id: str
    platform: str
    content_type: str
    published_date: str
    content_text: str
    
    # Performance metrics
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    clicks: int = 0
    
    # Engagement rates
    engagement_rate: float = 0.0
    click_through_rate: float = 0.0
    
    # AI learning data
    ai_confidence: float = 0.0
    source_credibility: float = 0.0
    content_quality_score: float = 0.0
    
    # Performance classification
    performance_tier: str = "unknown"  # "high", "medium", "low"

class ProsoraPerformanceTracker:
    def __init__(self):
        self.db_path = "data/prosora_performance.db"
        self.setup_database()
    
    def setup_database(self):
        """Set up SQLite database for performance tracking"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Content performance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT UNIQUE,
                platform TEXT,
                content_type TEXT,
                published_date TEXT,
                content_text TEXT,
                
                -- Performance metrics
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                
                -- Calculated metrics
                engagement_rate REAL DEFAULT 0.0,
                click_through_rate REAL DEFAULT 0.0,
                
                -- AI learning data
                ai_confidence REAL DEFAULT 0.0,
                source_credibility REAL DEFAULT 0.0,
                content_quality_score REAL DEFAULT 0.0,
                
                -- Performance classification
                performance_tier TEXT DEFAULT 'unknown',
                
                -- Timestamps
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # AI learning patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_learning_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                performance_correlation REAL,
                confidence_level REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Content feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT,
                feedback_type TEXT,
                feedback_data TEXT,
                user_rating INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content_performance (content_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Performance tracking database initialized")
    
    def track_published_content(self, content_data: Dict) -> str:
        """Track newly published content"""
        
        content_id = f"{content_data['platform']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO content_performance 
            (content_id, platform, content_type, published_date, content_text, 
             ai_confidence, source_credibility, content_quality_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            content_id,
            content_data.get('platform', ''),
            content_data.get('content_type', ''),
            datetime.now().isoformat(),
            content_data.get('content', '')[:500],  # Truncate for storage
            content_data.get('ai_confidence', 0.0),
            content_data.get('source_credibility', 0.0),
            content_data.get('content_quality_score', 0.0)
        ))
        
        conn.commit()
        conn.close()
        
        print(f"📊 Tracking content: {content_id}")
        return content_id
    
    def update_performance_metrics(self, content_id: str, metrics: Dict):
        """Update performance metrics for published content"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate engagement rate
        total_engagement = metrics.get('likes', 0) + metrics.get('comments', 0) + metrics.get('shares', 0)
        views = max(metrics.get('views', 1), 1)  # Avoid division by zero
        engagement_rate = (total_engagement / views) * 100
        
        # Calculate CTR if applicable
        clicks = metrics.get('clicks', 0)
        ctr = (clicks / views) * 100 if views > 0 else 0
        
        # Determine performance tier
        performance_tier = self._classify_performance(engagement_rate, total_engagement)
        
        cursor.execute('''
            UPDATE content_performance 
            SET views = ?, likes = ?, comments = ?, shares = ?, clicks = ?,
                engagement_rate = ?, click_through_rate = ?, performance_tier = ?,
                last_updated = ?
            WHERE content_id = ?
        ''', (
            metrics.get('views', 0),
            metrics.get('likes', 0),
            metrics.get('comments', 0),
            metrics.get('shares', 0),
            metrics.get('clicks', 0),
            engagement_rate,
            ctr,
            performance_tier,
            datetime.now().isoformat(),
            content_id
        ))
        
        conn.commit()
        conn.close()
        
        print(f"📈 Updated metrics for {content_id}: {engagement_rate:.1f}% engagement")
    
    def _classify_performance(self, engagement_rate: float, total_engagement: int) -> str:
        """Classify content performance into tiers"""
        
        if engagement_rate >= 5.0 and total_engagement >= 50:
            return "high"
        elif engagement_rate >= 2.0 and total_engagement >= 20:
            return "medium"
        else:
            return "low"
    
    def analyze_performance_patterns(self) -> Dict:
        """Analyze patterns in high-performing content"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Get performance data
        df = pd.read_sql_query('''
            SELECT * FROM content_performance 
            WHERE performance_tier != 'unknown'
            ORDER BY published_date DESC
        ''', conn)
        
        conn.close()
        
        if df.empty:
            return {"message": "No performance data available yet"}
        
        # Analyze patterns
        patterns = {
            "high_performers": self._analyze_high_performers(df),
            "platform_performance": self._analyze_platform_performance(df),
            "content_type_performance": self._analyze_content_type_performance(df),
            "timing_patterns": self._analyze_timing_patterns(df),
            "ai_correlation": self._analyze_ai_correlation(df)
        }
        
        return patterns
    
    def _analyze_high_performers(self, df: pd.DataFrame) -> Dict:
        """Analyze characteristics of high-performing content"""
        
        high_performers = df[df['performance_tier'] == 'high']
        
        if high_performers.empty:
            return {"message": "No high-performing content yet"}
        
        return {
            "count": len(high_performers),
            "avg_engagement_rate": high_performers['engagement_rate'].mean(),
            "avg_ai_confidence": high_performers['ai_confidence'].mean(),
            "avg_source_credibility": high_performers['source_credibility'].mean(),
            "common_platforms": high_performers['platform'].value_counts().to_dict(),
            "common_types": high_performers['content_type'].value_counts().to_dict()
        }
    
    def _analyze_platform_performance(self, df: pd.DataFrame) -> Dict:
        """Analyze performance by platform"""
        
        platform_stats = df.groupby('platform').agg({
            'engagement_rate': 'mean',
            'likes': 'mean',
            'comments': 'mean',
            'shares': 'mean'
        }).round(2)
        
        return platform_stats.to_dict()
    
    def _analyze_content_type_performance(self, df: pd.DataFrame) -> Dict:
        """Analyze performance by content type"""
        
        type_stats = df.groupby('content_type').agg({
            'engagement_rate': 'mean',
            'performance_tier': lambda x: (x == 'high').sum()
        }).round(2)
        
        return type_stats.to_dict()
    
    def _analyze_timing_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze timing patterns for high performance"""
        
        df['hour'] = pd.to_datetime(df['published_date']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['published_date']).dt.day_name()
        
        timing_patterns = {
            "best_hours": df.groupby('hour')['engagement_rate'].mean().nlargest(3).to_dict(),
            "best_days": df.groupby('day_of_week')['engagement_rate'].mean().nlargest(3).to_dict()
        }
        
        return timing_patterns
    
    def _analyze_ai_correlation(self, df: pd.DataFrame) -> Dict:
        """Analyze correlation between AI confidence and performance"""
        
        correlation = df['ai_confidence'].corr(df['engagement_rate'])
        
        return {
            "ai_confidence_correlation": round(correlation, 3),
            "interpretation": self._interpret_correlation(correlation)
        }
    
    def _interpret_correlation(self, correlation: float) -> str:
        """Interpret correlation strength"""
        
        if abs(correlation) >= 0.7:
            return "Strong correlation - AI confidence is a good predictor"
        elif abs(correlation) >= 0.3:
            return "Moderate correlation - AI confidence has some predictive value"
        else:
            return "Weak correlation - AI confidence needs improvement"
    
    def generate_ai_improvement_suggestions(self) -> List[str]:
        """Generate suggestions to improve AI based on performance data"""
        
        patterns = self.analyze_performance_patterns()
        suggestions = []
        
        # Platform-specific suggestions
        platform_perf = patterns.get('platform_performance', {})
        if platform_perf:
            best_platform = max(platform_perf.get('engagement_rate', {}), 
                              key=platform_perf.get('engagement_rate', {}).get, default='linkedin')
            suggestions.append(f"Focus more on {best_platform} - it shows highest engagement")
        
        # Content type suggestions
        type_perf = patterns.get('content_type_performance', {})
        if type_perf:
            best_type = max(type_perf.get('engagement_rate', {}), 
                          key=type_perf.get('engagement_rate', {}).get, default='insight_post')
            suggestions.append(f"Generate more {best_type} content - it performs best")
        
        # AI correlation suggestions
        ai_corr = patterns.get('ai_correlation', {})
        if ai_corr.get('ai_confidence_correlation', 0) < 0.3:
            suggestions.append("AI confidence scoring needs improvement - low correlation with performance")
        
        # Timing suggestions
        timing = patterns.get('timing_patterns', {})
        if timing.get('best_hours'):
            best_hour = max(timing['best_hours'], key=timing['best_hours'].get)
            suggestions.append(f"Schedule posts around {best_hour}:00 for better engagement")
        
        return suggestions
    
    def get_performance_dashboard_data(self) -> Dict:
        """Get data for performance dashboard"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Recent performance metrics
        recent_df = pd.read_sql_query('''
            SELECT * FROM content_performance 
            WHERE published_date >= date('now', '-30 days')
            ORDER BY published_date DESC
        ''', conn)
        
        conn.close()
        
        if recent_df.empty:
            return {"message": "No recent performance data"}
        
        dashboard_data = {
            "total_posts": len(recent_df),
            "avg_engagement_rate": recent_df['engagement_rate'].mean(),
            "high_performers": len(recent_df[recent_df['performance_tier'] == 'high']),
            "platform_breakdown": recent_df['platform'].value_counts().to_dict(),
            "performance_trend": recent_df.groupby(recent_df['published_date'].str[:10])['engagement_rate'].mean().to_dict(),
            "top_performing_posts": recent_df.nlargest(5, 'engagement_rate')[['content_id', 'platform', 'engagement_rate', 'content_text']].to_dict('records')
        }
        
        return dashboard_data
    
    def save_ai_learning_pattern(self, pattern_type: str, pattern_data: Dict, performance_correlation: float):
        """Save discovered patterns for AI learning"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ai_learning_patterns 
            (pattern_type, pattern_data, performance_correlation, confidence_level)
            VALUES (?, ?, ?, ?)
        ''', (
            pattern_type,
            json.dumps(pattern_data),
            performance_correlation,
            abs(performance_correlation)  # Use correlation as confidence
        ))
        
        conn.commit()
        conn.close()
        
        print(f"🧠 Saved AI learning pattern: {pattern_type}")

# Simple social media API integration for performance tracking
class SocialMediaTracker:
    def __init__(self):
        self.performance_tracker = ProsoraPerformanceTracker()
    
    def track_linkedin_performance(self, post_id: str, content_id: str):
        """Track LinkedIn post performance (simplified)"""
        
        # In production, this would use LinkedIn API
        # For now, simulate with realistic data
        
        import random
        
        metrics = {
            'views': random.randint(100, 1000),
            'likes': random.randint(5, 50),
            'comments': random.randint(0, 15),
            'shares': random.randint(0, 10),
            'clicks': random.randint(2, 25)
        }
        
        self.performance_tracker.update_performance_metrics(content_id, metrics)
        return metrics
    
    def track_twitter_performance(self, tweet_id: str, content_id: str):
        """Track Twitter post performance (simplified)"""
        
        import random
        
        metrics = {
            'views': random.randint(500, 5000),
            'likes': random.randint(10, 100),
            'comments': random.randint(0, 25),
            'shares': random.randint(0, 20),  # Retweets
            'clicks': random.randint(5, 50)
        }
        
        self.performance_tracker.update_performance_metrics(content_id, metrics)
        return metrics

if __name__ == "__main__":
    # Demo the performance tracking system
    tracker = ProsoraPerformanceTracker()
    
    # Simulate tracking some content
    sample_content = {
        'platform': 'linkedin',
        'content_type': 'insight_post',
        'content': 'AI is transforming product management...',
        'ai_confidence': 0.85,
        'source_credibility': 0.9,
        'content_quality_score': 0.8
    }
    
    content_id = tracker.track_published_content(sample_content)
    
    # Simulate performance update
    sample_metrics = {
        'views': 500,
        'likes': 25,
        'comments': 8,
        'shares': 3,
        'clicks': 12
    }
    
    tracker.update_performance_metrics(content_id, sample_metrics)
    
    # Analyze patterns
    patterns = tracker.analyze_performance_patterns()
    print("📊 Performance Patterns:")
    print(json.dumps(patterns, indent=2))
    
    # Get improvement suggestions
    suggestions = tracker.generate_ai_improvement_suggestions()
    print("\n💡 AI Improvement Suggestions:")
    for suggestion in suggestions:
        print(f"• {suggestion}")