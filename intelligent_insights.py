"""
Intelligent Insights Engine
Advanced AI analysis with source credibility weighting and personalized knowledge graphs
"""

import json
import yaml
import google.generativeai as genai
from typing import Dict, List, Tuple
from datetime import datetime
import numpy as np
from collections import defaultdict
from config import Config

class IntelligentInsightsEngine:
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.flash_model = genai.GenerativeModel('gemini-1.5-flash')  # Fast for most operations
        self.pro_model = genai.GenerativeModel('gemini-1.5-pro')     # Complex analysis only
        
        # Load your personalized source configuration
        with open('prosora_sources.yaml', 'r') as f:
            self.source_config = yaml.safe_load(f)
    
    def analyze_with_credibility_weighting(self, content: List[Dict]) -> Dict:
        """Analyze content with intelligent credibility weighting"""
        
        print("🧠 Starting Intelligent Analysis with Credibility Weighting...")
        
        # Separate content by credibility tiers
        premium_content = [c for c in content if c.get('credibility_score', 0) >= 0.8]
        standard_content = [c for c in content if 0.6 <= c.get('credibility_score', 0) < 0.8]
        experimental_content = [c for c in content if c.get('credibility_score', 0) < 0.6]
        
        insights = {
            "tier_1_insights": self._analyze_premium_content(premium_content),
            "tier_2_insights": self._analyze_standard_content(standard_content),
            "tier_3_signals": self._analyze_experimental_content(experimental_content),
            "cross_tier_synthesis": self._synthesize_across_tiers(premium_content, standard_content, experimental_content),
            "personalized_frameworks": self._generate_personalized_frameworks(content),
            "contrarian_opportunities": self._find_contrarian_opportunities(content),
            "knowledge_gaps": self._identify_knowledge_gaps(content),
            "prosora_index_advanced": self._calculate_advanced_prosora_index(content)
        }
        
        return insights
    
    def _analyze_premium_content(self, premium_content: List[Dict]) -> List[Dict]:
        """Deep analysis of high-credibility sources"""
        
        if not premium_content:
            return []
            
        # Combine premium content for analysis
        premium_text = self._extract_weighted_text(premium_content, weight_multiplier=1.0)
        
        prompt = f"""
        You are analyzing PREMIUM, HIGH-CREDIBILITY content from sources like:
        - a16z (Marc Andreessen, Ben Horowitz)
        - Stratechery (Ben Thompson)
        - First Round Review
        - Lenny's Newsletter
        - CB Insights
        
        This is Tier 1 intelligence. Extract the most sophisticated insights that only someone with 
        your background (IIT engineer + political consultant + product ops + FinTech MBA) would recognize.
        
        Content: {premium_text[:4000]}
        
        Generate 3 PREMIUM insights in this format:
        
        **Premium Insight [X]: [Sophisticated Title]**
        - **Core Pattern**: [What sophisticated pattern do you see?]
        - **Why It Matters**: [Strategic implications]
        - **Cross-Domain Connection**: [How does this connect tech/politics/product/finance?]
        - **Contrarian Angle**: [What would most people miss?]
        - **Actionable Intelligence**: [Specific action for someone with your background]
        - **Confidence Level**: [High/Medium based on source credibility]
        """
        
        try:
            response = self.flash_model.generate_content(prompt)  # Use Flash to avoid rate limits
            return self._parse_premium_insights(response.text)
        except Exception as e:
            print(f"Error in premium analysis: {e}")
            return []
    
    def _analyze_standard_content(self, standard_content: List[Dict]) -> List[Dict]:
        """Analysis of medium-credibility sources for supporting evidence"""
        
        if not standard_content:
            return []
            
        standard_text = self._extract_weighted_text(standard_content, weight_multiplier=0.7)
        
        prompt = f"""
        Analyze this STANDARD-CREDIBILITY content from sources like HBR, McKinsey, etc.
        Use this to SUPPORT and VALIDATE insights from premium sources.
        
        Content: {standard_text[:3000]}
        
        Find 2 SUPPORTING insights that:
        1. Validate patterns from premium sources
        2. Provide additional context or evidence
        3. Fill gaps in the premium analysis
        
        Format as supporting evidence, not primary insights.
        """
        
        try:
            response = self.flash_model.generate_content(prompt)
            return self._parse_standard_insights(response.text)
        except Exception as e:
            print(f"Error in standard analysis: {e}")
            return []
    
    def _analyze_experimental_content(self, experimental_content: List[Dict]) -> List[Dict]:
        """Analysis of low-credibility sources for weak signals and trends"""
        
        if not experimental_content:
            return []
            
        experimental_text = self._extract_weighted_text(experimental_content, weight_multiplier=0.4)
        
        prompt = f"""
        Analyze this EXPERIMENTAL content from sources like Hacker News, social media, etc.
        Look for WEAK SIGNALS and EMERGING TRENDS that might not be in mainstream sources yet.
        
        Content: {experimental_text[:2000]}
        
        Find 2 WEAK SIGNALS:
        1. Early indicators of future trends
        2. Contrarian viewpoints worth monitoring
        
        Mark these as experimental - low confidence but potentially high impact.
        """
        
        try:
            response = self.flash_model.generate_content(prompt)
            return self._parse_experimental_signals(response.text)
        except Exception as e:
            print(f"Error in experimental analysis: {e}")
            return []
    
    def _synthesize_across_tiers(self, premium: List[Dict], standard: List[Dict], experimental: List[Dict]) -> List[Dict]:
        """Synthesize insights across all credibility tiers"""
        
        prompt = f"""
        You have analyzed content across 3 credibility tiers:
        
        TIER 1 (Premium): {len(premium)} high-credibility sources
        TIER 2 (Standard): {len(standard)} medium-credibility sources  
        TIER 3 (Experimental): {len(experimental)} low-credibility sources
        
        Now synthesize across ALL tiers to find:
        1. Patterns that appear across multiple credibility levels
        2. Contradictions between tiers that reveal opportunities
        3. Unique insights only visible when combining all perspectives
        
        Create 2 SYNTHESIS insights that leverage your multi-tier analysis.
        """
        
        try:
            response = self.flash_model.generate_content(prompt)
            return self._parse_synthesis_insights(response.text)
        except Exception as e:
            print(f"Error in synthesis: {e}")
            return []
    
    def _generate_personalized_frameworks(self, content: List[Dict]) -> List[Dict]:
        """Generate frameworks specific to your background and interests"""
        
        # Weight content by personal relevance
        relevant_content = sorted(content, key=lambda x: x.get('personal_relevance', 0), reverse=True)[:10]
        
        prompt = f"""
        Based on your unique background (IIT engineer + political consultant + product ops + FinTech MBA),
        create 2 PERSONALIZED FRAMEWORKS from this content.
        
        These should be methodologies that only YOU could create given your specific experience.
        
        Examples of your style:
        - "The Political Product Manager"
        - "FinTech Democracy Framework"  
        - "The IIT-MBA Bridge"
        
        Create frameworks that are:
        1. Uniquely yours (leveraging your specific background)
        2. Actionable (people can apply them)
        3. Memorable (easy to reference and share)
        
        Content: {self._extract_weighted_text(relevant_content[:5])}
        """
        
        try:
            response = self.flash_model.generate_content(prompt)
            return self._parse_framework_insights(response.text)
        except Exception as e:
            print(f"Error generating frameworks: {e}")
            return []
    
    def _find_contrarian_opportunities(self, content: List[Dict]) -> List[Dict]:
        """Find contrarian opportunities using source diversity"""
        
        # Group content by domains
        domain_content = defaultdict(list)
        for item in content:
            for domain in item.get('expertise_domains', []):
                domain_content[domain].append(item)
        
        prompt = f"""
        You have content from multiple domains:
        - Tech: {len(domain_content.get('tech', []))} sources
        - Politics: {len(domain_content.get('politics', []))} sources
        - Product: {len(domain_content.get('product', []))} sources
        - Finance: {len(domain_content.get('finance', []))} sources
        
        Find 2 CONTRARIAN OPPORTUNITIES where:
        1. Different domains suggest opposite conclusions
        2. High-credibility sources disagree with conventional wisdom
        3. Your unique background lets you see what others miss
        
        These should be defensible contrarian positions, not just provocative statements.
        """
        
        try:
            response = self.flash_model.generate_content(prompt)
            return self._parse_contrarian_insights(response.text)
        except Exception as e:
            print(f"Error finding contrarian opportunities: {e}")
            return []
    
    def _calculate_advanced_prosora_index(self, content: List[Dict]) -> Dict:
        """Calculate advanced Prosora Index with credibility weighting"""
        
        domain_weights = self.source_config['domain_weights']
        
        # Calculate weighted scores
        weighted_scores = {
            'tech_innovation': 0,
            'political_stability': 0,
            'market_opportunity': 0,
            'social_impact': 0
        }
        
        total_weight = 0
        
        for item in content:
            credibility = item.get('credibility_score', 0.5)
            domains = item.get('expertise_domains', [])
            
            # Weight by credibility and personal relevance
            item_weight = credibility * item.get('personal_relevance', 0.5)
            total_weight += item_weight
            
            # Distribute across domains
            for domain in domains:
                if domain == 'tech':
                    weighted_scores['tech_innovation'] += item_weight
                elif domain == 'politics':
                    weighted_scores['political_stability'] += item_weight
                elif domain in ['finance', 'product']:
                    weighted_scores['market_opportunity'] += item_weight
                else:
                    weighted_scores['social_impact'] += item_weight
        
        # Normalize to 0-100 scale
        if total_weight > 0:
            for key in weighted_scores:
                weighted_scores[key] = min(100, (weighted_scores[key] / total_weight) * 100)
        
        # Calculate composite Prosora Score
        composite_score = sum(
            weighted_scores[key] * domain_weights.get(key.split('_')[0], 0.25)
            for key in weighted_scores
        )
        
        return {
            **weighted_scores,
            'composite_prosora_score': composite_score,
            'data_quality_score': total_weight / len(content) if content else 0,
            'source_diversity': len(set(item.get('source', '') for item in content))
        }
    
    def _extract_weighted_text(self, content: List[Dict], weight_multiplier: float = 1.0) -> str:
        """Extract text with credibility weighting"""
        
        weighted_texts = []
        
        for item in content:
            credibility = item.get('credibility_score', 0.5) * weight_multiplier
            text_content = item.get('content', '') or item.get('full_content', '') or item.get('transcript', '')
            
            # Repeat high-credibility content to give it more weight in analysis
            repeat_count = max(1, int(credibility * 3))
            for _ in range(repeat_count):
                weighted_texts.append(text_content[:1000])  # Limit per item
        
        return " ".join(weighted_texts)
    
    def _parse_premium_insights(self, text: str) -> List[Dict]:
        """Parse premium insights from AI response"""
        # Implementation for parsing structured insights
        return []
    
    def _parse_standard_insights(self, text: str) -> List[Dict]:
        """Parse standard insights from AI response"""
        return []
    
    def _parse_experimental_signals(self, text: str) -> List[Dict]:
        """Parse experimental signals from AI response"""
        return []
    
    def _parse_synthesis_insights(self, text: str) -> List[Dict]:
        """Parse synthesis insights from AI response"""
        return []
    
    def _parse_framework_insights(self, text: str) -> List[Dict]:
        """Parse framework insights from AI response"""
        return []
    
    def _parse_contrarian_insights(self, text: str) -> List[Dict]:
        """Parse contrarian insights from AI response"""
        return []
    
    def _identify_knowledge_gaps(self, content: List[Dict]) -> List[str]:
        """Identify gaps in your knowledge coverage"""
        
        # Analyze domain coverage
        domain_coverage = defaultdict(int)
        for item in content:
            for domain in item.get('expertise_domains', []):
                domain_coverage[domain] += 1
        
        gaps = []
        target_domains = ['tech', 'politics', 'product', 'finance']
        
        for domain in target_domains:
            if domain_coverage[domain] < 3:  # Less than 3 sources
                gaps.append(f"Need more {domain} sources")
        
        return gaps

if __name__ == "__main__":
    engine = IntelligentInsightsEngine()
    
    # Test with sample content
    sample_content = [
        {
            "content": "Sample premium content",
            "credibility_score": 0.9,
            "expertise_domains": ["tech", "product"],
            "personal_relevance": 0.8
        }
    ]
    
    insights = engine.analyze_with_credibility_weighting(sample_content)
    print(json.dumps(insights, indent=2))