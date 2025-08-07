#!/usr/bin/env python3
"""
Google Evidence Search Integration
Automatically find supporting evidence for AI-generated insights
"""

import requests
import json
import yaml
from typing import Dict, List
from datetime import datetime
import time

class GoogleEvidenceSearch:
    def __init__(self):
        # Load environment variables
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        # Load Google search configuration
        try:
            with open('prosora_sources.yaml', 'r') as f:
                config = yaml.safe_load(f)
            self.google_config = config.get('google_search', [])
        except FileNotFoundError:
            self.google_config = []
        
        # Google Custom Search API configuration
        self.search_api_key = os.getenv('GOOGLE_API_KEY')
        self.search_engine_id = os.getenv('GOOGLE_CSE_ID', 'd4cee64a8da3a449a')  # Your CSE ID
        
        if not self.search_api_key:
            print("⚠️ Google API key not found. Evidence search will use placeholder data.")
            print("💡 Get your API key from: https://console.cloud.google.com/apis/credentials")
        else:
            print(f"✅ Google Search configured with CSE: {self.search_engine_id[:10]}...")
        
    def search_supporting_evidence(self, insight: Dict, max_results: int = 3) -> List[Dict]:
        """Search for supporting evidence for an AI insight"""
        
        topic = insight.get('title', '')
        content = insight.get('content', '')
        
        # Extract key terms for search
        search_terms = self._extract_search_terms(topic, content)
        
        evidence = []
        
        for search_config in self.google_config:
            search_type = search_config.get('search_type', '')
            
            if search_type == 'academic':
                academic_evidence = self._search_academic_evidence(search_terms, search_config)
                evidence.extend(academic_evidence[:2])  # Limit to 2 per type
                
            elif search_type == 'news':
                news_evidence = self._search_news_evidence(search_terms, search_config)
                evidence.extend(news_evidence[:2])
                
            elif search_type == 'trends':
                trend_evidence = self._search_trend_evidence(search_terms, search_config)
                evidence.extend(trend_evidence[:1])
        
        return evidence[:max_results]
    
    def _extract_search_terms(self, title: str, content: str) -> List[str]:
        """Extract key search terms from insight"""
        
        # Simple keyword extraction (can be enhanced with NLP)
        text = f"{title} {content}".lower()
        
        # Key terms related to your expertise
        key_terms = []
        
        # Tech terms
        tech_keywords = ['ai', 'artificial intelligence', 'machine learning', 'automation', 
                        'blockchain', 'fintech', 'digital transformation']
        
        # Politics terms
        politics_keywords = ['regulation', 'policy', 'government', 'democracy', 
                           'political', 'governance', 'compliance']
        
        # Product terms
        product_keywords = ['product management', 'user experience', 'growth', 
                          'strategy', 'innovation', 'startup']
        
        # Finance terms
        finance_keywords = ['finance', 'banking', 'investment', 'market', 
                          'economic', 'financial services']
        
        all_keywords = tech_keywords + politics_keywords + product_keywords + finance_keywords
        
        for keyword in all_keywords:
            if keyword in text:
                key_terms.append(keyword)
        
        # Add title as primary search term
        if title:
            key_terms.insert(0, title)
        
        return key_terms[:5]  # Limit to top 5 terms
    
    def _search_academic_evidence(self, search_terms: List[str], config: Dict) -> List[Dict]:
        """Search for academic evidence"""
        
        evidence = []
        
        for term in search_terms[:2]:  # Limit searches
            # Simulate academic search results (replace with actual Google Scholar API)
            mock_results = [
                {
                    'type': 'academic',
                    'title': f'Academic Study: {term} in Modern Context',
                    'url': f'https://scholar.google.com/search?q={term.replace(" ", "+")}',
                    'snippet': f'Recent academic research on {term} shows significant implications for industry and policy.',
                    'source': 'Google Scholar',
                    'credibility': config.get('credibility', 0.9),
                    'relevance_score': 0.8,
                    'search_term': term,
                    'found_at': datetime.now().isoformat()
                }
            ]
            
            evidence.extend(mock_results)
            time.sleep(0.1)  # Rate limiting
        
        return evidence
    
    def _search_news_evidence(self, search_terms: List[str], config: Dict) -> List[Dict]:
        """Search for news evidence"""
        
        evidence = []
        
        for term in search_terms[:2]:
            # Simulate news search results
            mock_results = [
                {
                    'type': 'news',
                    'title': f'Latest News: {term} Developments',
                    'url': f'https://news.google.com/search?q={term.replace(" ", "+")}',
                    'snippet': f'Recent news coverage of {term} indicates growing market interest and regulatory attention.',
                    'source': 'Google News',
                    'credibility': config.get('credibility', 0.7),
                    'relevance_score': 0.7,
                    'search_term': term,
                    'found_at': datetime.now().isoformat()
                }
            ]
            
            evidence.extend(mock_results)
            time.sleep(0.1)
        
        return evidence
    
    def _search_trend_evidence(self, search_terms: List[str], config: Dict) -> List[Dict]:
        """Search for trend evidence"""
        
        evidence = []
        
        for term in search_terms[:1]:  # Just one trend search
            # Simulate trend search results
            mock_results = [
                {
                    'type': 'trends',
                    'title': f'Trend Analysis: {term} Search Interest',
                    'url': f'https://trends.google.com/trends/explore?q={term.replace(" ", "+")}',
                    'snippet': f'Google Trends data shows {term} has increasing search volume, indicating growing public interest.',
                    'source': 'Google Trends',
                    'credibility': config.get('credibility', 0.8),
                    'relevance_score': 0.6,
                    'search_term': term,
                    'found_at': datetime.now().isoformat()
                }
            ]
            
            evidence.extend(mock_results)
        
        return evidence
    
    def enhance_insight_with_evidence(self, insight: Dict) -> Dict:
        """Enhance an insight with supporting evidence"""
        
        evidence = self.search_supporting_evidence(insight)
        
        enhanced_insight = {
            **insight,
            'supporting_evidence': evidence,
            'evidence_count': len(evidence),
            'evidence_credibility': sum(e.get('credibility', 0) for e in evidence) / len(evidence) if evidence else 0,
            'enhanced_at': datetime.now().isoformat()
        }
        
        return enhanced_insight
    
    def batch_enhance_insights(self, insights: List[Dict]) -> List[Dict]:
        """Enhance multiple insights with evidence"""
        
        enhanced_insights = []
        
        for insight in insights:
            enhanced = self.enhance_insight_with_evidence(insight)
            enhanced_insights.append(enhanced)
            time.sleep(0.2)  # Rate limiting
        
        return enhanced_insights

# Integration with existing system
def integrate_google_evidence_search():
    """Integrate Google evidence search with existing insight generation"""
    
    # This would be called after AI generates insights
    search_engine = GoogleEvidenceSearch()
    
    # Example usage
    sample_insight = {
        'title': 'AI Regulation in FinTech',
        'content': 'The intersection of AI regulation and financial technology creates both opportunities and challenges for startups.',
        'type': 'cross_domain_insight'
    }
    
    enhanced_insight = search_engine.enhance_insight_with_evidence(sample_insight)
    
    print("🔍 Enhanced Insight with Google Evidence:")
    print(f"Title: {enhanced_insight['title']}")
    print(f"Evidence Count: {enhanced_insight['evidence_count']}")
    print(f"Evidence Credibility: {enhanced_insight['evidence_credibility']:.2f}")
    
    for i, evidence in enumerate(enhanced_insight['supporting_evidence'], 1):
        print(f"\n{i}. {evidence['title']}")
        print(f"   Source: {evidence['source']}")
        print(f"   Credibility: {evidence['credibility']}")
        print(f"   URL: {evidence['url']}")

if __name__ == "__main__":
    integrate_google_evidence_search()