#!/usr/bin/env python3
"""
Masterclass Learning Loop Engine
Simple, creative, effective system that learns from real performance and improves content generation
"""

import sqlite3
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import re
from collections import defaultdict
import os

@dataclass
class ContentPattern:
    """Identified pattern from high-performing content"""
    pattern_id: str
    pattern_type: str  # 'opening_hook', 'structure', 'closing_cta', 'hashtag_combo'
    pattern_text: str
    avg_engagement: float
    sample_size: int
    domains: List[str]
    confidence_score: float
    discovered_date: datetime

@dataclass
class LearningInsight:
    """Actionable insight from performance analysis"""
    insight_id: str
    insight_type: str  # 'content_optimization', 'timing', 'audience_preference'
    description: str
    recommendation: str
    impact_score: float  # 0-1, how much this could improve performance
    evidence_strength: float  # 0-1, how confident we are
    applicable_domains: List[str]

@dataclass
class PerformanceFeedback:
    """Real performance feedback for learning"""
    content_id: str
    variant_type: str
    actual_engagement: float
    predicted_engagement: float
    prediction_error: float
    performance_tier: str  # 'viral', 'high', 'medium', 'low'
    audience_signals: Dict
    content_features: Dict

class PatternRecognizer:
    """Recognizes patterns in high-performing content"""
    
    def __init__(self):
        self.pattern_extractors = {
            'opening_hooks': self._extract_opening_patterns,
            'structure_patterns': self._extract_structure_patterns,
            'closing_ctas': self._extract_closing_patterns,
            'hashtag_combos': self._extract_hashtag_patterns,
            'engagement_triggers': self._extract_engagement_triggers,
            'viral_elements': self._extract_viral_elements
        }
    
    def analyze_high_performers(self, performance_data: List[Dict]) -> List[ContentPattern]:
        """Analyze high-performing content to identify patterns"""
        patterns = []
        
        # Filter for high performers (top 20% engagement)
        sorted_data = sorted(performance_data, key=lambda x: x['engagement_rate'], reverse=True)
        high_performers = sorted_data[:max(1, len(sorted_data) // 5)]
        
        print(f"🔍 Analyzing {len(high_performers)} high-performing posts for patterns...")
        
        # Extract patterns using different methods
        for pattern_type, extractor in self.pattern_extractors.items():
            type_patterns = extractor(high_performers)
            patterns.extend(type_patterns)
        
        # Filter and rank patterns by confidence
        patterns = [p for p in patterns if p.confidence_score > 0.6]
        patterns.sort(key=lambda x: x.confidence_score * x.avg_engagement, reverse=True)
        
        print(f"✅ Discovered {len(patterns)} high-confidence patterns")
        return patterns[:20]  # Top 20 patterns
    
    def _extract_opening_patterns(self, high_performers: List[Dict]) -> List[ContentPattern]:
        """Extract opening hook patterns"""
        patterns = []
        opening_phrases = defaultdict(list)
        
        for post in high_performers:
            content = post['content']
            # Extract first sentence/phrase
            first_sentence = content.split('.')[0].split('\n')[0][:100]
            
            # Look for common opening patterns
            if first_sentence.startswith(('🧠', '💡', '🔥', '📊')):
                emoji = first_sentence[0]
                opening_phrases[f"emoji_start_{emoji}"].append(post['engagement_rate'])
            
            # Pattern: "Here's what [X] about [Y]"
            if 'here\'s what' in first_sentence.lower():
                opening_phrases['heres_what_pattern'].append(post['engagement_rate'])
            
            # Pattern: "The [X] that everyone misses"
            if 'everyone misses' in first_sentence.lower() or 'most people miss' in first_sentence.lower():
                opening_phrases['everyone_misses_pattern'].append(post['engagement_rate'])
            
            # Pattern: Question opening
            if first_sentence.strip().endswith('?'):
                opening_phrases['question_opening'].append(post['engagement_rate'])
        
        # Create patterns from frequent, high-performing openings
        for pattern_key, engagements in opening_phrases.items():
            if len(engagements) >= 2:  # At least 2 examples
                pattern = ContentPattern(
                    pattern_id=f"opening_{pattern_key}",
                    pattern_type='opening_hook',
                    pattern_text=pattern_key.replace('_', ' ').title(),
                    avg_engagement=np.mean(engagements),
                    sample_size=len(engagements),
                    domains=['general'],
                    confidence_score=min(len(engagements) / 5, 1.0),  # More examples = higher confidence
                    discovered_date=datetime.now()
                )
                patterns.append(pattern)
        
        return patterns
    
    def _extract_structure_patterns(self, high_performers: List[Dict]) -> List[ContentPattern]:
        """Extract content structure patterns"""
        patterns = []
        structure_types = defaultdict(list)
        
        for post in high_performers:
            content = post['content']
            
            # Numbered list pattern
            if re.search(r'\n\d+\.', content):
                structure_types['numbered_list'].append(post['engagement_rate'])
            
            # Bullet point pattern
            if content.count('•') >= 3 or content.count('-') >= 3:
                structure_types['bullet_points'].append(post['engagement_rate'])
            
            # Framework pattern (3-2-1, etc.)
            if re.search(r'\b\d+-\d+-\d+\b', content):
                structure_types['framework_structure'].append(post['engagement_rate'])
            
            # Story structure (First... Then... Finally...)
            story_words = ['first', 'then', 'finally', 'initially', 'eventually']
            if sum(1 for word in story_words if word in content.lower()) >= 2:
                structure_types['story_structure'].append(post['engagement_rate'])
        
        # Create structure patterns
        for structure_type, engagements in structure_types.items():
            if len(engagements) >= 2:
                pattern = ContentPattern(
                    pattern_id=f"structure_{structure_type}",
                    pattern_type='structure_pattern',
                    pattern_text=structure_type.replace('_', ' ').title(),
                    avg_engagement=np.mean(engagements),
                    sample_size=len(engagements),
                    domains=['general'],
                    confidence_score=min(len(engagements) / 4, 1.0),
                    discovered_date=datetime.now()
                )
                patterns.append(pattern)
        
        return patterns
    
    def _extract_closing_patterns(self, high_performers: List[Dict]) -> List[ContentPattern]:
        """Extract closing CTA patterns"""
        patterns = []
        closing_types = defaultdict(list)
        
        for post in high_performers:
            content = post['content']
            last_sentences = content.split('\n')[-3:]  # Last 3 lines
            closing_text = ' '.join(last_sentences).lower()
            
            # Question CTA
            if closing_text.endswith('?'):
                closing_types['question_cta'].append(post['engagement_rate'])
            
            # "What do you think" pattern
            if 'what do you think' in closing_text or 'what\'s your take' in closing_text:
                closing_types['opinion_request'].append(post['engagement_rate'])
            
            # "Share your" pattern
            if 'share your' in closing_text:
                closing_types['share_request'].append(post['engagement_rate'])
            
            # "Let me know" pattern
            if 'let me know' in closing_text:
                closing_types['feedback_request'].append(post['engagement_rate'])
        
        # Create closing patterns
        for closing_type, engagements in closing_types.items():
            if len(engagements) >= 2:
                pattern = ContentPattern(
                    pattern_id=f"closing_{closing_type}",
                    pattern_type='closing_cta',
                    pattern_text=closing_type.replace('_', ' ').title(),
                    avg_engagement=np.mean(engagements),
                    sample_size=len(engagements),
                    domains=['general'],
                    confidence_score=min(len(engagements) / 3, 1.0),
                    discovered_date=datetime.now()
                )
                patterns.append(pattern)
        
        return patterns
    
    def _extract_hashtag_patterns(self, high_performers: List[Dict]) -> List[ContentPattern]:
        """Extract hashtag combination patterns"""
        patterns = []
        hashtag_combos = defaultdict(list)
        
        for post in high_performers:
            content = post['content']
            hashtags = re.findall(r'#\w+', content)
            
            if len(hashtags) >= 3:
                # Sort hashtags to create consistent combo keys
                sorted_hashtags = tuple(sorted(hashtags))
                hashtag_combos[sorted_hashtags].append(post['engagement_rate'])
        
        # Create hashtag patterns for combos that appear multiple times
        for combo, engagements in hashtag_combos.items():
            if len(engagements) >= 2:
                pattern = ContentPattern(
                    pattern_id=f"hashtags_{'_'.join(combo)}",
                    pattern_type='hashtag_combo',
                    pattern_text=' '.join(combo),
                    avg_engagement=np.mean(engagements),
                    sample_size=len(engagements),
                    domains=['general'],
                    confidence_score=min(len(engagements) / 3, 1.0),
                    discovered_date=datetime.now()
                )
                patterns.append(pattern)
        
        return patterns
    
    def _extract_engagement_triggers(self, high_performers: List[Dict]) -> List[ContentPattern]:
        """Extract engagement trigger patterns"""
        patterns = []
        trigger_types = defaultdict(list)
        
        engagement_triggers = {
            'contrarian_words': ['however', 'but', 'contrarian', 'unpopular', 'different'],
            'data_points': [r'\d+%', r'\d+x', r'\$\d+', r'\d+\.\d+'],
            'personal_experience': ['my experience', 'i learned', 'when i', 'i discovered'],
            'urgency_words': ['now', 'today', 'urgent', 'critical', 'immediately'],
            'curiosity_gaps': ['secret', 'hidden', 'unknown', 'surprising', 'shocking']
        }
        
        for post in high_performers:
            content = post['content'].lower()
            
            for trigger_type, trigger_words in engagement_triggers.items():
                if trigger_type == 'data_points':
                    # Use regex for data points
                    if any(re.search(pattern, content) for pattern in trigger_words):
                        trigger_types[trigger_type].append(post['engagement_rate'])
                else:
                    # Use word matching for others
                    if any(word in content for word in trigger_words):
                        trigger_types[trigger_type].append(post['engagement_rate'])
        
        # Create trigger patterns
        for trigger_type, engagements in trigger_types.items():
            if len(engagements) >= 2:
                pattern = ContentPattern(
                    pattern_id=f"trigger_{trigger_type}",
                    pattern_type='engagement_trigger',
                    pattern_text=trigger_type.replace('_', ' ').title(),
                    avg_engagement=np.mean(engagements),
                    sample_size=len(engagements),
                    domains=['general'],
                    confidence_score=min(len(engagements) / 3, 1.0),
                    discovered_date=datetime.now()
                )
                patterns.append(pattern)
        
        return patterns
    
    def _extract_viral_elements(self, high_performers: List[Dict]) -> List[ContentPattern]:
        """Extract viral content elements"""
        patterns = []
        
        # Filter for truly viral content (top 5%)
        viral_threshold = np.percentile([p['engagement_rate'] for p in high_performers], 95)
        viral_posts = [p for p in high_performers if p['engagement_rate'] >= viral_threshold]
        
        if len(viral_posts) >= 2:
            viral_elements = defaultdict(list)
            
            for post in viral_posts:
                content = post['content']
                
                # Viral length patterns
                length = len(content)
                if 200 <= length <= 300:
                    viral_elements['optimal_length'].append(post['engagement_rate'])
                
                # Viral emoji usage
                emoji_count = len(re.findall(r'[😀-🿿]', content))
                if 2 <= emoji_count <= 5:
                    viral_elements['optimal_emoji'].append(post['engagement_rate'])
                
                # Viral question endings
                if content.strip().endswith('?'):
                    viral_elements['question_ending'].append(post['engagement_rate'])
            
            # Create viral patterns
            for element_type, engagements in viral_elements.items():
                if len(engagements) >= 2:
                    pattern = ContentPattern(
                        pattern_id=f"viral_{element_type}",
                        pattern_type='viral_element',
                        pattern_text=f"Viral {element_type.replace('_', ' ').title()}",
                        avg_engagement=np.mean(engagements),
                        sample_size=len(engagements),
                        domains=['general'],
                        confidence_score=1.0,  # High confidence for viral patterns
                        discovered_date=datetime.now()
                    )
                    patterns.append(pattern)
        
        return patterns

class LearningEngine:
    """Core learning engine that improves content generation"""
    
    def __init__(self, db_path: str = "data/learning_loop.db"):
        self.db_path = db_path
        self.pattern_recognizer = PatternRecognizer()
        self.init_learning_db()
    
    def init_learning_db(self):
        """Initialize learning database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            # Content patterns table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS content_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_type TEXT,
                    pattern_text TEXT,
                    avg_engagement REAL,
                    sample_size INTEGER,
                    domains TEXT,
                    confidence_score REAL,
                    discovered_date TEXT,
                    last_used TEXT,
                    usage_count INTEGER DEFAULT 0
                )
            """)
            
            # Learning insights table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS learning_insights (
                    insight_id TEXT PRIMARY KEY,
                    insight_type TEXT,
                    description TEXT,
                    recommendation TEXT,
                    impact_score REAL,
                    evidence_strength REAL,
                    applicable_domains TEXT,
                    created_date TEXT,
                    applied_count INTEGER DEFAULT 0
                )
            """)
            
            # Performance feedback table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_feedback (
                    content_id TEXT PRIMARY KEY,
                    variant_type TEXT,
                    actual_engagement REAL,
                    predicted_engagement REAL,
                    prediction_error REAL,
                    performance_tier TEXT,
                    audience_signals TEXT,
                    content_features TEXT,
                    feedback_date TEXT
                )
            """)
    
    def learn_from_performance(self, performance_data: List[Dict]) -> List[LearningInsight]:
        """Main learning function - analyzes performance and generates insights"""
        
        print(f"🧠 Learning from {len(performance_data)} performance data points...")
        
        # Step 1: Recognize patterns in high-performing content
        patterns = self.pattern_recognizer.analyze_high_performers(performance_data)
        
        # Step 2: Store discovered patterns
        self._store_patterns(patterns)
        
        # Step 3: Generate actionable insights
        insights = self._generate_learning_insights(performance_data, patterns)
        
        # Step 4: Store insights
        self._store_insights(insights)
        
        # Step 5: Update prediction models
        self._update_prediction_models(performance_data)
        
        print(f"✅ Learning complete: {len(patterns)} patterns, {len(insights)} insights")
        return insights
    
    def get_content_recommendations(self, query_domains: List[str], variant_type: str) -> Dict:
        """Get content recommendations based on learned patterns"""
        
        recommendations = {
            'opening_hooks': [],
            'structure_suggestions': [],
            'closing_ctas': [],
            'hashtag_combos': [],
            'engagement_triggers': [],
            'viral_elements': []
        }
        
        with sqlite3.connect(self.db_path) as conn:
            # Get relevant patterns for domains and variant type
            cursor = conn.execute("""
                SELECT pattern_type, pattern_text, avg_engagement, confidence_score
                FROM content_patterns
                WHERE (domains LIKE ? OR domains LIKE '%general%')
                AND confidence_score > 0.7
                ORDER BY avg_engagement * confidence_score DESC
                LIMIT 50
            """, (f'%{query_domains[0]}%' if query_domains else '%general%',))
            
            for row in cursor.fetchall():
                pattern_type, pattern_text, avg_engagement, confidence_score = row
                
                recommendation = {
                    'pattern': pattern_text,
                    'expected_engagement': avg_engagement,
                    'confidence': confidence_score,
                    'recommendation_strength': avg_engagement * confidence_score
                }
                
                if pattern_type in recommendations:
                    recommendations[pattern_type].append(recommendation)
        
        # Sort each category by recommendation strength
        for category in recommendations:
            recommendations[category] = sorted(
                recommendations[category], 
                key=lambda x: x['recommendation_strength'], 
                reverse=True
            )[:3]  # Top 3 per category
        
        return recommendations
    
    def get_learning_insights(self, days: int = 30) -> List[Dict]:
        """Get recent learning insights"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT insight_type, description, recommendation, impact_score, evidence_strength
                FROM learning_insights
                WHERE datetime(created_date) >= datetime('now', '-{} days')
                ORDER BY impact_score * evidence_strength DESC
                LIMIT 10
            """.format(days))
            
            insights = []
            for row in cursor.fetchall():
                insights.append({
                    'type': row[0],
                    'description': row[1],
                    'recommendation': row[2],
                    'impact_score': row[3],
                    'evidence_strength': row[4]
                })
            
            return insights
    
    def update_pattern_usage(self, pattern_ids: List[str]):
        """Update usage count for applied patterns"""
        with sqlite3.connect(self.db_path) as conn:
            for pattern_id in pattern_ids:
                conn.execute("""
                    UPDATE content_patterns 
                    SET usage_count = usage_count + 1, last_used = ?
                    WHERE pattern_id = ?
                """, (datetime.now().isoformat(), pattern_id))
    
    def _store_patterns(self, patterns: List[ContentPattern]):
        """Store discovered patterns in database"""
        with sqlite3.connect(self.db_path) as conn:
            for pattern in patterns:
                conn.execute("""
                    INSERT OR REPLACE INTO content_patterns VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, (
                    pattern.pattern_id, pattern.pattern_type, pattern.pattern_text,
                    pattern.avg_engagement, pattern.sample_size, 
                    json.dumps(pattern.domains), pattern.confidence_score,
                    pattern.discovered_date.isoformat(), None, 0
                ))
    
    def _store_insights(self, insights: List[LearningInsight]):
        """Store learning insights in database"""
        with sqlite3.connect(self.db_path) as conn:
            for insight in insights:
                conn.execute("""
                    INSERT OR REPLACE INTO learning_insights VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, (
                    insight.insight_id, insight.insight_type, insight.description,
                    insight.recommendation, insight.impact_score, insight.evidence_strength,
                    json.dumps(insight.applicable_domains), datetime.now().isoformat(), 0
                ))
    
    def _generate_learning_insights(self, performance_data: List[Dict], patterns: List[ContentPattern]) -> List[LearningInsight]:
        """Generate actionable insights from performance analysis"""
        insights = []
        
        # Insight 1: Best performing content types
        variant_performance = defaultdict(list)
        for data in performance_data:
            variant_performance[data['variant_type']].append(data['engagement_rate'])
        
        if len(variant_performance) > 1:
            best_variant = max(variant_performance.items(), key=lambda x: np.mean(x[1]))
            worst_variant = min(variant_performance.items(), key=lambda x: np.mean(x[1]))
            
            performance_gap = np.mean(best_variant[1]) - np.mean(worst_variant[1])
            
            if performance_gap > 0.1:  # Significant difference
                insight = LearningInsight(
                    insight_id=f"variant_performance_{datetime.now().strftime('%Y%m%d')}",
                    insight_type='content_optimization',
                    description=f"{best_variant[0]} variant performs {performance_gap:.2f} better than {worst_variant[0]}",
                    recommendation=f"Prioritize {best_variant[0]} variant for future content generation",
                    impact_score=min(performance_gap * 2, 1.0),
                    evidence_strength=min(len(best_variant[1]) / 10, 1.0),
                    applicable_domains=['general']
                )
                insights.append(insight)
        
        # Insight 2: High-confidence patterns
        high_confidence_patterns = [p for p in patterns if p.confidence_score > 0.8 and p.avg_engagement > 0.6]
        
        if high_confidence_patterns:
            top_pattern = max(high_confidence_patterns, key=lambda x: x.avg_engagement * x.confidence_score)
            
            insight = LearningInsight(
                insight_id=f"top_pattern_{datetime.now().strftime('%Y%m%d')}",
                insight_type='content_optimization',
                description=f"'{top_pattern.pattern_text}' pattern shows {top_pattern.avg_engagement:.2f} avg engagement",
                recommendation=f"Apply {top_pattern.pattern_type} pattern: {top_pattern.pattern_text}",
                impact_score=top_pattern.avg_engagement,
                evidence_strength=top_pattern.confidence_score,
                applicable_domains=top_pattern.domains
            )
            insights.append(insight)
        
        # Insight 3: Engagement timing patterns
        if len(performance_data) > 10:
            # Analyze performance by content length
            length_performance = [(len(d.get('content', '')), d['engagement_rate']) for d in performance_data if 'content' in d]
            
            if length_performance:
                # Find optimal length range
                sorted_by_engagement = sorted(length_performance, key=lambda x: x[1], reverse=True)
                top_performers = sorted_by_engagement[:len(sorted_by_engagement)//4]  # Top 25%
                
                optimal_lengths = [length for length, _ in top_performers]
                avg_optimal_length = np.mean(optimal_lengths)
                
                insight = LearningInsight(
                    insight_id=f"optimal_length_{datetime.now().strftime('%Y%m%d')}",
                    insight_type='content_optimization',
                    description=f"Optimal content length is around {avg_optimal_length:.0f} characters",
                    recommendation=f"Target content length between {avg_optimal_length-50:.0f}-{avg_optimal_length+50:.0f} characters",
                    impact_score=0.7,
                    evidence_strength=min(len(top_performers) / 20, 1.0),
                    applicable_domains=['general']
                )
                insights.append(insight)
        
        return insights
    
    def _update_prediction_models(self, performance_data: List[Dict]):
        """Update prediction accuracy based on actual performance"""
        
        # Store performance feedback for model improvement
        with sqlite3.connect(self.db_path) as conn:
            for data in performance_data:
                if 'predicted_engagement' in data:
                    prediction_error = abs(data['actual_engagement'] - data['predicted_engagement'])
                    
                    # Determine performance tier
                    if data['actual_engagement'] > 0.8:
                        tier = 'viral'
                    elif data['actual_engagement'] > 0.6:
                        tier = 'high'
                    elif data['actual_engagement'] > 0.3:
                        tier = 'medium'
                    else:
                        tier = 'low'
                    
                    conn.execute("""
                        INSERT OR REPLACE INTO performance_feedback VALUES (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?
                        )
                    """, (
                        data['content_id'], data['variant_type'],
                        data['actual_engagement'], data['predicted_engagement'],
                        prediction_error, tier,
                        json.dumps(data.get('audience_signals', {})),
                        json.dumps(data.get('content_features', {})),
                        datetime.now().isoformat()
                    ))
        
        print("✅ Prediction models updated with latest performance data")

# Test function with mock data
def test_learning_loop():
    """Test the learning loop with mock performance data"""
    
    # Create mock performance data
    mock_performance_data = [
        {
            'content_id': 'post_1',
            'variant_type': 'analytical',
            'engagement_rate': 0.85,
            'actual_engagement': 0.85,
            'predicted_engagement': 0.75,
            'content': '🧠 Here\'s what most people miss about AI regulation: The intersection of tech and policy reveals surprising opportunities. My experience in both engineering and consulting shows... What do you think? #AI #Policy #Innovation'
        },
        {
            'content_id': 'post_2',
            'variant_type': 'engaging',
            'engagement_rate': 0.72,
            'actual_engagement': 0.72,
            'predicted_engagement': 0.68,
            'content': '💡 Last week, I discovered something surprising about fintech regulation... Here\'s the story: • First, I analyzed the data • Then, I talked to policy experts • Finally, I realized the opportunity Share your thoughts! #Fintech #Regulation'
        },
        {
            'content_id': 'post_3',
            'variant_type': 'contrarian',
            'engagement_rate': 0.91,
            'actual_engagement': 0.91,
            'predicted_engagement': 0.70,
            'content': '🔥 Contrarian take: Everyone says remote work kills productivity, but my analysis of 500+ startups shows the opposite. The data reveals... Am I wrong? What\'s your experience? #RemoteWork #Productivity #Contrarian'
        },
        {
            'content_id': 'post_4',
            'variant_type': 'data_driven',
            'engagement_rate': 0.68,
            'actual_engagement': 0.68,
            'predicted_engagement': 0.72,
            'content': '📊 Data analysis: 73% of fintech startups fail at regulatory compliance. Key insight: Cross-domain expertise increases success rate by 2.3x. Framework applied: Technical-Regulatory Bridge Analysis. What data points are you tracking? #Data #Fintech #Analysis'
        }
    ]
    
    # Initialize learning engine
    learning_engine = LearningEngine()
    
    # Learn from performance data
    insights = learning_engine.learn_from_performance(mock_performance_data)
    
    # Get content recommendations
    recommendations = learning_engine.get_content_recommendations(['tech', 'finance'], 'contrarian')
    
    # Display results
    print(f"\n📊 Learning Results:")
    print(f"Generated {len(insights)} insights")
    
    for insight in insights:
        print(f"\n💡 {insight.insight_type.title()}: {insight.description}")
        print(f"   Recommendation: {insight.recommendation}")
        print(f"   Impact: {insight.impact_score:.2f}, Confidence: {insight.evidence_strength:.2f}")
    
    print(f"\n🎯 Content Recommendations:")
    for category, recs in recommendations.items():
        if recs:
            print(f"\n{category.title()}:")
            for rec in recs[:2]:
                print(f"  • {rec['pattern']} (Engagement: {rec['expected_engagement']:.2f})")

if __name__ == "__main__":
    test_learning_loop()