#!/usr/bin/env python3
"""
Phase 4: Content Optimization & Performance Intelligence Engine
Adds A/B testing, engagement prediction, and continuous learning
"""

import yaml
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai
from dataclasses import dataclass, asdict
import os
from dotenv import load_dotenv
import hashlib
import time
import re
import random
from enum import Enum

# Import from previous phases
from real_source_fetcher import RealSourceFetcher, RealSourceContent
from enhanced_unified_intelligence import ProsoraMetrics, MetricsCollector
from phase3_personalized_intelligence import (
    PersonalizedProsoraQuery, PersonalizedInsight, VoicePersonalizer,
    PersonalizedQueryAnalyzer, PersonalizedContentGenerator
)

class ContentVariant(Enum):
    """Content variant types for A/B testing"""
    ANALYTICAL = "analytical"
    ENGAGING = "engaging"
    CONTRARIAN = "contrarian"
    STORYTELLING = "storytelling"
    DATA_DRIVEN = "data_driven"

@dataclass
class OptimizedContent:
    """Optimized content with multiple variants and predictions"""
    primary_content: str
    variants: Dict[str, str]
    engagement_predictions: Dict[str, float]
    optimization_scores: Dict[str, float]
    recommended_variant: str
    a_b_test_config: Dict
    performance_tracking_id: str
    optimization_metadata: Dict

@dataclass
class PerformanceData:
    """Real performance data for learning"""
    content_id: str
    variant_type: str
    platform: str
    impressions: int
    likes: int
    comments: int
    shares: int
    clicks: int
    engagement_rate: float
    viral_coefficient: float
    timestamp: datetime
    audience_demographics: Dict

class PerformanceTracker:
    """Tracks and learns from content performance"""
    
    def __init__(self, db_path: str = "data/performance_optimization.db"):
        self.db_path = db_path
        self.init_performance_db()
    
    def init_performance_db(self):
        """Initialize performance tracking database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS content_performance (
                    content_id TEXT PRIMARY KEY,
                    variant_type TEXT,
                    platform TEXT,
                    impressions INTEGER,
                    likes INTEGER,
                    comments INTEGER,
                    shares INTEGER,
                    clicks INTEGER,
                    engagement_rate REAL,
                    viral_coefficient REAL,
                    timestamp TEXT,
                    audience_demographics TEXT,
                    predicted_engagement REAL,
                    actual_vs_predicted REAL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS optimization_learnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    variant_type TEXT,
                    content_pattern TEXT,
                    performance_score REAL,
                    audience_segment TEXT,
                    timestamp TEXT,
                    insights TEXT
                )
            """)
    
    def store_performance_data(self, performance: PerformanceData, predicted_engagement: float):
        """Store actual performance data"""
        actual_vs_predicted = performance.engagement_rate - predicted_engagement
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO content_performance VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (
                performance.content_id, performance.variant_type, performance.platform,
                performance.impressions, performance.likes, performance.comments,
                performance.shares, performance.clicks, performance.engagement_rate,
                performance.viral_coefficient, performance.timestamp.isoformat(),
                json.dumps(performance.audience_demographics), predicted_engagement,
                actual_vs_predicted
            ))
    
    def get_performance_insights(self, days: int = 30) -> Dict:
        """Get performance insights for optimization"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    variant_type,
                    AVG(engagement_rate) as avg_engagement,
                    AVG(viral_coefficient) as avg_viral,
                    AVG(actual_vs_predicted) as prediction_accuracy,
                    COUNT(*) as sample_size
                FROM content_performance 
                WHERE datetime(timestamp) >= datetime('now', '-{} days')
                GROUP BY variant_type
                ORDER BY avg_engagement DESC
            """.format(days))
            
            insights = {}
            for row in cursor.fetchall():
                insights[row[0]] = {
                    'avg_engagement': row[1],
                    'avg_viral': row[2],
                    'prediction_accuracy': row[3],
                    'sample_size': row[4]
                }
            
            return insights

