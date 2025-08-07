#!/usr/bin/env python3
"""
Phase 2: Enhanced Prosora Intelligence with Real Source Integration
Combines AI-powered analysis with real RSS/web content fetching
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

# Import our real source fetcher
from real_source_fetcher import RealSourceFetcher, RealSourceContent
from enhanced_unified_intelligence import (
    ProsoraMetrics, EnhancedProsoraQuery, MetricsCollector, EnhancedQueryAnalyzer
)

@dataclass
class EnhancedProsoraInsight:
    """Enhanced insight with real source backing"""
    title: str
    content: str
    tier: int
    credibility: float
    evidence_sources: List[RealSourceContent]
    domains: List[str]
    frameworks: List[str]
    contrarian_angle: Optional[str] = None
    real_source_count: int = 0
    freshness_score: float = 0.0

@dataclass
class EnhancedProsoraContent:
    """Enhanced content with real source integration"""
    linkedin_posts: List[Dict]
    twitter_threads: List[Dict]
    blog_outlines: List[Dict]
    insights_summary: Dict
    evidence_report: Dict
    real_sources_used: List[Dict]
    generation_metadata: Dict

class Phase2EnhancedIntelligence:
    """Phase 2: Real source integration with enhanced AI analysis"""
    
    def __init__(self):
        load_dotenv()
        
        # Initialize components
        self.metrics_collector = MetricsCollector()
        self.real_source_fetcher = RealSourceFetcher()
        
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
                print("✅ Phase 2: AI + Real Sources initialized")
            except Exception as e:
                print(f"⚠️ AI initialization failed: {e}")
                self.query_analyzer = EnhancedQueryAnalyzer(None)
        else:
            self.query_analyzer = EnhancedQueryAnalyzer(None)
        
        # Expertise domains
        self.expertise_domains = {
            'tech': 0.3,
            'politics': 0.2,
            'product': 0.25,
            'finance': 0.25
        }
        
        print("🚀 Phase 2 Enhanced Prosora Intelligence Engine initialized")
    
    def process_query_with_real_sources(self, query_text: str) -> Tuple[Dict, ProsoraMetrics]:
        """Process query with real source integration and comprehensive metrics"""
        
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
            print(f"🚀 Phase 2 Processing: {query_text}")
            
            # Phase 1: Enhanced Query Analysis
            enhanced_query = self.query_analyzer.analyze_query_with_ai(query_text)
            
            # Update metrics from query analysis
            metrics.query_clarity = self._calculate_query_clarity(enhanced_query)
            metrics.domain_coverage = len(enhanced_query.domains)
            metrics.complexity_level = {'simple': 1, 'cross_domain': 2, 'contrarian': 3}[enhanced_query.complexity]
            metrics.intent_confidence = enhanced_query.intent_confidence
            
            print(f"✅ Query Analysis: {enhanced_query.intent} | {enhanced_query.domains} | {enhanced_query.complexity}")
            
            # Phase 2: Real Source Fetching
            source_start = time.time()
            real_sources = self.real_source_fetcher.fetch_sources_for_query(
                enhanced_query.domains, 
                enhanced_query.semantic_keywords
            )
            metrics.source_fetch_time = time.time() - source_start
            
            print(f"✅ Real Sources Fetched: {len(real_sources)} articles")
            
            # Calculate source quality metrics
            if real_sources:
                metrics.source_quality_score = sum(s.source_credibility for s in real_sources) / len(real_sources)
                avg_freshness = sum(s.freshness_score for s in real_sources) / len(real_sources)
                avg_relevance = sum(s.relevance_score for s in real_sources) / len(real_sources)
                print(f"📊 Source Quality: {metrics.source_quality_score:.2f}, Freshness: {avg_freshness:.2f}, Relevance: {avg_relevance:.2f}")
            else:
                metrics.source_quality_score = 0.0
                print("⚠️ No real sources fetched")
            
            # Phase 3: AI-Powered Insight Generation
            insights = self._generate_ai_powered_insights(enhanced_query, real_sources)
            
            # Phase 4: Enhanced Content Generation
            content = self._generate_real_source_content(enhanced_query, insights, real_sources)
            
            # Calculate final metrics
            metrics.evidence_density = len(real_sources) / max(len(insights), 1) if insights else 0
            metrics.cross_domain_rate = len([i for i in insights if len(i.domains) > 1]) / max(len(insights), 1) if insights else 0
            metrics.content_authenticity = self._calculate_authenticity_score(content, real_sources)
            metrics.evidence_strength = metrics.source_quality_score
            metrics.engagement_potential = self._calculate_engagement_potential(content, enhanced_query, real_sources)
            metrics.uniqueness_score = self._calculate_uniqueness_score(enhanced_query, insights, real_sources)
            
            metrics.total_latency = time.time() - start_time
            metrics.ai_tokens_used = self.ai_tokens_used
            
            # Store metrics
            self.metrics_collector.store_metrics(metrics)
            
            # Prepare enhanced response
            response = {
                'query_analysis': asdict(enhanced_query),
                'real_sources_fetched': len(real_sources),
                'insights_generated': len(insights),
                'content': asdict(content),
                'metrics': asdict(metrics),
                'real_sources_summary': [
                    {
                        'title': source.title,
                        'source': source.source_name,
                        'credibility': source.source_credibility,
                        'freshness': source.freshness_score,
                        'relevance': source.relevance_score,
                        'url': source.url
                    } for source in real_sources[:5]  # Top 5 sources
                ],
                'performance_summary': {
                    'total_time': f"{metrics.total_latency:.2f}s",
                    'source_fetch_time': f"{metrics.source_fetch_time:.2f}s",
                    'quality_score': f"{metrics.source_quality_score:.2f}",
                    'authenticity': f"{metrics.content_authenticity:.2f}",
                    'uniqueness': f"{metrics.uniqueness_score:.2f}",
                    'real_sources_used': len(real_sources)
                }
            }
            
            print(f"🎉 Phase 2 Complete! Sources: {len(real_sources)}, Quality: {metrics.source_quality_score:.2f}, Time: {metrics.total_latency:.2f}s")
            return response, metrics
            
        except Exception as e:
            metrics.error_count = 1
            metrics.total_latency = time.time() - start_time
            self.metrics_collector.store_metrics(metrics)
            
            print(f"❌ Phase 2 Processing failed: {e}")
            return {'error': str(e), 'metrics': asdict(metrics)}, metrics
    
    def _generate_ai_powered_insights(self, query: EnhancedProsoraQuery, real_sources: List[RealSourceContent]) -> List[EnhancedProsoraInsight]:
        """Generate insights using AI with real source content"""
        insights = []
        
        if not self.ai_available or not real_sources:
            return self._fallback_insights(query, real_sources)
        
        try:
            # Prepare source content for AI analysis
            source_summaries = []
            for source in real_sources[:5]:  # Top 5 sources
                source_summaries.append(f"Source: {source.source_name} (Credibility: {source.source_credibility})\nTitle: {source.title}\nContent: {source.content[:300]}...")
            
            # AI-powered insight generation
            insight_prompt = f"""
            You are Akash's AI assistant generating insights for the Prosora Intelligence Engine.
            
            Query: "{query.text}"
            Intent: {query.intent}
            Domains: {query.domains}
            Complexity: {query.complexity}
            
            Real Sources:
            {chr(10).join(source_summaries)}
            
            Generate 3 high-quality insights based on these real sources:
            1. One premium insight from the highest credibility source
            2. One cross-domain insight connecting multiple domains
            3. One contrarian/unique perspective
            
            For each insight, provide:
            - Title (engaging and specific)
            - Content (2-3 sentences with evidence)
            - Key frameworks that apply
            - Why this matters for Akash's expertise
            
            Write in Akash's voice: analytical, cross-domain thinking, contrarian when appropriate.
            """
            
            response = self.ai_model.generate_content(insight_prompt)
            ai_insights_text = response.text
            
            # Parse AI response into structured insights
            insights = self._parse_ai_insights(ai_insights_text, real_sources)
            
            print(f"✅ AI Generated {len(insights)} insights from real sources")
            
        except Exception as e:
            print(f"⚠️ AI insight generation failed: {e}")
            insights = self._fallback_insights(query, real_sources)
        
        return insights
    
    def _parse_ai_insights(self, ai_text: str, real_sources: List[RealSourceContent]) -> List[EnhancedProsoraInsight]:
        """Parse AI-generated insights into structured format"""
        insights = []
        
        # Simple parsing - in production would use more sophisticated NLP
        sections = ai_text.split('\n\n')
        
        for i, section in enumerate(sections[:3]):
            if len(section.strip()) > 50:  # Valid insight
                insight = EnhancedProsoraInsight(
                    title=f"AI Insight {i+1}: {section[:50]}...",
                    content=section.strip(),
                    tier=i+1,
                    credibility=0.8,  # AI-generated credibility
                    evidence_sources=real_sources[:2],  # Top 2 sources
                    domains=['tech', 'finance'],  # Default domains
                    frameworks=[f"AI Framework {i+1}"],
                    real_source_count=len(real_sources),
                    freshness_score=sum(s.freshness_score for s in real_sources[:2]) / 2 if real_sources else 0
                )
                insights.append(insight)
        
        return insights
    
    def _fallback_insights(self, query: EnhancedProsoraQuery, real_sources: List[RealSourceContent]) -> List[EnhancedProsoraInsight]:
        """Fallback insight generation without AI"""
        insights = []
        
        for i, source in enumerate(real_sources[:3]):
            insight = EnhancedProsoraInsight(
                title=f"Analysis from {source.source_name}",
                content=f"Based on {source.title}: {source.content[:200]}...",
                tier=i+1,
                credibility=source.source_credibility,
                evidence_sources=[source],
                domains=source.domains,
                frameworks=[f"{source.source_name} Framework"],
                real_source_count=1,
                freshness_score=source.freshness_score
            )
            insights.append(insight)
        
        return insights
    
    def _generate_real_source_content(self, query: EnhancedProsoraQuery, insights: List[EnhancedProsoraInsight], real_sources: List[RealSourceContent]) -> EnhancedProsoraContent:
        """Generate content with real source integration"""
        
        # LinkedIn posts with real source backing
        linkedin_posts = []
        for insight in insights[:2]:
            post_content = f"""🧠 {insight.title}

