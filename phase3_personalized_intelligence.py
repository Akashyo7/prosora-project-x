#!/usr/bin/env python3
"""
Phase 3: AI-Powered Personalized Intelligence Engine
Focuses on voice personalization, personal frameworks, and intelligent content generation
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
import re

# Import from previous phases
from real_source_fetcher import RealSourceFetcher, RealSourceContent
from enhanced_unified_intelligence import ProsoraMetrics, MetricsCollector

@dataclass
class PersonalizedProsoraQuery:
    """Enhanced query with personalization context"""
    text: str
    intent: str
    intent_confidence: float
    domains: List[str]
    domain_weights: Dict[str, float]
    complexity: str
    evidence_level: str
    semantic_keywords: List[str]
    context_signals: Dict[str, float]
    personal_frameworks: List[str]
    voice_style: str
    contrarian_potential: float

@dataclass
class PersonalizedInsight:
    """Personalized insight with voice and framework integration"""
    title: str
    content: str
    tier: int
    credibility: float
    evidence_sources: List[RealSourceContent]
    domains: List[str]
    personal_frameworks: List[str]
    voice_elements: List[str]
    contrarian_angle: Optional[str] = None
    akash_perspective: str = ""
    cross_domain_connections: List[str] = None
    real_source_count: int = 0
    freshness_score: float = 0.0

class VoicePersonalizer:
    """Handles Akash's voice personalization and style"""
    
    def __init__(self):
        # Akash's voice characteristics
        self.voice_profile = {
            'background': "IIT Bombay engineer, political consultant, product ops lead, FinTech MBA student",
            'expertise_domains': ['tech', 'politics', 'product', 'finance'],
            'thinking_style': 'analytical, cross-domain, contrarian when appropriate',
            'communication_style': 'professional but engaging, data-driven, framework-oriented',
            'unique_angles': [
                'Cross-domain connections between tech and policy',
                'Product management in regulated industries',
                'Engineering perspective on business strategy',
                'Political analysis of tech trends'
            ]
        }
        
        # Personal frameworks
        self.personal_frameworks = {
            'IIT-MBA Technical Leadership': {
                'description': 'Combining engineering rigor with business strategy',
                'application': 'Technical product decisions, scaling challenges',
                'domains': ['tech', 'product']
            },
            'Political Product Management': {
                'description': 'Product strategy in regulated/political environments',
                'application': 'Compliance-first product development, stakeholder management',
                'domains': ['politics', 'product']
            },
            'Fintech Regulatory Navigation': {
                'description': 'Building financial products within regulatory constraints',
                'application': 'Fintech strategy, compliance automation',
                'domains': ['finance', 'politics']
            },
            'Cross-Domain Innovation': {
                'description': 'Finding innovation at the intersection of domains',
                'application': 'Identifying unique opportunities, contrarian analysis',
                'domains': ['tech', 'politics', 'product', 'finance']
            }
        }
        
        # Voice patterns and phrases
        self.voice_patterns = {
            'opening_hooks': [
                "Here's what most people miss about",
                "The intersection of {domain1} and {domain2} reveals",
                "My experience in both {domain1} and {domain2} shows",
                "From an engineering perspective,",
                "Having worked in both startups and policy,"
            ],
            'analytical_transitions': [
                "Breaking this down:",
                "The data suggests:",
                "From a systems thinking perspective:",
                "Looking at this through multiple lenses:"
            ],
            'contrarian_signals': [
                "The conventional wisdom says... but I think",
                "Everyone's focused on X, but the real opportunity is Y",
                "While others see a problem, I see",
                "The contrarian take:"
            ],
            'framework_introductions': [
                "Using my {framework} framework:",
                "This maps to what I call the {framework}:",
                "In my experience with {framework}:"
            ]
        }
    
    def get_relevant_frameworks(self, domains: List[str]) -> List[str]:
        """Get relevant personal frameworks for given domains"""
        relevant = []
        for framework, details in self.personal_frameworks.items():
            if any(domain in details['domains'] for domain in domains):
                relevant.append(framework)
        return relevant
    
    def generate_voice_elements(self, query: PersonalizedProsoraQuery) -> List[str]:
        """Generate voice elements for personalization"""
        elements = []
        
        # Add domain-specific expertise signals
        if 'tech' in query.domains and 'product' in query.domains:
            elements.append("engineering_product_perspective")
        if 'politics' in query.domains:
            elements.append("political_consultant_insight")
        if 'finance' in query.domains:
            elements.append("fintech_mba_knowledge")
        
        # Add complexity-based voice elements
        if query.complexity == 'cross_domain':
            elements.append("cross_domain_synthesis")
        if query.complexity == 'contrarian':
            elements.append("contrarian_analysis")
        
        return elements