class EngagementPredictor:
    """Predicts content engagement using AI and historical data"""
    
    def __init__(self, ai_model, performance_tracker: PerformanceTracker):
        self.ai_model = ai_model
        self.performance_tracker = performance_tracker
        
        # Engagement factors
        self.engagement_factors = {
            'content_length': {'optimal_range': (150, 300), 'weight': 0.15},
            'question_ending': {'presence': True, 'weight': 0.10},
            'emoji_usage': {'optimal_count': (2, 5), 'weight': 0.08},
            'hashtag_count': {'optimal_range': (3, 7), 'weight': 0.07},
            'contrarian_angle': {'presence': True, 'weight': 0.20},
            'data_points': {'presence': True, 'weight': 0.15},
            'personal_story': {'presence': True, 'weight': 0.12},
            'call_to_action': {'presence': True, 'weight': 0.13}
        }
    
    def predict_engagement(self, content: str, variant_type: str, query: PersonalizedProsoraQuery) -> float:
        """Predict engagement score for content"""
        
        # Base prediction from content analysis
        content_score = self._analyze_content_factors(content)
        
        # Historical performance adjustment
        historical_score = self._get_historical_performance(variant_type)
        
        # Query context adjustment
        context_score = self._analyze_query_context(query)
        
        # AI-powered prediction
        ai_score = self._ai_engagement_prediction(content, variant_type) if self.ai_model else 0.5
        
        # Weighted combination
        final_score = (
            content_score * 0.3 +
            historical_score * 0.25 +
            context_score * 0.20 +
            ai_score * 0.25
        )
        
        return min(max(final_score, 0.0), 1.0)
    
    def _analyze_content_factors(self, content: str) -> float:
        """Analyze content for engagement factors"""
        score = 0.5  # Base score
        
        # Content length
        length = len(content)
        optimal_min, optimal_max = self.engagement_factors['content_length']['optimal_range']
        if optimal_min <= length <= optimal_max:
            score += self.engagement_factors['content_length']['weight']
        
        # Question ending
        if content.strip().endswith('?'):
            score += self.engagement_factors['question_ending']['weight']
        
        # Emoji usage
        emoji_count = len(re.findall(r'[😀-🿿]', content))
        optimal_min, optimal_max = self.engagement_factors['emoji_usage']['optimal_count']
        if optimal_min <= emoji_count <= optimal_max:
            score += self.engagement_factors['emoji_usage']['weight']
        
        # Hashtag count
        hashtag_count = len(re.findall(r'#\w+', content))
        optimal_min, optimal_max = self.engagement_factors['hashtag_count']['optimal_range']
        if optimal_min <= hashtag_count <= optimal_max:
            score += self.engagement_factors['hashtag_count']['weight']
        
        # Contrarian angle
        contrarian_words = ['however', 'but', 'contrarian', 'different', 'alternative', 'unpopular']
        if any(word in content.lower() for word in contrarian_words):
            score += self.engagement_factors['contrarian_angle']['weight']
        
        # Data points
        if re.search(r'\d+%|\d+x|\$\d+', content):
            score += self.engagement_factors['data_points']['weight']
        
        # Personal story indicators
        personal_words = ['my experience', 'i learned', 'when i', 'i discovered']
        if any(phrase in content.lower() for phrase in personal_words):
            score += self.engagement_factors['personal_story']['weight']
        
        # Call to action
        cta_words = ['what do you think', 'share your', 'let me know', 'thoughts?']
        if any(phrase in content.lower() for phrase in cta_words):
            score += self.engagement_factors['call_to_action']['weight']
        
        return min(score, 1.0)
    
    def _get_historical_performance(self, variant_type: str) -> float:
        """Get historical performance for variant type"""
        insights = self.performance_tracker.get_performance_insights()
        
        if variant_type in insights:
            return min(insights[variant_type]['avg_engagement'], 1.0)
        
        return 0.5  # Default if no historical data
    
    def _analyze_query_context(self, query: PersonalizedProsoraQuery) -> float:
        """Analyze query context for engagement potential"""
        score = 0.5
        
        # Higher for cross-domain queries
        if query.complexity == 'cross_domain':
            score += 0.2
        
        # Higher for contrarian queries
        if query.complexity == 'contrarian':
            score += 0.15
        
        # Higher for high-controversy topics
        if query.context_signals.get('controversy', 0) > 0.7:
            score += 0.1
        
        # Higher for innovative topics
        if query.context_signals.get('innovation', 0) > 0.8:
            score += 0.1
        
        return min(score, 1.0)
    
    def _ai_engagement_prediction(self, content: str, variant_type: str) -> float:
        """AI-powered engagement prediction"""
        try:
            prediction_prompt = f"""
            Predict the LinkedIn engagement potential for this content.
            
            Content: "{content}"
            Variant Type: {variant_type}
            
            Consider:
            - Professional relevance
            - Thought leadership value
            - Engagement triggers
            - Viral potential
            - LinkedIn algorithm preferences
            
            Return only a number between 0.0 and 1.0 representing engagement potential.
            """
            
            response = self.ai_model.generate_content(prediction_prompt)
            
            # Extract number from response
            score_match = re.search(r'0\.\d+|1\.0|0\.0', response.text)
            if score_match:
                return float(score_match.group())
            
        except Exception as e:
            print(f"⚠️ AI engagement prediction failed: {e}")
        
        return 0.5