{insight.content}

📊 Backed by {insight.real_source_count} real sources including {', '.join(s.source_name for s in insight.evidence_sources[:2])}

Key insights:
• Credibility score: {insight.credibility:.2f}
• Freshness: {insight.freshness_score:.2f}
• Cross-domain analysis: {' × '.join(insight.domains)}

#Innovation #Strategy #Leadership #DataDriven"""
            
            post = {
                'content': post_content,
                'tier': f"Tier {insight.tier}",
                'credibility_score': insight.credibility,
                'evidence_count': len(insight.evidence_sources),
                'real_source_count': insight.real_source_count,
                'freshness_score': insight.freshness_score,
                'supporting_evidence': [
                    {
                        'source': source.source_name,
                        'credibility': source.source_credibility,
                        'url': source.url,
                        'title': source.title,
                        'freshness': source.freshness_score
                    } for source in insight.evidence_sources
                ],
                'domains': insight.domains,
                'frameworks': insight.frameworks
            }
            linkedin_posts.append(post)
        
        # Enhanced insights summary
        insights_summary = {
            'total_insights': len(insights),
            'real_sources_used': len(real_sources),
            'average_credibility': sum(i.credibility for i in insights) / len(insights) if insights else 0,
            'average_freshness': sum(i.freshness_score for i in insights) / len(insights) if insights else 0,
            'domains_covered': list(set(domain for insight in insights for domain in insight.domains)),
            'frameworks_applied': list(set(framework for insight in insights for framework in insight.frameworks)),
            'source_breakdown': {
                'premium': len([s for s in real_sources if s.source_tier == 'premium']),
                'standard': len([s for s in real_sources if s.source_tier == 'standard']),
                'experimental': len([s for s in real_sources if s.source_tier == 'experimental'])
            }
        }
        
        # Enhanced evidence report
        evidence_report = {
            'total_real_sources': len(real_sources),
            'average_credibility': sum(s.source_credibility for s in real_sources) / len(real_sources) if real_sources else 0,
            'average_freshness': sum(s.freshness_score for s in real_sources) / len(real_sources) if real_sources else 0,
            'average_relevance': sum(s.relevance_score for s in real_sources) / len(real_sources) if real_sources else 0,
            'source_details': [
                {
                    'name': source.source_name,
                    'title': source.title,
                    'credibility': source.source_credibility,
                    'freshness': source.freshness_score,
                    'relevance': source.relevance_score,
                    'domains': source.domains,
                    'url': source.url
                } for source in real_sources
            ]
        }
        
        # Real sources used summary
        real_sources_used = [
            {
                'source_name': source.source_name,
                'title': source.title,
                'credibility': source.source_credibility,
                'freshness': source.freshness_score,
                'url': source.url,
                'content_preview': source.content[:150] + "..."
            } for source in real_sources[:10]
        ]
        
        return EnhancedProsoraContent(
            linkedin_posts=linkedin_posts,
            twitter_threads=[],  # TODO: Implement
            blog_outlines=[],    # TODO: Implement
            insights_summary=insights_summary,
            evidence_report=evidence_report,
            real_sources_used=real_sources_used,
            generation_metadata={
                'query': query.text,
                'total_insights': len(insights),
                'real_sources_count': len(real_sources),
                'credibility_score': sum(i.credibility for i in insights) / len(insights) if insights else 0,
                'freshness_score': sum(s.freshness_score for s in real_sources) / len(real_sources) if real_sources else 0,
                'generated_at': datetime.now().isoformat(),
                'prosora_version': '2.0-phase2-real-sources'
            }
        )
    
    def _calculate_query_clarity(self, query: EnhancedProsoraQuery) -> float:
        """Calculate query clarity score"""
        clarity_score = 0.0
        clarity_score += query.intent_confidence * 0.4
        domain_specificity = sum(query.domain_weights.values()) / len(query.domain_weights) if query.domain_weights else 0
        clarity_score += domain_specificity * 0.3
        keyword_richness = min(len(query.semantic_keywords) / 10, 1.0)
        clarity_score += keyword_richness * 0.3
        return min(clarity_score, 1.0)
    
    def _calculate_authenticity_score(self, content: EnhancedProsoraContent, real_sources: List[RealSourceContent]) -> float:
        """Calculate authenticity score with real source factor"""
        base_score = 0.7
        
        # Bonus for real sources
        if real_sources:
            real_source_bonus = min(len(real_sources) / 10, 0.2)
            base_score += real_source_bonus
        
        # Bonus for cross-domain content
        if content.insights_summary['domains_covered'] and len(content.insights_summary['domains_covered']) > 1:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _calculate_engagement_potential(self, content: EnhancedProsoraContent, query: EnhancedProsoraQuery, real_sources: List[RealSourceContent]) -> float:
        """Calculate engagement potential with real source backing"""
        engagement_score = 0.5
        
        # Higher for fresh content
        if real_sources:
            avg_freshness = sum(s.freshness_score for s in real_sources) / len(real_sources)
            engagement_score += avg_freshness * 0.3
        
        # Higher for controversial topics
        if query.context_signals.get('controversy', 0) > 0.7:
            engagement_score += 0.2
        
        return min(engagement_score, 1.0)
    
    def _calculate_uniqueness_score(self, query: EnhancedProsoraQuery, insights: List[EnhancedProsoraInsight], real_sources: List[RealSourceContent]) -> float:
        """Calculate uniqueness score with real source diversity"""
        uniqueness = 0.5
        
        # Higher for contrarian complexity
        if query.complexity == 'contrarian':
            uniqueness += 0.2
        
        # Higher for source diversity
        if real_sources:
            unique_sources = len(set(s.source_name for s in real_sources))
            source_diversity_bonus = min(unique_sources / 10, 0.2)
            uniqueness += source_diversity_bonus
        
        # Higher for cross-domain insights
        cross_domain_count = len([i for i in insights if len(i.domains) > 1])
        uniqueness += min(cross_domain_count * 0.1, 0.1)
        
        return min(uniqueness, 1.0)
    
    def get_system_metrics(self, days: int = 7) -> Dict:
        """Get system performance metrics"""
        return self.metrics_collector.get_metrics_summary(days)

# Test function
def test_phase2_system():
    """Test Phase 2 system with real sources"""
    engine = Phase2EnhancedIntelligence()
    
    test_queries = [
        "AI regulation impact on fintech startups",
        "Cross-domain analysis of product strategy in tech",
        "Contrarian view on startup funding trends"
    ]
    
    for query in test_queries:
        print(f"\n🧪 Phase 2 Testing: {query}")
        response, metrics = engine.process_query_with_real_sources(query)
        
        if 'error' not in response:
            print(f"📊 Real Sources: {response['real_sources_fetched']}")
            print(f"📊 Quality: {metrics.source_quality_score:.2f}")
            print(f"📊 Time: {metrics.total_latency:.2f}s")
            print(f"📊 Authenticity: {metrics.content_authenticity:.2f}")

if __name__ == "__main__":
    test_phase2_system()