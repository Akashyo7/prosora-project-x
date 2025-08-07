#!/usr/bin/env python3
"""
Prosora Data Manager
Smart data storage system that scales from local to cloud
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import pandas as pd

@dataclass
class StorageConfig:
    """Configuration for data storage"""
    storage_type: str = "local"  # "local", "firebase", "hybrid"
    local_db_path: str = "data/prosora.db"
    backup_enabled: bool = True
    sync_interval: int = 3600  # seconds
    max_local_records: int = 10000

class ProsoraDataManager:
    def __init__(self, config: StorageConfig = None):
        self.config = config or StorageConfig()
        self.setup_storage()
    
    def setup_storage(self):
        """Set up storage based on configuration"""
        
        if self.config.storage_type in ["local", "hybrid"]:
            self.setup_local_storage()
        
        if self.config.storage_type in ["firebase", "hybrid"]:
            self.setup_cloud_storage()
        
        print(f"✅ Data storage initialized: {self.config.storage_type}")
    
    def setup_local_storage(self):
        """Set up local SQLite database"""
        
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(self.config.local_db_path)
        cursor = conn.cursor()
        
        # Content table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT UNIQUE,
                content_type TEXT,
                platform TEXT,
                title TEXT,
                content_text TEXT,
                source_data TEXT,
                ai_metadata TEXT,
                status TEXT DEFAULT 'draft',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_id TEXT UNIQUE,
                insight_type TEXT,
                title TEXT,
                content TEXT,
                source_credibility REAL,
                ai_confidence REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Performance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT,
                platform TEXT,
                metrics TEXT,
                engagement_rate REAL,
                performance_tier TEXT,
                tracked_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content (content_id)
            )
        ''')
        
        # User feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT,
                feedback_type TEXT,
                feedback_data TEXT,
                rating INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content (content_id)
            )
        ''')
        
        # AI learning table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_learning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                performance_correlation REAL,
                confidence_level REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def setup_cloud_storage(self):
        """Set up cloud storage (Firebase/Firestore)"""
        
        # Placeholder for Firebase setup
        # In production, this would initialize Firebase
        print("🔄 Cloud storage setup (placeholder)")
    
    def save_content(self, content_data: Dict) -> str:
        """Save content with smart storage routing"""
        
        content_id = content_data.get('content_id') or self._generate_content_id()
        
        if self.config.storage_type in ["local", "hybrid"]:
            self._save_content_local(content_id, content_data)
        
        if self.config.storage_type in ["firebase", "hybrid"]:
            self._save_content_cloud(content_id, content_data)
        
        return content_id
    
    def _save_content_local(self, content_id: str, content_data: Dict):
        """Save content to local database"""
        
        conn = sqlite3.connect(self.config.local_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO content 
            (content_id, content_type, platform, title, content_text, 
             source_data, ai_metadata, status, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            content_id,
            content_data.get('content_type', ''),
            content_data.get('platform', ''),
            content_data.get('title', ''),
            content_data.get('content', ''),
            json.dumps(content_data.get('source_data', {})),
            json.dumps(content_data.get('ai_metadata', {})),
            content_data.get('status', 'draft'),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _save_content_cloud(self, content_id: str, content_data: Dict):
        """Save content to cloud storage"""
        
        # Placeholder for cloud storage
        # In production, this would save to Firebase/Firestore
        pass
    
    def get_content(self, content_id: str = None, filters: Dict = None) -> List[Dict]:
        """Get content with smart retrieval"""
        
        if self.config.storage_type == "local":
            return self._get_content_local(content_id, filters)
        elif self.config.storage_type == "firebase":
            return self._get_content_cloud(content_id, filters)
        else:  # hybrid
            # Try local first, fallback to cloud
            local_data = self._get_content_local(content_id, filters)
            if local_data:
                return local_data
            return self._get_content_cloud(content_id, filters)
    
    def _get_content_local(self, content_id: str = None, filters: Dict = None) -> List[Dict]:
        """Get content from local database"""
        
        conn = sqlite3.connect(self.config.local_db_path)
        
        if content_id:
            query = "SELECT * FROM content WHERE content_id = ?"
            df = pd.read_sql_query(query, conn, params=(content_id,))
        else:
            query = "SELECT * FROM content ORDER BY created_at DESC"
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        # Convert to list of dictionaries
        content_list = df.to_dict('records')
        
        # Parse JSON fields
        for item in content_list:
            item['source_data'] = json.loads(item.get('source_data', '{}'))
            item['ai_metadata'] = json.loads(item.get('ai_metadata', '{}'))
        
        return content_list
    
    def _get_content_cloud(self, content_id: str = None, filters: Dict = None) -> List[Dict]:
        """Get content from cloud storage"""
        
        # Placeholder for cloud retrieval
        return []
    
    def save_performance_data(self, content_id: str, performance_data: Dict):
        """Save performance data"""
        
        conn = sqlite3.connect(self.config.local_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance 
            (content_id, platform, metrics, engagement_rate, performance_tier)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            content_id,
            performance_data.get('platform', ''),
            json.dumps(performance_data.get('metrics', {})),
            performance_data.get('engagement_rate', 0.0),
            performance_data.get('performance_tier', 'unknown')
        ))
        
        conn.commit()
        conn.close()
    
    def get_performance_analytics(self, days: int = 30) -> Dict:
        """Get performance analytics"""
        
        conn = sqlite3.connect(self.config.local_db_path)
        
        query = '''
            SELECT c.content_type, c.platform, p.engagement_rate, p.performance_tier, p.tracked_at
            FROM content c
            JOIN performance p ON c.content_id = p.content_id
            WHERE p.tracked_at >= date('now', '-{} days')
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return {"message": "No performance data available"}
        
        analytics = {
            "total_posts": len(df),
            "avg_engagement": df['engagement_rate'].mean(),
            "high_performers": len(df[df['performance_tier'] == 'high']),
            "platform_performance": df.groupby('platform')['engagement_rate'].mean().to_dict(),
            "content_type_performance": df.groupby('content_type')['engagement_rate'].mean().to_dict(),
            "performance_trend": df.groupby(df['tracked_at'].str[:10])['engagement_rate'].mean().to_dict()
        }
        
        return analytics
    
    def save_user_feedback(self, content_id: str, feedback_data: Dict):
        """Save user feedback for AI learning"""
        
        conn = sqlite3.connect(self.config.local_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_feedback 
            (content_id, feedback_type, feedback_data, rating)
            VALUES (?, ?, ?, ?)
        ''', (
            content_id,
            feedback_data.get('type', ''),
            json.dumps(feedback_data),
            feedback_data.get('rating', 0)
        ))
        
        conn.commit()
        conn.close()
    
    def get_ai_learning_data(self) -> Dict:
        """Get data for AI learning and improvement"""
        
        conn = sqlite3.connect(self.config.local_db_path)
        
        # Get feedback patterns
        feedback_df = pd.read_sql_query('''
            SELECT uf.feedback_type, uf.rating, c.content_type, c.platform
            FROM user_feedback uf
            JOIN content c ON uf.content_id = c.content_id
        ''', conn)
        
        # Get performance patterns
        performance_df = pd.read_sql_query('''
            SELECT c.content_type, c.platform, p.engagement_rate, p.performance_tier
            FROM content c
            JOIN performance p ON c.content_id = p.content_id
        ''', conn)
        
        conn.close()
        
        learning_data = {
            "feedback_patterns": self._analyze_feedback_patterns(feedback_df),
            "performance_patterns": self._analyze_performance_patterns(performance_df),
            "improvement_suggestions": self._generate_improvement_suggestions(feedback_df, performance_df)
        }
        
        return learning_data
    
    def _analyze_feedback_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze user feedback patterns"""
        
        if df.empty:
            return {"message": "No feedback data available"}
        
        return {
            "common_issues": df['feedback_type'].value_counts().to_dict(),
            "avg_rating_by_type": df.groupby('content_type')['rating'].mean().to_dict(),
            "avg_rating_by_platform": df.groupby('platform')['rating'].mean().to_dict()
        }
    
    def _analyze_performance_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze performance patterns"""
        
        if df.empty:
            return {"message": "No performance data available"}
        
        return {
            "high_performer_characteristics": df[df['performance_tier'] == 'high']['content_type'].value_counts().to_dict(),
            "platform_success_rates": df.groupby('platform')['performance_tier'].apply(lambda x: (x == 'high').mean()).to_dict(),
            "content_type_success_rates": df.groupby('content_type')['performance_tier'].apply(lambda x: (x == 'high').mean()).to_dict()
        }
    
    def _generate_improvement_suggestions(self, feedback_df: pd.DataFrame, performance_df: pd.DataFrame) -> List[str]:
        """Generate AI improvement suggestions based on data"""
        
        suggestions = []
        
        # Feedback-based suggestions
        if not feedback_df.empty:
            common_issues = feedback_df['feedback_type'].value_counts()
            if len(common_issues) > 0:
                top_issue = common_issues.index[0]
                suggestions.append(f"Focus on improving: {top_issue} (most common feedback)")
        
        # Performance-based suggestions
        if not performance_df.empty:
            platform_performance = performance_df.groupby('platform')['engagement_rate'].mean()
            if len(platform_performance) > 0:
                best_platform = platform_performance.idxmax()
                suggestions.append(f"Generate more content for {best_platform} (highest engagement)")
        
        return suggestions
    
    def _generate_content_id(self) -> str:
        """Generate unique content ID"""
        return f"content_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def backup_data(self):
        """Backup data to JSON files"""
        
        if not self.config.backup_enabled:
            return
        
        backup_dir = "data/backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Backup content
        content_data = self.get_content()
        with open(f"{backup_dir}/content_backup_{timestamp}.json", "w") as f:
            json.dump(content_data, f, indent=2)
        
        # Backup performance data
        performance_data = self.get_performance_analytics(days=365)  # Full year
        with open(f"{backup_dir}/performance_backup_{timestamp}.json", "w") as f:
            json.dump(performance_data, f, indent=2)
        
        print(f"✅ Data backed up to {backup_dir}")
    
    def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
        
        conn = sqlite3.connect(self.config.local_db_path)
        
        stats = {}
        
        # Count records in each table
        tables = ['content', 'insights', 'performance', 'user_feedback', 'ai_learning']
        for table in tables:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
            stats[f"{table}_count"] = cursor.fetchone()[0]
        
        # Database size
        stats['db_size_mb'] = os.path.getsize(self.config.local_db_path) / (1024 * 1024)
        
        conn.close()
        
        return stats

# Simple usage example
if __name__ == "__main__":
    # Initialize data manager
    data_manager = ProsoraDataManager()
    
    # Save sample content
    sample_content = {
        'content_type': 'linkedin_post',
        'platform': 'linkedin',
        'title': 'AI in Product Management',
        'content': 'AI is transforming how we build products...',
        'source_data': {'source': 'a16z', 'credibility': 0.9},
        'ai_metadata': {'confidence': 0.85, 'quality_score': 0.8},
        'status': 'approved'
    }
    
    content_id = data_manager.save_content(sample_content)
    print(f"✅ Saved content: {content_id}")
    
    # Save sample performance data
    performance_data = {
        'platform': 'linkedin',
        'metrics': {'views': 500, 'likes': 25, 'comments': 8},
        'engagement_rate': 6.6,
        'performance_tier': 'high'
    }
    
    data_manager.save_performance_data(content_id, performance_data)
    print("✅ Saved performance data")
    
    # Get analytics
    analytics = data_manager.get_performance_analytics()
    print("📊 Analytics:", json.dumps(analytics, indent=2))
    
    # Get storage stats
    stats = data_manager.get_storage_stats()
    print("💾 Storage Stats:", json.dumps(stats, indent=2))