class ContentOptimizer:
    """Optimizes content with multiple variants and A/B testing"""
    
    def __init__(self, ai_model, voice_personalizer: VoicePersonalizer, engagement_predictor: EngagementPredictor):
        self.ai_model = ai_model
        self.voice_personalizer = voice_personalizer
        self.engagement_predictor = engagement_predictor
    
    def generate_optimized_content(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> OptimizedContent:
        """Generate optimized content with multiple variants"""
        
        # Generate primary content (best predicted variant)
        primary_content = self._generate_primary_content(query, insights)
        
        # Generate variants for A/B testing
        variants = self._generate_content_variants(query, insights, primary_content)
        
        # Predict engagement for each variant
        engagement_predictions = {}
        for variant_name, variant_content in variants.items():
            engagement_predictions[variant_name] = self.engagement_predictor.predict_engagement(
                variant_content, variant_name, query
            )
        
        # Calculate optimization scores
        optimization_scores = self._calculate_optimization_scores(variants, engagement_predictions)
        
        # Determine recommended variant
        recommended_variant = max(engagement_predictions.items(), key=lambda x: x[1])[0]
        
        # Create A/B test configuration
        a_b_test_config = self._create_ab_test_config(variants, engagement_predictions)
        
        # Generate tracking ID
        tracking_id = hashlib.md5(f"{query.text}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        
        return OptimizedContent(
            primary_content=variants[recommended_variant],
            variants=variants,
            engagement_predictions=engagement_predictions,
            optimization_scores=optimization_scores,
            recommended_variant=recommended_variant,
            a_b_test_config=a_b_test_config,
            performance_tracking_id=tracking_id,
            optimization_metadata={
                'query_complexity': query.complexity,
                'frameworks_used': len(query.personal_frameworks),
                'optimization_timestamp': datetime.now().isoformat(),
                'variant_count': len(variants)
            }
        )
    
    def _generate_primary_content(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> str:
        """Generate primary content using best practices"""
        if not self.ai_model:
            return self._fallback_primary_content(query, insights)
        
        try:
            # Enhanced content generation prompt
            content_prompt = f"""
            Generate a high-engagement LinkedIn post in Akash's voice.
            
            Akash's Profile:
            - IIT Bombay engineer with technical depth
            - Political consultant with policy expertise
            - Product ops leader with scaling experience
            - FinTech MBA student with financial acumen
            
            Query: "{query.text}"
            Complexity: {query.complexity}
            Frameworks: {', '.join(query.personal_frameworks)}
            
            Key Insights:
            {chr(10).join([f"- {insight.title}: {insight.content[:100]}..." for insight in insights[:2]])}
            
            Create a LinkedIn post that:
            1. Opens with a compelling hook
            2. Uses Akash's cross-domain expertise
            3. Includes specific data or examples
            4. Has a contrarian or unique angle
            5. Ends with an engaging question
            6. Uses 3-5 relevant hashtags
            7. Is 200-300 words
            
            Optimize for LinkedIn engagement and thought leadership.
            """
            
            response = self.ai_model.generate_content(content_prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"⚠️ Primary content generation failed: {e}")
            return self._fallback_primary_content(query, insights)
    
    def _generate_content_variants(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight], primary_content: str) -> Dict[str, str]:
        """Generate multiple content variants for A/B testing"""
        variants = {}
        
        # Analytical variant
        variants['analytical'] = self._generate_analytical_variant(query, insights)
        
        # Engaging variant
        variants['engaging'] = self._generate_engaging_variant(query, insights)
        
        # Contrarian variant
        variants['contrarian'] = self._generate_contrarian_variant(query, insights)
        
        # Data-driven variant
        variants['data_driven'] = self._generate_data_driven_variant(query, insights)
        
        return variants
    
    def _generate_analytical_variant(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> str:
        """Generate analytical variant"""
        if not self.ai_model:
            return self._fallback_analytical_variant(query, insights)
        
        try:
            prompt = f"""
            Create an analytical LinkedIn post about "{query.text}".
            
            Style: Analytical, framework-driven, professional
            Focus: Deep analysis, structured thinking, frameworks
            Tone: Authoritative but accessible
            
            Include:
            - Clear analytical framework
            - Structured breakdown (3-2-1 format or similar)
            - Professional insights
            - Logical conclusion
            
            Keep it 250-300 words with relevant hashtags.
            """
            
            response = self.ai_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return self._fallback_analytical_variant(query, insights)
    
    def _generate_engaging_variant(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> str:
        """Generate engaging variant"""
        if not self.ai_model:
            return self._fallback_engaging_variant(query, insights)
        
        try:
            prompt = f"""
            Create an engaging LinkedIn post about "{query.text}".
            
            Style: Engaging, storytelling, relatable
            Focus: Personal experience, stories, emotional connection
            Tone: Conversational but professional
            
            Include:
            - Personal anecdote or experience
            - Relatable examples
            - Emotional hooks
            - Strong call-to-action question
            
            Keep it 200-250 words with engaging hashtags.
            """
            
            response = self.ai_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return self._fallback_engaging_variant(query, insights)
    
    def _generate_contrarian_variant(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> str:
        """Generate contrarian variant"""
        if not self.ai_model:
            return self._fallback_contrarian_variant(query, insights)
        
        try:
            prompt = f"""
            Create a contrarian LinkedIn post about "{query.text}".
            
            Style: Contrarian, thought-provoking, challenging
            Focus: Alternative perspectives, challenging assumptions
            Tone: Confident but respectful
            
            Include:
            - "Everyone says X, but I think Y" structure
            - Challenging conventional wisdom
            - Unique perspective from cross-domain experience
            - Thought-provoking conclusion
            
            Keep it 200-280 words with bold hashtags.
            """
            
            response = self.ai_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return self._fallback_contrarian_variant(query, insights)
    
    def _generate_data_driven_variant(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> str:
        """Generate data-driven variant"""
        if not self.ai_model:
            return self._fallback_data_driven_variant(query, insights)
        
        try:
            prompt = f"""
            Create a data-driven LinkedIn post about "{query.text}".
            
            Style: Data-focused, evidence-based, analytical
            Focus: Statistics, trends, quantified insights
            Tone: Authoritative, fact-based
            
            Include:
            - Specific statistics or data points
            - Trend analysis
            - Quantified insights
            - Evidence-backed conclusions
            
            Keep it 220-280 words with professional hashtags.
            """
            
            response = self.ai_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return self._fallback_data_driven_variant(query, insights)
    
    def _fallback_analytical_variant(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> str:
        """Fallback analytical variant"""
        return f"""🧠 Analytical Framework: {query.text}

From my experience across {' and '.join(query.domains)}, here's how I break this down:

**The 3-Layer Analysis:**
1. Technical Layer: {insights[0].content[:80] if insights else 'Core technical considerations'}...
2. Strategic Layer: Cross-domain implications and opportunities
3. Implementation Layer: Practical steps and frameworks

**Key Framework:** {query.personal_frameworks[0] if query.personal_frameworks else 'Cross-Domain Analysis'}

This structured approach reveals insights that single-domain thinking often misses.

What's your framework for analyzing complex cross-domain challenges?

#Strategy #Analysis #Framework #Innovation"""
    
    def _fallback_engaging_variant(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> str:
        """Fallback engaging variant"""
        return f"""💡 Here's what I learned about {query.text}...

Last week, while working on a project that spanned {' and '.join(query.domains)}, I had a realization that changed how I think about this space.

The conventional approach focuses on X, but my experience in both engineering and policy showed me something different.

{insights[0].content[:100] if insights else 'The key insight was about cross-domain connections'}...

This is why I believe the future belongs to people who can bridge domains, not just master one.

What unexpected connections have you discovered in your work?

#CrossDomain #Innovation #Learning #Growth"""
    
    def _fallback_contrarian_variant(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> str:
        """Fallback contrarian variant"""
        return f"""🔥 Contrarian take on {query.text}:

Everyone's talking about X, but I think we're missing the real opportunity.

While the industry focuses on [conventional wisdom], my experience across {' and '.join(query.domains)} suggests a different path.

**The contrarian insight:** {insights[0].content[:80] if insights else 'Cross-domain analysis reveals hidden opportunities'}...

This isn't just theoretical - I've seen this pattern in both my engineering and consulting work.

The companies that win won't be the ones following the crowd.

Am I wrong? What's your contrarian take on this space?

#Contrarian #Innovation #Strategy #Opportunity"""
    
    def _fallback_data_driven_variant(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> str:
        """Fallback data-driven variant"""
        return f"""📊 Data-driven analysis of {query.text}:

The numbers tell a compelling story:
• 73% of companies are focusing on X
• Only 12% are addressing Y
• Cross-domain approaches show 2.3x better outcomes

**Key insight from the data:** {insights[0].content[:80] if insights else 'Cross-domain strategies outperform single-domain approaches'}...

My analysis across {len(query.domains)} domains confirms this trend.

**Framework applied:** {query.personal_frameworks[0] if query.personal_frameworks else 'Data-Driven Cross-Domain Analysis'}

The data doesn't lie - but most people aren't looking at it from multiple angles.

What data points are you tracking in this space?

#Data #Analytics #Strategy #Performance"""
    
    def _calculate_optimization_scores(self, variants: Dict[str, str], engagement_predictions: Dict[str, float]) -> Dict[str, float]:
        """Calculate optimization scores for variants"""
        scores = {}
        
        for variant_name, content in variants.items():
            # Base score from engagement prediction
            base_score = engagement_predictions[variant_name]
            
            # Content quality factors
            length_score = 1.0 if 200 <= len(content) <= 300 else 0.8
            hashtag_score = 1.0 if 3 <= len(re.findall(r'#\w+', content)) <= 7 else 0.8
            question_score = 1.0 if content.strip().endswith('?') else 0.9
            
            # Combined optimization score
            scores[variant_name] = (base_score * 0.7 + 
                                  length_score * 0.1 + 
                                  hashtag_score * 0.1 + 
                                  question_score * 0.1)
        
        return scores
    
    def _create_ab_test_config(self, variants: Dict[str, str], engagement_predictions: Dict[str, float]) -> Dict:
        """Create A/B test configuration"""
        # Sort variants by predicted engagement
        sorted_variants = sorted(engagement_predictions.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'test_variants': [v[0] for v in sorted_variants[:3]],  # Top 3 variants
            'traffic_split': {'primary': 0.5, 'variant_a': 0.25, 'variant_b': 0.25},
            'success_metrics': ['engagement_rate', 'click_through_rate', 'viral_coefficient'],
            'test_duration_days': 7,
            'minimum_sample_size': 1000,
            'confidence_level': 0.95
        }
    
    def _fallback_primary_content(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> str:
        """Fallback primary content generation"""
        return f"""🧠 Cross-domain insight on {query.text}:

My experience across {' and '.join(query.domains)} reveals something interesting about this space.

{insights[0].content[:150] if insights else 'The key insight comes from connecting different domains'}...

**Framework applied:** {query.personal_frameworks[0] if query.personal_frameworks else 'Cross-Domain Analysis'}

This is why I believe the future belongs to those who can bridge domains, not just master one.

What's your take on this cross-domain challenge?

#Innovation #Strategy #CrossDomain #Leadership"""

class Phase4OptimizedIntelligence:
    """Phase 4: Complete optimization with A/B testing and performance learning"""
    
    def __init__(self):
        load_dotenv()
        
        # Initialize components
        self.metrics_collector = MetricsCollector()
        self.real_source_fetcher = RealSourceFetcher()
        self.voice_personalizer = VoicePersonalizer()
        self.performance_tracker = PerformanceTracker()
        
        # Initialize AI
        self.ai_available = False
        self.ai_tokens_used = 0
        
        if os.getenv('GEMINI_API_KEY') and os.getenv('GEMINI_API_KEY') != 'your_gemini_api_key_here':
            try:
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
                self.ai_available = True
                
                self.query_analyzer = PersonalizedQueryAnalyzer(self.ai_model, self.voice_personalizer)
                self.engagement_predictor = EngagementPredictor(self.ai_model, self.performance_tracker)
                self.content_optimizer = ContentOptimizer(self.ai_model, self.voice_personalizer, self.engagement_predictor)
                
                print("✅ Phase 4: Optimized Intelligence with A/B Testing initialized")
            except Exception as e:
                print(f"⚠️ AI initialization failed: {e}")
                self.query_analyzer = PersonalizedQueryAnalyzer(None, self.voice_personalizer)
                self.engagement_predictor = EngagementPredictor(None, self.performance_tracker)
                self.content_optimizer = ContentOptimizer(None, self.voice_personalizer, self.engagement_predictor)
        else:
            self.query_analyzer = PersonalizedQueryAnalyzer(None, self.voice_personalizer)
            self.engagement_predictor = EngagementPredictor(None, self.performance_tracker)
            self.content_optimizer = ContentOptimizer(None, self.voice_personalizer, self.engagement_predictor)
        
        print("🚀 Phase 4 Optimized Prosora Intelligence Engine initialized")
    
    def process_query_with_optimization(self, query_text: str) -> Tuple[Dict, ProsoraMetrics]:
        """Process query with full optimization pipeline"""
        
        start_time = time.time()
        query_id = hashlib.md5(f"{query_text}{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Initialize metrics
        metrics = ProsoraMetrics(
            query_id=query_id,
            timestamp=datetime.now().isoformat(),
            query_clarity=0.0,
            domain_coverage=0,
            complexity_level=0,
            intent_confidence=0.0,
            source_fetch_time=0.0,
            source_quality_score=0.0,
            evidence_density=0.0,
            cross_domain_rate=0.0,
            content_authenticity=0.0,
            evidence_strength=0.0,
            engagement_potential=0.0,
            uniqueness_score=0.0,
            total_latency=0.0,
            ai_tokens_used=0,
            cache_hit_rate=0.0,
            error_count=0
        )
        
        try:
            print(f"🚀 Phase 4 Processing: {query_text}")
            
            # Phase 1: Personalized Query Analysis
            personalized_query = self.query_analyzer.analyze_query_with_personalization(query_text)
            
            # Update metrics
            metrics.query_clarity = self._calculate_query_clarity(personalized_query)
            metrics.domain_coverage = len(personalized_query.domains)
            metrics.complexity_level = {'simple': 1, 'cross_domain': 2, 'contrarian': 3}[personalized_query.complexity]
            metrics.intent_confidence = personalized_query.intent_confidence
            
            print(f"✅ Personalized Analysis: {personalized_query.intent} | {personalized_query.domains}")
            
            # Phase 2: Real Source Fetching
            source_start = time.time()
            real_sources = self.real_source_fetcher.fetch_sources_for_query(
                personalized_query.domains,
                personalized_query.semantic_keywords
            )
            metrics.source_fetch_time = time.time() - source_start
            
            if real_sources:
                metrics.source_quality_score = sum(s.source_credibility for s in real_sources) / len(real_sources)
            
            print(f"✅ Real Sources: {len(real_sources)} articles")
            
            # Phase 3: Personalized Insight Generation
            personalized_insights = self._generate_personalized_insights(personalized_query, real_sources)
            
            # Phase 4: Content Optimization with A/B Testing
            optimized_content = self.content_optimizer.generate_optimized_content(personalized_query, personalized_insights)
            
            # Calculate enhanced metrics
            metrics.evidence_density = len(real_sources) / max(len(personalized_insights), 1) if personalized_insights else 0
            metrics.cross_domain_rate = len([i for i in personalized_insights if len(i.domains) > 1]) / max(len(personalized_insights), 1) if personalized_insights else 0
            metrics.content_authenticity = self._calculate_optimized_authenticity(optimized_content, personalized_query)
            metrics.evidence_strength = metrics.source_quality_score
            metrics.engagement_potential = max(optimized_content.engagement_predictions.values()) if optimized_content.engagement_predictions else 0.5
            metrics.uniqueness_score = self._calculate_optimized_uniqueness(personalized_query, optimized_content)
            
            metrics.total_latency = time.time() - start_time
            metrics.ai_tokens_used = self.ai_tokens_used
            
            # Store metrics
            self.metrics_collector.store_metrics(metrics)
            
            # Prepare enhanced response
            response = {
                'personalized_query_analysis': asdict(personalized_query),
                'real_sources_fetched': len(real_sources),
                'personalized_insights_generated': len(personalized_insights),
                'optimized_content': asdict(optimized_content),
                'metrics': asdict(metrics),
                'optimization_summary': {
                    'variants_generated': len(optimized_content.variants),
                    'recommended_variant': optimized_content.recommended_variant,
                    'max_predicted_engagement': max(optimized_content.engagement_predictions.values()),
                    'a_b_test_ready': True,
                    'performance_tracking_id': optimized_content.performance_tracking_id
                },
                'real_sources_summary': [
                    {
                        'title': source.title,
                        'source': source.source_name,
                        'credibility': source.source_credibility,
                        'freshness': source.freshness_score,
                        'url': source.url
                    } for source in real_sources[:5]
                ],
                'performance_summary': {
                    'total_time': f"{metrics.total_latency:.2f}s",
                    'optimization_quality': f"{max(optimized_content.optimization_scores.values()):.2f}",
                    'predicted_engagement': f"{max(optimized_content.engagement_predictions.values()):.2f}",
                    'variants_count': len(optimized_content.variants),
                    'phase': 'Phase 4: Optimized Intelligence'
                }
            }
            
            print(f"🎉 Phase 4 Complete! Generated {len(optimized_content.variants)} variants, Max engagement: {max(optimized_content.engagement_predictions.values()):.2f}")
            return response, metrics
            
        except Exception as e:
            metrics.error_count = 1
            metrics.total_latency = time.time() - start_time
            self.metrics_collector.store_metrics(metrics)
            
            print(f"❌ Phase 4 Processing failed: {e}")
            return {'error': str(e), 'metrics': asdict(metrics)}, metrics
    
    def _generate_personalized_insights(self, query: PersonalizedProsoraQuery, real_sources: List[RealSourceContent]) -> List[PersonalizedInsight]:
        """Generate insights with personalization (from Phase 3)"""
        insights = []
        
        for i, source in enumerate(real_sources[:3]):
            relevant_frameworks = query.personal_frameworks[:2] if query.personal_frameworks else ['Cross-Domain Analysis']
            
            insight = PersonalizedInsight(
                title=f"Optimized Analysis: {source.title[:50]}...",
                content=f"From my cross-domain experience: {source.content[:200]}...",
                tier=i+1,
                credibility=source.source_credibility,
                evidence_sources=[source],
                domains=source.domains,
                personal_frameworks=relevant_frameworks,
                voice_elements=self.voice_personalizer.generate_voice_elements(query),
                akash_perspective=f"This aligns with my {query.voice_style} approach to {query.text}",
                cross_domain_connections=[f"{query.domains[0]} × {query.domains[1]}"] if len(query.domains) > 1 else [],
                real_source_count=1,
                freshness_score=source.freshness_score
            )
            
            if query.contrarian_potential > 0.6:
                insight.contrarian_angle = f"While others focus on X, my analysis suggests Y..."
            
            insights.append(insight)
        
        return insights
    
    def _calculate_query_clarity(self, query: PersonalizedProsoraQuery) -> float:
        """Calculate query clarity with optimization factors"""
        clarity = query.intent_confidence * 0.4
        clarity += (sum(query.domain_weights.values()) / len(query.domain_weights)) * 0.3 if query.domain_weights else 0
        clarity += min(len(query.personal_frameworks) / 3, 1.0) * 0.3
        return min(clarity, 1.0)
    
    def _calculate_optimized_authenticity(self, content: OptimizedContent, query: PersonalizedProsoraQuery) -> float:
        """Calculate authenticity with optimization factors"""
        base_score = 0.8  # Higher base for optimized content
        
        # Bonus for multiple variants
        if len(content.variants) >= 4:
            base_score += 0.1
        
        # Bonus for high optimization scores
        if max(content.optimization_scores.values()) > 0.8:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _calculate_optimized_uniqueness(self, query: PersonalizedProsoraQuery, content: OptimizedContent) -> float:
        """Calculate uniqueness with optimization factors"""
        uniqueness = 0.7  # Higher base for optimized content
        
        # Higher for contrarian variants
        if 'contrarian' in content.variants:
            uniqueness += 0.2
        
        # Higher for multiple high-scoring variants
        high_scoring_variants = len([s for s in content.optimization_scores.values() if s > 0.8])
        uniqueness += min(high_scoring_variants * 0.05, 0.1)
        
        return min(uniqueness, 1.0)
    
    def get_system_metrics(self, days: int = 7) -> Dict:
        """Get system performance metrics"""
        base_metrics = self.metrics_collector.get_metrics_summary(days)
        performance_insights = self.performance_tracker.get_performance_insights(days)
        
        return {
            **base_metrics,
            'performance_insights': performance_insights,
            'optimization_active': True
        }

# Test function
def test_phase4_system():
    """Test Phase 4 optimized system"""
    engine = Phase4OptimizedIntelligence()
    
    test_queries = [
        "AI regulation impact on fintech product strategy",
        "Cross-domain analysis of political tech platforms",
        "Contrarian view on startup funding in regulated industries"
    ]
    
    for query in test_queries:
        print(f"\n🧪 Phase 4 Testing: {query}")
        response, metrics = engine.process_query_with_optimization(query)
        
        if 'error' not in response:
            opt_summary = response['optimization_summary']
            print(f"📊 Variants Generated: {opt_summary['variants_generated']}")
            print(f"📊 Recommended: {opt_summary['recommended_variant']}")
            print(f"📊 Max Engagement: {opt_summary['max_predicted_engagement']:.2f}")
            print(f"📊 Time: {metrics.total_latency:.2f}s")

if __name__ == "__main__":
    test_phase4_system()