class PersonalizedQueryAnalyzer:
    """Enhanced query analyzer with personalization"""
    
    def __init__(self, ai_model, voice_personalizer: VoicePersonalizer):
        self.ai_model = ai_model
        self.voice_personalizer = voice_personalizer
    
    def analyze_query_with_personalization(self, query_text: str) -> PersonalizedProsoraQuery:
        """Analyze query with personalization context"""
        
        if not self.ai_model:
            return self._fallback_analysis(query_text)
        
        try:
            # Enhanced prompt with better JSON structure
            analysis_prompt = f"""
            Analyze this query for Akash's Prosora Intelligence Engine.
            
            Akash's Background:
            - IIT Bombay engineer with technical depth
            - Political consultant with policy expertise  
            - Product ops lead with scaling experience
            - FinTech MBA student with financial knowledge
            
            Query: "{query_text}"
            
            Return a valid JSON object with this structure:
            {{
                "intent": "linkedin_post",
                "intent_confidence": 0.85,
                "domains": ["tech", "finance"],
                "domain_weights": {{"tech": 0.8, "finance": 0.7}},
                "complexity": "cross_domain",
                "evidence_level": "premium",
                "semantic_keywords": ["ai", "regulation", "fintech"],
                "context_signals": {{"urgency": 0.6, "controversy": 0.7, "innovation": 0.8}},
                "personal_frameworks": ["IIT-MBA Technical Leadership", "Fintech Regulatory Navigation"],
                "voice_style": "analytical_cross_domain",
                "contrarian_potential": 0.6
            }}
            
            Focus on Akash's unique cross-domain expertise and contrarian thinking ability.
            """
            
            response = self.ai_model.generate_content(analysis_prompt)
            
            # Clean the response to extract JSON
            response_text = response.text.strip()
            
            # Find JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group()
                analysis = json.loads(json_text)
                
                return PersonalizedProsoraQuery(
                    text=query_text,
                    intent=analysis.get('intent', 'comprehensive'),
                    intent_confidence=analysis.get('intent_confidence', 0.7),
                    domains=analysis.get('domains', ['general']),
                    domain_weights=analysis.get('domain_weights', {}),
                    complexity=analysis.get('complexity', 'simple'),
                    evidence_level=analysis.get('evidence_level', 'basic'),
                    semantic_keywords=analysis.get('semantic_keywords', []),
                    context_signals=analysis.get('context_signals', {}),
                    personal_frameworks=analysis.get('personal_frameworks', []),
                    voice_style=analysis.get('voice_style', 'professional'),
                    contrarian_potential=analysis.get('contrarian_potential', 0.3)
                )
            else:
                print("⚠️ No JSON found in AI response, using fallback")
                return self._fallback_analysis(query_text)
                
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}, using fallback")
            return self._fallback_analysis(query_text)
    
    def _fallback_analysis(self, query_text: str) -> PersonalizedProsoraQuery:
        """Fallback analysis with personalization"""
        query_lower = query_text.lower()
        
        # Determine domains
        domains = []
        domain_weights = {}
        
        domain_keywords = {
            'tech': ['ai', 'software', 'digital', 'automation', 'blockchain', 'algorithm'],
            'politics': ['regulation', 'policy', 'government', 'political', 'law', 'compliance'],
            'product': ['product', 'strategy', 'market', 'user', 'growth', 'business'],
            'finance': ['fintech', 'finance', 'investment', 'funding', 'banking', 'payment']
        }
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                domains.append(domain)
                domain_weights[domain] = min(score / len(keywords), 1.0)
        
        if not domains:
            domains = ['general']
            domain_weights = {'general': 1.0}
        
        # Determine complexity
        complexity = 'simple'
        if len(domains) > 1:
            complexity = 'cross_domain'
        if any(word in query_lower for word in ['contrarian', 'alternative', 'different']):
            complexity = 'contrarian'
        
        # Get relevant frameworks
        relevant_frameworks = self.voice_personalizer.get_relevant_frameworks(domains)
        
        return PersonalizedProsoraQuery(
            text=query_text,
            intent='comprehensive',
            intent_confidence=0.7,
            domains=domains,
            domain_weights=domain_weights,
            complexity=complexity,
            evidence_level='premium' if complexity != 'simple' else 'basic',
            semantic_keywords=query_text.split(),
            context_signals={'urgency': 0.5, 'controversy': 0.3, 'innovation': 0.7},
            personal_frameworks=relevant_frameworks,
            voice_style='analytical_cross_domain' if len(domains) > 1 else 'professional',
            contrarian_potential=0.7 if complexity == 'contrarian' else 0.3
        )

