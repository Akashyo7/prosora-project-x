import feedparser
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
from typing import List, Dict
from config import Config

class ContentAggregator:
    def __init__(self):
        self.config = Config()
        
    def fetch_newsletter_content(self) -> List[Dict]:
        """Fetch content from newsletter RSS feeds"""
        content = []
        
        for source_url in self.config.NEWSLETTER_SOURCES:
            try:
                feed = feedparser.parse(source_url)
                for entry in feed.entries[:5]:  # Get latest 5 articles
                    content.append({
                        "type": "newsletter",
                        "title": entry.title,
                        "summary": entry.summary if hasattr(entry, 'summary') else "",
                        "url": entry.link,
                        "published": entry.published if hasattr(entry, 'published') else "",
                        "source": feed.feed.title if hasattr(feed.feed, 'title') else source_url,
                        "timestamp": datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"Error fetching from {source_url}: {e}")
                
        return content
    
    def fetch_youtube_transcripts(self) -> List[Dict]:
        """Fetch YouTube video transcripts from leadership channels"""
        content = []
        
        for channel_id in self.config.YOUTUBE_CHANNELS:
            try:
                # Get recent videos from channel (simplified - in production use YouTube API)
                videos = self._get_recent_videos(channel_id)
                
                for video in videos[:3]:  # Process 3 recent videos per channel
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video['id'])
                        full_text = " ".join([item['text'] for item in transcript])
                        
                        content.append({
                            "type": "youtube",
                            "title": video['title'],
                            "transcript": full_text,
                            "url": f"https://youtube.com/watch?v={video['id']}",
                            "channel": video['channel'],
                            "timestamp": datetime.now().isoformat()
                        })
                    except Exception as e:
                        print(f"Error getting transcript for {video['id']}: {e}")
                        
            except Exception as e:
                print(f"Error processing channel {channel_id}: {e}")
                
        return content
    
    def _get_recent_videos(self, channel_id: str) -> List[Dict]:
        """Simplified video fetching - replace with YouTube API in production"""
        # Placeholder - implement YouTube API integration
        return [
            {"id": "sample_video_id", "title": "Sample Video", "channel": "Sample Channel"}
        ]
    
    def fetch_serp_trends(self, keywords: List[str]) -> List[Dict]:
        """Fetch trending topics using SERP API"""
        trends = []
        
        if not self.config.SERP_API_KEY:
            print("SERP API key not configured")
            return trends
            
        for keyword in keywords:
            try:
                url = "https://serpapi.com/search"
                params = {
                    "q": keyword,
                    "api_key": self.config.SERP_API_KEY,
                    "engine": "google",
                    "num": 10
                }
                
                response = requests.get(url, params=params)
                data = response.json()
                
                if "organic_results" in data:
                    for result in data["organic_results"][:5]:
                        trends.append({
                            "type": "serp_trend",
                            "keyword": keyword,
                            "title": result.get("title", ""),
                            "snippet": result.get("snippet", ""),
                            "url": result.get("link", ""),
                            "timestamp": datetime.now().isoformat()
                        })
                        
            except Exception as e:
                print(f"Error fetching SERP data for {keyword}: {e}")
                
        return trends
    
    def aggregate_all_content(self) -> Dict:
        """Aggregate content from all sources"""
        print("🔄 Starting content aggregation...")
        
        all_content = {
            "newsletters": self.fetch_newsletter_content(),
            "youtube": self.fetch_youtube_transcripts(),
            "trends": self.fetch_serp_trends(self.config.BRAND_KEYWORDS),
            "aggregated_at": datetime.now().isoformat()
        }
        
        # Save to file
        with open("data/raw_content.json", "w") as f:
            json.dump(all_content, f, indent=2)
            
        print(f"✅ Aggregated {len(all_content['newsletters'])} newsletter articles")
        print(f"✅ Aggregated {len(all_content['youtube'])} YouTube transcripts")
        print(f"✅ Aggregated {len(all_content['trends'])} trend items")
        
        return all_content

if __name__ == "__main__":
    aggregator = ContentAggregator()
    content = aggregator.aggregate_all_content()