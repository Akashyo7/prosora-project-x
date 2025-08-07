#!/usr/bin/env python3
"""
Enhanced Unified Prosora Intelligence Engine
Phase 1: Smart Query Analysis & Metrics Foundation
"""

import yaml
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai
from dataclasses import dataclass, asdict
import os
from dotenv import load_dotenv
import hashlib
import time

@dataclass
class ProsoraMetrics:
    """Comprehensive metrics for tracking system performance"""
    query_id: str
    timestamp: str
    
    # Input metrics
    query_clarity: float
    domain_coverage: int
    complexity_level: int
    intent_confidence: float
    
    # Processing metrics
    source_fetch_time: float
    source_quality_score: float
    evidence_density: float
    cross_domain_rate: float
    
    # Output metrics
    content_authenticity: float
    evidence_strength: float
    engagement_potential: float
    uniqueness_score: float
    
    # Performance metrics
    total_latency: float
    ai_tokens_used: int
    cache_hit_rate: float
    error_count: int

@dataclass
class EnhancedProsoraQuery:
    """Enhanced query with AI-powered analysis"""
    text: str
    intent: str
    intent_confidence: float
    domains: List[str]
    domain_weights: Dict[str, float]
    complexity: str
    evidence_level: str
    semantic_keywords: List[str]
    context_signals: Dict[str, float]

@dataclass
class ProsoraSource:
    """Enhanced source with real-time data"""
    name: str
    content: str
    credibility: float
    tier: str
    domains: List[str]
    url: Optional[str] = None
    timestamp: Optional[datetime] = None
    freshness_score: float = 0.0
    relevance_score: float = 0.0

class MetricsCollector:
    """Handles metrics collection and storage"""
    
    def __init__(self, db_path: str = "data/prosora_metrics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize metrics database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prosora_metrics (
                    query_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    query_clarity REAL,
                    domain_coverage INTEGER,
                    complexity_level INTEGER,
                    intent_confidence REAL,
                    source_fetch_time REAL,
                    source_quality_score REAL,
                    evidence_density REAL,
                    cross_domain_rate REAL,
                    content_authenticity REAL,
                    evidence_strength REAL,
                    engagement_potential REAL,
                    uniqueness_score REAL,
                    total_latency REAL,
                    ai_tokens_used INTEGER,
                    cache_hit_rate REAL,
                    error_count INTEGER
                )
            """)
    
    def store_metrics(self, metrics: ProsoraMetrics):
        """Store metrics in database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO prosora_metrics VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (
                metrics.query_id, metrics.timestamp, metrics.query_clarity,
                metrics.domain_coverage, metrics.complexity_level, metrics.intent_confidence,
                metrics.source_fetch_time, metrics.source_quality_score,
                metrics.evidence_density, metrics.cross_domain_rate,
                metrics.content_authenticity, metrics.evidence_strength,
                metrics.engagement_potential, metrics.uniqueness_score,
                metrics.total_latency, metrics.ai_tokens_used,
                metrics.cache_hit_rate, metrics.error_count
            ))
    
    def get_metrics_summary(self, days: int = 7) -> Dict:
        """Get metrics summary for the last N days"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_queries,
                    AVG(query_clarity) as avg_clarity,
                    AVG(source_quality_score) as avg_source_quality,
                    AVG(content_authenticity) as avg_authenticity,
                    AVG(total_latency) as avg_latency,
                    SUM(ai_tokens_used) as total_tokens
                FROM prosora_metrics 
                WHERE datetime(timestamp) >= datetime('now', '-{} days')
            """.format(days))
            
            row = cursor.fetchone()
            return {
                'total_queries': row[0] or 0,
                'avg_clarity': row[1] or 0,
                'avg_source_quality': row[2] or 0,
                'avg_authenticity': row[3] or 0,
                'avg_latency': row[4] or 0,
                'total_tokens': row[5] or 0
            }

