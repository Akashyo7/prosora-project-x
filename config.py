import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    @classmethod
    def validate_api_keys(cls):
        """Validate that required API keys are present"""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is required! Please set it in your .env file or environment variables."
            )
    SERP_API_KEY = os.getenv("SERP_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    # Email Configuration for Newsletter Aggregation
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # App password for Gmail
    
    # Content Sources
    NEWSLETTER_SOURCES = [
        "https://feeds.feedburner.com/venturebeat/SZYF",  # VentureBeat
        "https://techcrunch.com/feed/",  # TechCrunch
        "https://feeds.feedburner.com/oreilly/radar",  # O'Reilly Radar
        "https://hbr.org/feed",  # Harvard Business Review
        "https://www.mckinsey.com/feed/articles",  # McKinsey
    ]
    
    YOUTUBE_CHANNELS = [
        "UC-rqL-1oaQ91R38LkbJZHjg",  # Y Combinator
        "UCG4H_2MLswfDKdOCjwZcHlA",  # First Round
        "UC7cs8q-gJRlGwj4A8OmCmXg",  # a16z
        "UCMtFYi3ehI4EzNs0f2XnYsg",  # Harvard Business Review
    ]
    
    # Prosora Brand Keywords
    BRAND_KEYWORDS = [
        "product management", "fintech", "political consulting", 
        "IIT", "MBA", "innovation", "strategy", "leadership",
        "technology policy", "digital transformation"
    ]
    
    # Content Generation Settings
    CONTENT_TYPES = {
        "linkedin_post": {"max_length": 3000, "tone": "professional"},
        "twitter_thread": {"max_length": 280, "tone": "engaging"},
        "blog_post": {"max_length": 2000, "tone": "thought_leadership"},
        "newsletter": {"max_length": 1500, "tone": "informative"}
    }
    
    # Prosora Index Components
    PROSORA_INDEX_WEIGHTS = {
        "tech_innovation": 0.3,
        "political_stability": 0.2,
        "market_opportunity": 0.3,
        "social_impact": 0.2
    }