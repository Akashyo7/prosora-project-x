"""
Prosora Advanced Content Aggregator
Intelligent, weighted, multi-source content aggregation system
"""

import json
import imaplib
import email
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
import feedparser
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import re
from dataclasses import dataclass
from config import Config

@dataclass
class ContentSource:
    """Structured content source with metadata"""
    name: str
    url: str
    source_type: str  # 'newsletter', 'youtube', 'blog', 'social', 'email'
    credibility_score: float  # 0.0 to 1.0
    expertise_domains: List[str]  # ['tech', 'politics', 'finance', 'product']
    update_frequency: str  # 'daily', 'weekly', 'monthly'
    content_quality: str  # 'premium', 'standard', 'experimental'
    personal_relevance: float  # 0.0 to 1.0 - how relevant to your interests

class AdvancedContentAggregator:
    def __init__(self):
        self.config = Config()
        self.sources = self._load_curated_sources()
        self.knowledge_graph = {}
        
    def _load_curated_sources(self) -> List[ContentSource]:
        """Load your curated, weighted content sources"""
        
        # Your Premium Sources (High Credibility)
        premium_sources = [
            # Tech Leadership
            ContentSource("a16z Podcast", "UC7cs8q-gJRlGwj4A8OmCmXg", "youtube", 0.9, 
                         ["tech", "product", "finance"], "weekly", "premium", 0.95),
            ContentSource("First Round Review", "https://review.firstround.com/feed", "blog", 0.95,
                         ["product", "tech"], "weekly", "premium", 0.9),
            ContentSource("Stratechery", "https://stratechery.com/feed/", "newsletter", 0.95,
                         ["tech", "product", "finance"], "daily", "premium", 0.9),
            
            # Political/Policy
            ContentSource("Politico Playbook", "politico_playbook", "email", 0.85,
                         ["politics"], "daily", "premium", 0.8),
            ContentSource("The Dispatch", "https://thedispatch.com/feed/", "newsletter", 0.8,
                         ["politics"], "daily", "standard", 0.7),
            
            # FinTech/Finance
            ContentSource("Fintech Weekly", "https://www.fintechweekly.com/feed", "newsletter", 0.8,
                         ["finance", "tech"], "weekly", "standard", 0.85),
            ContentSource("CB Insights", "https://www.cbinsights.com/feed", "blog", 0.85,
                         ["tech", "finance"], "weekly", "premium", 0.8),
            
            # Product Management
            ContentSource("Lenny's Newsletter", "lennys_newsletter", "email", 0.9,
                         ["product"], "weekly", "premium", 0.95),
            ContentSource("Product Hunt Daily", "https://www.producthunt.com/feed", "newsletter", 0.7,
                         ["product", "tech"], "daily", "standard", 0.6),
        ]
        
        # Your Personal/Experimental Sources (Medium Credibility)
        experimental_sources = [
            ContentSource("Hacker News", "https://hnrss.org/frontpage", "social", 0.6,
                         ["tech"], "daily", "experimental", 0.7),
            ContentSource("LinkedIn Tech Leaders", "linkedin_feed", "social", 0.5,
                         ["tech", "product"], "daily", "experimental", 0.6),
        ]
        
        return premium_sources + experimental_sources
    
    def fetch_email_newsletters(self) -> List[Dict]:
        """Fetch newsletters from your email subscriptions"""
        content = []
        
        try:
            # Connect to Gmail (you'll need app password)
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.config.EMAIL_ADDRESS, self.config.EMAIL_PASSWORD)
            mail.select('inbox')
            
            # Search for newsletters from last 7 days
            date_since = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
            
            # Define newsletter senders
            newsletter_senders = [
                "newsletter@stratechery.com",
                "team@lenny.com", 
                "playbook@politico.com",
                "insights@cbinsights.com",
                "weekly@fintech.com"
            ]
            
            for sender in newsletter_senders:
                search_criteria = f'(FROM "{sender}" SINCE {date_since})'
                result, data = mail.search(None, search_criteria)
                
                for num in data[0].split()[-5:]:  # Get last 5 emails
                    result, data = mail.fetch(num, '(RFC822)')
                    raw_email = data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    
                    # Extract content
                    subject = email_message['Subject']
                    sender_email = email_message['From']
                    
                    # Get email body
                    body = self._extract_email_body(email_message)
                    
                    # Find matching source
                    source = self._find_source_by_email(sender_email)
                    
                    content.append({
                        "type": "email_newsletter",
                        "title": subject,
                        "content": body,
                        "sender": sender_email,
                        "source_credibility": source.credibility_score if source else 0.5,
                        "expertise_domains": source.expertise_domains if source else ["general"],
                        "personal_relevance": source.personal_relevance if source else 0.5,
                        "timestamp": datetime.now().isoformat()
                    })
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            print(f"Error fetching email newsletters: {e}")
            
        return content
    
    def fetch_weighted_youtube_content(self) -> List[Dict]:
        """Fetch YouTube content with credibility weighting"""
        content = []
        
        youtube_sources = [s for s in self.sources if s.source_type == "youtube"]
        
        for source in youtube_sources:
            try:
                # Get recent videos (you'll implement YouTube API)
                videos = self._get_recent_videos_advanced(source.url, limit=3)
                
                for video in videos:
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video['id'])
                        full_text = " ".join([item['text'] for item in transcript])
                        
                        # Apply source weighting
                        content.append({
                            "type": "youtube_weighted",
                            "title": video['title'],
                            "transcript": full_text,
                            "url": f"https://youtube.com/watch?v={video['id']}",
                            "channel": source.name,
                            "credibility_score": source.credibility_score,
                            "expertise_domains": source.expertise_domains,
                            "personal_relevance": source.personal_relevance,
                            "content_quality": source.content_quality,
                            "timestamp": datetime.now().isoformat()
                        })
                        
                    except Exception as e:
                        print(f"Error getting transcript for {video['id']}: {e}")
                        
            except Exception as e:
                print(f"Error processing YouTube source {source.name}: {e}")
                
        return content
    
    def fetch_curated_blog_content(self) -> List[Dict]:
        """Fetch content from your curated blog sources"""
        content = []
        
        blog_sources = [s for s in self.sources if s.source_type in ["blog", "newsletter"]]
        
        for source in blog_sources:
            try:
                feed = feedparser.parse(source.url)
                
                for entry in feed.entries[:3]:  # Top 3 articles per source
                    # Extract full article content
                    article_content = self._extract_full_article(entry.link)
                    
                    content.append({
                        "type": "curated_blog",
                        "title": entry.title,
                        "summary": entry.summary if hasattr(entry, 'summary') else "",
                        "full_content": article_content,
                        "url": entry.link,
                        "source": source.name,
                        "credibility_score": source.credibility_score,
                        "expertise_domains": source.expertise_domains,
                        "personal_relevance": source.personal_relevance,
                        "content_quality": source.content_quality,
                        "published": entry.published if hasattr(entry, 'published') else "",
                        "timestamp": datetime.now().isoformat()
                    })
                    
            except Exception as e:
                print(f"Error fetching from {source.name}: {e}")
                
        return content
    
    def fetch_social_signals(self) -> List[Dict]:
        """Fetch social media signals from your curated accounts"""
        content = []
        
        # LinkedIn posts from specific thought leaders
        linkedin_accounts = [
            "naval", "elonmusk", "pmarca", "chamath", "balajis"  # Your curated list
        ]
        
        # Twitter threads from specific accounts
        twitter_accounts = [
            "paulg", "sama", "pmarca", "naval"  # Your curated list
        ]
        
        # Instagram insights from business leaders
        instagram_accounts = [
            "garyvee", "thesharkdaymond"  # Your curated list
        ]
        
        # Implementation would use respective APIs
        # For now, placeholder structure
        
        return content
    
    def create_knowledge_graph(self, all_content: List[Dict]) -> Dict:
        """Create a knowledge graph with weighted connections"""
        
        knowledge_graph = {
            "nodes": {},  # Content pieces
            "edges": {},  # Connections between content
            "clusters": {},  # Topic clusters
            "insights": {},  # Generated insights
            "credibility_matrix": {}  # Source credibility relationships
        }
        
        # Process content by credibility tiers
        premium_content = [c for c in all_content if c.get("content_quality") == "premium"]
        standard_content = [c for c in all_content if c.get("content_quality") == "standard"]
        experimental_content = [c for c in all_content if c.get("content_quality") == "experimental"]
        
        # Weight insights based on source credibility
        for content in all_content:
            credibility = content.get("credibility_score", 0.5)
            relevance = content.get("personal_relevance", 0.5)
            
            # Calculate composite score
            composite_score = (credibility * 0.7) + (relevance * 0.3)
            content["composite_score"] = composite_score
            
        return knowledge_graph
    
    def generate_personalized_insights(self, knowledge_graph: Dict) -> List[Dict]:
        """Generate insights based on your personal knowledge graph"""
        
        insights = []
        
        # Cross-reference high-credibility sources
        premium_insights = self._cross_reference_premium_sources(knowledge_graph)
        
        # Find unique patterns in your curated content
        unique_patterns = self._find_unique_patterns(knowledge_graph)
        
        # Generate contrarian takes based on source diversity
        contrarian_insights = self._generate_contrarian_from_diversity(knowledge_graph)
        
        return premium_insights + unique_patterns + contrarian_insights
    
    def _cross_reference_premium_sources(self, knowledge_graph: Dict) -> List[Dict]:
        """Cross-reference high-credibility sources for premium insights"""
        
        premium_insights = []
        
        # Get high-credibility nodes
        high_credibility_nodes = [
            node for node in knowledge_graph.get('nodes', [])
            if node.get('credibility_score', 0) >= 0.8
        ]
        
        # Create insights from premium sources
        for node in high_credibility_nodes[:5]:  # Top 5 premium insights
            insight = {
                'title': node.get('title', 'Premium Insight'),
                'content': node.get('content', 'High-credibility analysis'),
                'credibility_score': node.get('credibility_score', 0.8),
                'source': node.get('source', 'Premium Source'),
                'type': 'premium_insight'
            }
            premium_insights.append(insight)
        
        return premium_insights
    
    def _find_unique_patterns(self, knowledge_graph: Dict) -> List[Dict]:
        """Find unique patterns in curated content"""
        
        unique_patterns = []
        
        # Analyze connections for unique patterns
        connections = knowledge_graph.get('connections', [])
        
        # Look for cross-domain connections
        cross_domain_connections = [
            conn for conn in connections
            if len(set(conn.get('domains', []))) > 1
        ]
        
        # Create pattern insights
        for conn in cross_domain_connections[:3]:  # Top 3 patterns
            pattern = {
                'title': f"Cross-domain Pattern: {' + '.join(conn.get('domains', []))}",
                'content': f"Unique connection identified across {', '.join(conn.get('domains', []))}",
                'credibility_score': conn.get('strength', 0.7),
                'domains': conn.get('domains', []),
                'type': 'unique_pattern'
            }
            unique_patterns.append(pattern)
        
        return unique_patterns
    
    def _generate_contrarian_from_diversity(self, knowledge_graph: Dict) -> List[Dict]:
        """Generate contrarian insights from source diversity"""
        
        contrarian_insights = []
        
        # Get diverse viewpoints
        nodes = knowledge_graph.get('nodes', [])
        
        # Group by domains
        domain_groups = {}
        for node in nodes:
            for domain in node.get('domains', ['general']):
                if domain not in domain_groups:
                    domain_groups[domain] = []
                domain_groups[domain].append(node)
        
        # Generate contrarian takes for each domain
        for domain, domain_nodes in domain_groups.items():
            if len(domain_nodes) >= 2:  # Need at least 2 sources for contrarian view
                contrarian = {
                    'title': f"Contrarian View: {domain.title()}",
                    'content': f"Alternative perspective on {domain} based on diverse source analysis",
                    'credibility_score': 0.6,  # Lower confidence for contrarian views
                    'domain': domain,
                    'source_count': len(domain_nodes),
                    'type': 'contrarian_insight'
                }
                contrarian_insights.append(contrarian)
        
        return contrarian_insights[:2]  # Max 2 contrarian insights
    
    def _extract_email_body(self, email_message) -> str:
        """Extract clean text from email body"""
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            body = email_message.get_payload(decode=True).decode('utf-8')
        
        # Clean up HTML and formatting
        soup = BeautifulSoup(body, 'html.parser')
        return soup.get_text()
    
    def _extract_full_article(self, url: str) -> str:
        """Extract full article content from URL"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Limit to 5000 characters
            
        except Exception as e:
            print(f"Error extracting article from {url}: {e}")
            return ""
    
    def _find_source_by_email(self, email_address: str) -> ContentSource:
        """Find content source by email address"""
        for source in self.sources:
            if email_address in source.url or source.url in email_address:
                return source
        return None
    
    def _get_recent_videos_advanced(self, channel_id: str, limit: int = 3) -> List[Dict]:
        """Get recent videos with advanced filtering"""
        # Placeholder - implement YouTube API v3
        return [
            {"id": "sample_video_id", "title": "Sample Video", "channel": "Sample Channel"}
        ]
    
    def run_advanced_aggregation(self) -> Dict:
        """Run the complete advanced aggregation pipeline"""
        print("🧠 Starting Advanced Prosora Aggregation...")
        print("=" * 60)
        
        all_content = []
        
        # Fetch from all sources with weighting
        print("📧 Fetching email newsletters...")
        email_content = self.fetch_email_newsletters()
        all_content.extend(email_content)
        
        print("🎥 Fetching weighted YouTube content...")
        youtube_content = self.fetch_weighted_youtube_content()
        all_content.extend(youtube_content)
        
        print("📰 Fetching curated blog content...")
        blog_content = self.fetch_curated_blog_content()
        all_content.extend(blog_content)
        
        print("📱 Fetching social signals...")
        social_content = self.fetch_social_signals()
        all_content.extend(social_content)
        
        # Create knowledge graph
        print("🕸️ Creating knowledge graph...")
        knowledge_graph = self.create_knowledge_graph(all_content)
        
        # Generate personalized insights
        print("💡 Generating personalized insights...")
        insights = self.generate_personalized_insights(knowledge_graph)
        
        # Compile results
        results = {
            "total_sources": len(self.sources),
            "content_pieces": len(all_content),
            "premium_content": len([c for c in all_content if c.get("content_quality") == "premium"]),
            "knowledge_graph": knowledge_graph,
            "personalized_insights": insights,
            "aggregated_at": datetime.now().isoformat()
        }
        
        # Save results
        with open("data/advanced_aggregation.json", "w") as f:
            json.dump(results, f, indent=2)
            
        print(f"✅ Advanced aggregation complete!")
        print(f"📊 Processed {len(all_content)} pieces from {len(self.sources)} sources")
        print(f"🏆 {results['premium_content']} premium content pieces")
        
        return results

if __name__ == "__main__":
    aggregator = AdvancedContentAggregator()
    results = aggregator.run_advanced_aggregation()