class EnhancedQueryAnalyzer:
    """AI-powered query analysis"""
    
    def __init__(self, ai_model):
        self.ai_model = ai_model
        self.domain_keywords = {
            'tech': ['ai', 'software', 'digital', 'automation', 'blockchain', 'crypto', 'algorithm', 'data', 'cloud', 'api'],
            'politics': ['regulation', 'policy', 'government', 'political', 'law', 'compliance', 'governance', 'public'],
            'product': ['product', 'strategy', 'market', 'user', 'growth', 'business', 'startup', 'venture', 'scale'],
            'finance': ['fintech', 'finance', 'investment', 'funding', 'banking', 'payment', 'credit', 'lending', 'wealth']
        }
    
    def analyze_query_with_ai(self, query_text: str) -> EnhancedProsoraQuery:
        """Use AI to deeply analyze the query"""
        
        analysis_prompt = f"""
        Analyze this query for Akash's Prosora Intelligence Engine: "{query_text}"
        
        Return ONLY a valid JSON object with this exact structure:
        {{
            "intent": "comprehensive",
            "intent_confidence": 0.8,
            "domains": ["tech", "finance"],
            "domain_weights": {{"tech": 0.7, "finance": 0.6}},
            "complexity": "cross_domain",
            "evidence_level": "premium",
            "semantic_keywords": ["ai", "regulation", "fintech"],
            "context_signals": {{"urgency": 0.6, "controversy": 0.7, "innovation": 0.8}}
        }}
        
        Analyze based on Akash's expertise: Tech (30%), Politics (20%), Product (25%), Finance (25%).
        """
        
        try:
            response = self.ai_model.generate_content(analysis_prompt)
            analysis = json.loads(response.text.strip())
            
            return EnhancedProsoraQuery(
                text=query_text,
                intent=analysis.get('intent', 'comprehensive'),
                intent_confidence=analysis.get('intent_confidence', 0.5),
                domains=analysis.get('domains', ['general']),
                domain_weights=analysis.get('domain_weights', {}),
                complexity=analysis.get('complexity', 'simple'),
                evidence_level=analysis.get('evidence_level', 'basic'),
                semantic_keywords=analysis.get('semantic_keywords', []),
                context_signals=analysis.get('context_signals', {})
            )
            
        except Exception as e:
            print(f"⚠️ AI analysis failed, falling back to rule-based: {e}")
            return self._fallback_analysis(query_text)
    
    def _fallback_analysis(self, query_text: str) -> EnhancedProsoraQuery:
        """Fallback rule-based analysis"""
        query_lower = query_text.lower()
        
        # Determine intent
        intent = 'comprehensive'
        intent_confidence = 0.6
        
        if any(word in query_lower for word in ['linkedin', 'post']):
            intent = 'linkedin_post'
            intent_confidence = 0.8
        elif any(word in query_lower for word in ['twitter', 'thread']):
            intent = 'twitter_thread'
            intent_confidence = 0.8
        
        # Identify domains with weights
        domains = []
        domain_weights = {}
        
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                domains.append(domain)
                domain_weights[domain] = min(score / len(keywords), 1.0)
        
        if not domains:
            domains = ['general']
            domain_weights = {'general': 1.0}
        
        # Assess complexity
        complexity = 'simple'
        if len(domains) > 1:
            complexity = 'cross_domain'
        if any(word in query_lower for word in ['contrarian', 'alternative', 'different']):
            complexity = 'contrarian'
        
        return EnhancedProsoraQuery(
            text=query_text,
            intent=intent,
            intent_confidence=intent_confidence,
            domains=domains,
            domain_weights=domain_weights,
            complexity=complexity,
            evidence_level='premium' if complexity != 'simple' else 'basic',
            semantic_keywords=query_text.split(),
            context_signals={'urgency': 0.5, 'controversy': 0.3, 'innovation': 0.7}
        )

