import json
import google.generativeai as genai
from typing import List, Dict, Any
from datetime import datetime
from config import Config
import re

class AIAnalyzer:
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def analyze_content_for_insights(self, content: Dict) -> Dict:
        """Analyze aggregated content for unique insights"""
        print("🧠 Starting AI content analysis...")
        
        insights = {
            "cross_domain_connections": self._find_cross_domain_connections(content),
            "contrarian_opportunities": self._identify_contrarian_takes(content),
            "prosora_index_signals": self._calculate_prosora_signals(content),
            "trending_intersections": self._find_trending_intersections(content),
            "content_gaps": self._identify_content_gaps(content),
            "analyzed_at": datetime.now().isoformat()
        }
        
        # Save analysis
        with open("data/content_analysis.json", "w") as f:
            json.dump(insights, f, indent=2)
            
        return insights
    
    def _find_cross_domain_connections(self, content: Dict) -> List[Dict]:
        """Find connections between tech, politics, product, and fintech"""
        connections = []
        
        # Combine all content text
        all_text = self._extract_all_text(content)
        
        prompt = f"""
        As an expert in technology, politics, product management, and fintech, analyze this content 
        and identify 3 unique cross-domain connections that someone with background in:
        - IIT Engineering
        - Political Consulting  
        - Product Operations
        - FinTech MBA
        
        Could uniquely comment on. Focus on non-obvious connections.
        
        Content: {all_text[:3000]}
        
        Return insights in this format:
        1. Connection: [brief title]
           Domains: [which domains connect]
           Insight: [unique perspective]
           Content Hook: [engaging angle for social media]
        """
        
        try:
            response = self.model.generate_content(prompt)
            connections_text = response.text
            connections = self._parse_connections(connections_text)
            
        except Exception as e:
            print(f"Error in cross-domain analysis: {e}")
            
        return connections
    
    def _identify_contrarian_takes(self, content: Dict) -> List[Dict]:
        """Identify contrarian but data-backed perspectives"""
        contrarian_takes = []
        
        all_text = self._extract_all_text(content)
        
        prompt = f"""
        Based on this content, identify 3 contrarian but defensible takes that would generate 
        discussion on LinkedIn/Twitter. Focus on perspectives that challenge conventional wisdom
        in tech, politics, product management, or fintech.
        
        Content: {all_text[:3000]}
        
        Format:
        1. Contrarian Take: [provocative but professional statement]
           Supporting Evidence: [data/logic from content]
           Discussion Starter: [question to engage audience]
        """
        
        try:
            response = self.model.generate_content(prompt)
            takes_text = response.text
            contrarian_takes = self._parse_contrarian_takes(takes_text)
            
        except Exception as e:
            print(f"Error in contrarian analysis: {e}")
            
        return contrarian_takes
    
    def _calculate_prosora_signals(self, content: Dict) -> Dict:
        """Calculate Prosora Index signals from content"""
        signals = {
            "tech_innovation": 0,
            "political_stability": 0, 
            "market_opportunity": 0,
            "social_impact": 0
        }
        
        # Simple keyword-based scoring (enhance with ML later)
        all_text = self._extract_all_text(content).lower()
        
        tech_keywords = ["ai", "blockchain", "automation", "innovation", "startup"]
        political_keywords = ["policy", "regulation", "government", "election", "democracy"]
        market_keywords = ["market", "opportunity", "growth", "investment", "revenue"]
        social_keywords = ["impact", "society", "community", "inclusion", "sustainability"]
        
        signals["tech_innovation"] = sum(all_text.count(kw) for kw in tech_keywords)
        signals["political_stability"] = sum(all_text.count(kw) for kw in political_keywords)
        signals["market_opportunity"] = sum(all_text.count(kw) for kw in market_keywords)
        signals["social_impact"] = sum(all_text.count(kw) for kw in social_keywords)
        
        # Normalize to 0-100 scale
        max_score = max(signals.values()) if max(signals.values()) > 0 else 1
        for key in signals:
            signals[key] = min(100, (signals[key] / max_score) * 100)
            
        return signals
    
    def _find_trending_intersections(self, content: Dict) -> List[str]:
        """Find trending topics at intersection of your domains"""
        intersections = []
        
        # Extract trending topics and find intersections
        trends = content.get("trends", [])
        for trend in trends:
            title = trend.get("title", "").lower()
            snippet = trend.get("snippet", "").lower()
            
            # Check if trend intersects multiple domains
            domains_hit = 0
            if any(kw in title + snippet for kw in ["tech", "ai", "digital", "innovation"]):
                domains_hit += 1
            if any(kw in title + snippet for kw in ["policy", "government", "regulation"]):
                domains_hit += 1
            if any(kw in title + snippet for kw in ["product", "management", "strategy"]):
                domains_hit += 1
            if any(kw in title + snippet for kw in ["fintech", "finance", "banking"]):
                domains_hit += 1
                
            if domains_hit >= 2:
                intersections.append(trend.get("title", ""))
                
        return intersections[:5]
    
    def _identify_content_gaps(self, content: Dict) -> List[str]:
        """Identify content gaps in current discourse"""
        gaps = [
            "Technical debt in political campaigns",
            "Product management lessons from election strategies", 
            "FinTech regulation through engineering lens",
            "Scaling democracy like scaling products",
            "Political consulting meets growth hacking"
        ]
        return gaps
    
    def _extract_all_text(self, content: Dict) -> str:
        """Extract all text content for analysis"""
        text_parts = []
        
        for newsletter in content.get("newsletters", []):
            text_parts.append(newsletter.get("title", ""))
            text_parts.append(newsletter.get("summary", ""))
            
        for youtube in content.get("youtube", []):
            text_parts.append(youtube.get("title", ""))
            text_parts.append(youtube.get("transcript", "")[:1000])  # Limit transcript length
            
        for trend in content.get("trends", []):
            text_parts.append(trend.get("title", ""))
            text_parts.append(trend.get("snippet", ""))
            
        return " ".join(text_parts)
    
    def _parse_connections(self, text: str) -> List[Dict]:
        """Parse AI response into structured connections"""
        # Simple parsing - enhance as needed
        connections = []
        lines = text.split('\n')
        current_connection = {}
        
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.')):
                if current_connection:
                    connections.append(current_connection)
                current_connection = {"title": line.strip()}
            elif "Domains:" in line:
                current_connection["domains"] = line.replace("Domains:", "").strip()
            elif "Insight:" in line:
                current_connection["insight"] = line.replace("Insight:", "").strip()
            elif "Content Hook:" in line:
                current_connection["hook"] = line.replace("Content Hook:", "").strip()
                
        if current_connection:
            connections.append(current_connection)
            
        return connections
    
    def _parse_contrarian_takes(self, text: str) -> List[Dict]:
        """Parse contrarian takes from AI response"""
        takes = []
        lines = text.split('\n')
        current_take = {}
        
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.')):
                if current_take:
                    takes.append(current_take)
                current_take = {"statement": line.strip()}
            elif "Supporting Evidence:" in line:
                current_take["evidence"] = line.replace("Supporting Evidence:", "").strip()
            elif "Discussion Starter:" in line:
                current_take["discussion_starter"] = line.replace("Discussion Starter:", "").strip()
                
        if current_take:
            takes.append(current_take)
            
        return takes

if __name__ == "__main__":
    analyzer = AIAnalyzer()
    
    # Load content
    with open("data/raw_content.json", "r") as f:
        content = json.load(f)
        
    insights = analyzer.analyze_content_for_insights(content)