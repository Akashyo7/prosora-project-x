#!/usr/bin/env python3
"""
Real Source Fetcher for Prosora Intelligence
Phase 2: Replace mocked content with actual RSS/API fetching
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time
import hashlib
import sqlite3
import os
from dataclasses import dataclass
import yaml
from bs4 import BeautifulSoup
import re

@dataclass
class RealSourceContent:
    """Real content fetched from sources"""
    title: str
    content: str
    url: str
    published: datetime
    source_name: str
    source_credibility: float
    source_tier: str
    domains: List[str]
    freshness_score: float
    relevance_score: float = 0.0

class SourceCache:
    """Caching system for fetched content"""
    
    def __init__(self, db_path: str = "data/source_cache.db"):
        self.db_path = db_path
        self.init_cache_db()
    
    def init_cache_db(self):
        """Initialize cache database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS source_cache (
                    url_hash TEXT PRIMARY KEY,
                    url TEXT,
                    title TEXT,
                    content TEXT,
                    published TEXT,
                    source_name TEXT,
                    source_credibility REAL,
                    source_tier TEXT,
                    domains TEXT,
                    freshness_score REAL,
                    cached_at TEXT,
                    expires_at TEXT
                )
            """)
    
    def get_cached_content(self, url: str) -> Optional[RealSourceContent]:
        """Get cached content if still valid"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM source_cache 
                WHERE url_hash = ? AND datetime(expires_at) > datetime('now')
            """, (url_hash,))
            
            row = cursor.fetchone()
            if row:
                return RealSourceContent(
                    title=row[2],
                    content=row[3],
                    url=row[1],
                    published=datetime.fromisoformat(row[4]),
                    source_name=row[5],
                    source_credibility=row[6],
                    source_tier=row[7],
                    domains=row[8].split(',') if row[8] else [],
                    freshness_score=row[9]
                )
        return None
    
    def cache_content(self, content: RealSourceContent, cache_hours: int = 6):
        """Cache content with expiration"""
        url_hash = hashlib.md5(content.url.encode()).hexdigest()
        expires_at = datetime.now() + timedelta(hours=cache_hours)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO source_cache VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (
                url_hash, content.url, content.title, content.content,
                content.published.isoformat(), content.source_name,
                content.source_credibility, content.source_tier,
                ','.join(content.domains), content.freshness_score,
                datetime.now().isoformat(), expires_at.isoformat()
            ))

class RealSourceFetcher:
    """Fetches real content from RSS feeds and APIs"""
    
    def __init__(self, sources_config_path: str = "prosora_sources.yaml"):
        with open(sources_config_path, 'r') as f:
            self.sources_config = yaml.safe_load(f)
        
        self.cache = SourceCache()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Prosora Intelligence Engine 2.0 (Educational Research)'
        })
        
        print("📡 Real Source Fetcher initialized")
    
    def fetch_rss_content(self, rss_url: str, source_config: Dict) -> List[RealSourceContent]:
        """Fetch content from RSS feed"""
        contents = []
        
        try:
            # Check cache first
            cached = self.cache.get_cached_content(rss_url)
            if cached:
                return [cached]
            
            print(f"📡 Fetching RSS: {source_config['name']}")
            
            # Parse RSS feed
            feed = feedparser.parse(rss_url)
            
            if feed.bozo:
                print(f"⚠️ RSS parsing warning for {source_config['name']}: {feed.bozo_exception}")
            
            # Process entries (limit to recent ones)
            for entry in feed.entries[:5]:  # Top 5 recent articles
                try:
                    # Extract content
                    content_text = self._extract_content_from_entry(entry)
                    if not content_text:
                        continue
                    
                    # Parse published date
                    published = self._parse_published_date(entry)
                    
                    # Calculate freshness score
                    freshness = self._calculate_freshness_score(published)
                    
                    # Create content object
                    real_content = RealSourceContent(
                        title=entry.get('title', 'No Title'),
                        content=content_text,
                        url=entry.get('link', rss_url),
                        published=published,
                        source_name=source_config['name'],
                        source_credibility=source_config.get('credibility', 0.7),
                        source_tier=source_config.get('tier', 'standard'),
                        domains=source_config.get('domains', []),
                        freshness_score=freshness
                    )
                    
                    contents.append(real_content)
                    
                    # Cache the content
                    self.cache.cache_content(real_content)
                    
                except Exception as e:
                    print(f"⚠️ Error processing entry from {source_config['name']}: {e}")
                    continue
            
            print(f"✅ Fetched {len(contents)} articles from {source_config['name']}")
            
        except Exception as e:
            print(f"❌ Failed to fetch RSS from {source_config['name']}: {e}")
        
        return contents
    
    def fetch_web_content(self, url: str, source_config: Dict) -> Optional[RealSourceContent]:
        """Fetch content from web page"""
        try:
            # Check cache first
            cached = self.cache.get_cached_content(url)
            if cached:
                return cached
            
            print(f"🌐 Fetching web content: {source_config['name']}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No Title"
            
            # Extract main content (heuristic approach)
            content_text = self._extract_web_content(soup)
            
            if not content_text:
                return None
            
            # Create content object
            real_content = RealSourceContent(
                title=title_text,
                content=content_text,
                url=url,
                published=datetime.now(),  # Use current time for web scraping
                source_name=source_config['name'],
                source_credibility=source_config.get('credibility', 0.7),
                source_tier=source_config.get('tier', 'standard'),
                domains=source_config.get('domains', []),
                freshness_score=0.9  # Assume fresh for direct web content
            )
            
            # Cache the content
            self.cache.cache_content(real_content)
            
            print(f"✅ Fetched web content from {source_config['name']}")
            return real_content
            
        except Exception as e:
            print(f"❌ Failed to fetch web content from {source_config['name']}: {e}")
            return None
    
    def fetch_sources_for_query(self, query_domains: List[str], query_keywords: List[str]) -> List[RealSourceContent]:
        """Fetch relevant sources for a specific query"""
        all_contents = []
        
        print(f"📡 Fetching real sources for domains: {query_domains}")
        
        # Fetch from premium sources
        premium_sources = self.sources_config.get('premium_sources', [])
        for source_config in premium_sources:
            if self._is_source_relevant(source_config, query_domains):
                contents = self._fetch_from_source(source_config)
                all_contents.extend(contents)
        
        # Fetch from standard sources
        standard_sources = self.sources_config.get('standard_sources', [])
        for source_config in standard_sources:
            if self._is_source_relevant(source_config, query_domains):
                contents = self._fetch_from_source(source_config)
                all_contents.extend(contents)
        
        # Calculate relevance scores
        for content in all_contents:
            content.relevance_score = self._calculate_relevance_score(content, query_keywords)
        
        # Sort by relevance and freshness
        all_contents.sort(key=lambda x: (x.relevance_score * x.freshness_score * x.source_credibility), reverse=True)
        
        print(f"✅ Fetched {len(all_contents)} real content pieces")
        return all_contents[:15]  # Top 15 most relevant
    
    def _fetch_from_source(self, source_config: Dict) -> List[RealSourceContent]:
        """Fetch from a single source configuration"""
        contents = []
        
        # Handle RSS feeds
        if 'rss_url' in source_config:
            contents.extend(self.fetch_rss_content(source_config['rss_url'], source_config))
        
        # Handle direct URLs
        elif 'url' in source_config:
            web_content = self.fetch_web_content(source_config['url'], source_config)
            if web_content:
                contents.append(web_content)
        
        return contents
    
    def _is_source_relevant(self, source_config: Dict, query_domains: List[str]) -> bool:
        """Check if source is relevant to query domains"""
        source_domains = source_config.get('domains', [])
        return any(domain in query_domains for domain in source_domains) or 'general' in query_domains
    
    def _extract_content_from_entry(self, entry) -> str:
        """Extract meaningful content from RSS entry"""
        content = ""
        
        # Try different content fields
        if hasattr(entry, 'content') and entry.content:
            content = entry.content[0].value if isinstance(entry.content, list) else entry.content
        elif hasattr(entry, 'summary') and entry.summary:
            content = entry.summary
        elif hasattr(entry, 'description') and entry.description:
            content = entry.description
        
        # Clean HTML tags
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            content = soup.get_text().strip()
            
            # Limit content length
            if len(content) > 1000:
                content = content[:1000] + "..."
        
        return content
    
    def _extract_web_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from web page"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find main content areas
        content_selectors = [
            'article', 'main', '.content', '.post-content', 
            '.entry-content', '.article-content', 'p'
        ]
        
        content_text = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                content_text = ' '.join([elem.get_text().strip() for elem in elements[:3]])
                break
        
        # Fallback to body text
        if not content_text:
            content_text = soup.get_text()
        
        # Clean and limit content
        content_text = re.sub(r'\s+', ' ', content_text).strip()
        if len(content_text) > 1000:
            content_text = content_text[:1000] + "..."
        
        return content_text
    
    def _parse_published_date(self, entry) -> datetime:
        """Parse published date from RSS entry"""
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                return datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                return datetime(*entry.updated_parsed[:6])
        except:
            pass
        
        return datetime.now()  # Fallback to current time
    
    def _calculate_freshness_score(self, published: datetime) -> float:
        """Calculate freshness score based on publication date"""
        now = datetime.now()
        age_hours = (now - published).total_seconds() / 3600
        
        # Fresher content gets higher scores
        if age_hours < 24:
            return 1.0
        elif age_hours < 72:
            return 0.8
        elif age_hours < 168:  # 1 week
            return 0.6
        elif age_hours < 720:  # 1 month
            return 0.4
        else:
            return 0.2
    
    def _calculate_relevance_score(self, content: RealSourceContent, query_keywords: List[str]) -> float:
        """Calculate relevance score based on keyword matching"""
        if not query_keywords:
            return 0.5
        
        # Combine title and content for analysis
        text = f"{content.title} {content.content}".lower()
        
        # Count keyword matches
        matches = sum(1 for keyword in query_keywords if keyword.lower() in text)
        
        # Calculate relevance score
        relevance = min(matches / len(query_keywords), 1.0)
        
        return relevance

# Test function
def test_real_source_fetcher():
    """Test the real source fetcher"""
    fetcher = RealSourceFetcher()
    
    # Test with sample query
    test_domains = ['tech', 'finance']
    test_keywords = ['ai', 'fintech', 'regulation']
    
    print("🧪 Testing real source fetching...")
    contents = fetcher.fetch_sources_for_query(test_domains, test_keywords)
    
    print(f"\n📊 Results:")
    for i, content in enumerate(contents[:3]):
        print(f"\n{i+1}. {content.title}")
        print(f"   Source: {content.source_name} (Credibility: {content.source_credibility})")
        print(f"   Freshness: {content.freshness_score:.2f}, Relevance: {content.relevance_score:.2f}")
        print(f"   Content: {content.content[:100]}...")

if __name__ == "__main__":
    test_real_source_fetcher()