class EnhancedUnifiedProsoraIntelligence:
    """Enhanced Prosora Intelligence Engine with metrics and AI analysis"""
    
    def __init__(self):
        load_dotenv()
        
        # Initialize components
        self.metrics_collector = MetricsCollector()
        
        # Load configuration
        with open('prosora_sources.yaml', 'r') as f:
            self.sources_config = yaml.safe_load(f)
        
        # Initialize AI
        self.ai_available = False
        self.ai_tokens_used = 0
        
        if os.getenv('GEMINI_API_KEY') and os.getenv('GEMINI_API_KEY') != 'your_gemini_api_key_here':
            try:
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
                self.ai_available = True
                self.query_analyzer = EnhancedQueryAnalyzer(self.ai_model)
                print("✅ Enhanced AI analysis initialized")
            except Exception as e:
                print(f"⚠️ AI initialization failed: {e}")
                self.query_analyzer = EnhancedQueryAnalyzer(None)
        else:
            self.query_analyzer = EnhancedQueryAnalyzer(None)
        
        # Expertise domains and weights
        self.expertise_domains = {
            'tech': 0.3,
            'politics': 0.2,
            'product': 0.25,
            'finance': 0.25
        }
        
        print("🧠 Enhanced Prosora Intelligence Engine initialized")
    
    def process_query_with_metrics(self, query_text: str) -> Tuple[Dict, ProsoraMetrics]:
        """Process query with comprehensive metrics collection"""
        
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
            print(f"🚀 Processing query with enhanced analysis: {query_text}")
            
            # Phase 1: Enhanced Query Analysis
            analysis_start = time.time()
            enhanced_query = self.query_analyzer.analyze_query_with_ai(query_text)
            
            # Update metrics from query analysis
            metrics.query_clarity = self._calculate_query_clarity(enhanced_query)
            metrics.domain_coverage = len(enhanced_query.domains)
            metrics.complexity_level = {'simple': 1, 'cross_domain': 2, 'contrarian': 3}[enhanced_query.complexity]
            metrics.intent_confidence = enhanced_query.intent_confidence
            
            print(f"✅ Enhanced analysis complete: {enhanced_query.intent} | {enhanced_query.domains} | {enhanced_query.complexity}")
            
            # Phase 2: Source Fetching (with timing)
            source_start = time.time()
            sources = self._fetch_enhanced_sources(enhanced_query)
            metrics.source_fetch_time = time.time() - source_start
            metrics.source_quality_score = sum(s.credibility for s in sources) / len(sources) if sources else 0
            
            # Phase 3: Generate insights and content
            insights = self._generate_enhanced_insights(enhanced_query, sources)
            content = self._generate_enhanced_content(enhanced_query, insights)
            
            # Calculate final metrics
            metrics.evidence_density = len(sources) / max(len(insights), 1) if insights else 0
            metrics.cross_domain_rate = len([i for i in insights if len(i.get('domains', [])) > 1]) / max(len(insights), 1) if insights else 0
            metrics.content_authenticity = self._calculate_authenticity_score(content)
            metrics.evidence_strength = metrics.source_quality_score
            metrics.engagement_potential = self._calculate_engagement_potential(content, enhanced_query)
            metrics.uniqueness_score = self._calculate_uniqueness_score(enhanced_query, insights)
            
            metrics.total_latency = time.time() - start_time
            metrics.ai_tokens_used = self.ai_tokens_used
            
            # Store metrics
            self.metrics_collector.store_metrics(metrics)
            
            # Prepare response
            response = {
                'query_analysis': asdict(enhanced_query),
                'sources_found': len(sources),
                'insights_generated': len(insights),
                'content': content,
                'metrics': asdict(metrics),
                'performance_summary': {
                    'total_time': f"{metrics.total_latency:.2f}s",
                    'quality_score': f"{metrics.source_quality_score:.2f}",
                    'authenticity': f"{metrics.content_authenticity:.2f}",
                    'uniqueness': f"{metrics.uniqueness_score:.2f}"
                }
            }
            
            print(f"🎉 Enhanced processing complete! Quality: {metrics.source_quality_score:.2f}, Time: {metrics.total_latency:.2f}s")
            return response, metrics
            
        except Exception as e:
            metrics.error_count = 1
            metrics.total_latency = time.time() - start_time
            self.metrics_collector.store_metrics(metrics)
            
            print(f"❌ Processing failed: {e}")
            return {'error': str(e), 'metrics': asdict(metrics)}, metrics
    
    def _calculate_query_clarity(self, query: EnhancedProsoraQuery) -> float:
        """Calculate how clear and well-defined the query is"""
        clarity_score = 0.0
        
        # Intent confidence contributes 40%
        clarity_score += query.intent_confidence * 0.4
        
        # Domain specificity contributes 30%
        domain_specificity = sum(query.domain_weights.values()) / len(query.domain_weights) if query.domain_weights else 0
        clarity_score += domain_specificity * 0.3
        
        # Semantic keyword richness contributes 30%
        keyword_richness = min(len(query.semantic_keywords) / 10, 1.0)
        clarity_score += keyword_richness * 0.3
        
        return min(clarity_score, 1.0)
    
    def _fetch_enhanced_sources(self, query: EnhancedProsoraQuery) -> List[ProsoraSource]:
        """Enhanced source fetching with relevance scoring"""
        sources = []
        
        # For now, still using mock data but with enhanced scoring
        premium_sources = self.sources_config.get('premium_sources', [])
        
        for source_config in premium_sources:
            source_domains = source_config.get('domains', [])
            
            # Calculate relevance score based on domain weights
            relevance_score = 0.0
            for domain in source_domains:
                if domain in query.domain_weights:
                    relevance_score += query.domain_weights[domain]
            
            if relevance_score > 0:
                # Enhanced mock content with query context
                content = f"Enhanced analysis from {source_config['name']} on {query.text}. "
                content += f"Focusing on {', '.join(source_domains)} perspectives with {relevance_score:.2f} relevance."
                
                source = ProsoraSource(
                    name=source_config['name'],
                    content=content,
                    credibility=source_config.get('credibility', 0.9),
                    tier='premium',
                    domains=source_domains,
                    url=source_config.get('url', ''),
                    timestamp=datetime.now(),
                    freshness_score=0.9,  # Mock freshness
                    relevance_score=relevance_score
                )
                sources.append(source)
        
        # Sort by relevance and credibility
        sources.sort(key=lambda x: (x.relevance_score * x.credibility), reverse=True)
        return sources[:10]  # Top 10 most relevant
    
    def _generate_enhanced_insights(self, query: EnhancedProsoraQuery, sources: List[ProsoraSource]) -> List[Dict]:
        """Generate insights with enhanced logic"""
        insights = []
        
        # Tier 1: Premium insights
        for source in sources[:3]:
            insight = {
                'title': f"Premium Analysis: {query.text}",
                'content': f"Based on {source.name}: {source.content[:200]}...",
                'tier': 1,
                'credibility': source.credibility,
                'domains': source.domains,
                'evidence_sources': [source.name],
                'relevance_score': source.relevance_score
            }
            insights.append(insight)
        
        # Cross-domain insights if applicable
        if query.complexity in ['cross_domain', 'contrarian']:
            cross_domain_insight = {
                'title': f"Cross-Domain Analysis: {' × '.join(query.domains)}",
                'content': f"Connecting insights across {', '.join(query.domains)} domains for {query.text}",
                'tier': 2,
                'credibility': 0.8,
                'domains': query.domains,
                'evidence_sources': [s.name for s in sources[:2]],
                'cross_domain': True
            }
            insights.append(cross_domain_insight)
        
        return insights
    
    def _generate_enhanced_content(self, query: EnhancedProsoraQuery, insights: List[Dict]) -> Dict:
        """Generate content with enhanced personalization"""
        content = {
            'linkedin_posts': [],
            'twitter_threads': [],
            'blog_outlines': [],
            'insights_summary': {
                'total_insights': len(insights),
                'average_credibility': sum(i['credibility'] for i in insights) / len(insights) if insights else 0,
                'domains_covered': list(set(domain for insight in insights for domain in insight.get('domains', []))),
                'cross_domain_insights': len([i for i in insights if i.get('cross_domain', False)])
            }
        }
        
        # Generate LinkedIn post if requested
        if query.intent in ['linkedin_post', 'comprehensive']:
            for insight in insights[:2]:
                post = {
                    'content': f"🧠 {insight['title']}\n\n{insight['content']}\n\n#Innovation #Strategy #Leadership",
                    'tier': f"Tier {insight['tier']}",
                    'credibility_score': insight['credibility'],
                    'evidence_count': len(insight['evidence_sources']),
                    'domains': insight['domains'],
                    'estimated_engagement': 'High' if insight['credibility'] > 0.8 else 'Medium'
                }
                content['linkedin_posts'].append(post)
        
        return content
    
    def _calculate_authenticity_score(self, content: Dict) -> float:
        """Calculate how authentic the content sounds"""
        # Mock calculation - in reality would compare against writing samples
        base_score = 0.7
        
        # Bonus for cross-domain content
        if content['insights_summary']['cross_domain_insights'] > 0:
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def _calculate_engagement_potential(self, content: Dict, query: EnhancedProsoraQuery) -> float:
        """Predict engagement potential"""
        engagement_score = 0.5
        
        # Higher for controversial topics
        if query.context_signals.get('controversy', 0) > 0.7:
            engagement_score += 0.3
        
        # Higher for innovative topics
        if query.context_signals.get('innovation', 0) > 0.7:
            engagement_score += 0.2
        
        return min(engagement_score, 1.0)
    
    def _calculate_uniqueness_score(self, query: EnhancedProsoraQuery, insights: List[Dict]) -> float:
        """Calculate how unique/contrarian the analysis is"""
        uniqueness = 0.5
        
        # Higher for contrarian complexity
        if query.complexity == 'contrarian':
            uniqueness += 0.3
        
        # Higher for cross-domain insights
        cross_domain_count = len([i for i in insights if i.get('cross_domain', False)])
        uniqueness += min(cross_domain_count * 0.1, 0.2)
        
        return min(uniqueness, 1.0)
    
    def get_system_metrics(self, days: int = 7) -> Dict:
        """Get system performance metrics"""
        return self.metrics_collector.get_metrics_summary(days)

# Test function
def test_enhanced_system():
    """Test the enhanced system"""
    engine = EnhancedUnifiedProsoraIntelligence()
    
    test_queries = [
        "AI regulation in fintech",
        "Cross-domain analysis of blockchain governance",
        "Contrarian view on crypto regulation"
    ]
    
    for query in test_queries:
        print(f"\n🧪 Testing: {query}")
        response, metrics = engine.process_query_with_metrics(query)
        print(f"📊 Quality: {metrics.source_quality_score:.2f}, Time: {metrics.total_latency:.2f}s")

if __name__ == "__main__":
    test_enhanced_system()