class PersonalizedContentGenerator:
    """Generates content with Akash's voice and frameworks"""
    
    def __init__(self, ai_model, voice_personalizer: VoicePersonalizer):
        self.ai_model = ai_model
        self.voice_personalizer = voice_personalizer
    
    def generate_personalized_linkedin_post(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> Dict:
        """Generate LinkedIn post in Akash's voice"""
        
        if not self.ai_model or not insights:
            return self._fallback_linkedin_post(query, insights)
        
        try:
            # Prepare insight summaries
            insight_summaries = []
            for insight in insights[:2]:
                summary = f"- {insight.title}: {insight.content[:150]}..."
                if insight.evidence_sources:
                    summary += f" (Source: {insight.evidence_sources[0].source_name})"
                insight_summaries.append(summary)
            
            # Generate personalized content
            content_prompt = f"""
            Write a LinkedIn post in Akash's voice based on this analysis.
            
            Akash's Profile:
            - IIT Bombay engineer turned product leader
            - Political consultant with policy expertise
            - FinTech MBA student
            - Known for cross-domain thinking and contrarian insights
            
            Query: "{query.text}"
            Complexity: {query.complexity}
            Domains: {', '.join(query.domains)}
            Personal Frameworks: {', '.join(query.personal_frameworks)}
            
            Key Insights:
            {chr(10).join(insight_summaries)}
            
            Write a LinkedIn post that:
            1. Opens with Akash's unique perspective
            2. Uses his cross-domain expertise
            3. Includes relevant frameworks
            4. Sounds analytical but engaging
            5. Includes a contrarian angle if appropriate
            6. Ends with a thought-provoking question
            
            Keep it under 300 words, professional but personal.
            Use emojis sparingly and strategically.
            """
            
            response = self.ai_model.generate_content(content_prompt)
            content_text = response.text.strip()
            
            # Calculate metrics
            credibility = sum(i.credibility for i in insights) / len(insights) if insights else 0.7
            evidence_count = sum(len(i.evidence_sources) for i in insights)
            
            return {
                'content': content_text,
                'tier': 'Personalized',
                'credibility_score': credibility,
                'evidence_count': evidence_count,
                'personal_frameworks': query.personal_frameworks,
                'voice_elements': self.voice_personalizer.generate_voice_elements(query),
                'domains': query.domains,
                'authenticity_score': 0.9,  # High for personalized content
                'supporting_evidence': [
                    {
                        'source': source.source_name,
                        'credibility': source.source_credibility,
                        'url': source.url,
                        'title': source.title
                    } for insight in insights for source in insight.evidence_sources
                ]
            }
            
        except Exception as e:
            print(f"⚠️ Personalized content generation failed: {e}")
            return self._fallback_linkedin_post(query, insights)
    
    def _fallback_linkedin_post(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> Dict:
        """Fallback LinkedIn post generation"""
        
        # Use templates with personalization
        opening = f"As someone who's worked across {' and '.join(query.domains)}, here's what I'm seeing with {query.text}:"
        
        content_parts = [opening]
        
        for insight in insights[:2]:
            content_parts.append(f"\n• {insight.title}")
            content_parts.append(f"  {insight.content[:100]}...")
        
        if query.personal_frameworks:
            content_parts.append(f"\nUsing my {query.personal_frameworks[0]} framework, this suggests...")
        
        content_parts.append(f"\nWhat's your take on this cross-domain challenge?")
        content_parts.append(f"\n#Innovation #Strategy #{query.domains[0].title()}Strategy")
        
        return {
            'content': ''.join(content_parts),
            'tier': 'Template-Personalized',
            'credibility_score': 0.8,
            'evidence_count': len(insights),
            'personal_frameworks': query.personal_frameworks,
            'voice_elements': ['cross_domain_perspective'],
            'domains': query.domains,
            'authenticity_score': 0.7
        }

class Phase3PersonalizedIntelligence:
    """Phase 3: Personalized Intelligence with Voice and Frameworks"""
    
    def __init__(self):
        load_dotenv()
        
        # Initialize components
        self.metrics_collector = MetricsCollector()
        self.real_source_fetcher = RealSourceFetcher()
        self.voice_personalizer = VoicePersonalizer()
        
        # Initialize AI
        self.ai_available = False
        self.ai_tokens_used = 0
        
        if os.getenv('GEMINI_API_KEY') and os.getenv('GEMINI_API_KEY') != 'your_gemini_api_key_here':
            try:
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
                self.ai_available = True
                
                self.query_analyzer = PersonalizedQueryAnalyzer(self.ai_model, self.voice_personalizer)
                self.content_generator = PersonalizedContentGenerator(self.ai_model, self.voice_personalizer)
                
                print("✅ Phase 3: Personalized AI Intelligence initialized")
            except Exception as e:
                print(f"⚠️ AI initialization failed: {e}")
                self.query_analyzer = PersonalizedQueryAnalyzer(None, self.voice_personalizer)
                self.content_generator = PersonalizedContentGenerator(None, self.voice_personalizer)
        else:
            self.query_analyzer = PersonalizedQueryAnalyzer(None, self.voice_personalizer)
            self.content_generator = PersonalizedContentGenerator(None, self.voice_personalizer)
        
        print("🚀 Phase 3 Personalized Prosora Intelligence Engine initialized")
    
    def process_query_with_personalization(self, query_text: str) -> Tuple[Dict, ProsoraMetrics]:
        """Process query with full personalization pipeline"""
        
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
            print(f"🚀 Phase 3 Processing: {query_text}")
            
            # Phase 1: Personalized Query Analysis
            personalized_query = self.query_analyzer.analyze_query_with_personalization(query_text)
            
            # Update metrics
            metrics.query_clarity = self._calculate_query_clarity(personalized_query)
            metrics.domain_coverage = len(personalized_query.domains)
            metrics.complexity_level = {'simple': 1, 'cross_domain': 2, 'contrarian': 3}[personalized_query.complexity]
            metrics.intent_confidence = personalized_query.intent_confidence
            
            print(f"✅ Personalized Analysis: {personalized_query.intent} | {personalized_query.domains} | Frameworks: {personalized_query.personal_frameworks}")
            
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
            
            # Phase 4: Voice-Personalized Content Generation
            personalized_content = self._generate_voice_personalized_content(personalized_query, personalized_insights)
            
            # Calculate enhanced metrics
            metrics.evidence_density = len(real_sources) / max(len(personalized_insights), 1) if personalized_insights else 0
            metrics.cross_domain_rate = len([i for i in personalized_insights if len(i.domains) > 1]) / max(len(personalized_insights), 1) if personalized_insights else 0
            metrics.content_authenticity = self._calculate_personalized_authenticity(personalized_content, personalized_query)
            metrics.evidence_strength = metrics.source_quality_score
            metrics.engagement_potential = self._calculate_personalized_engagement(personalized_content, personalized_query)
            metrics.uniqueness_score = self._calculate_personalized_uniqueness(personalized_query, personalized_insights)
            
            metrics.total_latency = time.time() - start_time
            metrics.ai_tokens_used = self.ai_tokens_used
            
            # Store metrics
            self.metrics_collector.store_metrics(metrics)
            
            # Prepare enhanced response
            response = {
                'personalized_query_analysis': asdict(personalized_query),
                'real_sources_fetched': len(real_sources),
                'personalized_insights_generated': len(personalized_insights),
                'personalized_content': personalized_content,
                'metrics': asdict(metrics),
                'voice_personalization': {
                    'frameworks_applied': personalized_query.personal_frameworks,
                    'voice_style': personalized_query.voice_style,
                    'contrarian_potential': personalized_query.contrarian_potential,
                    'authenticity_score': metrics.content_authenticity
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
                    'personalization_quality': f"{metrics.content_authenticity:.2f}",
                    'uniqueness': f"{metrics.uniqueness_score:.2f}",
                    'frameworks_used': len(personalized_query.personal_frameworks),
                    'phase': 'Phase 3: Personalized Intelligence'
                }
            }
            
            print(f"🎉 Phase 3 Complete! Personalized content with {len(personalized_query.personal_frameworks)} frameworks, Authenticity: {metrics.content_authenticity:.2f}")
            return response, metrics
            
        except Exception as e:
            metrics.error_count = 1
            metrics.total_latency = time.time() - start_time
            self.metrics_collector.store_metrics(metrics)
            
            print(f"❌ Phase 3 Processing failed: {e}")
            return {'error': str(e), 'metrics': asdict(metrics)}, metrics
    
    def _generate_personalized_insights(self, query: PersonalizedProsoraQuery, real_sources: List[RealSourceContent]) -> List[PersonalizedInsight]:
        """Generate insights with personalization"""
        insights = []
        
        # Generate insights using personal frameworks
        for i, source in enumerate(real_sources[:3]):
            # Use AI-generated frameworks directly (they're already personalized)
            relevant_frameworks = query.personal_frameworks[:2] if query.personal_frameworks else ['Cross-Domain Analysis']
            
            insight = PersonalizedInsight(
                title=f"Cross-Domain Analysis: {source.title[:50]}...",
                content=f"From my experience in {' and '.join(query.domains)}: {source.content[:200]}...",
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
            
            # Add contrarian angle if appropriate
            if query.contrarian_potential > 0.6:
                insight.contrarian_angle = f"While conventional wisdom focuses on X, my analysis suggests Y because..."
            
            insights.append(insight)
        
        return insights
    
    def _generate_voice_personalized_content(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> Dict:
        """Generate content with voice personalization"""
        
        # Generate personalized LinkedIn post
        linkedin_post = self.content_generator.generate_personalized_linkedin_post(query, insights)
        
        # Enhanced content structure
        personalized_content = {
            'linkedin_posts': [linkedin_post] if linkedin_post else [],
            'twitter_threads': [],  # TODO: Implement
            'blog_outlines': [],    # TODO: Implement
            'personalization_summary': {
                'frameworks_applied': query.personal_frameworks,
                'voice_style': query.voice_style,
                'contrarian_elements': len([i for i in insights if i.contrarian_angle]),
                'cross_domain_connections': sum(len(i.cross_domain_connections or []) for i in insights),
                'authenticity_indicators': [
                    'personal_frameworks_used',
                    'cross_domain_perspective',
                    'voice_personalization',
                    'real_source_backing'
                ]
            },
            'insights_summary': {
                'total_insights': len(insights),
                'personalized_insights': len([i for i in insights if i.personal_frameworks]),
                'average_credibility': sum(i.credibility for i in insights) / len(insights) if insights else 0,
                'frameworks_coverage': list(set(f for i in insights for f in i.personal_frameworks))
            }
        }
        
        return personalized_content
    
    def _calculate_query_clarity(self, query: PersonalizedProsoraQuery) -> float:
        """Calculate query clarity with personalization factors"""
        clarity = query.intent_confidence * 0.4
        clarity += (sum(query.domain_weights.values()) / len(query.domain_weights)) * 0.3 if query.domain_weights else 0
        clarity += min(len(query.personal_frameworks) / 3, 1.0) * 0.3
        return min(clarity, 1.0)
    
    def _calculate_personalized_authenticity(self, content: Dict, query: PersonalizedProsoraQuery) -> float:
        """Calculate authenticity with personalization factors"""
        base_score = 0.7
        
        # Bonus for personal frameworks
        if query.personal_frameworks:
            base_score += min(len(query.personal_frameworks) / 4, 0.2)
        
        # Bonus for voice personalization
        if query.voice_style != 'professional':
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _calculate_personalized_engagement(self, content: Dict, query: PersonalizedProsoraQuery) -> float:
        """Calculate engagement potential with personalization"""
        engagement = 0.6  # Base for personalized content
        
        # Higher for contrarian content
        if query.contrarian_potential > 0.6:
            engagement += 0.2
        
        # Higher for cross-domain insights
        if query.complexity == 'cross_domain':
            engagement += 0.1
        
        return min(engagement, 1.0)
    
    def _calculate_personalized_uniqueness(self, query: PersonalizedProsoraQuery, insights: List[PersonalizedInsight]) -> float:
        """Calculate uniqueness with personalization factors"""
        uniqueness = 0.6  # Base for personalized content
        
        # Higher for personal frameworks
        if query.personal_frameworks:
            uniqueness += min(len(query.personal_frameworks) / 4, 0.2)
        
        # Higher for contrarian insights
        contrarian_count = len([i for i in insights if i.contrarian_angle])
        uniqueness += min(contrarian_count * 0.1, 0.2)
        
        return min(uniqueness, 1.0)
    
    def get_system_metrics(self, days: int = 7) -> Dict:
        """Get system performance metrics"""
        return self.metrics_collector.get_metrics_summary(days)

# Test function
def test_phase3_system():
    """Test Phase 3 personalized system"""
    engine = Phase3PersonalizedIntelligence()
    
    test_queries = [
        "AI regulation impact on fintech product strategy",
        "Cross-domain analysis of political tech platforms",
        "Contrarian view on startup funding in regulated industries"
    ]
    
    for query in test_queries:
        print(f"\n🧪 Phase 3 Testing: {query}")
        response, metrics = engine.process_query_with_personalization(query)
        
        if 'error' not in response:
            print(f"📊 Frameworks Applied: {len(response['personalized_query_analysis']['personal_frameworks'])}")
            print(f"📊 Authenticity: {metrics.content_authenticity:.2f}")
            print(f"📊 Uniqueness: {metrics.uniqueness_score:.2f}")
            print(f"📊 Time: {metrics.total_latency:.2f}s")

if __name__ == "__main__":
    test_phase3_system()